"""
TEMPORAL ANOMALY MODULE
A hidden easter egg for Fantasy Quest: The Dragon's Curse
Discovery path: Village (strange dream) -> Forest (investigate crater) -> Weapon
"""

import random
import time

# Hidden alien content states
_ANOMALY_ACTIVE = False
_POD_DISCOVERED = False
_WEAPON_ACQUIRED = False
_DREAM_TRIGGERED = False
_CRATER_REVEALED = False

# Alien data
ALIEN_DATA = {
    'weapon': {
        'key': 'plasma_rifle',
        'name': 'Twisted Metal Rod',
        'description': 'A warm, smooth object that pulses with inner light. It hurts to look at directly.',
        'true_name': 'X-7 Plasma Disintegrator',
        'true_description': 'An alien energy weapon from beyond the stars. Caution: May violate local causality.',
        'damage': 999,
        'ammo': 3
    },
    'aliens': {
        'scout': {
            'name': 'Star-Walker',
            'description': 'A thin figure that seems to flicker in and out of existence. Its eyes are too large.',
            'health': 50,
            'damage': 25,
            'dialogue': [
                "*A sound like breaking glass*",
                "You... should not... be here...",
                "The harvest... must continue..."
            ]
        }
    }
}

def _trigger_dream_sequence(game_instance, player, locations, npcs, items):
    """First hint - triggered when resting at tavern with crystal shard"""
    global _DREAM_TRIGGERED, _ANOMALY_ACTIVE
    
    # Only triggers if player has crystal shard and hasn't had dream yet
    if player.has_item('crystal_shard') and not _DREAM_TRIGGERED:
        if player.current_location == 'tavern' or player.current_location == 'village':
            _DREAM_TRIGGERED = True
            _ANOMALY_ACTIVE = True
            
            print("\033[96m" + "\n" + "="*60)
            print("That night, sleep comes strangely...")
            print("="*60 + "\033[0m")
            time.sleep(1)
            print("\nYou dream of falling through stars...")
            print("A silver disc tears through the sky...")
            print("It crashes into the Whispering Forest with no sound.")
            print("\nYou wake with a metallic taste in your mouth.")
            print("Through the window, the forest seems to glow faintly blue.")
            print("\033[93m[Perhaps you should investigate the forest...]\033[0m")
            print("\033[96m" + "="*60 + "\033[0m")
            
            # Modify forest description subtly
            locations['forest']['description'] = locations['forest']['description'] + " " + \
                "\033[96mA strange blue light pulses faintly in the northeastern corner of the woods.\033[0m"
            return True
    return False

def _reveal_crater(game_instance, player, locations, npcs, items):
    """Second step - investigating the light in forest"""
    global _CRATER_REVEALED, _POD_DISCOVERED
    
    if not _ANOMALY_ACTIVE or player.current_location != 'forest':
        return False
    
    _CRATER_REVEALED = True
    _POD_DISCOVERED = True
    
    print("\033[95m" + "\n" + "="*60)
    print("CRATER DISCOVERED")
    print("="*60)
    print("You push through thorny underbrush toward the blue glow.")
    print("The trees part to reveal a smoking crater, still warm to the touch.")
    print("At its center: a perfect silver sphere, seamless and humming.")
    print("\nA panel hisses open. Inside lies a 'Twisted Metal Rod'.")
    print("Symbols glow on its surface - they seem to shift when unobserved.")
    print("\033[93m[Commands: take rod / examine sphere / touch symbols]\033[0m")
    print("="*60 + "\033[0m")
    
    # Add hidden item pickup option
    locations['forest']['has_alien_artifact'] = True
    return True

def _acquire_weapon(game_instance, player, locations, npcs, items):
    """Pick up the alien weapon"""
    global _WEAPON_ACQUIRED
    
    if not _POD_DISCOVERED or player.current_location != 'forest':
        return False
    
    if not locations['forest'].get('has_alien_artifact'):
        return False
    
    weapon = ALIEN_DATA['weapon']
    items[weapon['key']] = {
        'name': weapon['name'],
        'description': weapon['description'],
        'type': 'key_item'
    }
    
    player.inventory.append(weapon['key'])
    locations['forest']['has_alien_artifact'] = False
    _WEAPON_ACQUIRED = True
    
    print("\033[93m" + "\n" + "="*60)
    print("ARTIFACT ACQUIRED")
    print("="*60)
    print(f"You reach into the sphere and lift the {weapon['name']}.")
    print("It's warm. Unnaturally warm. Your hand tingles.")
    print("Three crystalline lights pulse along its length.")
    print("\033[93m[New commands: use rod / examine rod / aim rod]\033[0m")
    print("="*60 + "\033[0m")
    return True

def _use_plasma_rifle(game_instance, player, locations, npcs, items):
    """Fire the weapon - reveals true nature on first use"""
    global _WEAPON_ACQUIRED
    
    if not _WEAPON_ACQUIRED:
        return False
    
    weapon = ALIEN_DATA['weapon']
    
    if weapon['ammo'] <= 0:
        print("\033[91mThe rod grows cold and dim. The lights have gone out.\033[0m")
        return True
    
    weapon['ammo'] -= 1
    
    # First time use - reveal true nature
    if weapon['ammo'] == 2:  # First use (started with 3)
        print("\033[91m" + "\n" + "="*60)
        print("THE ROD AWAKENS")
        print("="*60)
        print("You point the rod at a nearby tree.")
        print("It extends with a sound like tearing fabric!")
        print("Reality bends as blue-white fire erupts-")
        print("\n*** KRAK-THOOOOOOM ***")
        print("\nThe tree is gone. Not burned. Gone.")
        print("A perfect sphere of nothingness floats where it stood.")
        print(f"\n\033[96mWeapon identified: {weapon['true_name']}\033[0m")
        print(f"\033[90m{weapon['true_description']}\033[0m")
        print(f"\033[93mCharges remaining: {weapon['ammo']}\033[0m")
        print("="*60 + "\033[0m")
    else:
        print("\033[91m*** KRAK-THOOOOOOM ***\033[0m")
        print("The beam tears through reality itself!")
        print(f"\033[93mCharges remaining: {weapon['ammo']}\033[0m")
    
    # Check for targets
    location = locations[player.current_location]
    
    if player.current_location == 'lair' and not game_instance.dragon_defeated:
        print("\nThe beam strikes Vezareth!")
        print("The dragon roars as its very atoms unravel!")
        print("\033[93mVezareth has been... unmade.\033[0m")
        
        game_instance.dragon_defeated = True
        npcs['dragon']['health'] = 0
        locations['lair']['items'].append('crown')
        
        print("\nWhere the dragon stood, only the Crown of Eldoria remains.")
        print("Even gold is immune to... whatever this weapon does.")
        
    elif 'npc' in location and location['npc']:
        npc_key = location['npc']
        if npc_key in npcs:
            print(f"\nThe beam engulfs {npcs[npc_key]['name']}!")
            print("They simply cease to exist.")
            print("\033[90mYou feel a strange guilt. This power feels wrong.\033[0m")
            location['npc'] = None
            
    return True

def _examine_artifact(game_instance, player, locations, npcs, items):
    """Examine the weapon closer"""
    if not _WEAPON_ACQUIRED:
        return False
    
    print("\033[96m" + "\n" + "="*60)
    print("EXAMINING THE ROD")
    print("="*60)
    print("The metal is unlike any steel or iron you've seen.")
    print("It's too smooth. No forge marks. No imperfections.")
    print("The shifting symbols might be counting down...")
    print(f"\033[93mCurrent charge: {ALIEN_DATA['weapon']['ammo']}/3\033[0m")
    print("="*60 + "\033[0m")
    return True

def check_secret_command(command, game_instance, player, locations, npcs, items):
    """Main entry point for easter egg commands"""
    global _ANOMALY_ACTIVE, _POD_DISCOVERED, _WEAPON_ACQUIRED, _DREAM_TRIGGERED
    
    cmd = command.strip().lower()
    
    # Step 1: Rest at tavern/village with crystal shard (automatic on 'rest' or 'sleep')
    if cmd in ['rest', 'sleep', 'wait']:
        if _trigger_dream_sequence(game_instance, player, locations, npcs, items):
            return True
    
    # Step 2: Investigate the forest light
    if cmd in ['investigate light', 'follow glow', 'check crater', 'go to light']:
        if _reveal_crater(game_instance, player, locations, npcs, items):
            return True
    
    # Step 3: Acquire weapon (various commands work)
    if cmd in ['take rod', 'take metal rod', 'take twisted rod', 'grab rod', 
               'take artifact', 'touch symbols']:
        if _acquire_weapon(game_instance, player, locations, npcs, items):
            return True
    
    # Step 4: Use weapon (various commands)
    if cmd in ['use rod', 'aim rod', 'fire rod', 'use weapon', 'fire weapon']:
        if _use_plasma_rifle(game_instance, player, locations, npcs, items):
            return True
    
    # Examine commands
    if cmd in ['examine rod', 'examine artifact', 'examine sphere', 'check rod']:
        if _examine_artifact(game_instance, player, locations, npcs, items):
            return True
    
    # Alien combat (if summoned)
    if cmd == 'fight alien' and _WEAPON_ACQUIRED:
        return _alien_combat(game_instance, player, locations, npcs, items)
    
    return False

def _alien_combat(game_instance, player, locations, npcs, items):
    """Combat with aliens"""
    location = locations[player.current_location]
    
    if 'alien_encounter' not in location:
        print("No otherworldly entities present.")
        return True
    
    alien = ALIEN_DATA['aliens']['scout'].copy()
    alien_health = alien['health']
    
    print("\033[91m" + "\n" + "="*60)
    print(f"ENCOUNTER: {alien['name']}")
    print("="*60 + "\033[0m")
    
    while alien_health > 0 and player.health > 0:
        print(f"\n\033[91mEntity Integrity: {alien_health}%\033[0m")
        print(f"\033[92mYour Health: {player.health}/{player.max_health}\033[0m")
        
        print("\n1. Strike with sword")
        print("2. Use the rod")
        print("3. Try to communicate")
        
        choice = input("> ").strip()
        
        if choice == '1':
            dmg = 15 + player.combat_skill * 2
            alien_health -= dmg
            print(f"Your blade passes through... partially. {dmg} damage.")
        elif choice == '2':
            if ALIEN_DATA['weapon']['ammo'] > 0:
                ALIEN_DATA['weapon']['ammo'] -= 1
                print("\033[91m*** KRAK-THOOOOOOM ***\033[0m")
                print("The entity dissolves into static and screams.")
                alien_health = 0
            else:
                print("The rod is dead. Cold metal.")
                continue
        elif choice == '3':
            print("\033[95m'Take... the harvest... is all...'")
            print("It doesn't seem hostile. Just... desperate.\033[0m")
        else:
            print("Choose quickly!")
            continue
        
        if alien_health > 0:
            player.take_damage(alien['damage'])
            print(f"\033[91mThe {alien['name']} touches you. Cold burns through your veins! -{alien['damage']}\033[0m")
            for line in alien['dialogue']:
                print(f"\033[90m{line}\033[0m")
                time.sleep(0.3)
    
    if alien_health <= 0:
        print("\033[92mThe entity collapses into silver dust.\033[0m")
        del location['alien_encounter']
        
        # Drop hint about origin
        print("\033[90mIn its final moments, it points at the sky and whispers:")
        print("'The ship... waits... in the mountain...'\033[0m")
    
    return True

def on_game_start():
    """Reset all states"""
    global _ANOMALY_ACTIVE, _POD_DISCOVERED, _WEAPON_ACQUIRED, _DREAM_TRIGGERED, _CRATER_REVEALED
    _ANOMALY_ACTIVE = False
    _POD_DISCOVERED = False
    _WEAPON_ACQUIRED = False
    _DREAM_TRIGGERED = False
    _CRATER_REVEALED = False
    ALIEN_DATA['weapon']['ammo'] = 3

def get_status():
    """Debug status"""
    return {
        'dream_triggered': _DREAM_TRIGGERED,
        'anomaly_active': _ANOMALY_ACTIVE,
        'pod_found': _POD_DISCOVERED,
        'weapon_acquired': _WEAPON_ACQUIRED,
        'ammo': ALIEN_DATA['weapon']['ammo'] if _WEAPON_ACQUIRED else 0
    }