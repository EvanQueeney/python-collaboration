import random
class Location:
    def __init__(self, name, description, food_chance, items, requires=None):
        self.name = name
        self.description = description
        self.food_chance = food_chance
        self.items = items
        self.neighbors = {}
        self.requires = requires
        self.visited = False
        self.has_campfire = False
        self.locked_box_opened = False  # Track if the locked box has been opened
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        neighbor.neighbors[self] = cost
    
    def search_for_food(self):
        return "Food" if random.random() < self.food_chance else None
    
    def search_for_items(self):
        # Prevent the locked box from being found here
        if self.name == "Crash Site" and not self.locked_box_opened:
            return None  # The locked box won't be found
        return random.choice(self.items) if self.items else None

class Player:
    def __init__(self, start_location):
        self.energy = 100
        self.inventory = []
        self.location = start_location
        self.water_uses = 0
        self.purified = False
        self.wet = 0
        self.rescued = False  # Track if the player has been rescued
    
    def move(self, new_location):
        if new_location in self.location.neighbors:
            if new_location.requires and new_location.requires not in self.inventory:
                print(f"You need {new_location.requires} to enter {new_location.name}.")
                return
            cost = self.location.neighbors[new_location]
            if self.wet > 0:
                cost += 10
                self.wet -= 1
                print("You are wet, so you lose extra energy!")
            if self.energy >= cost:
                self.energy -= cost
                self.location = new_location
                print(f"You moved to {self.location.name}. Energy left: {self.energy}")
                if not self.location.visited:
                    print(self.location.description)
                    self.location.visited = True
                if self.location.name == "Waterfall":
                    self.wet = 3
                    print("You got wet from the waterfall! Moving will cost extra energy for a while.")
            else:
                print("Not enough energy to move there!")
        else:
            print("You can't move to that location!")
    
    def search(self):
        food = self.location.search_for_food()
        if food:
            self.inventory.append(food.lower())  # Add food to inventory in lowercase
            print("You found food and stored it in your inventory!")
        else:
            print("No food found here.")
        
        item = self.location.search_for_items()
        if item:
            self.inventory.append(item.lower())  # Add found items to inventory in lowercase
            self.location.items.remove(item)
            print(f"You found a {item}!")
        else:
            print("No items found here.")

    
    def use_item(self, item): 
        if item == "knife":
            if self.location.name == "Crash Site" and not self.location.locked_box_opened:
                print("You use the knife to open the locked box, revealing a flare!")
                self.inventory.append("Flare")  # Add the flare to inventory
                self.location.locked_box_opened = True
            else:
                print("There is no locked box to open here.")
        
        elif item == "flare":
            if self.location.name == "Mountain" and "Flare" in self.inventory:
                print("You use the flare. A helicopter spots it from afar and comes to rescue you!")
                print("You have been rescued! Game Over!")
                self.rescued = True  # Mark player as rescued
            else:
                print("You need to be at the Mountain with a flare to signal for rescue.")
        
        elif item.lower() == "food":
            if self.energy < 100:
                self.energy += 10
                if self.energy > 100:
                    self.energy = 100
                self.inventory.remove("Food")  # Remove the item from the inventory after use
                print(f"You ate the food. Energy restored to {self.energy}.")
            else:
                print("You already have full energy. Eating food won't help.")
        
        elif item == "water bottle":
            if self.location.name == "Lake":
                print("You filled the water bottle with lake water. It needs to be purified before drinking.")
                self.purified = False
            elif self.water_uses > 0 and self.purified:
                self.energy += 20
                self.water_uses -= 1
                if self.energy > 100:
                    self.energy = 100
                print(f"You drank purified water. Energy restored to {self.energy}. Uses left: {self.water_uses}")
            else:
                print("The water is not purified. You need a campfire to purify it.")
        
        elif item == "stick" and self.location.name == "Clearing":
            if not self.location.has_campfire:
                print("You built a campfire using the stick!")
                self.location.has_campfire = True
                self.inventory.remove("Stick")  # Remove the stick after use
            else:
                print("There is already a campfire here.")
        
        else:
            print(f"You used {item}, but nothing happened.")


def create_map():
    crash_site = Location("Crash Site", "The remains of your crashed plane lay scattered around, smoke still rising. You see a locked box here.", 0.4, [])
    clearing = Location("Clearing", "A bright open space with short grass, offering a good view of your surroundings.", 0.3, [])
    forest = Location("Forest", "A dense woodland with towering trees.", 0.5, ["Stick"])
    dense_forest = Location("Dense Forest", "Thick vegetation blocks most of the light.", 0, ["Climbing Gear"], requires="Knife")
    cave = Location("Cave", "A dark and eerie cave. The air feels damp.", 0, ["Knife", "Flare"], requires="Flashlight")
    lake = Location("Lake", "A serene lake with crystal-clear water.", 0.7, ["Water Bottle"])
    waterfall = Location("Waterfall", "A powerful waterfall crashes down into the rocks.", 0, ["Flashlight"])
    mountain = Location("Mountain", "A steep and rocky mountain.", 0.1, [], requires="Climbing Gear")
    
    crash_site.add_neighbor(clearing, 10)
    clearing.add_neighbor(forest, 10)
    clearing.add_neighbor(lake, 15)
    forest.add_neighbor(cave, 20)
    forest.add_neighbor(dense_forest, 25)
    dense_forest.add_neighbor(mountain, 30)
    cave.add_neighbor(forest, 20)
    lake.add_neighbor(waterfall, 5)
    waterfall.add_neighbor(lake, 5)
    
    return crash_site  # Starting location

class Game:
    def __init__(self):
        self.running = True
        self.player = Player(create_map())
    
    def display_menu(self):
        if not self.player.rescued:  # Only show menu if the player hasn't been rescued
            print("\n--- Survival Game Menu ---")
            print("1. Move to another location")
            print("2. Search for food and items")
            print("3. Use an item from inventory")
            print("4. View Inventory")
            print("5. Check Energy")
            print("6. Exit Game")
    
    def run(self):
        print("You wake up in the wreckage of a plane crash, deep in the forest. You are the only survivor.")
        print("Your goal is to escape by finding the necessary tools and reaching civilization.")
        print(self.player.location.description)  # First location description
        self.player.location.visited = True
        
        while self.running and self.player.energy > 0 and not self.player.rescued:
            print(f"\nCurrent location: {self.player.location.name}")
            print("Available moves:")
            for loc in self.player.location.neighbors:
                print(f" - {loc.name} (Cost: {self.player.location.neighbors[loc]})")
            
            self.display_menu()
            choice = input("Choose an option: ")
            
            if choice == "1":
                destination_name = input("Enter the name of the location you want to move to: ")
                for loc in self.player.location.neighbors:
                    if loc.name.lower() == destination_name.lower():
                        self.player.move(loc)
                        break
                else:
                    print("Invalid location!")
            elif choice == "2":
                self.player.search()
            elif choice == "3":
                print("Inventory: ", self.player.inventory)
                item = input("Enter item to use: ")
                if item.lower() in self.player.inventory:
                    self.player.use_item(item.lower())
                else:
                    print("Item not found in inventory.")
            elif choice == "4":
                print("Inventory: ", self.player.inventory)
            elif choice == "5":
                print(f"Energy: {self.player.energy}")
            elif choice == "6":
                self.running = False

        if self.player.rescued:
            print("Game Over! You have been rescued.")
        else:
            print("Game Over! You ran out of energy.")

game = Game()
game.run()
