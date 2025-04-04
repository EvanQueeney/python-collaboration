import random
import time

#method to print text slowly to enhance user experience
def fancy_prent(msg):
    for c in msg:
        print(c, end='')
        time.sleep(0.01)
    print()

#Encounter class to define random encounters in the game    
class Encounter:
    def __init__(self, description, action, probability): #initialize encounters
        self.description = description
        self.action = action
        self.probability = probability  # Chance of the encounter happening (0-1)

    def trigger(self, player): #how the encounter will happen
        if random.random() < self.probability:
            fancy_prent(self.description)
            self.action(player)

# Define specific encounters
def bear_encounter(player): #encounter with a bear
    fancy_prent("A bear appears! Do you want to (1) run or (2) fight?")
    choice = input("> ")
    if choice == "1":
        fancy_prent("You run away, losing 15 energy!")
        player.energy -= 15
    elif choice == "2":
        if random.random() < 0.5:# 50% chance to win the fight with the bear
            fancy_prent("You fight off the bear with your knife but lose 10 energy!")
            player.energy -= 10
        else: 
            fancy_prent("The bear badly injures you! Lose 40 energy!")
            player.energy -= 40
    else:
        fancy_prent("You hesitate, and the bear swipes at you! Lose 25 energy.")
        player.energy -= 25

def fishing_encounter(player):#encounter finding a fishing rod
    fancy_prent("You find a fishing rod by the lake! Do you want to (1) fish or (2) walk away?")
    choice = input("> ")
    if choice == "1":
        if random.random() < 0.7:  # 70% chance to catch a fish
            fancy_prent("You caught a fish! It has been added to your inventory.")
            player.inventory.append("food")
        else:
            fancy_prent("You didn't catch anything.")
    else:
        fancy_prent("You leave the fishing rod where it is.")

def fall_encounter(player):#encounter falling down the mountain
    fancy_prent("You slip while climbing the mountain and lose 20 energy!")
    player.energy -= 20

#Location class to define each location on the map    
class Location:
    def __init__(self, name, description, food_chance, items, requires=None, encounter=None):#constructor for locations
        self.name = name
        self.description = description
        self.food_chance = food_chance
        self.items = items
        self.neighbors = {}
        self.requires = requires
        self.visited = False
        self.has_campfire = False
        self.locked_box_opened = False  # Track if the locked box has been opened
        self.encounter = encounter  # Store the encounter for this location

    def add_neighbor(self, neighbor, cost):#function to add a neighbor to a location allowing a player to move between the two
        self.neighbors[neighbor] = cost
        neighbor.neighbors[self] = cost
    
    def search_for_food(self):#function to allow the player to search for food in a location
        return "Food" if random.random() < self.food_chance else None
    
    def search_for_items(self):#function to allow the player to search for an item in a location
        if self.name == "Crash Site" and not self.locked_box_opened:# Prevent the locked box from being found here
            return None  # The locked box won't be found
        return random.choice(self.items) if self.items else None

#Player class to define what the player can do
class Player:
    def __init__(self, start_location):#PLayer contstructor
        self.energy = 100
        self.inventory = []
        self.location = start_location
        self.water_uses = 0
        self.purified = False
        self.wet = 0
        self.rescued = False  # Track if the player has been rescued
    
    def move(self, new_location):#function to allow a player to move between locations
        if new_location in self.location.neighbors:
            if new_location.requires and new_location.requires not in self.inventory:
                fancy_prent(f"You need {new_location.requires} to enter {new_location.name}.")
                return
            cost = self.location.neighbors[new_location]
            if self.wet > 0:#if the player is wet from the waterfall they lose extra energy
                cost += 10
                self.wet -= 1
                fancy_prent("You are wet, so you lose extra energy!")
            if self.energy >= cost:
                self.energy -= cost
                self.location = new_location
                fancy_prent(f"You moved to {self.location.name}. Energy left: {self.energy}")
                if not self.location.visited:#check to see if a location has been visited before
                    fancy_prent(self.location.description)
                    if self.location.encounter:  # Trigger encounter if there is one
                        self.location.encounter.trigger(self)
                    self.location.visited = True
                if self.location.name == "Waterfall":
                    self.wet = 3
                    fancy_prent("You got wet from the waterfall! Moving will cost extra energy for a while.")
            else:
                fancy_prent("Not enough energy to move there! You run out of energy and die!")
                self.energy = 0
                self.running = False
        else:
            fancy_prent("You can't move to that location!")
    
    def search(self): #function to allow a player to search for food and items
        food = self.location.search_for_food()
        if food:
            self.inventory.append(food.lower())  # Add food to inventory in lowercase
            fancy_prent("You found food and stored it in your inventory!")
        else:
            fancy_prent("No food found here.")
            
        item = self.location.search_for_items()#checks to see if there is an item in a location
        if item:
            self.inventory.append(item.lower())  # Add found items to inventory in lowercase
            self.location.items.remove(item)
            fancy_prent(f"You found a {item}!")
        else:
            fancy_prent("No items found here.")

    def use_item(self, item): #function to allow a player to use an item
        if item == "knife":#the knife is used at the crashsite to open the box
            if self.location.name == "Crash Site" and not self.location.locked_box_opened:
                fancy_prent("You use the knife to open the locked box, revealing a flare!")
                self.inventory.append("flare")  # Add the flare to inventory
                self.location.locked_box_opened = True
            else:
                fancy_prent("There is no locked box to open here.")
        
        elif item == "flare":#the flare is used at the mountain to call for rescue
            if self.location.name == "Mountain" and "flare" in self.inventory:
                fancy_prent("You use the flare. A helicopter spots it from afar and comes to rescue you!")
                fancy_prent("You have been rescued! Game Over!")
                self.rescued = True  # Mark player as rescued
            else:
                fancy_prent("You need to be at the Mountain with a flare to signal for rescue.")
        
        elif item.lower() == "food":#food is used to regain your energy
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
        
        elif item == "water bottle":#the water bottle is able to be filled at the lake then purified at the campfire to drink
            if self.location.name == "Lake":
                fancy_prent("You filled the water bottle with lake water. It needs to be purified before drinking.")
                self.purified = False
            elif self.water_uses > 0 and self.purified:#checks if the water is purified
                self.energy += 20
                self.water_uses -= 1
                if self.energy > 100:
                    self.energy = 100
                fancy_prent(f"You drank purified water. Energy restored to {self.energy}. Uses left: {self.water_uses}")
            else:
                fancy_prent("The water is not purified. You need a campfire to purify it.")
        
        elif item == "stick" and self.location.name == "Clearing":#the stick is used at the clearing to make a campfire
            if not self.location.has_campfire:
                fancy_prent("You built a campfire using the stick!")
                self.location.has_campfire = True
                self.inventory.remove("stick")  # Remove the stick after use
            else:
                fancy_prent("There is already a campfire here.")
        else:
            fancy_prent(f"You used {item}, but nothing happened.")

#definition to create the map by defining each location
def create_map():
    #defining the parameters of each location
    crash_site = Location("Crash Site", "The remains of your crashed plane lay scattered around, smoke still rising. You see a locked box here.", 0.4, [])
    clearing = Location("Clearing", "A bright open space with short grass, offering a good view of your surroundings, the remains of a campfire lay here.", 0.3, [])
    forest = Location("Forest", "A dense woodland with towering trees.", 0.5, ["stick"])
    dense_forest = Location("Dense Forest", "Thick vegetation blocks most of the light.", 0, ["climbing gear"], requires="knife", 
                            encounter=Encounter("You hear rustling in the bushes...", bear_encounter, 0.5))  # 50% chance
    cave = Location("Cave", "A dark and eerie cave. The air feels damp.", 0, ["knife"], requires="flashlight")
    lake = Location("Lake", "A serene lake with crystal-clear water.", 0.7, ["water bottle"], 
                    encounter=Encounter("You see something shiny near the water...", fishing_encounter, 0.6))  # 60% chance
    waterfall = Location("Waterfall", "A powerful waterfall crashes down into the rocks.", 0, ["flashlight"])
    mountain = Location("Mountain", "A steep and rocky mountain.", 0.1, [], requires="climbing gear",
                        encounter=Encounter("The path is slippery...", fall_encounter, 0.4))  # 40% chance
    
    #creating the map by assinging neighbors
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

#defining the game class which runs the actual game
class Game:
    def __init__(self):
        self.running = True
        self.player = Player(create_map())
    
    def display_menu(self):#function to display the menu to the player to give them gameplay options
        if not self.player.rescued:  # Only show menu if the player hasn't been rescued
            fancy_prent("\n--- Survival Game Menu ---")
            fancy_prent("1. Move to another location")
            fancy_prent("2. Search for food and items")
            fancy_prent("3. Use an item from inventory")
            fancy_prent("4. View Inventory")
            fancy_prent("5. Check Energy")
            fancy_prent("6. Exit Game")
    
    def run(self):#function that runs the game
        fancy_prent("You wake up in the wreckage of a plane crash, deep in the forest. You are the only survivor.")
        fancy_prent("Your goal is to escape by finding the necessary tools and reaching civilization.")
        fancy_prent(self.player.location.description)  # First location description
        self.player.location.visited = True
        
        while self.running and self.player.energy > 0 and not self.player.rescued:#while the player has energy and has not been rescued continue the game
            fancy_prent(f"\nCurrent location: {self.player.location.name}")
            fancy_prent("Available moves:")
            for loc in self.player.location.neighbors:
                fancy_prent(f" - {loc.name} (Cost: {self.player.location.neighbors[loc]})")
            
            self.display_menu()
            choice = input("Choose an option: ")
            
            if choice == "1":#this option allows the player to move
                destination_name = input("Enter the name of the location you want to move to: ")
                for loc in self.player.location.neighbors:
                    if loc.name.lower() == destination_name.lower():
                        self.player.move(loc)
                        break
                else:
                    fancy_prent("Invalid location!")
            elif choice == "2":#this option allows the player to search the location they are at for items
                self.player.search()
                
            elif choice == "3":#this option allows the player to use items from their inventory
                fancy_prent(f"Inventory: {self.player.inventory}")
                item = input("Enter item to use: ")
                if item.lower() in self.player.inventory:
                    self.player.use_item(item.lower())
                else:
                    fancy_prent("Item not found in inventory.")
                    
            elif choice == "4":#this option allows the player to check their inventory
                fancy_prent(f"Inventory: {self.player.inventory}")
                
            elif choice == "5":#this option allows the player to check their energy
                fancy_prent(f"Energy: {self.player.energy}")
                
            elif choice == "6":#this option ends the game
                self.running = False

        if self.player.rescued:#if the player has been rescued end the game
            fancy_prent("Game Over! You have been rescued.")
        else:
            fancy_prent("Game Over! You ran out of energy.")

game = Game()
game.run()