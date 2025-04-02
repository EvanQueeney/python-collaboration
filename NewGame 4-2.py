import random
import time

def fancy_prent(msg):
    for c in msg:
        print(c, end='')
        time.sleep(0.01)
    print()
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
                fancy_prent(f"You need {new_location.requires} to enter {new_location.name}.")
                return
            cost = self.location.neighbors[new_location]
            if self.wet > 0:
                cost += 10
                self.wet -= 1
                fancy_prent("You are wet, so you lose extra energy!")
            if self.energy >= cost:
                self.energy -= cost
                self.location = new_location
                fancy_prent(f"You moved to {self.location.name}. Energy left: {self.energy}")
                if not self.location.visited:
                    fancy_prent(self.location.description)
                    self.location.visited = True
                if self.location.name == "Waterfall":
                    self.wet = 3
                    fancy_prent("You got wet from the waterfall! Moving will cost extra energy for a while.")
            else:
                fancy_prent("Not enough energy to move there!")
        else:
            fancy_prent("You can't move to that location!")
    
    def search(self):
        food = self.location.search_for_food()
        if food:
            self.inventory.append(food.lower())  # Add food to inventory in lowercase
            fancy_prent("You found food and stored it in your inventory!")
        else:
            fancy_prent("No food found here.")
        
        item = self.location.search_for_items()
        if item:
            self.inventory.append(item.lower())  # Add found items to inventory in lowercase
            self.location.items.remove(item)
            fancy_prent(f"You found a {item}!")
        else:
            fancy_prent("No items found here.")

    def use_item(self, item): 
        if item == "knife":
            if self.location.name == "Crash Site" and not self.location.locked_box_opened:
                fancy_prent("You use the knife to open the locked box, revealing a flare!")
                self.inventory.append("flare")  # Add the flare to inventory
                self.location.locked_box_opened = True
            else:
                fancy_prent("There is no locked box to open here.")
        
        elif item == "flare":
            if self.location.name == "Mountain" and "flare" in self.inventory:
                fancy_prent("You use the flare. A helicopter spots it from afar and comes to rescue you!")
                fancy_prent("You have been rescued! Game Over!")
                self.rescued = True  # Mark player as rescued
            else:
                fancy_prent("You need to be at the Mountain with a flare to signal for rescue.")
        
        elif item.lower() == "food":
            if self.energy < 100:
                self.energy += 10
                if self.energy > 100:
                    self.energy = 100
                if "food" in self.inventory:
                    self.inventory.remove("food")  # Remove the item from the inventory after use
                    fancy_prent(f"You ate the food. Energy restored to {self.energy}.")
                else:
                    fancy_prent(self.inventory)
            else:
                fancy_prent("You already have full energy. Eating food won't help.")
        
        elif item == "water bottle":
            if self.location.name == "Lake":
                fancy_prent("You filled the water bottle with lake water. It needs to be purified before drinking.")
                self.purified = False
            elif self.water_uses > 0 and self.purified:
                self.energy += 20
                self.water_uses -= 1
                if self.energy > 100:
                    self.energy = 100
                fancy_prent(f"You drank purified water. Energy restored to {self.energy}. Uses left: {self.water_uses}")
            else:
                fancy_prent("The water is not purified. You need a campfire to purify it.")
        
        elif item == "stick" and self.location.name == "Clearing":
            if not self.location.has_campfire:
                fancy_prent("You built a campfire using the stick!")
                self.location.has_campfire = True
                self.inventory.remove("stick")  # Remove the stick after use
            else:
                fancy_prent("There is already a campfire here.")
        
        else:
            fancy_prent(f"You used {item}, but nothing happened.")


def create_map():
    crash_site = Location("Crash Site", "The remains of your crashed plane lay scattered around, smoke still rising. You see a locked box here.", 0.4, [])
    clearing = Location("Clearing", "A bright open space with short grass, offering a good view of your surroundings, the remains of a campfire lay here.", 0.3, [])
    forest = Location("Forest", "A dense woodland with towering trees.", 0.5, ["stick"])
    dense_forest = Location("Dense Forest", "Thick vegetation blocks most of the light.", 0, ["climbing gear"], requires="knife")
    cave = Location("Cave", "A dark and eerie cave. The air feels damp.", 0, ["knife"], requires="flashlight")
    lake = Location("Lake", "A serene lake with crystal-clear water.", 0.7, ["water bottle"])
    waterfall = Location("Waterfall", "A powerful waterfall crashes down into the rocks.", 0, ["flashlight"])
    mountain = Location("Mountain", "A steep and rocky mountain.", 0.1, [], requires="climbing gear")
    
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
            fancy_prent("\n--- Survival Game Menu ---")
            fancy_prent("1. Move to another location")
            fancy_prent("2. Search for food and items")
            fancy_prent("3. Use an item from inventory")
            fancy_prent("4. View Inventory")
            fancy_prent("5. Check Energy")
            fancy_prent("6. Exit Game")
    
    def run(self):
        fancy_prent("You wake up in the wreckage of a plane crash, deep in the forest. You are the only survivor.")
        fancy_prent("Your goal is to escape by finding the necessary tools and reaching civilization.")
        fancy_prent(self.player.location.description)  # First location description
        self.player.location.visited = True
        
        while self.running and self.player.energy > 0 and not self.player.rescued:
            fancy_prent(f"\nCurrent location: {self.player.location.name}")
            fancy_prent("Available moves:")
            for loc in self.player.location.neighbors:
                fancy_prent(f" - {loc.name} (Cost: {self.player.location.neighbors[loc]})")
            
            self.display_menu()
            choice = input("Choose an option: ")
            
            if choice == "1":
                destination_name = input("Enter the name of the location you want to move to: ")
                for loc in self.player.location.neighbors:
                    if loc.name.lower() == destination_name.lower():
                        self.player.move(loc)
                        break
                else:
                    fancy_prent("Invalid location!")
            elif choice == "2":
                self.player.search()
            elif choice == "3":
                fancy_prent("Inventory: ", self.player.inventory)
                item = input("Enter item to use: ")
                if item.lower() in self.player.inventory:
                    self.player.use_item(item.lower())
                else:
                    fancy_prent("Item not found in inventory.")
            elif choice == "4":
                fancy_prent("Inventory: ", self.player.inventory)
            elif choice == "5":
                fancy_prent(f"Energy: {self.player.energy}")
            elif choice == "6":
                self.running = False

        if self.player.rescued:
            fancy_prent("Game Over! You have been rescued.")
        else:
            fancy_prent("Game Over! You ran out of energy.")

game = Game()
game.player.inventory = ['stick', 'flashlight', 'water bottle', 'knife', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'food', 'climbing gear', 'flare', '']
game.run()
