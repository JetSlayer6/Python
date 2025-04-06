import random
import time
import os

def clear_screen():
    """
    Clears the terminal screen for better readability.
    Works on both Windows (cls) and Unix-based systems (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def print_slow(text, delay=0.03):
    """
    Prints text character by character for a cool typing effect.
    Args:
        text (str): The text to be printed
        delay (float): The time delay between each character
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
    
class Player:
    """
    Represents the player character with attributes and inventory management
    """
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.equipped_weapon = None
        self.gold = 0
        self.experience = 0
        self.level = 1
        
    def add_item(self, item):
        """Adds an item to the player's inventory"""
        self.inventory.append(item)
        print_slow(f"Added {item} to inventory!")
        
    def remove_item(self, item):
        """Removes an item from a player's inventory if it exists"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def show_stats(self):
        """Displays current player's statistics"""
        print_slow(f"\n=== {self.name}'s Stets ===")
        print_slow(f"Health: {self.health}/{self.max_health}")
        print_slow(f"Level: {self.level}")
        print_slow(f"Experience: {self.experience}")
        print_slow(f"Koen: {self.gold}")
        print_slow(f"Equipped Weapon: {self.equipped_weapon or 'None'}")
        print_slow("\nInventory:")
        if self.inventory:
            for item in self.inventory:
                print_slow(f"- {item}")
        else:
            print_slow("Empty")
            
    def blacksmith(player):
        """Creates a weapon"""
        blacksmith_items = {
            '1': {'name': 'sword', 'cost': 25},
            '2': {'name': 'dagger', 'cost': 50},
            '3': {'name': 'pistol', 'cost': 100}
        }
        
        while True:
            clear_screen()
            print_slow("\n=== Blacksmith ===")
            print_slow(f"\nYour koen: {player.gold}")
            print_slow("Available Options:")
            print_slow("1. Sword - 25 koen")
            print_slow("2. Dagger - 50 koen")
            print_slow("3. Pistol - 100 koen")
            print_slow("4. Exit shop")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '4':
                break
            elif choice in blacksmith_items:
                item = blacksmith_items[choice]
                if player.gold >= item['cost']:
                        player.gold -= item['cost']
                player.add_item(item['name'])
                if item['name'] == 'Sword':
                    player.equipped_weapon = 'Sword'
                elif item['name'] == 'Dagger':
                    player.equipped_weapon = 'Dagger'
                elif item['name'] == 'Pistol':
                    player.equipped_weapon = 'Pistol'
            else:
                print_slow(f"You don't have enough koen, {player.name}!")
        else:
            print_slow(f"Invalid choice, {player.name}!")
                
            
        
            
    def heal(self, amount):
        """Heals the player by the specified amount"""
        self.health = min(self.health + amount, self.max_health)
        print_slow(f"Healed {self.name}'s health for {amount} HP. Current Health: {self.health} HP")
        
class Enemy:
    """
    Represents enemies the player can encounter and fight
    """
    def __init__(self, name, health, damage, gold_reward, exp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward
        
    def is_alive(self):
        """Checks if the enemy is still alive"""
        return self.health > 0
    
def create_enemy():
    """
    Creates a random enemy from a predefined list with varying stats
    Returns:
        Enemy: A new enemy instance with random attributes
    """
    enemies = [
        ("Goblin", 30, 5, 10, 20),
        ("Skeleton", 40, 8, 15, 25),
        ("Orc", 60, 12, 25, 25),
        ("Dark Wizard", 45, 15, 30, 40),
        ("Cave Troll", 100, 20, 50, 60),
        ("Zombie Army", 150, 30, 90, 200)
    ]
    enemy_type = random.choice(enemies)
    # Add some randomness to enemy stats
    health_variance = random.randint(-5, 5)
    damage_variance = random.randint(-2, 2)
    return Enemy(
        enemy_type[0],
        enemy_type[1] + health_variance,
        enemy_type[2] + damage_variance,
        enemy_type[3],
        enemy_type[4]
    )
    
def combat_round(player, enemy):
    """
    Handles a single round of combat between player and enemy
    Args:
        player (Player): The player character
        enemy (Enemy): The enemy being fought
    Returns:
        bool: True if combat should continue, False if it's over
    """
    # Player's turn
    print_slow(f"\n{player.name}'s turn!")
    print_slow("Choos your action:")
    print_slow("1. Attack")
    print_slow("2. Use Health Potion")
    print_slow("3. Try to Run")
    
    while True:
        choice = input("\nEnter your choice (1-3): ")
        if choice in ['1', '2', '3']:
            break
        print_slow("Invalid choice! Try again.")
        
    if choice == '1':
        # Basic attack
        damage = random.randint(1, 20)
        if player.equipped_weapon:
            damage += 5
        enemy.health -= damage
        print_slow(f"You hit the {enemy.name} and he lost {damage} HP!")
        
    elif choice == '2':
        # Use health potion
        if 'Health Potion' in player.inventory:
            player.remove_item('Health Potion')
            heal_amount = random.randint(20, 70)
            player.heal(heal_amount)
        else:
            print_slow("You don't have any health potions!")
            return True
        
    elif choice == '3':
        # Attempt to run away
        if random.random() < 0.5:
            print_slow(f"You outran the {enemy.name}!")
            return False
        print_slow(f"The {enemy.name} has caught up!")
        
    # Show enemy health
    if enemy.health > 0:
        print_slow(f"\nThe {enemy.name}'s Health: {enemy.health} HP/{enemy.max_health} HP")
        
    # Enemy's turn (if still alive)
    if enemy.health > 0:
        print_slow(f"\nThe {enemy.name}'s turn!")
        damage = random.randint(enemy.damage - 2, enemy.damage + 2)
        player.health -= damage
        print_slow(f"The {enemy.name} hit you and removes {damage} HP from your health!")
        print_slow(f"Your Health: {player.health} HP/{player.max_health} HP")
        
    # Check if anyone died
    if player.health <= 0:
        print(f"\nYou have been defeated by the {enemy.name}!")
        return False
    elif enemy.health <= 0:
        print_slow(f"\nYou defeated the {enemy.name}!")
        player.gold += enemy.gold_reward
        player.experience += enemy.exp_reward
        print_slow(f"You gained {enemy.gold_reward} koen and gained {enemy.exp_reward} experience!")
        
        # Level up check
        if player.experience >= player.level * 100:
            player.level += 1
            player.max_health += 20
            player.health = player.max_health
            print_slow(f"\nCongratulations {player.name}! You are now in Level {player.level}!")
            print_slow("Your maximum health has increased by 20 HP!")
        return False

    return True

def shop(player):
    """
    Implements a shop where the player can buy items
    Args:
        player (Player): The player character
    """
    shop_items = {
        '1': {'name': 'Sword', 'cost': 50},
        '2': {'name': 'Health Potion', 'cost': 70},
        '3': {'name': 'Shield', 'cost': 60},
        '4': {'name': 'Dagger', 'cost': 100},
        '5': {'name': 'Pistol', 'cost': 200}
    }
    
    while True:
        clear_screen()
        print_slow("\n=== Shop ===")
        print_slow(f"Your koen: {player.gold}")
        print_slow("\nAvailable Options:")
        print_slow("1. Sword - 50 koen")
        print_slow("2. Health Potion - 70 koen")
        print_slow("3. Shield - 60 koen")
        print_slow("4. Dagger - 100 koen")
        print_slow("5. Pistol - 200 koen")
        print_slow("6. Exit shop")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '6':
            break
        elif choice in shop_items:
            item = shop_items[choice]
            if player.gold >= item['cost']:
                player.gold -= item['cost']
                player.add_item(item['name'])
                if item['name'] == 'Sword':
                    player.equipped_weapon = 'Sword'
                elif item['name'] == 'Dagger':
                    player.equipped_weapon = 'Dagger'
                elif item['name'] == 'Pistol':
                    player.equipped_weapon = 'Pistol'
            else:
                print_slow(f"You don't have enough koen, {player.name}!")
        else:
            print_slow(f"Invalid choice, {player.name}!")
            
        input("\nPress Enter to continue")
        
def explore_location():
    """
    Generates a random event when exploring
    Returns:
        str: Description of what is found
    """
    events = [
        "You found a hidden treasure chest!",
        "You dicovered an ancient shrine!",
        "You stumbled upon a mysterious cave!"
        "You found an abandoned camp!"
        "You discovered a peaceful clearing!"
        "You have tresspassed into a haunted graveyard!"
    ]
    return random.choice(events)

def main_game():
    """
    Main game loop that ties all the game mechanics together
    """
    clear_screen()
    print_slow("Welcome to the Python Adventure!")
    print_slow("\nIn this game, you'll explore a magical world, fight monsters,")
    print_slow("collect treasure, and become the strongest, bravest and most daring adventurer!")
    
    # Get a player name
    name = input("\nEnter your character's name: ")
    player = Player(name)
    
    # Main game loop
    while player.health > 0:
        clear_screen()
        print_slow("\nWhat would you like to do?")
        print_slow("1. Explore")
        print_slow("2. Visit the shop")
        print_slow("3. Check stats")
        print_slow("4. Make a weapon")
        print_slow("5. Rest (Heal 40 HP)")
        print_slow("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            # Exploration and combat
            print_slow("\n" + explore_location())
            
            # 75% chance to encounter an enemy
            if random.random() < 0.75:
                enemy = create_enemy()
                print_slow(f"\nWatch out, {player.name}. The {enemy.name} appears!")
                
                # Combat loop
                while combat_round(player, enemy):
                    continue
                
                if player.health <= 0:
                    break
                
                # 35% chance to find a health potion after combat
                if random.random() < 0.35:
                    print_slow(f"\nCongrats, {player.name}, you found a Health Potion!")
                    player.add_item("Health Potion")
                    
            input("\nPress Enter to continue")
            
        elif choice == '2':
            # Shop
            shop(player)
            
        elif choice == '3':
            # Show stats
            player.show_stats()
            input("\nPress Enter to continue")
            
        elif choice == '4':
            # Blacksmith
            player.blacksmith()
            input("\nPress Enter to continue")
            
            
        elif choice == '5':
            # Rest to heal
            if player.health < player.max_health:
                player.heal(40)
            else:
                print_slow(f"{player.name}, you are already at full health!")
            input("\nPress Enter to continue")
        
        elif choice == '6':
            # Exit
            print_slow("Thanks, young adventurer!")
            break
        
    if player.health <= 0:
        print_slow("\nGame Over!")
        print_slow(f"\nFinal Stats for {player.name}:")
        player.show_stats()
        
if __name__ == "__main__":
    main_game()
        