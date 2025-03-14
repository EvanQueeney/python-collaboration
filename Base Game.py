import random

class Location:
    def __init__(self, name, food_chance, items):
        self.name = name
        self.food_chance = food_chance  # Probability of finding food (0 to 1)
        self.items = items  # List of items that can be found here
        self.neighbors = {}  # Connected locations and their movement cost
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
    
    def search_for_food(self):
        return random.random() < self.food_chance
    
    def search_for_items(self):
        return random.choice(self.items) if self.items else None

class Player:
    def __init__(self, start_location):
        self.energy = 100
        self.inventory = []
        self.location = start_location
    
    def move(self, new_location):
        if new_location in self.location.neighbors:
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
        if self.location.search_for_food():
            self.energy += 20
            print("You found food and ate it! Energy restored.")
        else:
            print("No food found here.")
        
        item = self.location.search_for_items()
        if item:
            self.inventory.append(item)
            print(f"You found a {item}!")
        else:
            print("No items found here.")
    
    def show_inventory(self):
        if self.inventory:
            print("\n--- Inventory ---")
            for item in self.inventory:
                print(f"- {item}")
        else:
            print("Your inventory is empty.")
    
    def check_energy(self):
        print(f"Current Energy: {self.energy}/100")
    
    def gather_resources(self):
        if self.energy > 10:
            print("You gathered some wood and berries.")
            self.inventory.append("Wood")
            self.inventory.append("Berries")
            self.energy -= 10
        else:
            print("Not enough energy to gather resources. Rest to regain energy.")

def create_map():
    forest = Location("Forest", 0.5, ["Stick", "Berries"])
    cave = Location("Cave", 0.2, ["Rock", "Torch"])
    lake = Location("Lake", 0.8, ["Fish", "Water Bottle"])
    
    forest.add_neighbor(cave, 20)
    forest.add_neighbor(lake, 10)
    cave.add_neighbor(forest, 20)
    lake.add_neighbor(forest, 10)
    
    return forest  # Starting location

class Game:
    def __init__(self):
        self.running = True
        self.player = Player(create_map())
    
    def display_menu(self):
        print("\n--- Survival Game Menu ---")
        print("1. Move to another location")
        print("2. Search for food and items")
        print("3. View Inventory")
        print("4. Check Energy")
        print("5. Gather Resources")
        print("6. Exit Game")
    
    def run(self):
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
                self.player.show_inventory()
            elif choice == "4":
                self.player.check_energy()
            elif choice == "5":
                self.player.gather_resources()
            elif choice == "6":
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
