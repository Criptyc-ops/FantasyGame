"""
Fantasy Quest: The Dragon's Curse
A text-based adventure game set in the magical Kingdom of Eldoria
"""

import sys
import time
try:
    import temporal_anomaly as anomaly
    ANOMALY_ENABLED = True
except ImportError:
    ANOMALY_ENABLED = False

# Game Constants
GAME_TITLE = "FANTASY QUEST: The Dragon's Curse"
GAME_VERSION = "1.0"
MAX_HEALTH = 100
WIN_CONDITION = False

# Color codes for terminal output (bonus feature)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Game Data Structures
locations = {
    'village': {
        'name': 'Thorndale Village',
        'description': 'A quaint medieval village with cobblestone streets and thatched-roof cottages. The air smells of fresh bread from the bakery, and you can hear the blacksmith\'s hammer in the distance.',
        'exits': {'north': 'forest', 'east': 'market', 'south': 'tavern'},
        'items': ['healing_potion'],
        'npc': 'elder'
    },
    'forest': {
        'name': 'Whispering Forest',
        'description': 'Ancient oak trees tower above you, their leaves whispering secrets in the wind. Sunlight filters through the canopy, creating dancing patterns of light and shadow.',
        'exits': {'south': 'village', 'east': 'tower', 'north': 'cave'},
        'items': ['magic_mushroom'],
        'npc': 'hermit'
    },
    'tower': {
        'name': 'Wizard\'s Tower',
        'description': 'A spiraling tower of dark stone reaches toward the sky. Strange magical energies pulse from within, and mystical symbols glow faintly on the walls.',
        'exits': {'west': 'forest', 'north': 'mountain'},
        'items': ['spell_book'],
        'npc': 'wizard'
    },
    'mountain': {
        'name': 'Dragon\'s Peak',
        'description': 'Craggy peaks pierce the clouds, and the air grows thin and cold. In the distance, you can see smoke rising from what must be the dragon\'s lair.',
        'exits': {'south': 'tower', 'east': 'lair'},
        'items': ['dragon_scale'],
        'npc': None
    },
    'lair': {
        'name': 'Dragon\'s Lair',
        'description': 'A massive cavern filled with glittering treasure. Bones of previous adventurers litter the floor, and you can hear the thunderous breathing of the great wyrm.',
        'exits': {'west': 'mountain'},
        'items': ['crown'],
        'npc': 'dragon',
        'locked': True
    },
    'cave': {
        'name': 'Crystal Cave',
        'description': 'Shimmering crystals line the walls of this underground chamber, casting rainbow reflections everywhere. The air hums with magical energy.\n\n\033[96mOne crystal pulses with an unusual blue resonance. It feels warm, almost alive.\033[0m',
        'exits': {'south': 'forest'},
        'items': ['crystal_shard'],
        'npc': None
    },
    'market': {
        'name': 'Merchant\'s Square',
        'description': 'Bustling stalls display wares from across the kingdom. Merchants call out their goods, and the smell of exotic spices fills the air.',
        'exits': {'west': 'village', 'north': 'castle'},
        'items': ['rope'],
        'npc': 'merchant'
    },
    'castle': {
        'name': 'Castle Eldoria',
        'description': 'Majestic towers rise before you, banners bearing the royal crest fluttering in the breeze. Guards in polished armor stand at attention.',
        'exits': {'south': 'market'},
        'items': ['sword'],
        'npc': 'knight'
    },
    'tavern': {
        'name': 'The Prancing Pony Tavern',
        'description': 'Warm firelight and the sound of merrymaking spill from this cozy tavern. The smell of ale and roasted meat makes your mouth water.',
        'exits': {'north': 'village'},
        'items': ['ale'],
        'npc': 'bard'
    }
}

items = {
    'healing_potion': {
        'name': 'Healing Potion',
        'description': 'A glowing red liquid that restores 25 health points when consumed.',
        'type': 'consumable',
        'effect': 25
    },
    'magic_mushroom': {
        'name': 'Magic Mushroom',
        'description': 'A luminescent fungus that enhances magical abilities when consumed.',
        'type': 'consumable',
        'effect': 15
    },
    'spell_book': {
        'name': 'Ancient Spell Book',
        'description': 'A leather-bound tome filled with powerful incantations. Required to learn magic.',
        'type': 'key_item'
    },
    'crystal_shard': {
        'name': 'Crystal Shard',
        'description': 'A fragment of pure magical crystal. Glows with inner light.',
        'type': 'key_item'
    },
    'sword': {
        'name': 'Knight\'s Sword',
        'description': 'A finely crafted blade etched with protective runes. Increases combat effectiveness.',
        'type': 'weapon'
    },
    'rope': {
        'name': 'Climbing Rope',
        'description': 'A sturdy rope that might help you reach difficult places.',
        'type': 'tool'
    },
    'dragon_scale': {
        'name': 'Dragon Scale',
        'description': 'A massive scale from an ancient dragon. Nearly indestructible.',
        'type': 'key_item'
    },
    'crown': {
        'name': 'Crown of Eldoria',
        'description': 'The legendary crown that grants authority over the realm. Your ultimate quest objective!',
        'type': 'quest_item'
    },
    'ale': {
        'name': 'Dwarven Ale',
        'description': 'A strong alcoholic beverage that might loosen tongues or courage.',
        'type': 'consumable',
        'effect': 10
    }
}

npcs = {
    'elder': {
        'name': 'Village Elder',
        'dialogue': [
            'Welcome, brave adventurer! The Kingdom of Eldoria is in great peril.',
            'The ancient dragon Vezareth has awakened and stolen the Crown of Eldoria!',
            'Without the crown, our kingdom will fall into chaos and darkness.',
            'You must retrieve the crown from the dragon\'s lair atop Dragon\'s Peak!',
            'Speak with the wizard in his tower. He may have magic that can help you.',
            '\033[90m*The elder rubs his temples* I keep having strange dreams of silver lights in the forest...\033[0m'
        ],
        'quest_given': True,
        'reward': 'healing_potion'
    },
    'wizard': {
        'name': 'Archmage Zephyrus',
        'dialogue': [
            'Ah, I have been expecting you. The elder\'s visions are seldom wrong.',
            'To defeat the dragon, you will need more than mere steel and courage.',
            'Take this spell book. Within it lies the incantation to breach the dragon\'s lair.',
            'You must also gather a crystal shard from the Crystal Cave to power the spell.',
            'Combine the spell book and crystal shard when you face the dragon\'s barrier.'
        ],
        'requires_item': None,
        'reward': 'spell_book'
    },
    'knight': {
        'name': 'Sir Gareth the Bold',
        'dialogue': [
            'By the king\'s beard! Another would-be dragonslayer?',
            'I admire your courage, but many have tried and failed.',
            'Take my sword. It has been blessed by the royal priest and may serve you better than most.',
            'Remember: strike for the heart, where the scales are weakest!'
        ],
        'requires_item': 'ale',
        'reward': 'sword'
    },
    'merchant': {
        'name': 'Trader Matthias',
        'dialogue': [
            'Finest wares in the kingdom! What catches your eye?',
            'Ah, for a dragonslayer, I have just the thing!',
            'This rope is woven from giant\'s hair. Strong enough to hold even you!',
            'It might help you scale the treacherous paths to the dragon\'s peak.'
        ],
        'requires_item': None,
        'reward': 'rope'
    },
    'hermit': {
        'name': 'Forest Hermit',
        'dialogue': [
            'The trees whisper of your coming, young hero.',
            'I have lived in these woods for decades, gathering rare herbs and mushrooms.',
            'This magic mushroom will enhance your vitality when consumed.',
            'Beware the dragon\'s fire. It burns hotter than any forge in the kingdom.',
            '\033[90m*He squints northeast* The lights have been strange lately. Blue. Wrong color for foxfire...\033[0m'
        ],
        'requires_item': None,
        'reward': 'magic_mushroom'
    },
    'bard': {
        'name': 'Tavern Bard',
        'dialogue': [
            '♪ Oh gather \'round and hear my tale, of dragon fierce and bold! ♪',
            '♪ Who stole the crown from royal brow, in caverns dark and cold! ♪',
            'Many have tried to claim it back, but none have yet returned...',
            'Perhaps you\'ll be the hero whose name will be well-earned!',
            'Speak with Sir Gareth upstairs. He\'s been in a foul mood since the crown was taken.'
        ],
        'requires_item': None,
        'reward': None
    },
    'dragon': {
        'name': 'Vezareth the Ancient',
        'dialogue': [
            'FOOLISH MORTAL! You dare enter the domain of Vezareth?',
            'I have lived for a thousand years! I have devoured countless heroes!',
            'You think your pathetic magic can harm me? I AM THE EMBODIMENT OF POWER!',
            'Very well... face my wrath and become another pile of bones in my collection!'
        ],
        'is_enemy': True,
        'health': 150,
        'damage': 30
    }
}

class Player:
    """Player character class with all attributes and methods"""
    
    def __init__(self, name):
        self.name = name
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.inventory = []
        self.current_location = 'village'
        self.visited_locations = ['village']
        self.quests_completed = []
        self.spells_learned = []
        self.combat_skill = 1
        self.magic_power = 1
        
    def take_damage(self, amount):
        """Apply damage to player"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            return True  # Player died
        return False
    
    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)
    
    def add_item(self, item_key):
        """Add item to inventory"""
        if item_key in items:
            self.inventory.append(item_key)
            return True
        return False
    
    def remove_item(self, item_key):
        """Remove item from inventory"""
        if item_key in self.inventory:
            self.inventory.remove(item_key)
            return True
        return False
    
    def has_item(self, item_key):
        """Check if player has item"""
        return item_key in self.inventory
    
    def get_stats(self):
        """Get player statistics"""
        return {
            'name': self.name,
            'health': f"{self.health}/{self.max_health}",
            'inventory_count': len(self.inventory),
            'locations_visited': len(self.visited_locations),
            'quests_completed': len(self.quests_completed),
            'combat_skill': self.combat_skill,
            'magic_power': self.magic_power
        }

class Game:
    """Main game class that handles all game logic"""
    
    def __init__(self):
        self.player = None
        self.game_running = True
        self.dragon_defeated = False
        if ANOMALY_ENABLED:
            anomaly.on_game_start()

    def slow_print(self, text, delay=0.03):
        """Print text with typewriter effect for dramatic moments"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def display_title_screen(self):
        """Show the game title and introduction"""
        print(Colors.CYAN + Colors.BOLD)
        print("=" * 60)
        print("            FANTASY QUEST: The Dragon's Curse")
        print("=" * 60)
        print(Colors.RESET)
        print()
        self.slow_print("Welcome to the Kingdom of Eldoria!", 0.05)
        self.slow_print("The ancient dragon Vezareth has awakened from his thousand-year slumber...", 0.04)
        self.slow_print("He has stolen the Crown of Eldoria - the symbol of royal authority!", 0.04)
        self.slow_print("Without it, the kingdom will fall into chaos and darkness...", 0.04)
        self.slow_print("You are the realm's last hope. Will you accept this quest?", 0.04)
        print()
    
    def get_player_name(self):
        """Get player name at game start"""
        while True:
            name = input("Enter your hero's name: ").strip()
            if name and len(name) > 0:
                return name
            print("Please enter a valid name.")
    
    def display_location(self):
        """Display current location information"""
        location = locations[self.player.current_location]
        print(Colors.YELLOW + Colors.BOLD + f"\n=== {location['name']} ===" + Colors.RESET)
        print(location['description'])
        
        # Show exits
        print(Colors.GREEN + "\nExits: " + Colors.RESET, end="")
        exit_list = list(location['exits'].keys())
        print(", ".join(exit_list))
        
        # Show items
        if location['items']:
            print(Colors.BLUE + "\nItems here: " + Colors.RESET, end="")
            item_names = [items[item]['name'] for item in location['items']]
            print(", ".join(item_names))
        
        # Show NPCs
        if location['npc']:
            npc_name = npcs[location['npc']]['name']
            print(Colors.PURPLE + f"\n{npc_name} is here." + Colors.RESET)
    
    def process_command(self, command):
        """Process player commands"""
        if ANOMALY_ENABLED:
            handled = anomaly.check_secret_command(command, self, self.player, locations, npcs, items)
            if handled:
                return
        elif verb == 'rest' or verb == 'sleep':
            print("You find a safe spot to rest for a while...")
        command = command.strip().lower()
        parts = command.split()
        
        if not parts:
            return
        
        verb = parts[0]
        
        # Movement commands
        if verb in ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
            direction = verb[0] if len(verb) == 1 else verb
            self.move_player(direction)
        
        # Action commands
        elif verb == 'take' or verb == 'get':
            if len(parts) > 1:
                self.take_item(' '.join(parts[1:]))
            else:
                print("Take what?")
        
        elif verb == 'drop':
            if len(parts) > 1:
                self.drop_item(' '.join(parts[1:]))
            else:
                print("Drop what?")
        
        elif verb == 'use':
            if len(parts) > 1:
                self.use_item(' '.join(parts[1:]))
            else:
                print("Use what?")
        
        elif verb == 'talk':
            if len(parts) > 1:
                self.talk_to_npc(' '.join(parts[1:]))
            else:
                self.talk_to_npc(None)
        
        elif verb == 'examine' or verb == 'look':
            self.display_location()
        
        # System commands
        elif verb == 'inventory' or verb == 'inv':
            self.show_inventory()
        
        elif verb == 'stats':
            self.show_stats()
        
        elif verb == 'help' or verb == 'h':
            self.show_help()
        
        elif verb == 'quit' or verb == 'exit':
            self.game_running = False
            print("Thanks for playing! Farewell, brave adventurer!")
        
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")
    
    def move_player(self, direction):
        """Move player to a new location"""
        location = locations[self.player.current_location]
        
        if direction in location['exits']:
            new_location = location['exits'][direction]
            
            # Check if location is locked
            if 'locked' in locations[new_location] and locations[new_location]['locked']:
                if new_location == 'lair':
                    if self.player.has_item('spell_book') and self.player.has_item('crystal_shard'):
                        print(Colors.CYAN + "\nYou raise the spell book and crystal shard...")
                        self.slow_print("Ancient words flow from your lips as magical energy surrounds you!")
                        self.slow_print("The dragon's barrier shimmers and fades away!")
                        locations[new_location]['locked'] = False
                        print(Colors.GREEN + "The way to the dragon's lair is now open!" + Colors.RESET)
                    else:
                        print(Colors.RED + "\nA magical barrier blocks your path!")
                        print("You need a spell book and crystal shard to pass." + Colors.RESET)
                        return
                else:
                    print("This way is blocked.")
                    return
            
            self.player.current_location = new_location
            if new_location not in self.player.visited_locations:
                self.player.visited_locations.append(new_location)
            
            print(Colors.GREEN + f"\nYou go {direction}..." + Colors.RESET)
            self.display_location()
        else:
            print("You can't go that way.")
    
    def take_item(self, item_name):
        """Take an item from the current location"""
        location = locations[self.player.current_location]
        
        # Find item by name
        item_key = None
        for key, item in items.items():
            if item['name'].lower() == item_name.lower():
                item_key = key
                break
        
        if item_key and item_key in location['items']:
            self.player.add_item(item_key)
            location['items'].remove(item_key)
            print(Colors.GREEN + f"\nYou picked up {items[item_key]['name']}!" + Colors.RESET)
            print(items[item_key]['description'])
            
            # Special item effects
            if item_key == 'spell_book':
                self.player.spells_learned.append('fireball')
                self.player.magic_power += 2
                print(Colors.PURPLE + "You learned the Fireball spell!" + Colors.RESET)
            elif item_key == 'sword':
                self.player.combat_skill += 3
                print(Colors.PURPLE + "Your combat skill increased!" + Colors.RESET)
        else:
            print("That item is not here.")
    
    def drop_item(self, item_name):
        """Drop an item from inventory"""
        item_key = None
        for key, item in items.items():
            if item['name'].lower() == item_name.lower():
                item_key = key
                break
        
        if item_key and self.player.has_item(item_key):
            self.player.remove_item(item_key)
            locations[self.player.current_location]['items'].append(item_key)
            print(Colors.YELLOW + f"\nYou dropped {items[item_key]['name']}." + Colors.RESET)
        else:
            print("You don't have that item.")
    
    def use_item(self, item_name):
        """Use an item from inventory"""
        item_key = None
        for key, item in items.items():
            if item['name'].lower() == item_name.lower():
                item_key = key
                break
        
        if not item_key or not self.player.has_item(item_key):
            print("You don't have that item.")
            return
        
        item = items[item_key]
        
        if item['type'] == 'consumable':
            self.player.heal(item['effect'])
            self.player.remove_item(item_key)
            print(Colors.GREEN + f"\nYou used {item['name']} and restored {item['effect']} health!" + Colors.RESET)
            print(f"Health: {self.player.health}/{self.player.max_health}")
        
        elif item['type'] == 'key_item':
            print(Colors.PURPLE + f"\nYou examine the {item['name']} carefully..." + Colors.RESET)
            print(item['description'])
        
        else:
            print("You can't use that item right now.")
    
    def talk_to_npc(self, npc_name):
        """Talk to an NPC in the current location"""
        location = locations[self.player.current_location]
        
        if not location['npc']:
            print("There\'s no one here to talk to.")
            return
        
        npc = npcs[location['npc']]
        
        # Display dialogue
        print(Colors.PURPLE + f"\n{npc['name']} says:" + Colors.RESET)
        for line in npc['dialogue']:
            print(f'"{line}"')
            time.sleep(0.5)
        
        # Handle rewards
        if 'reward' in npc and npc['reward']:
            reward = npc['reward']
            if not self.player.has_item(reward) and reward not in location['items']:
                location['items'].append(reward)
                print(Colors.GREEN + f"\n{npc['name']} gives you {items[reward]['name']}!" + Colors.RESET)
        
        # Special NPC interactions
        if location['npc'] == 'dragon' and not self.dragon_defeated:
            self.start_dragon_combat()
    
    def start_dragon_combat(self):
        """Start combat with the dragon"""
        print(Colors.RED + Colors.BOLD)
        print("\n" + "="*50)
        print("         COMBAT BEGINS!")
        print("="*50)
        print(Colors.RESET)
        
        dragon = npcs['dragon']
        dragon_health = dragon['health']
        
        while dragon_health > 0 and self.player.health > 0:
            print(f"\n{Colors.RED}Dragon Health: {dragon_health}/{dragon['health']}{Colors.RESET}")
            print(f"{Colors.GREEN}Your Health: {self.player.health}/{self.player.max_health}{Colors.RESET}")
            
            print("\nWhat will you do?")
            print("1. Attack with sword")
            print("2. Cast fireball spell")
            print("3. Use healing potion")
            print("4. Try to reason with the dragon")
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == '1':
                if self.player.has_item('sword'):
                    damage = 20 + (self.player.combat_skill * 5)
                    print(Colors.GREEN + f"\nYou strike with your sword for {damage} damage!" + Colors.RESET)
                    dragon_health -= damage
                else:
                    damage = 5 + self.player.combat_skill
                    print(Colors.YELLOW + f"\nYou attack bare-handed for {damage} damage!" + Colors.RESET)
                    dragon_health -= damage
            
            elif choice == '2':
                if 'fireball' in self.player.spells_learned:
                    damage = 35 + (self.player.magic_power * 10)
                    print(Colors.PURPLE + f"\nYour fireball explodes for {damage} damage!" + Colors.RESET)
                    dragon_health -= damage
                else:
                    print(Colors.YELLOW + "\nYou don't know any spells!" + Colors.RESET)
                    continue
            
            elif choice == '3':
                if self.player.has_item('healing_potion'):
                    self.player.use_item('healing_potion')
                else:
                    print(Colors.YELLOW + "\nYou don't have any healing potions!" + Colors.RESET)
                    continue
            
            elif choice == '4':
                print(Colors.CYAN + "\nYou attempt to speak with the dragon...")
                self.slow_print("Vezareth laughs, a sound like thunder rolling across the mountains!")
                self.slow_print("'FOOL! I do not parley with insects who dare challenge my power!'")
                print(Colors.RESET)
            
            else:
                print("Invalid choice!")
                continue
            
            # Dragon's turn
            if dragon_health > 0:
                print(Colors.RED + "\nThe dragon attacks!" + Colors.RESET)
                dragon_damage = dragon['damage']
                
                if self.player.has_item('dragon_scale'):
                    print(Colors.CYAN + "Your dragon scale absorbs some of the damage!" + Colors.RESET)
                    dragon_damage -= 10
                
                died = self.player.take_damage(max(dragon_damage, 5))
                print(Colors.RED + f"You take {dragon_damage} damage!" + Colors.RESET)
                
                if died:
                    print(Colors.RED + Colors.BOLD + "\nThe dragon's flames consume you...")
                    print("You have been defeated!" + Colors.RESET)
                    return
        
        # Combat ended
        if dragon_health <= 0:
            self.dragon_defeated = True
            print(Colors.GREEN + Colors.BOLD)
            print("\n" + "="*50)
            print("     VICTORY! DRAGON DEFEATED!")
            print("="*50)
            print(Colors.RESET)
            self.slow_print("The mighty dragon Vezareth crashes to the ground, defeated!")
            self.slow_print("Among the treasure, you spot the Crown of Eldoria!")
            print(Colors.YELLOW + Colors.BOLD + "\nYou have retrieved the Crown of Eldoria!" + Colors.RESET)
            locations['lair']['items'].append('crown')
    
    def show_inventory(self):
        """Display player inventory"""
        print(Colors.BLUE + Colors.BOLD + "\n=== INVENTORY ===" + Colors.RESET)
        if not self.player.inventory:
            print("Your inventory is empty.")
        else:
            for item_key in self.player.inventory:
                item = items[item_key]
                print(f"- {item['name']}: {item['description']}")
        print()
    
    def show_stats(self):
        """Display player statistics"""
        stats = self.player.get_stats()
        print(Colors.CYAN + Colors.BOLD + "\n=== CHARACTER SHEET ===" + Colors.RESET)
        print(f"Name: {stats['name']}")
        print(f"Health: {stats['health']}")
        print(f"Combat Skill: {stats['combat_skill']}")
        print(f"Magic Power: {stats['magic_power']}")
        print(f"Items Collected: {stats['inventory_count']}")
        print(f"Locations Visited: {stats['locations_visited']}")
        print(f"Quests Completed: {stats['quests_completed']}")
        
        if self.player.spells_learned:
            print(f"Spells Learned: {', '.join(self.player.spells_learned)}")
        print()
    
    def show_help(self):
        """Display help information"""
        print(Colors.WHITE + Colors.BOLD + "\n=== HELP ===" + Colors.RESET)
        print("Movement Commands:")
        print("  north/n, south/s, east/e, west/w - Move in specified direction")
        print()
        print("Action Commands:")
        print("  take [item] - Pick up an item")
        print("  drop [item] - Drop an item from inventory")
        print("  use [item] - Use an item")
        print("  talk [npc] - Talk to a character")
        print("  examine/look - Look around current location")
        print()
        print("System Commands:")
        print("  inventory/inv - Show your inventory")
        print("  stats - Show character statistics")
        print("  help/h - Show this help message")
        print("  quit/exit - Exit the game")
        print()
        print("Your quest: Retrieve the Crown of Eldoria from the dragon's lair!")
        print()
    
    def check_win_condition(self):
        """Check if player has won the game"""
        if self.player.has_item('crown'):
            print(Colors.GREEN + Colors.BOLD)
            print("\n" + "="*60)
            print("               CONGRATULATIONS!")
            print("="*60)
            print(Colors.RESET)
            self.slow_print("You have successfully retrieved the Crown of Eldoria!")
            self.slow_print("The kingdom is saved from the dragon's curse!")
            self.slow_print("Bards will sing of your heroic deeds for generations to come!")
            print(Colors.YELLOW + Colors.BOLD + f"\n{self.player.name}, Hero of Eldoria!" + Colors.RESET)
            print()
            self.show_stats()
            return True
        return False
    
    def main_game_loop(self):
        """Main game loop"""
        self.display_title_screen()
        player_name = self.get_player_name()
        self.player = Player(player_name)
        
        print(Colors.GREEN + f"\nWelcome, {player_name}! Your adventure begins now!" + Colors.RESET)
        print(Colors.YELLOW + "Type 'help' for a list of commands." + Colors.RESET)
        
        self.display_location()
        
        while self.game_running:
            if self.check_win_condition():
                break
            
            command = input(Colors.BOLD + "\n> " + Colors.RESET).strip()
            self.process_command(command)
            
            # Check for game over
            if self.player.health <= 0:
                print(Colors.RED + Colors.BOLD + "\nYou have fallen in battle...")
                print("The Kingdom of Eldoria is doomed..." + Colors.RESET)
                break

def main():
    """Main function to start the game"""
    game = Game()
    try:
        game.main_game_loop()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")

if __name__ == "__main__":
    main()
