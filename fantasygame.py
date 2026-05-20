"""
Fantasy Quest: The Dragon's Curse
A text-based adventure game set in the magical Kingdom of Eldoria
Features: Quest system, XP/Leveling, Random Encounters, Combat, Crafting, Factions
"""

import sys
import time
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Game Constants
GAME_TITLE = "FANTASY QUEST: The Dragon's Curse"
GAME_VERSION = "2.0"
MAX_HEALTH_BASE = 100
MAX_MANA_BASE = 50

# Color codes for terminal output
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
    DARK_GRAY = '\033[90m'
    ORANGE = '\033[38;5;208m'

# ==================== ENUMS & DATA CLASSES ====================

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class QuestType(Enum):
    MAIN = "main"
    SIDE = "side"
    BOUNTY = "bounty"
    DELIVERY = "delivery"

class EnemyType(Enum):
    WOLF = "wolf"
    BANDIT = "bandit"
    SKELETON = "skeleton"
    GOBLIN = "goblin"
    TROLL = "troll"
    WRAITH = "wraith"
    DRAGON = "dragon"

class DamageType(Enum):
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    POISON = "poison"
    HOLY = "holy"

@dataclass
class Quest:
    id: str
    name: str
    description: str
    quest_type: QuestType
    status: QuestStatus = QuestStatus.NOT_STARTED
    objectives: List[str] = field(default_factory=list)
    completed_objectives: List[str] = field(default_factory=list)
    rewards: Dict = field(default_factory=dict)
    prerequisites: List[str] = field(default_factory=list)
    giver: str = ""
    location: str = ""
    xp_reward: int = 0
    gold_reward: int = 0

    def is_complete(self):
        return len(self.completed_objectives) >= len(self.objectives)

    def get_progress(self):
        if not self.objectives:
            return 0
        return len(self.completed_objectives) / len(self.objectives)

@dataclass
class Enemy:
    name: str
    enemy_type: EnemyType
    health: int
    max_health: int
    damage: int
    defense: int
    xp_value: int
    gold_drop: int
    weaknesses: List[DamageType] = field(default_factory=list)
    resistances: List[DamageType] = field(default_factory=list)
    special_ability: Optional[str] = None
    loot_table: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class Skill:
    name: str
    description: str
    damage_type: DamageType
    base_damage: int
    mana_cost: int
    cooldown: int = 0
    level_required: int = 1
    effect: Optional[str] = None


# ==================== ENEMY DEFINITIONS ====================

ENEMIES = {
    EnemyType.WOLF: Enemy(
        name="Dire Wolf",
        enemy_type=EnemyType.WOLF,
        health=40,
        max_health=40,
        damage=8,
        defense=2,
        xp_value=25,
        gold_drop=5,
        weaknesses=[DamageType.FIRE],
        loot_table=["wolf_pelt", "wolf_fang"],
        description="A massive wolf with glowing yellow eyes and matted gray fur."
    ),
    EnemyType.BANDIT: Enemy(
        name="Highway Bandit",
        enemy_type=EnemyType.BANDIT,
        health=55,
        max_health=55,
        damage=12,
        defense=5,
        xp_value=35,
        gold_drop=15,
        weaknesses=[DamageType.HOLY],
        loot_table=["rusty_dagger", "leather_armor", "bandit_map"],
        description="A rough-looking outlaw with a scarred face and greedy eyes."
    ),
    EnemyType.SKELETON: Enemy(
        name="Ancient Skeleton",
        enemy_type=EnemyType.SKELETON,
        health=35,
        max_health=35,
        damage=10,
        defense=8,
        xp_value=30,
        gold_drop=8,
        weaknesses=[DamageType.HOLY, DamageType.FIRE],
        resistances=[DamageType.POISON, DamageType.ICE],
        loot_table=["bone_fragments", "ancient_coin"],
        description="A clattering skeleton animated by dark magic, armed with a rusted sword."
    ),
    EnemyType.GOBLIN: Enemy(
        name="Cave Goblin",
        enemy_type=EnemyType.GOBLIN,
        health=30,
        max_health=30,
        damage=7,
        defense=1,
        xp_value=20,
        gold_drop=10,
        weaknesses=[DamageType.FIRE],
        loot_table=["goblin_ear", "small_gem", "crude_dagger"],
        description="A small, green-skinned creature with sharp teeth and beady red eyes."
    ),
    EnemyType.TROLL: Enemy(
        name="Forest Troll",
        enemy_type=EnemyType.TROLL,
        health=80,
        max_health=80,
        damage=15,
        defense=10,
        xp_value=60,
        gold_drop=25,
        weaknesses=[DamageType.FIRE],
        resistances=[DamageType.ICE, DamageType.POISON],
        special_ability="regenerate",
        loot_table=["troll_hide", "troll_blood", "large_gem"],
        description="A hulking brute with moss-covered skin and a foul stench. It regenerates wounds!"
    ),
    EnemyType.WRAITH: Enemy(
        name="Shadow Wraith",
        enemy_type=EnemyType.WRAITH,
        health=50,
        max_health=50,
        damage=14,
        defense=3,
        xp_value=50,
        gold_drop=20,
        weaknesses=[DamageType.HOLY, DamageType.FIRE],
        resistances=[DamageType.PHYSICAL],
        special_ability="drain_life",
        loot_table=["shadow_essence", "wraith_dust"],
        description="A spectral figure wreathed in darkness. Its touch drains life force."
    ),
    EnemyType.DRAGON: Enemy(
        name="Vezareth the Ancient",
        enemy_type=EnemyType.DRAGON,
        health=200,
        max_health=200,
        damage=25,
        defense=15,
        xp_value=500,
        gold_drop=200,
        weaknesses=[DamageType.ICE],
        resistances=[DamageType.FIRE],
        special_ability="fire_breath",
        loot_table=["dragon_scale", "dragon_heart", "crown"],
        description="An enormous dragon with scales like black iron and eyes burning with ancient malice."
    )
}


# ==================== ENCOUNTER TABLES ====================

ENCOUNTER_TABLES = {
    'village': [],
    'forest': [
        (EnemyType.WOLF, 0.4),
        (EnemyType.BANDIT, 0.3),
        (EnemyType.TROLL, 0.1),
        (None, 0.2)
    ],
    'tower': [
        (EnemyType.WRAITH, 0.3),
        (EnemyType.SKELETON, 0.3),
        (None, 0.4)
    ],
    'mountain': [
        (EnemyType.TROLL, 0.3),
        (EnemyType.WOLF, 0.2),
        (EnemyType.BANDIT, 0.2),
        (None, 0.3)
    ],
    'lair': [
        (EnemyType.DRAGON, 1.0)
    ],
    'cave': [
        (EnemyType.GOBLIN, 0.4),
        (EnemyType.SKELETON, 0.3),
        (EnemyType.WRAITH, 0.2),
        (None, 0.1)
    ],
    'market': [],
    'castle': [],
    'tavern': []
}

# ==================== SKILLS ====================

SKILLS = {
    'fireball': Skill(
        name="Fireball",
        description="Hurl a ball of flame at your enemy. Strong against beasts and undead.",
        damage_type=DamageType.FIRE,
        base_damage=25,
        mana_cost=15,
        level_required=2
    ),
    'ice_shard': Skill(
        name="Ice Shard",
        description="Launch a razor-sharp shard of ice. Strong against dragons and fire creatures.",
        damage_type=DamageType.ICE,
        base_damage=20,
        mana_cost=12,
        level_required=3
    ),
    'lightning_bolt': Skill(
        name="Lightning Bolt",
        description="Strike your foe with lightning from the sky. Bypasses some armor.",
        damage_type=DamageType.LIGHTNING,
        base_damage=30,
        mana_cost=20,
        level_required=4
    ),
    'heal': Skill(
        name="Healing Light",
        description="Restore health using holy magic. Scales with magic power.",
        damage_type=DamageType.HOLY,
        base_damage=-30,
        mana_cost=15,
        level_required=2
    ),
    'holy_smite': Skill(
        name="Holy Smite",
        description="Smite evil creatures with divine power. Very strong against undead.",
        damage_type=DamageType.HOLY,
        base_damage=35,
        mana_cost=25,
        level_required=5
    ),
    'poison_dart': Skill(
        name="Poison Dart",
        description="Throw a poisoned dart that deals damage over time.",
        damage_type=DamageType.POISON,
        base_damage=15,
        mana_cost=10,
        level_required=3
    )
}


# ==================== LOCATION DATA ====================

locations = {
    'village': {
        'name': 'Thorndale Village',
        'description': "A quaint medieval village with cobblestone streets and thatched-roof cottages. The air smells of fresh bread from the bakery, and you can hear the blacksmith's hammer in the distance. Children play in the square while elders watch from wooden benches.",
        'exits': {'north': 'forest', 'east': 'market', 'south': 'tavern'},
        'items': ['healing_potion', 'healing_potion'],
        'npc': 'elder',
        'danger_level': 0,
        'encounter_chance': 0.0,
        'special': 'rest_area'
    },
    'forest': {
        'name': 'Whispering Forest',
        'description': "Ancient oak trees tower above you, their leaves whispering secrets in the wind. Sunlight filters through the canopy, creating dancing patterns of light and shadow. The deeper you go, the darker it becomes. You sense eyes watching from the shadows.",
        'exits': {'south': 'village', 'east': 'tower', 'north': 'cave', 'west': 'ruins'},
        'items': ['magic_mushroom', 'forest_herbs'],
        'npc': 'hermit',
        'danger_level': 2,
        'encounter_chance': 0.45,
        'special': None
    },
    'ruins': {
        'name': 'Ancient Ruins',
        'description': "Crumbling stone pillars mark what was once a grand temple. Vines crawl over weathered statues of forgotten gods. The air feels heavy with ancient magic, and strange runes glow faintly on the walls. Something stirs in the darkness below.",
        'exits': {'east': 'forest'},
        'items': ['ancient_relic', 'ruined_scroll'],
        'npc': None,
        'danger_level': 4,
        'encounter_chance': 0.6,
        'special': 'dungeon_entrance'
    },
    'tower': {
        'name': "Wizard's Tower",
        'description': "A spiraling tower of dark stone reaches toward the sky. Strange magical energies pulse from within, and mystical symbols glow faintly on the walls. The door is enchanted - only those with magical aptitude may enter.",
        'exits': {'west': 'forest', 'north': 'mountain'},
        'items': ['spell_book', 'mana_potion'],
        'npc': 'wizard',
        'danger_level': 3,
        'encounter_chance': 0.35,
        'special': 'magic_shop'
    },
    'mountain': {
        'name': "Dragon's Peak",
        'description': "Craggy peaks pierce the clouds, and the air grows thin and cold. Jagged rocks make footing treacherous. In the distance, you can see smoke rising from what must be the dragon's lair. The wind howls like a dying beast.",
        'exits': {'south': 'tower', 'east': 'lair', 'west': 'mine'},
        'items': ['dragon_scale', 'climbing_gear'],
        'npc': None,
        'danger_level': 5,
        'encounter_chance': 0.5,
        'special': None
    },
    'mine': {
        'name': 'Abandoned Mine',
        'description': "A dark tunnel leads into the mountainside. Wooden supports creak ominously overhead. The smell of sulfur and earth fills your nostrils. You can hear distant clinking - goblins, perhaps, or something worse.",
        'exits': {'east': 'mountain'},
        'items': ['iron_ore', 'silver_ore'],
        'npc': None,
        'danger_level': 4,
        'encounter_chance': 0.55,
        'special': 'mining'
    },
    'lair': {
        'name': "Dragon's Lair",
        'description': "A massive cavern filled with glittering treasure. Bones of previous adventurers litter the floor, and you can hear the thunderous breathing of the great wyrm. The heat is oppressive, and the air shimmers with dragonfire residue.",
        'exits': {'west': 'mountain'},
        'items': [],
        'npc': 'dragon',
        'danger_level': 10,
        'encounter_chance': 1.0,
        'locked': True,
        'special': 'boss_arena'
    },
    'cave': {
        'name': 'Crystal Cave',
        'description': "Shimmering crystals line the walls of this underground chamber, casting rainbow reflections everywhere. The air hums with magical energy. One crystal pulses with an unusual blue resonance. It feels warm, almost alive.",
        'exits': {'south': 'forest', 'east': 'underground_lake'},
        'items': ['crystal_shard', 'glowing_mushroom'],
        'npc': None,
        'danger_level': 3,
        'encounter_chance': 0.4,
        'special': None
    },
    'underground_lake': {
        'name': 'Underground Lake',
        'description': "An vast underground lake stretches before you, its surface perfectly still and reflecting the crystal light from above. The water is impossibly clear, revealing strange shapes moving in the depths. A small boat is tied to a crystal pillar.",
        'exits': {'west': 'cave'},
        'items': ['pearl', 'water_breathing_potion'],
        'npc': 'mermaid',
        'danger_level': 3,
        'encounter_chance': 0.3,
        'special': 'fishing'
    },
    'market': {
        'name': "Merchant's Square",
        'description': "Bustling stalls display wares from across the kingdom. Merchants call out their goods, and the smell of exotic spices fills the air. A crowd of travelers, nobles, and adventurers haggle over prices. A notice board displays wanted posters and job listings.",
        'exits': {'west': 'village', 'north': 'castle'},
        'items': ['rope', 'torch', 'lockpick'],
        'npc': 'merchant',
        'danger_level': 0,
        'encounter_chance': 0.0,
        'special': 'shop'
    },
    'castle': {
        'name': 'Castle Eldoria',
        'description': "Majestic towers rise before you, banners bearing the royal crest fluttering in the breeze. Guards in polished armor stand at attention. The throne room awaits within, where the King's steward manages affairs in the monarch's absence.",
        'exits': {'south': 'market'},
        'items': ['sword', 'royal_seal'],
        'npc': 'knight',
        'danger_level': 0,
        'encounter_chance': 0.0,
        'special': 'quest_hub'
    },
    'tavern': {
        'name': 'The Prancing Pony Tavern',
        'description': "Warm firelight and the sound of merrymaking spill from this cozy tavern. The smell of ale and roasted meat makes your mouth water. Adventurers share tales at wooden tables, and a bard plays a lute in the corner. Rooms are available for rent.",
        'exits': {'north': 'village', 'east': 'stable'},
        'items': ['ale', 'stew', 'bread'],
        'npc': 'bard',
        'danger_level': 0,
        'encounter_chance': 0.0,
        'special': 'rest_area'
    },
    'stable': {
        'name': 'Royal Stables',
        'description': "Rows of well-kept stalls house horses of various breeds. The smell of hay and leather fills the air. A stablemaster tends to a magnificent white stallion. Mounts can be rented for faster travel between discovered locations.",
        'exits': {'west': 'tavern'},
        'items': ['horse_brush', 'apple'],
        'npc': 'stablemaster',
        'danger_level': 0,
        'encounter_chance': 0.0,
        'special': 'mount_shop'
    }
}


# ==================== ITEM DEFINITIONS ====================

items = {
    'healing_potion': {
        'name': 'Healing Potion',
        'description': "A glowing red liquid that restores 40 health points when consumed.",
        'type': 'consumable',
        'effect': 40,
        'value': 25,
        'rarity': 'common'
    },
    'mana_potion': {
        'name': 'Mana Potion',
        'description': "A shimmering blue liquid that restores 30 mana points.",
        'type': 'consumable',
        'effect': 30,
        'effect_type': 'mana',
        'value': 30,
        'rarity': 'common'
    },
    'magic_mushroom': {
        'name': 'Magic Mushroom',
        'description': "A luminescent fungus that enhances magical abilities. Permanently increases magic power by 1.",
        'type': 'permanent_boost',
        'effect': 1,
        'effect_type': 'magic_power',
        'value': 50,
        'rarity': 'rare'
    },
    'forest_herbs': {
        'name': 'Forest Herbs',
        'description': "Medicinal herbs gathered from the Whispering Forest. Can be used to craft healing items.",
        'type': 'crafting',
        'value': 10,
        'rarity': 'common'
    },
    'glowing_mushroom': {
        'name': 'Glowing Mushroom',
        'description': "A bioluminescent fungus that emits soft light. Useful for crafting potions.",
        'type': 'crafting',
        'value': 15,
        'rarity': 'uncommon'
    },
    'spell_book': {
        'name': 'Ancient Spell Book',
        'description': "A leather-bound tome filled with powerful incantations. Teaches the Fireball spell.",
        'type': 'key_item',
        'value': 100,
        'rarity': 'rare',
        'teaches': 'fireball'
    },
    'crystal_shard': {
        'name': 'Crystal Shard',
        'description': "A fragment of pure magical crystal. Glows with inner light. Essential for dragon lair barrier.",
        'type': 'key_item',
        'value': 75,
        'rarity': 'rare'
    },
    'sword': {
        'name': "Knight's Sword",
        'description': "A finely crafted blade etched with protective runes. Increases combat effectiveness significantly.",
        'type': 'weapon',
        'damage_bonus': 15,
        'value': 80,
        'rarity': 'uncommon'
    },
    'rusty_dagger': {
        'name': 'Rusty Dagger',
        'description': "A worn but functional blade. Better than nothing.",
        'type': 'weapon',
        'damage_bonus': 5,
        'value': 10,
        'rarity': 'common'
    },
    'crude_dagger': {
        'name': 'Crude Dagger',
        'description': "A goblin-made weapon. Surprisingly sharp despite its crude construction.",
        'type': 'weapon',
        'damage_bonus': 7,
        'value': 12,
        'rarity': 'common'
    },
    'rope': {
        'name': 'Climbing Rope',
        'description': "A sturdy rope woven from giant's hair. Strong enough to hold even a heavily armored warrior.",
        'type': 'tool',
        'value': 15,
        'rarity': 'common'
    },
    'torch': {
        'name': 'Torch',
        'description': "A wooden torch that provides light in dark places. May reveal hidden passages.",
        'type': 'tool',
        'value': 5,
        'rarity': 'common'
    },
    'lockpick': {
        'name': 'Lockpick Set',
        'description': "A set of fine tools for opening locked doors and chests. Requires skill to use effectively.",
        'type': 'tool',
        'value': 20,
        'rarity': 'uncommon'
    },
    'dragon_scale': {
        'name': 'Dragon Scale',
        'description': "A massive scale from an ancient dragon. Nearly indestructible. Provides fire resistance.",
        'type': 'key_item',
        'value': 150,
        'rarity': 'epic'
    },
    'dragon_heart': {
        'name': 'Dragon Heart',
        'description': "The still-warm heart of a dragon. Contains immense magical power. Can be used to craft legendary items.",
        'type': 'crafting',
        'value': 500,
        'rarity': 'legendary'
    },
    'crown': {
        'name': 'Crown of Eldoria',
        'description': "The legendary crown that grants authority over the realm. Forged by the First Kings and blessed by the gods. Your ultimate quest objective!",
        'type': 'quest_item',
        'value': 1000,
        'rarity': 'legendary'
    },
    'ale': {
        'name': 'Dwarven Ale',
        'description': "A strong alcoholic beverage that might loosen tongues or courage. Restores 15 health but reduces accuracy briefly.",
        'type': 'consumable',
        'effect': 15,
        'value': 8,
        'rarity': 'common'
    },
    'stew': {
        'name': 'Hearty Stew',
        'description': "A warm, nourishing stew of meat and vegetables. Restores 25 health and 10 mana.",
        'type': 'consumable',
        'effect': 25,
        'effect_type': 'health_mana',
        'value': 12,
        'rarity': 'common'
    },
    'bread': {
        'name': 'Fresh Bread',
        'description': "A crusty loaf of bread, still warm from the oven. Restores 10 health.",
        'type': 'consumable',
        'effect': 10,
        'value': 5,
        'rarity': 'common'
    },
    'ancient_relic': {
        'name': 'Ancient Relic',
        'description': "A strange artifact from a forgotten civilization. Pulsing with unknown magic. A collector would pay dearly for this.",
        'type': 'valuable',
        'value': 200,
        'rarity': 'epic'
    },
    'ruined_scroll': {
        'name': 'Ruined Scroll',
        'description': "A damaged scroll containing fragments of a powerful spell. Could be restored by a skilled wizard.",
        'type': 'quest_item',
        'value': 50,
        'rarity': 'uncommon'
    },
    'iron_ore': {
        'name': 'Iron Ore',
        'description': "Raw iron ore that can be smelted into weapons or armor. Common crafting material.",
        'type': 'crafting',
        'value': 15,
        'rarity': 'common'
    },
    'silver_ore': {
        'name': 'Silver Ore',
        'description': "Precious silver ore. Silver weapons are effective against undead and werewolves.",
        'type': 'crafting',
        'value': 40,
        'rarity': 'uncommon'
    },
    'pearl': {
        'name': 'Luminous Pearl',
        'description': "A pearl that glows with soft inner light. Found only in the Underground Lake. Highly valuable.",
        'type': 'valuable',
        'value': 100,
        'rarity': 'rare'
    },
    'water_breathing_potion': {
        'name': 'Water Breathing Potion',
        'description': "Allows breathing underwater for 10 minutes. The mermaids use these to trade with surface dwellers.",
        'type': 'consumable',
        'effect': 0,
        'effect_type': 'water_breathing',
        'value': 35,
        'rarity': 'uncommon'
    },
    'horse_brush': {
        'name': 'Horse Brush',
        'description': "A quality brush for grooming horses. Horses appreciate good care.",
        'type': 'tool',
        'value': 8,
        'rarity': 'common'
    },
    'apple': {
        'name': 'Red Apple',
        'description': "A crisp, sweet apple. Horses love them. Restores 5 health.",
        'type': 'consumable',
        'effect': 5,
        'value': 3,
        'rarity': 'common'
    },
    'royal_seal': {
        'name': 'Royal Seal',
        'description': "The official seal of the Kingdom of Eldoria. Grants authority to speak on behalf of the crown.",
        'type': 'key_item',
        'value': 200,
        'rarity': 'epic'
    },
    'climbing_gear': {
        'name': 'Climbing Gear',
        'description': "Professional climbing equipment. Essential for scaling Dragon's Peak safely.",
        'type': 'tool',
        'value': 30,
        'rarity': 'uncommon'
    },
    'wolf_pelt': {
        'name': 'Wolf Pelt',
        'description': "The thick fur of a dire wolf. Can be sold to merchants or crafted into armor.",
        'type': 'crafting',
        'value': 20,
        'rarity': 'common'
    },
    'wolf_fang': {
        'name': 'Wolf Fang',
        'description': "A sharp fang from a dire wolf. Used in crafting or as a trophy.",
        'type': 'crafting',
        'value': 12,
        'rarity': 'common'
    },
    'bandit_map': {
        'name': "Bandit's Map",
        'description': "A crude map showing bandit hideout locations and patrol routes. Could be useful to the guards.",
        'type': 'quest_item',
        'value': 30,
        'rarity': 'uncommon'
    },
    'leather_armor': {
        'name': 'Leather Armor',
        'description': "Sturdy leather armor offering basic protection. Increases defense by 5.",
        'type': 'armor',
        'defense_bonus': 5,
        'value': 35,
        'rarity': 'common'
    },
    'bone_fragments': {
        'name': 'Bone Fragments',
        'description': "Fragments of ancient bone. Necromancers value these for their rituals.",
        'type': 'crafting',
        'value': 15,
        'rarity': 'common'
    },
    'ancient_coin': {
        'name': 'Ancient Coin',
        'description': "A coin from a civilization long forgotten. Collectors pay well for these.",
        'type': 'valuable',
        'value': 25,
        'rarity': 'uncommon'
    },
    'goblin_ear': {
        'name': 'Goblin Ear',
        'description': "Proof of goblin slaying. Bounty hunters collect these for rewards.",
        'type': 'bounty',
        'value': 10,
        'rarity': 'common'
    },
    'small_gem': {
        'name': 'Small Gem',
        'description': "A small but valuable gemstone. Goblins hoard these obsessively.",
        'type': 'valuable',
        'value': 20,
        'rarity': 'common'
    },
    'troll_hide': {
        'name': 'Troll Hide',
        'description': "Thick, regenerating troll skin. Highly prized by armorers.",
        'type': 'crafting',
        'value': 50,
        'rarity': 'uncommon'
    },
    'troll_blood': {
        'name': 'Troll Blood',
        'description': "The regenerative blood of a troll. Alchemists use it in powerful healing potions.",
        'type': 'crafting',
        'value': 40,
        'rarity': 'uncommon'
    },
    'large_gem': {
        'name': 'Large Gem',
        'description': "A fist-sized gemstone of exceptional quality. Worth a small fortune.",
        'type': 'valuable',
        'value': 100,
        'rarity': 'rare'
    },
    'shadow_essence': {
        'name': 'Shadow Essence',
        'description': "A vial containing pure darkness. Handle with extreme care. Used in dark magic.",
        'type': 'crafting',
        'value': 60,
        'rarity': 'rare'
    },
    'wraith_dust': {
        'name': 'Wraith Dust',
        'description': "Fine powder left behind by a destroyed wraith. Glows faintly in moonlight.",
        'type': 'crafting',
        'value': 45,
        'rarity': 'uncommon'
    }
}


# ==================== NPC DEFINITIONS ====================

npcs = {
    'elder': {
        'name': 'Village Elder Aldric',
        'dialogue': [
            "Welcome, brave adventurer! I am Elder Aldric, keeper of Thorndale's wisdom.",
            "The Kingdom of Eldoria is in great peril. The ancient dragon Vezareth has awakened!",
            "He stole the Crown of Eldoria from Castle Eldoria three moons ago.",
            "Without the crown, the kingdom will fall into chaos and darkness.",
            "You must retrieve the crown from the dragon's lair atop Dragon's Peak!",
            "But first, you must prepare. Speak with the wizard in his tower - he knows magic that can breach the dragon's barrier.",
            "Also visit Sir Gareth at the castle. He may lend you his blessed sword.",
            "May the gods guide your path, hero."
        ],
        'quest_given': 'main_dragon_curse',
        'reward': None,
        'shop': False
    },
    'wizard': {
        'name': 'Archmage Zephyrus',
        'dialogue': [
            "Ah, I have been expecting you. The elder's visions are seldom wrong.",
            "To defeat the dragon, you will need more than mere steel and courage.",
            "Take this spell book. Within it lies the incantation to breach the dragon's lair barrier.",
            "You must also gather a crystal shard from the Crystal Cave to power the spell.",
            "Combine the spell book and crystal shard when you face the barrier.",
            "I sense great potential in you. Return when you are stronger, and I may teach you more spells."
        ],
        'requires_item': None,
        'reward': 'spell_book',
        'shop': True,
        'shop_items': ['mana_potion', 'ruined_scroll'],
        'teaches_spells': ['ice_shard', 'lightning_bolt']
    },
    'knight': {
        'name': 'Sir Gareth the Bold',
        'dialogue': [
            "By the king's beard! Another would-be dragonslayer?",
            "I admire your courage, but many have tried and failed before you.",
            "I was there when the dragon attacked. I saw good men burn alive.",
            "Take my sword. It has been blessed by the royal priest and may serve you better than most.",
            "Remember: strike for the heart, where the scales are weakest!",
            "Also, if you find any bandits on the roads, bring me proof. There's a bounty on their heads."
        ],
        'requires_item': None,
        'reward': 'sword',
        'shop': False,
        'gives_quest': 'bandit_bounty'
    },
    'merchant': {
        'name': 'Trader Matthias',
        'dialogue': [
            "Finest wares in the kingdom! What catches your eye, friend?",
            "Ah, for a dragonslayer, I have just the thing!",
            "This rope is woven from giant's hair. Strong enough to hold even a heavily armored warrior.",
            "I also have climbing gear for the treacherous paths to Dragon's Peak.",
            "If you bring me rare materials - pelts, gems, relics - I'll pay top coin!"
        ],
        'requires_item': None,
        'reward': None,
        'shop': True,
        'shop_items': ['healing_potion', 'mana_potion', 'rope', 'torch', 'climbing_gear', 'lockpick']
    },
    'hermit': {
        'name': 'Forest Hermit Graybeard',
        'dialogue': [
            "The trees whisper of your coming, young hero. I have lived here for decades.",
            "I gather rare herbs and mushrooms from these woods. This magic mushroom will enhance your vitality.",
            "Beware the dragon's fire. It burns hotter than any forge in the kingdom.",
            "The ruins to the west are cursed. Ancient evil stirs there. Enter at your own peril.",
            "If you bring me forest herbs, I can teach you to craft better potions."
        ],
        'requires_item': None,
        'reward': 'magic_mushroom',
        'shop': False,
        'crafting': True
    },
    'bard': {
        'name': 'Tavern Bard Lyrion',
        'dialogue': [
            "Oh gather 'round and hear my tale, of dragon fierce and bold!",
            "Who stole the crown from royal brow, in caverns dark and cold!",
            "Many have tried to claim it back, but none have yet returned...",
            "Perhaps you'll be the hero whose name will be well-earned!",
            "Speak with Sir Gareth upstairs. He's been in a foul mood since the crown was taken.",
            "If you complete any great deeds, come tell me! I'll compose a ballad in your honor."
        ],
        'requires_item': None,
        'reward': None,
        'shop': False
    },
    'dragon': {
        'name': 'Vezareth the Ancient',
        'dialogue': [
            "FOOLISH MORTAL! You dare enter the domain of Vezareth?",
            "I have lived for a thousand years! I have devoured countless heroes!",
            "You think your pathetic magic can harm me? I AM THE EMBODIMENT OF POWER!",
            "Very well... face my wrath and become another pile of bones in my collection!"
        ],
        'is_enemy': True,
        'health': 200,
        'damage': 25,
        'shop': False
    },
    'mermaid': {
        'name': 'Nerissa the Lake Guardian',
        'dialogue': [
            "Greetings, surface dweller. I am Nerissa, guardian of these waters.",
            "The lake holds many secrets, and some dangers. The depths are not safe for mortals.",
            "I have lived here for centuries, watching the world above change.",
            "If you bring me pearls from the deep, I can reward you with water breathing potions.",
            "Beware the shadow that has fallen over the kingdom. Even the waters feel its chill."
        ],
        'requires_item': None,
        'reward': 'water_breathing_potion',
        'shop': True,
        'shop_items': ['pearl', 'water_breathing_potion']
    },
    'stablemaster': {
        'name': 'Stablemaster Hrothgar',
        'dialogue': [
            "Welcome to the royal stables, traveler! Finest mounts in the realm.",
            "For 50 gold, I can rent you a horse that knows all the safe paths.",
            "With a mount, you can travel between discovered locations instantly!",
            "Just say 'mount' or 'travel' when you want to ride.",
            "Take good care of the horse, or I'll take it out of your hide!"
        ],
        'requires_item': None,
        'reward': None,
        'shop': True,
        'shop_items': ['horse_brush', 'apple'],
        'service': 'mount_rental'
    }
}


# ==================== QUEST DEFINITIONS ====================

QUESTS = {
    'main_dragon_curse': Quest(
        id='main_dragon_curse',
        name="The Dragon's Curse",
        description="The ancient dragon Vezareth has stolen the Crown of Eldoria. Retrieve it from the dragon's lair atop Dragon's Peak to save the kingdom.",
        quest_type=QuestType.MAIN,
        objectives=[
            "Speak with the Village Elder",
            "Obtain the Spell Book from the Wizard",
            "Gather a Crystal Shard from the Crystal Cave",
            "Obtain a weapon from Sir Gareth",
            "Defeat the dragon Vezareth",
            "Retrieve the Crown of Eldoria"
        ],
        rewards={'xp': 1000, 'gold': 500, 'item': 'crown'},
        giver='elder',
        location='village',
        xp_reward=1000,
        gold_reward=500
    ),
    'bandit_bounty': Quest(
        id='bandit_bounty',
        name='Road Bandits',
        description="Bandits have been terrorizing the roads between the village and forest. Sir Gareth has posted a bounty. Bring proof of 3 bandit kills.",
        quest_type=QuestType.BOUNTY,
        objectives=[
            "Defeat 3 bandits in the forest or roads",
            "Collect proof of kills (Bandit Maps or trophies)",
            "Return to Sir Gareth for reward"
        ],
        rewards={'xp': 200, 'gold': 100, 'item': 'leather_armor'},
        giver='knight',
        location='castle',
        xp_reward=200,
        gold_reward=100
    ),
    'crystal_hunt': Quest(
        id='crystal_hunt',
        name='Crystal Hunt',
        description="The Wizard needs more crystal shards for his research. Gather 3 crystal shards from the Crystal Cave.",
        quest_type=QuestType.SIDE,
        objectives=[
            "Enter the Crystal Cave",
            "Gather 3 crystal shards",
            "Return to the Wizard"
        ],
        rewards={'xp': 150, 'gold': 75, 'spell': 'lightning_bolt'},
        prerequisites=['main_dragon_curse'],
        giver='wizard',
        location='tower',
        xp_reward=150,
        gold_reward=75
    ),
    'herb_gathering': Quest(
        id='herb_gathering',
        name='Herb Gathering',
        description="The Forest Hermit needs rare herbs for his potion brewing. Gather 5 forest herbs from the Whispering Forest.",
        quest_type=QuestType.DELIVERY,
        objectives=[
            "Gather 5 forest herbs",
            "Return to the Forest Hermit"
        ],
        rewards={'xp': 100, 'gold': 50, 'item': 'healing_potion'},
        giver='hermit',
        location='forest',
        xp_reward=100,
        gold_reward=50
    ),
    'ruins_exploration': Quest(
        id='ruins_exploration',
        name='Secrets of the Past',
        description="Ancient ruins have been discovered west of the forest. Explore them and find any artifacts or information about the old civilization.",
        quest_type=QuestType.SIDE,
        objectives=[
            "Find the Ancient Ruins",
            "Explore the ruins and defeat any guardians",
            "Find an ancient relic",
            "Return to the Village Elder"
        ],
        rewards={'xp': 300, 'gold': 150, 'item': 'ancient_relic'},
        giver='elder',
        location='village',
        xp_reward=300,
        gold_reward=150
    ),
    'goblin_menace': Quest(
        id='goblin_menace',
        name='Goblin Menace',
        description="Goblins have infested the abandoned mine. Clear them out and bring back proof of their leader's presence.",
        quest_type=QuestType.BOUNTY,
        objectives=[
            "Enter the Abandoned Mine",
            "Defeat 5 goblins",
            "Find proof of the goblin leader's presence",
            "Return to the Merchant"
        ],
        rewards={'xp': 250, 'gold': 125, 'item': 'silver_ore'},
        giver='merchant',
        location='market',
        xp_reward=250,
        gold_reward=125
    ),
    'lake_mystery': Quest(
        id='lake_mystery',
        name='Mystery of the Deep',
        description="Strange lights have been seen in the Underground Lake. Investigate and report back to the Mermaid Guardian.",
        quest_type=QuestType.SIDE,
        objectives=[
            "Reach the Underground Lake",
            "Investigate the strange lights",
            "Find the source of the disturbance",
            "Report to Nerissa"
        ],
        rewards={'xp': 200, 'gold': 100, 'item': 'pearl'},
        giver='mermaid',
        location='underground_lake',
        xp_reward=200,
        gold_reward=100
    )
}


# ==================== PLAYER CLASS ====================

class Player:
    """Enhanced player character with XP, leveling, skills, and stats"""

    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.health = MAX_HEALTH_BASE
        self.max_health = MAX_HEALTH_BASE
        self.mana = MAX_MANA_BASE
        self.max_mana = MAX_MANA_BASE
        self.gold = 50
        self.inventory = []
        self.current_location = 'village'
        self.visited_locations = ['village']
        self.discovered_locations = ['village', 'market', 'tavern']
        self.quests = {}
        self.completed_quests = []
        self.spells_learned = []
        self.combat_skill = 1
        self.magic_power = 1
        self.defense = 0
        self.luck = 1
        self.equipped_weapon = None
        self.equipped_armor = None
        self.enemies_defeated = 0
        self.bandits_killed = 0
        self.goblins_killed = 0
        self.deaths = 0
        self.total_gold_earned = 0
        self.potions_consumed = 0
        self.has_mount = False
        self.reputation = {
            'village': 0,
            'castle': 0,
            'wizard': 0,
            'merchant': 0
        }

    def take_damage(self, amount):
        """Apply damage to player, accounting for defense"""
        actual_damage = max(amount - self.defense, 1)
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            self.deaths += 1
            return True
        return False

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)

    def restore_mana(self, amount):
        """Restore mana"""
        self.mana = min(self.mana + amount, self.max_mana)

    def use_mana(self, amount):
        """Use mana for spells"""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def add_xp(self, amount):
        """Add XP and check for level ups"""
        self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()
            leveled_up = True
        return leveled_up

    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.max_health += 15
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.combat_skill += 1
        self.magic_power += 1
        self.luck += 0.5

    def add_item(self, item_key):
        """Add item to inventory"""
        if item_key in items:
            self.inventory.append(item_key)
            if items[item_key]['type'] == 'weapon' and not self.equipped_weapon:
                self.equip_item(item_key)
            elif items[item_key]['type'] == 'armor' and not self.equipped_armor:
                self.equip_item(item_key)
            return True
        return False

    def remove_item(self, item_key):
        """Remove item from inventory"""
        if item_key in self.inventory:
            self.inventory.remove(item_key)
            if self.equipped_weapon == item_key:
                self.equipped_weapon = None
            if self.equipped_armor == item_key:
                self.equipped_armor = None
            return True
        return False

    def has_item(self, item_key):
        """Check if player has item"""
        return item_key in self.inventory

    def equip_item(self, item_key):
        """Equip a weapon or armor"""
        if item_key not in self.inventory:
            return False
        item = items[item_key]
        if item['type'] == 'weapon':
            if self.equipped_weapon:
                old = items[self.equipped_weapon]
                if 'damage_bonus' in old:
                    self.combat_skill -= old['damage_bonus'] // 10
            self.equipped_weapon = item_key
            if 'damage_bonus' in item:
                self.combat_skill += item['damage_bonus'] // 10
            return True
        elif item['type'] == 'armor':
            if self.equipped_armor:
                old = items[self.equipped_armor]
                if 'defense_bonus' in old:
                    self.defense -= old['defense_bonus']
            self.equipped_armor = item_key
            if 'defense_bonus' in item:
                self.defense += item['defense_bonus']
            return True
        return False

    def get_attack_damage(self):
        """Calculate attack damage"""
        base = 5 + (self.combat_skill * 3) + (self.level * 2)
        if self.equipped_weapon and items[self.equipped_weapon]['type'] == 'weapon':
            base += items[self.equipped_weapon].get('damage_bonus', 0)
        variation = random.randint(-2, 3)
        return max(base + variation, 1)

    def get_spell_damage(self, spell_name):
        """Calculate spell damage"""
        if spell_name not in SKILLS:
            return 0
        skill = SKILLS[spell_name]
        base = skill.base_damage
        multiplier = 1 + (self.magic_power * 0.2) + (self.level * 0.1)
        return int(base * multiplier)

    def get_stats(self):
        """Get comprehensive player statistics"""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'xp_to_next': self.xp_to_next,
            'health': f"{self.health}/{self.max_health}",
            'mana': f"{self.mana}/{self.max_mana}",
            'gold': self.gold,
            'combat_skill': self.combat_skill,
            'magic_power': self.magic_power,
            'defense': self.defense,
            'luck': self.luck,
            'inventory_count': len(self.inventory),
            'locations_discovered': len(self.discovered_locations),
            'quests_active': len([q for q in self.quests.values() if q.status == QuestStatus.ACTIVE]),
            'quests_completed': len(self.completed_quests),
            'enemies_defeated': self.enemies_defeated,
            'deaths': self.deaths
        }


# ==================== GAME CLASS ====================

class Game:
    """Enhanced main game class with quest system, encounters, and deep mechanics"""

    def __init__(self):
        self.player = None
        self.game_running = True
        self.dragon_defeated = False
        self.turn_count = 0
        self.current_enemy = None
        self.in_combat = False
        self.difficulty_modifiers = {
            'easy': 0.7,
            'normal': 1.0,
            'hard': 1.3,
            'nightmare': 1.8
        }
        self.difficulty = 'normal'

    def slow_print(self, text, delay=0.03):
        """Print text with typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def print_header(self, text, color=Colors.CYAN):
        """Print a formatted header"""
        print(color + Colors.BOLD)
        print("=" * 60)
        print(f"{text:^60}")
        print("=" * 60)
        print(Colors.RESET)

    def display_title_screen(self):
        """Show the game title and introduction"""
        print(Colors.CYAN + Colors.BOLD)
        print("=" * 70)
        print("       FANTASY QUEST: The Dragon's Curse")
        print("              ~ Enhanced Edition ~")
        print("=" * 70)
        print(Colors.RESET)
        print()
        self.slow_print("Welcome to the Kingdom of Eldoria!", 0.05)
        self.slow_print("The ancient dragon Vezareth has awakened from his thousand-year slumber...", 0.04)
        self.slow_print("He has stolen the Crown of Eldoria - the symbol of royal authority!", 0.04)
        self.slow_print("Without it, the kingdom will fall into chaos and darkness...", 0.04)
        self.slow_print("You are the realm's last hope. Will you accept this quest?", 0.04)
        print()
        print(Colors.YELLOW + "Features: Quest System | XP & Leveling | Random Encounters | Crafting | Factions" + Colors.RESET)
        print()

    def get_player_name(self):
        """Get player name at game start"""
        while True:
            name = input("Enter your hero's name: ").strip()
            if name and len(name) > 0:
                return name
            print("Please enter a valid name.")

    def choose_difficulty(self):
        """Let player choose difficulty"""
        print(Colors.YELLOW + "\nChoose your difficulty:" + Colors.RESET)
        print("1. Easy - Enemies are weaker, more resources")
        print("2. Normal - Balanced challenge")
        print("3. Hard - Enemies are stronger, fewer resources")
        print("4. Nightmare - Only for the bravest heroes")

        while True:
            choice = input("\nChoice (1-4): ").strip()
            difficulties = {'1': 'easy', '2': 'normal', '3': 'hard', '4': 'nightmare'}
            if choice in difficulties:
                self.difficulty = difficulties[choice]
                mod = self.difficulty_modifiers[self.difficulty]
                print(Colors.GREEN + f"\nDifficulty set to {self.difficulty.upper()}. Enemy strength: {mod}x" + Colors.RESET)
                return
            print("Invalid choice.")

    def display_location(self):
        """Display current location information with enhanced details"""
        location = locations[self.player.current_location]

        print(Colors.YELLOW + Colors.BOLD + f"\n{'='*60}" + Colors.RESET)
        print(Colors.YELLOW + Colors.BOLD + f"  {location['name']}" + Colors.RESET)
        print(Colors.YELLOW + f"{'='*60}" + Colors.RESET)
        print(location['description'])

        danger = location.get('danger_level', 0)
        if danger > 0:
            danger_color = Colors.GREEN if danger <= 2 else Colors.YELLOW if danger <= 4 else Colors.RED
            print(danger_color + f"\n[Danger Level: {danger}/10]" + Colors.RESET)

        print(Colors.GREEN + "\nExits: " + Colors.RESET, end="")
        exit_list = list(location['exits'].keys())
        print(", ".join(exit_list))

        if location['items']:
            print(Colors.BLUE + "\nItems here: " + Colors.RESET, end="")
            item_names = [items[item]['name'] for item in location['items']]
            print(", ".join(item_names))

        if location['npc']:
            npc_name = npcs[location['npc']]['name']
            print(Colors.PURPLE + f"\n{npc_name} is here." + Colors.RESET)

        special = location.get('special')
        if special == 'rest_area':
            print(Colors.CYAN + "\n[Rest Area - You can 'rest' here to recover]" + Colors.RESET)
        elif special == 'shop':
            print(Colors.CYAN + "\n[Market - You can 'trade' with merchants]" + Colors.RESET)
        elif special == 'quest_hub':
            print(Colors.CYAN + "\n[Quest Hub - Check the 'board' for jobs]" + Colors.RESET)

        print(Colors.YELLOW + f"{'='*60}" + Colors.RESET)

    def check_random_encounter(self):
        """Check for random encounters when entering dangerous areas"""
        location = locations[self.player.current_location]
        danger = location.get('danger_level', 0)
        encounter_chance = location.get('encounter_chance', 0)

        if danger == 0 or encounter_chance == 0:
            return False

        if random.random() > encounter_chance:
            return False

        table = ENCOUNTER_TABLES.get(self.player.current_location, [])
        if not table:
            return False

        roll = random.random()
        cumulative = 0
        selected_enemy = None

        for enemy_type, weight in table:
            cumulative += weight
            if roll <= cumulative:
                selected_enemy = enemy_type
                break

        if selected_enemy is None:
            return False

        self.spawn_encounter(selected_enemy)
        return True

    def spawn_encounter(self, enemy_type):
        """Spawn a random encounter"""
        if enemy_type not in ENEMIES:
            return

        base_enemy = ENEMIES[enemy_type]
        mod = self.difficulty_modifiers[self.difficulty]

        enemy = Enemy(
            name=base_enemy.name,
            enemy_type=base_enemy.enemy_type,
            health=int(base_enemy.health * mod),
            max_health=int(base_enemy.max_health * mod),
            damage=int(base_enemy.damage * mod),
            defense=base_enemy.defense,
            xp_value=int(base_enemy.xp_value * mod),
            gold_drop=int(base_enemy.gold_drop * mod),
            weaknesses=base_enemy.weaknesses,
            resistances=base_enemy.resistances,
            special_ability=base_enemy.special_ability,
            loot_table=base_enemy.loot_table,
            description=base_enemy.description
        )

        self.current_enemy = enemy
        self.in_combat = True

        print(Colors.RED + Colors.BOLD)
        print("\n" + "!" * 60)
        print("           RANDOM ENCOUNTER!")
        print("!" * 60)
        print(Colors.RESET)
        print(Colors.RED + f"A {enemy.name} appears!" + Colors.RESET)
        print(Colors.DARK_GRAY + enemy.description + Colors.RESET)
        print()

        self.combat_loop()


    def combat_loop(self):
        """Main combat loop for both random encounters and boss fights"""
        enemy = self.current_enemy
        if not enemy:
            return

        if enemy.enemy_type == EnemyType.DRAGON:
            self.print_header("BOSS BATTLE: Vezareth the Ancient", Colors.RED)
            for line in npcs['dragon']['dialogue']:
                self.slow_print(f'"{line}"', 0.04)
                time.sleep(0.3)
        else:
            self.print_header(f"COMBAT: {enemy.name}", Colors.ORANGE)

        turn = 0
        while enemy.health > 0 and self.player.health > 0:
            turn += 1
            print(f"\n{Colors.RED}Enemy: {enemy.name} | Health: {enemy.health}/{enemy.max_health}{Colors.RESET}")
            print(f"{Colors.GREEN}You: {self.player.health}/{self.player.max_health} HP | {self.player.mana}/{self.player.max_mana} MP{Colors.RESET}")

            if self.player.equipped_weapon:
                print(f"{Colors.CYAN}Weapon: {items[self.player.equipped_weapon]['name']}{Colors.RESET}")

            print("\nWhat will you do?")
            print(f"{Colors.YELLOW}1.{Colors.RESET} Attack with weapon")
            print(f"{Colors.YELLOW}2.{Colors.RESET} Cast spell")
            print(f"{Colors.YELLOW}3.{Colors.RESET} Use item")
            print(f"{Colors.YELLOW}4.{Colors.RESET} Defend")
            print(f"{Colors.YELLOW}5.{Colors.RESET} Flee")

            choice = input("\nYour choice (1-5): ").strip()

            if choice == '1':
                damage = self.player.get_attack_damage()

                crit_chance = 0.05 + (self.player.luck * 0.02)
                if random.random() < crit_chance:
                    damage = int(damage * 1.5)
                    print(Colors.YELLOW + "\nCRITICAL HIT!" + Colors.RESET)

                actual_damage = max(damage - enemy.defense, 1)
                enemy.health -= actual_damage
                print(Colors.GREEN + f"\nYou strike for {actual_damage} damage!" + Colors.RESET)

            elif choice == '2':
                if not self.player.spells_learned:
                    print(Colors.YELLOW + "\nYou don't know any spells!" + Colors.RESET)
                    continue

                print("\nAvailable spells:")
                for i, spell in enumerate(self.player.spells_learned, 1):
                    skill = SKILLS[spell]
                    print(f"{i}. {skill.name} (MP: {skill.mana_cost}, DMG: {self.player.get_spell_damage(spell)})")
                print(f"{len(self.player.spells_learned)+1}. Cancel")

                spell_choice = input("\nChoose spell: ").strip()
                try:
                    idx = int(spell_choice) - 1
                    if idx == len(self.player.spells_learned):
                        continue
                    if 0 <= idx < len(self.player.spells_learned):
                        spell_name = self.player.spells_learned[idx]
                        skill = SKILLS[spell_name]

                        if not self.player.use_mana(skill.mana_cost):
                            print(Colors.RED + "\nNot enough mana!" + Colors.RESET)
                            continue

                        damage = self.player.get_spell_damage(spell_name)

                        if skill.damage_type in enemy.weaknesses:
                            damage = int(damage * 1.5)
                            print(Colors.YELLOW + "\nIt's super effective!" + Colors.RESET)
                        elif skill.damage_type in enemy.resistances:
                            damage = int(damage * 0.5)
                            print(Colors.YELLOW + "\nIt's not very effective..." + Colors.RESET)

                        if skill.base_damage < 0:
                            heal_amount = abs(damage)
                            self.player.heal(heal_amount)
                            print(Colors.GREEN + f"\nYou cast {skill.name} and heal for {heal_amount} HP!" + Colors.RESET)
                        else:
                            actual_damage = max(damage - enemy.defense, 1)
                            enemy.health -= actual_damage
                            print(Colors.PURPLE + f"\nYou cast {skill.name} for {actual_damage} damage!" + Colors.RESET)
                    else:
                        continue
                except ValueError:
                    continue

            elif choice == '3':
                self.use_item_in_combat()
                continue

            elif choice == '4':
                print(Colors.CYAN + "\nYou take a defensive stance! Damage reduced this turn." + Colors.RESET)
                self.player.defense += 5

            elif choice == '5':
                if enemy.enemy_type == EnemyType.DRAGON:
                    print(Colors.RED + "\nYou cannot flee from the dragon!" + Colors.RESET)
                    continue
                flee_chance = 0.4 + (self.player.luck * 0.05)
                if random.random() < flee_chance:
                    print(Colors.GREEN + "\nYou successfully flee from combat!" + Colors.RESET)
                    self.in_combat = False
                    self.current_enemy = None
                    return
                else:
                    print(Colors.RED + "\nFailed to flee!" + Colors.RESET)
            else:
                print("Invalid choice!")
                continue

            # Enemy's turn
            if enemy.health > 0:
                print(Colors.RED + f"\nThe {enemy.name} attacks!" + Colors.RESET)

                enemy_damage = enemy.damage

                if enemy.special_ability == 'regenerate' and random.random() < 0.3:
                    heal = int(enemy.max_health * 0.1)
                    enemy.health = min(enemy.health + heal, enemy.max_health)
                    print(Colors.RED + f"The {enemy.name} regenerates {heal} health!" + Colors.RESET)

                if enemy.special_ability == 'drain_life' and random.random() < 0.25:
                    drain = int(enemy_damage * 0.3)
                    enemy.health = min(enemy.health + drain, enemy.max_health)
                    print(Colors.RED + f"The {enemy.name} drains {drain} life from you!" + Colors.RESET)

                if enemy.special_ability == 'fire_breath' and random.random() < 0.4:
                    enemy_damage = int(enemy_damage * 1.5)
                    print(Colors.RED + f"The {enemy.name} breathes fire!" + Colors.RESET)

                died = self.player.take_damage(enemy_damage)
                print(Colors.RED + f"You take {enemy_damage} damage!" + Colors.RESET)

                if died:
                    print(Colors.RED + Colors.BOLD + "\nYou have been defeated!" + Colors.RESET)
                    print(Colors.DARK_GRAY + "The darkness takes you... but the gods are not done with you yet." + Colors.RESET)
                    self.player.health = self.player.max_health // 2
                    self.player.mana = self.player.max_mana // 2
                    self.player.gold = max(self.player.gold - 20, 0)
                    self.player.current_location = 'village'
                    print(Colors.GREEN + "\nYou awaken back in Thorndale Village, wounded but alive..." + Colors.RESET)
                    self.in_combat = False
                    self.current_enemy = None
                    return

            if choice == '4':
                self.player.defense -= 5

        # Combat ended
        if enemy.health <= 0:
            self.player.enemies_defeated += 1

            if enemy.enemy_type == EnemyType.BANDIT:
                self.player.bandits_killed += 1
            elif enemy.enemy_type == EnemyType.GOBLIN:
                self.player.goblins_killed += 1

            xp_gain = enemy.xp_value
            gold_gain = enemy.gold_drop

            leveled = self.player.add_xp(xp_gain)
            self.player.gold += gold_gain
            self.player.total_gold_earned += gold_gain

            print(Colors.GREEN + Colors.BOLD)
            print("\n" + "=" * 50)
            print(f"     VICTORY! {enemy.name} DEFEATED!")
            print("=" * 50)
            print(Colors.RESET)
            print(Colors.YELLOW + f"Gained {xp_gain} XP and {gold_gain} gold!" + Colors.RESET)

            if leveled:
                print(Colors.PURPLE + Colors.BOLD + f"\n*** LEVEL UP! You are now level {self.player.level}! ***" + Colors.RESET)
                print(Colors.CYAN + f"Max HP: {self.player.max_health} | Max MP: {self.player.max_mana}" + Colors.RESET)
                print(Colors.CYAN + f"Combat Skill: {self.player.combat_skill} | Magic Power: {self.player.magic_power}" + Colors.RESET)
                self.check_new_spells()

            if enemy.loot_table:
                dropped = random.choice(enemy.loot_table)
                if dropped in items:
                    self.player.add_item(dropped)
                    print(Colors.BLUE + f"\nLoot: Found {items[dropped]['name']}!" + Colors.RESET)

            if enemy.enemy_type == EnemyType.DRAGON:
                self.dragon_defeated = True
                print(Colors.YELLOW + Colors.BOLD + "\n*** THE DRAGON IS SLAIN! ***" + Colors.RESET)
                print(Colors.CYAN + "Among the treasure, you spot the Crown of Eldoria!" + Colors.RESET)
                locations['lair']['items'].append('crown')
                self.complete_quest_objective('main_dragon_curse', 'Defeat the dragon Vezareth')
                self.complete_quest_objective('main_dragon_curse', 'Retrieve the Crown of Eldoria')

            self.in_combat = False
            self.current_enemy = None


    def check_new_spells(self):
        """Check if player can learn new spells on level up"""
        for spell_name, skill in SKILLS.items():
            if skill.level_required <= self.player.level and spell_name not in self.player.spells_learned:
                if spell_name == 'fireball' and not self.player.has_item('spell_book'):
                    continue
                self.player.spells_learned.append(spell_name)
                print(Colors.PURPLE + f"\nNew spell learned: {skill.name}!" + Colors.RESET)
                print(Colors.DARK_GRAY + skill.description + Colors.RESET)

    def use_item_in_combat(self):
        """Use an item during combat"""
        consumables = [item for item in self.player.inventory if items[item]['type'] == 'consumable']

        if not consumables:
            print(Colors.YELLOW + "\nNo usable items!" + Colors.RESET)
            return

        print("\nAvailable items:")
        for i, item_key in enumerate(consumables, 1):
            print(f"{i}. {items[item_key]['name']}")
        print(f"{len(consumables)+1}. Cancel")

        choice = input("\nUse item: ").strip()
        try:
            idx = int(choice) - 1
            if idx == len(consumables):
                return
            if 0 <= idx < len(consumables):
                item_key = consumables[idx]
                self.use_item_by_key(item_key)
        except ValueError:
            pass

    def process_command(self, command):
        """Process player commands"""
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
            self.talk_to_npc()

        elif verb == 'examine' or verb == 'look':
            self.display_location()

        elif verb == 'equip':
            if len(parts) > 1:
                self.equip_item(' '.join(parts[1:]))
            else:
                print("Equip what?")

        elif verb == 'unequip':
            if len(parts) > 1:
                self.unequip_item(' '.join(parts[1:]))
            else:
                print("Unequip what?")

        # System commands
        elif verb == 'inventory' or verb == 'inv' or verb == 'i':
            self.show_inventory()

        elif verb == 'stats' or verb == 'status':
            self.show_stats()

        elif verb == 'quest' or verb == 'quests':
            self.show_quests()

        elif verb == 'journal':
            self.show_journal()

        elif verb == 'map':
            self.show_map()

        elif verb == 'craft':
            self.show_crafting()

        elif verb == 'rest' or verb == 'sleep':
            self.rest()

        elif verb == 'help' or verb == 'h' or verb == '?':
            self.show_help()

        elif verb == 'quit' or verb == 'exit':
            self.game_running = False
            print("Thanks for playing! Farewell, brave adventurer!")

        else:
            print("I don't understand that command. Type 'help' for a list of commands.")


    def move_player(self, direction):
        """Move player to a new location with encounter checks"""
        location = locations[self.player.current_location]

        if direction in location['exits']:
            new_location = location['exits'][direction]

            # Check if location is locked
            if 'locked' in locations[new_location] and locations[new_location]['locked']:
                if new_location == 'lair':
                    if self.player.has_item('spell_book') and self.player.has_item('crystal_shard'):
                        print(Colors.CYAN + "\nYou raise the spell book and crystal shard..." + Colors.RESET)
                        self.slow_print("Ancient words flow from your lips as magical energy surrounds you!")
                        self.slow_print("The dragon's barrier shimmers and fades away!")
                        locations[new_location]['locked'] = False
                        print(Colors.GREEN + "The way to the dragon's lair is now open!" + Colors.RESET)
                        self.complete_quest_objective('main_dragon_curse', 'Gather a Crystal Shard from the Crystal Cave')
                    else:
                        print(Colors.RED + "\nA magical barrier blocks your path!" + Colors.RESET)
                        print(Colors.RED + "You need a spell book and crystal shard to pass." + Colors.RESET)
                        return
                else:
                    print("This way is blocked.")
                    return

            self.player.current_location = new_location

            # Track discovered locations
            if new_location not in self.player.discovered_locations:
                self.player.discovered_locations.append(new_location)
                print(Colors.GREEN + f"\n[New location discovered: {locations[new_location]['name']}]" + Colors.RESET)

            if new_location not in self.player.visited_locations:
                self.player.visited_locations.append(new_location)

            print(Colors.GREEN + f"\nYou go {direction}..." + Colors.RESET)
            self.display_location()

            # Check for random encounter
            if not self.check_random_encounter():
                # No encounter, but still update quest progress for exploration
                if new_location == 'cave':
                    self.complete_quest_objective('crystal_hunt', 'Enter the Crystal Cave')
                elif new_location == 'ruins':
                    self.complete_quest_objective('ruins_exploration', 'Find the Ancient Ruins')
                elif new_location == 'mine':
                    self.complete_quest_objective('goblin_menace', 'Enter the Abandoned Mine')
                elif new_location == 'underground_lake':
                    self.complete_quest_objective('lake_mystery', 'Reach the Underground Lake')
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
                if 'fireball' not in self.player.spells_learned:
                    self.player.spells_learned.append('fireball')
                self.player.magic_power += 2
                print(Colors.PURPLE + "\nYou learned the Fireball spell!" + Colors.RESET)
                self.complete_quest_objective('main_dragon_curse', 'Obtain the Spell Book from the Wizard')

            elif item_key == 'crystal_shard':
                self.complete_quest_objective('main_dragon_curse', 'Gather a Crystal Shard from the Crystal Cave')
                # Check crystal hunt quest
                shards = sum(1 for i in self.player.inventory if i == 'crystal_shard')
                if shards >= 3:
                    self.complete_quest_objective('crystal_hunt', 'Gather 3 crystal shards')

            elif item_key == 'sword':
                self.player.combat_skill += 3
                print(Colors.PURPLE + "\nYour combat skill increased!" + Colors.RESET)
                self.complete_quest_objective('main_dragon_curse', 'Obtain a weapon from Sir Gareth')

            elif item_key == 'magic_mushroom':
                self.player.magic_power += 1
                print(Colors.PURPLE + "\nYour magic power increased!" + Colors.RESET)

            elif item_key == 'crown':
                print(Colors.YELLOW + Colors.BOLD + "\n*** You have retrieved the Crown of Eldoria! ***" + Colors.RESET)
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

        self.use_item_by_key(item_key)

    def use_item_by_key(self, item_key):
        """Use item by key"""
        item = items[item_key]

        if item['type'] == 'consumable':
            effect = item['effect']
            effect_type = item.get('effect_type', 'health')

            if effect_type == 'health':
                self.player.heal(effect)
                print(Colors.GREEN + f"\nYou used {item['name']} and restored {effect} health!" + Colors.RESET)
            elif effect_type == 'mana':
                self.player.restore_mana(effect)
                print(Colors.BLUE + f"\nYou used {item['name']} and restored {effect} mana!" + Colors.RESET)
            elif effect_type == 'health_mana':
                self.player.heal(effect)
                self.player.restore_mana(effect // 2)
                print(Colors.GREEN + f"\nYou used {item['name']} and restored {effect} health and {effect//2} mana!" + Colors.RESET)

            self.player.potions_consumed += 1
            self.player.remove_item(item_key)
            print(f"Health: {self.player.health}/{self.player.max_health} | Mana: {self.player.mana}/{self.player.max_mana}")

        elif item['type'] == 'permanent_boost':
            effect = item['effect']
            effect_type = item.get('effect_type', 'magic_power')

            if effect_type == 'magic_power':
                self.player.magic_power += effect
                print(Colors.PURPLE + f"\nYou consumed {item['name']} and permanently gained +{effect} Magic Power!" + Colors.RESET)

            self.player.remove_item(item_key)

        elif item['type'] == 'key_item' or item['type'] == 'quest_item':
            print(Colors.PURPLE + f"\nYou examine the {item['name']} carefully..." + Colors.RESET)
            print(item['description'])

        elif item['type'] == 'weapon':
            print(Colors.YELLOW + f"\nUse 'equip {item['name']}' to equip this weapon." + Colors.RESET)

        elif item['type'] == 'armor':
            print(Colors.YELLOW + f"\nUse 'equip {item['name']}' to equip this armor." + Colors.RESET)

        else:
            print("You can't use that item right now.")

    def equip_item(self, item_name):
        """Equip a weapon or armor"""
        item_key = None
        for key, item in items.items():
            if item['name'].lower() == item_name.lower():
                item_key = key
                break

        if not item_key or not self.player.has_item(item_key):
            print("You don't have that item.")
            return

        item = items[item_key]
        if item['type'] not in ['weapon', 'armor']:
            print("You can only equip weapons and armor.")
            return

        if self.player.equip_item(item_key):
            print(Colors.GREEN + f"\nEquipped {item['name']}!" + Colors.RESET)
        else:
            print("Failed to equip item.")

    def unequip_item(self, item_name):
        """Unequip a weapon or armor"""
        item_key = None
        for key, item in items.items():
            if item['name'].lower() == item_name.lower():
                item_key = key
                break

        if not item_key:
            print("Item not found.")
            return

        if self.player.equipped_weapon == item_key:
            self.player.equipped_weapon = None
            if 'damage_bonus' in items[item_key]:
                self.player.combat_skill -= items[item_key]['damage_bonus'] // 10
            print(Colors.YELLOW + f"\nUnequipped {items[item_key]['name']}." + Colors.RESET)
        elif self.player.equipped_armor == item_key:
            self.player.equipped_armor = None
            if 'defense_bonus' in items[item_key]:
                self.player.defense -= items[item_key]['defense_bonus']
            print(Colors.YELLOW + f"\nUnequipped {items[item_key]['name']}." + Colors.RESET)
        else:
            print("That item is not equipped.")


    def talk_to_npc(self):
        """Talk to an NPC in the current location"""
        location = locations[self.player.current_location]

        if not location['npc']:
            print("There's no one here to talk to.")
            return

        npc = npcs[location['npc']]

        # Display dialogue
        print(Colors.PURPLE + f"\n{npc['name']} says:" + Colors.RESET)
        for line in npc['dialogue']:
            print(f'  "{line}"')
            time.sleep(0.3)

        # Handle quest giving
        if 'quest_given' in npc and npc['quest_given']:
            quest_id = npc['quest_given']
            if quest_id in QUESTS and quest_id not in self.player.quests:
                self.start_quest(quest_id)

        # Handle additional quest giving
        if 'gives_quest' in npc and npc['gives_quest']:
            quest_id = npc['gives_quest']
            if quest_id in QUESTS and quest_id not in self.player.quests:
                self.start_quest(quest_id)

        # Handle rewards
        if 'reward' in npc and npc['reward']:
            reward = npc['reward']
            if not self.player.has_item(reward) and reward not in location['items']:
                location['items'].append(reward)
                print(Colors.GREEN + f"\n{npc['name']} gives you {items[reward]['name']}!" + Colors.RESET)

        # Handle shop
        if npc.get('shop', False):
            self.open_shop(npc)

        # Handle special services
        if 'service' in npc and npc['service'] == 'mount_rental':
            self.rent_mount()

        # Special NPC interactions
        if location['npc'] == 'dragon' and not self.dragon_defeated:
            self.current_enemy = ENEMIES[EnemyType.DRAGON]
            self.in_combat = True
            self.combat_loop()

    def start_quest(self, quest_id):
        """Start a new quest"""
        if quest_id not in QUESTS:
            return

        quest = QUESTS[quest_id]

        # Check prerequisites
        for prereq in quest.prerequisites:
            if prereq not in self.player.completed_quests:
                print(Colors.YELLOW + f"\n[Quest '{quest.name}' requires completing another quest first]" + Colors.RESET)
                return

        # Create quest copy
        quest_copy = Quest(
            id=quest.id,
            name=quest.name,
            description=quest.description,
            quest_type=quest.quest_type,
            status=QuestStatus.ACTIVE,
            objectives=list(quest.objectives),
            rewards=dict(quest.rewards),
            prerequisites=list(quest.prerequisites),
            giver=quest.giver,
            location=quest.location,
            xp_reward=quest.xp_reward,
            gold_reward=quest.gold_reward
        )

        self.player.quests[quest_id] = quest_copy

        print(Colors.CYAN + Colors.BOLD)
        print("\n" + "=" * 50)
        print(f"     NEW QUEST: {quest.name}")
        print("=" * 50)
        print(Colors.RESET)
        print(Colors.WHITE + quest.description + Colors.RESET)
        print(Colors.YELLOW + f"\nObjectives:" + Colors.RESET)
        for obj in quest.objectives:
            print(f"  - {obj}")
        print(Colors.GREEN + f"\nRewards: {quest.xp_reward} XP, {quest.gold_reward} Gold" + Colors.RESET)
        if 'item' in quest.rewards:
            print(Colors.GREEN + f"Item: {items[quest.rewards['item']]['name']}" + Colors.RESET)
        if 'spell' in quest.rewards:
            print(Colors.PURPLE + f"Spell: {SKILLS[quest.rewards['spell']].name}" + Colors.RESET)

    def complete_quest_objective(self, quest_id, objective):
        """Complete a quest objective"""
        if quest_id not in self.player.quests:
            return

        quest = self.player.quests[quest_id]
        if quest.status != QuestStatus.ACTIVE:
            return

        if objective in quest.objectives and objective not in quest.completed_objectives:
            quest.completed_objectives.append(objective)
            print(Colors.GREEN + f"\n[Quest Update: {quest.name} - '{objective}' completed!]" + Colors.RESET)

            # Check if quest is complete
            if quest.is_complete():
                self.complete_quest(quest_id)

    def complete_quest(self, quest_id):
        """Complete a quest and award rewards"""
        if quest_id not in self.player.quests:
            return

        quest = self.player.quests[quest_id]
        quest.status = QuestStatus.COMPLETED
        self.player.completed_quests.append(quest_id)
        del self.player.quests[quest_id]

        print(Colors.GREEN + Colors.BOLD)
        print("\n" + "=" * 50)
        print(f"     QUEST COMPLETE: {quest.name}!")
        print("=" * 50)
        print(Colors.RESET)

        # Award rewards
        if quest.xp_reward > 0:
            leveled = self.player.add_xp(quest.xp_reward)
            print(Colors.YELLOW + f"Gained {quest.xp_reward} XP!" + Colors.RESET)
            if leveled:
                print(Colors.PURPLE + Colors.BOLD + f"\n*** LEVEL UP! You are now level {self.player.level}! ***" + Colors.RESET)
                self.check_new_spells()

        if quest.gold_reward > 0:
            self.player.gold += quest.gold_reward
            self.player.total_gold_earned += quest.gold_reward
            print(Colors.YELLOW + f"Gained {quest.gold_reward} Gold!" + Colors.RESET)

        if 'item' in quest.rewards:
            item_key = quest.rewards['item']
            self.player.add_item(item_key)
            print(Colors.BLUE + f"Received: {items[item_key]['name']}!" + Colors.RESET)

        if 'spell' in quest.rewards:
            spell = quest.rewards['spell']
            if spell not in self.player.spells_learned:
                self.player.spells_learned.append(spell)
                print(Colors.PURPLE + f"Learned spell: {SKILLS[spell].name}!" + Colors.RESET)

    def open_shop(self, npc):
        """Open NPC shop interface"""
        if 'shop_items' not in npc:
            return

        print(Colors.YELLOW + f"\n=== {npc['name']}'s Shop ===" + Colors.RESET)
        print(f"Your Gold: {self.player.gold}")
        print("\nItems for sale:")

        for i, item_key in enumerate(npc['shop_items'], 1):
            if item_key in items:
                item = items[item_key]
                print(f"{i}. {item['name']} - {item['value']} gold ({item['rarity']})")

        print(f"{len(npc['shop_items'])+1}. Exit shop")

        choice = input("\nBuy item (number): ").strip()
        try:
            idx = int(choice) - 1
            if idx == len(npc['shop_items']):
                return
            if 0 <= idx < len(npc['shop_items']):
                item_key = npc['shop_items'][idx]
                item = items[item_key]

                if self.player.gold >= item['value']:
                    self.player.gold -= item['value']
                    self.player.add_item(item_key)
                    print(Colors.GREEN + f"\nPurchased {item['name']} for {item['value']} gold!" + Colors.RESET)
                else:
                    print(Colors.RED + "\nNot enough gold!" + Colors.RESET)
        except ValueError:
            pass

    def rent_mount(self):
        """Rent a mount for fast travel"""
        if self.player.has_mount:
            print(Colors.YELLOW + "\nYou already have a mount!" + Colors.RESET)
            return

        cost = 50
        if self.player.gold >= cost:
            self.player.gold -= cost
            self.player.has_mount = True
            print(Colors.GREEN + f"\nYou rented a horse for {cost} gold!" + Colors.RESET)
            print(Colors.CYAN + "Use 'travel' or 'mount' to fast travel between discovered locations." + Colors.RESET)
        else:
            print(Colors.RED + f"\nNot enough gold! Need {cost} gold." + Colors.RESET)

    def rest(self):
        """Rest to recover health and mana"""
        location = locations[self.player.current_location]
        if location.get('special') == 'rest_area':
            cost = 10
            if self.player.gold >= cost:
                self.player.gold -= cost
                self.player.health = self.player.max_health
                self.player.mana = self.player.max_mana
                print(Colors.GREEN + f"\nYou rest for the night. (-{cost} gold)" + Colors.RESET)
                print(Colors.GREEN + f"Health and mana fully restored!" + Colors.RESET)
            else:
                print(Colors.YELLOW + f"\nNot enough gold for a room. Need {cost} gold." + Colors.RESET)
                print(Colors.YELLOW + "You rest outside instead..." + Colors.RESET)
                self.player.health = min(self.player.health + 20, self.player.max_health)
                self.player.mana = min(self.player.mana + 15, self.player.max_mana)
                print(Colors.GREEN + f"Recovered some health and mana." + Colors.RESET)
        else:
            print(Colors.YELLOW + "\nYou can only rest in safe areas like the village or tavern." + Colors.RESET)


    def show_inventory(self):
        """Display player inventory with detailed info"""
        print(Colors.BLUE + Colors.BOLD + "\n=== INVENTORY ===" + Colors.RESET)
        print(f"Gold: {self.player.gold}")

        if not self.player.inventory:
            print("Your inventory is empty.")
        else:
            # Group by type
            by_type = {}
            for item_key in self.player.inventory:
                item_type = items[item_key]['type']
                if item_type not in by_type:
                    by_type[item_type] = []
                by_type[item_type].append(item_key)

            for item_type, item_list in sorted(by_type.items()):
                print(f"\n[{item_type.upper()}]")
                for item_key in item_list:
                    item = items[item_key]
                    marker = ""
                    if self.player.equipped_weapon == item_key:
                        marker = " [EQUIPPED]"
                    elif self.player.equipped_armor == item_key:
                        marker = " [EQUIPPED]"
                    print(f"  - {item['name']}{marker}: {item['description'][:60]}...")

        print()

    def show_stats(self):
        """Display comprehensive player statistics"""
        stats = self.player.get_stats()
        print(Colors.CYAN + Colors.BOLD + "\n=== CHARACTER SHEET ===" + Colors.RESET)
        print(f"Name: {stats['name']}")
        print(f"Level: {stats['level']} ({stats['xp']}/{stats['xp_to_next']} XP to next)")
        print(f"Health: {stats['health']}")
        print(f"Mana: {stats['mana']}")
        print(f"Gold: {stats['gold']}")
        print(f"Combat Skill: {stats['combat_skill']}")
        print(f"Magic Power: {stats['magic_power']}")
        print(f"Defense: {self.player.defense}")
        print(f"Luck: {self.player.luck:.1f}")
        print(f"Items: {stats['inventory_count']}")
        print(f"Locations: {stats['locations_discovered']} discovered")
        print(f"Quests: {stats['quests_active']} active, {stats['quests_completed']} completed")
        print(f"Enemies Defeated: {stats['enemies_defeated']}")
        print(f"Deaths: {stats['deaths']}")

        if self.player.equipped_weapon:
            print(f"\nWeapon: {items[self.player.equipped_weapon]['name']}")
        if self.player.equipped_armor:
            print(f"Armor: {items[self.player.equipped_armor]['name']}")

        if self.player.spells_learned:
            print(f"\nSpells: {', '.join(SKILLS[s].name for s in self.player.spells_learned)}")

        print()

    def show_quests(self):
        """Display active and completed quests"""
        print(Colors.YELLOW + Colors.BOLD + "\n=== QUEST LOG ===" + Colors.RESET)

        if not self.player.quests and not self.player.completed_quests:
            print("No quests yet. Talk to NPCs to find quests!")
            print()
            return

        if self.player.quests:
            print(Colors.CYAN + "\nACTIVE QUESTS:" + Colors.RESET)
            for quest in self.player.quests.values():
                progress = quest.get_progress()
                bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
                print(f"\n[{quest.quest_type.value.upper()}] {quest.name}")
                print(f"Progress: [{bar}] {int(progress*100)}%")
                for obj in quest.objectives:
                    status = "✓" if obj in quest.completed_objectives else "○"
                    print(f"  {status} {obj}")

        if self.player.completed_quests:
            print(Colors.GREEN + "\n\nCOMPLETED QUESTS:" + Colors.RESET)
            for qid in self.player.completed_quests:
                if qid in QUESTS:
                    print(f"  ✓ {QUESTS[qid].name}")

        print()

    def show_journal(self):
        """Show game journal with notable events"""
        print(Colors.WHITE + Colors.BOLD + "\n=== ADVENTURE JOURNAL ===" + Colors.RESET)
        print(f"Turns played: {self.turn_count}")
        print(f"Locations visited: {len(self.player.visited_locations)}")
        print(f"Enemies defeated: {self.player.enemies_defeated}")
        print(f"Potions consumed: {self.player.potions_consumed}")
        print(f"Total gold earned: {self.player.total_gold_earned}")
        print(f"Deaths: {self.player.deaths}")
        print()

    def show_map(self):
        """Show discovered locations"""
        print(Colors.GREEN + Colors.BOLD + "\n=== WORLD MAP ===" + Colors.RESET)
        print(f"Current: {locations[self.player.current_location]['name']}")
        print("\nDiscovered locations:")
        for loc_id in self.player.discovered_locations:
            loc = locations[loc_id]
            marker = " ← You are here" if loc_id == self.player.current_location else ""
            print(f"  - {loc['name']}{marker}")
        print()

    def show_crafting(self):
        """Show crafting recipes"""
        print(Colors.ORANGE + Colors.BOLD + "\n=== CRAFTING ===" + Colors.RESET)
        print("Recipes:")
        print("  2 Forest Herbs + 1 Glowing Mushroom = Healing Potion")
        print("  1 Wolf Pelt + 1 Troll Hide = Leather Armor")
        print("  1 Iron Ore + 1 Silver Ore = Knight's Sword")
        print("\nUse 'craft [recipe]' to craft (not yet implemented)")
        print()

    def show_help(self):
        """Display comprehensive help information"""
        print(Colors.WHITE + Colors.BOLD + "\n=== HELP ===" + Colors.RESET)

        print(Colors.YELLOW + "\nMovement:" + Colors.RESET)
        print("  north/n, south/s, east/e, west/w - Move")
        print("  map - Show discovered locations")

        print(Colors.YELLOW + "\nActions:" + Colors.RESET)
        print("  take/get [item] - Pick up item")
        print("  drop [item] - Drop item")
        print("  use [item] - Use consumable or examine item")
        print("  equip [item] - Equip weapon/armor")
        print("  unequip [item] - Unequip item")
        print("  talk - Talk to NPC")
        print("  examine/look - Look around")
        print("  rest - Rest and recover (safe areas only)")

        print(Colors.YELLOW + "\nInfo:" + Colors.RESET)
        print("  inventory/inv/i - Show inventory")
        print("  stats/status - Character sheet")
        print("  quest/quests - Show quest log")
        print("  journal - Adventure statistics")
        print("  craft - Show crafting recipes")
        print("  help/h/? - This help message")

        print(Colors.YELLOW + "\nSystem:" + Colors.RESET)
        print("  quit/exit - Exit game")

        print(Colors.CYAN + "\nYour quest: Retrieve the Crown of Eldoria from the dragon's lair!" + Colors.RESET)
        print(Colors.CYAN + "Talk to the Village Elder to begin your journey." + Colors.RESET)
        print()

    def check_win_condition(self):
        """Check if player has won the game"""
        if self.player.has_item('crown'):
            self.print_header("CONGRATULATIONS!", Colors.GREEN)
            self.slow_print("You have successfully retrieved the Crown of Eldoria!")
            self.slow_print("The kingdom is saved from the dragon's curse!")
            self.slow_print("Bards will sing of your heroic deeds for generations to come!")

            print(Colors.YELLOW + Colors.BOLD + f"\n{self.player.name}, Hero of Eldoria!" + Colors.RESET)
            print(Colors.CYAN + f"Level {self.player.level} | {self.player.xp} XP | {self.player.enemies_defeated} Enemies Defeated" + Colors.RESET)
            print()
            self.show_journal()
            return True
        return False

    def main_game_loop(self):
        """Main game loop"""
        self.display_title_screen()
        player_name = self.get_player_name()
        self.player = Player(player_name)

        self.choose_difficulty()

        print(Colors.GREEN + f"\nWelcome, {player_name}! Your adventure begins now!" + Colors.RESET)
        print(Colors.YELLOW + "Type 'help' for a list of commands." + Colors.RESET)

        self.display_location()

        # Auto-start main quest
        self.start_quest('main_dragon_curse')
        self.complete_quest_objective('main_dragon_curse', 'Speak with the Village Elder')

        while self.game_running:
            if self.check_win_condition():
                break

            self.turn_count += 1
            command = input(Colors.BOLD + "\n> " + Colors.RESET).strip()
            self.process_command(command)

            # Check for game over
            if self.player.health <= 0 and not self.in_combat:
                print(Colors.RED + Colors.BOLD + "\nYou have fallen..." + Colors.RESET)
                print(Colors.DARK_GRAY + "But the gods give you another chance..." + Colors.RESET)
                self.player.health = self.player.max_health // 2
                self.player.current_location = 'village'
                print(Colors.GREEN + "You awaken back in Thorndale Village..." + Colors.RESET)

def main():
    """Main function to start the game"""
    game = Game()
    try:
        game.main_game_loop()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")

if __name__ == "__main__":
    main()