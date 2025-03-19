import random

class Location:
    def __init__(self, name, food_chance, items, requires=None):
        self.name = name
        self.food_chance = food_chance  # Probability of finding food (0 to 1)
        self.items = items  # List of items that can be found here
        self.neighbors = {}  # Connected locations and their movement cost
        self.requires = requires  # Item required to access this location
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
    
    def search_for_food(self):
        return "Food" if random.random() < self.food_chance else None
    
    def search_for_items(self):
        return random.choice(self.items) if self.items else None

class Player:
    def __init__(self, start_location):
        self.energy = 100
        self.inventory = []
        self.location = start_location
        self.water_uses = 0  # Tracks water bottle uses
        self.purified = False  # Tracks if water is purified
    
    def move(self, new_location):
        if new_location in self.location.neighbors:
            if new_location.requires and new_location.requires not in self.inventory:
                print(f"You need {new_location.requires} to enter {new_location.name}.")
                return
            cost = self.location.neighbors[new_location]
            if self.energy >= cost:
                self.energy -= cost
                self.location = new_location
                print(f"You moved to {self.location.name}. Energy left: {self.energy}")
            else:
                print("Not enough energy to move there!")
        else:
            print("You can't move to that location!")
    
    def search(self):
        food = self.location.search_for_food()
        if food:
            self.inventory.append("Food")
            print("You found food and stored it in your inventory!")
        else:
            print("No food found here.")
        
        item = self.location.search_for_items()
        if item:
            self.inventory.append(item)
            self.location.items.remove(item)
            print(f"You found a {item}!")
        else:
            print("No items found here.")
    
    def use_food(self):
        if "Food" in self.inventory:
            self.energy = min(100, self.energy + 20)
            self.inventory.remove("Food")
            print("You ate some food and restored energy!")
        else:
            print("You have no food to eat.")
    
    def fill_water_bottle(self):
        if "Water Bottle" in self.inventory and self.location.name == "Lake":
            self.water_uses = 3
            self.purified = False
            print("You filled your water bottle with untreated water.")
        else:
            print("You need a water bottle and must be at the lake to fill it.")
    
    def drink_water(self):
        if self.water_uses > 0:
            self.water_uses -= 1
            print("You drank water.")
            if not self.purified and random.random() < 0.1:
                print("You got sick from drinking untreated water! Energy -20.")
                self.energy = max(0, self.energy - 20)
        else:
            print("Your water bottle is empty.")
    
    def purify_water(self):
        if "Water Bottle" in self.inventory and "Torch" in self.inventory:
            self.purified = True
            print("You used the torch to purify your water. It is now safe to drink!")
        else:
            print("You need a water bottle and a torch to purify water.")
    
    def show_inventory(self):
        if self.inventory:
            print("\n--- Inventory ---")
            for item in self.inventory:
                print(f"- {item}")
        else:
            print("Your inventory is empty.")
    
    def check_energy(self):
        print(f"Current Energy: {self.energy}/100")

def create_map():
    crash_site = Location("Crash Site", 0.6, ["Flashlight", "Locked Box"])
    forest = Location("Dense Forest", 0.5, ["Stick"])
    cave = Location("Cave", 0.2, ["Knife"], requires="Flashlight")
    lake = Location("Lake", 0.8, ["Water Bottle"])
    mountain = Location("Mountain", 0.1, [], requires="Climbing Gear")
    
    crash_site.add_neighbor(forest, 10)
    forest.add_neighbor(cave, 20)
    forest.add_neighbor(lake, 15)
    forest.add_neighbor(mountain, 30)
    cave.add_neighbor(forest, 20)
    lake.add_neighbor(forest, 15)
    mountain.add_neighbor(forest, 30)
    
    return crash_site  # Starting location

class Game:
    def __init__(self):
        self.running = True
        self.player = Player(create_map())
    
    def display_menu(self):
        print("\n--- Survival Game Menu ---")
        print("1. Move to another location")
        print("2. Search for food and items")
        print("3. Eat Food")
        print("4. Fill Water Bottle")
        print("5. Drink Water")
        print("6. Purify Water")
        print("7. View Inventory")
        print("8. Check Energy")
        print("9. Exit Game")
    
    def run(self):
        print("You wake up in the wreckage of a plane crash, deep in the forest. You are the only survivor.")
        print("Your goal is to escape by finding the necessary tools and reaching civilization.")
        
        while self.running and self.player.energy > 0:
            print(f"\nCurrent location: {self.player.location.name}")
            print("Available moves:")
            for loc in self.player.location.neighbors:
                print(f" - {loc.name} (Cost: {self.player.location.neighbors[loc]})")
            
            self.display_menu()
            choice = input("Choose an option: ")
            
            if choice == "1":
                destination = input("Where do you want to go? ").strip().title()
                for loc in self.player.location.neighbors:
                    if loc.name.lower() == destination.lower():
                        self.player.move(loc)
                        break
                else:
                    print("Invalid location!")
            elif choice == "2":
                self.player.search()
            elif choice == "3":
                self.player.use_food()
            elif choice == "4":
                self.player.fill_water_bottle()
            elif choice == "5":
                self.player.drink_water()
            elif choice == "6":
                self.player.purify_water()
            elif choice == "7":
                self.player.show_inventory()
            elif choice == "8":
                self.player.check_energy()
            elif choice == "9":
                print("Exiting game...")
                self.running = False
            else:
                print("Invalid option, please try again.")
            
            if self.player.energy <= 0:
                print("You have run out of energy and died. Game over!")
                break

if __name__ == "__main__":
    game = Game()
    game.run()
