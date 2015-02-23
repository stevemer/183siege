#####################################
# Enable/Disable student AI 
#####################################

USE_AI = False
ENABLE_STORYLINE = False

#####################################
# Game mechanics and const globals 
#####################################

# Map ratios
MAP_WIDTH = 80
MAP_HEIGHT = 38
VISIBLE_TILES = ['X', ' ', '@']

# Globals
RIGHT_HAND = 1
LEFT_HAND = 0
STRENGTHNAMES = {
    0: "",
    1: "Very Weak",
    2: "Weak",
    3: "Average",
    4: "Strong",
    5: "Very Strong"
}

DANGERS = {
    0: "Totally Safe!",
    1: "Extremely Safe",
    2: "Very Safe",
    3: "Safe",
    4: "Average",
    5: "Risky",
    6: "Very Risky",
    7: "Extremely Risky",
    8: "Dangerous",
    9: "Very Dangerous",
    10: "Extremely Dangerous!",
}

#####################################
# Probabilities and balancing factors
#####################################

# Misc Items
ITEM_STRENGTHS = {
    "Potions": 25,
    "Keys": 1,
    "Trinkets": 1,
}

ITEM_START_VALUES = {
    "Potions": 5,
    "Keys": 0,
    "Trinkets": 1,
}

# Enemies
ENEMY_DAMAGE_CONSTANT = 0.5

# Ranged damage bonus
RANGE_COMBAT_FACTOR = 2
OFFHAND_FACTOR = 0.5    

# Defense
SHIELD_BASE_CHANCE = 0.75
SHIELD_LEVEL_BONUS = 0.05

# Event Probabilities
DANGER_MODIFIER = 0.3
ITEM_DROP_PROBABILITY = 0.5
BASE_ENEMY_ENCOUNTER_CHANCE = .03 #10 / 187.5

# Health
PLAYER_MAX_HEALTH = 300

#####################################
# Custom game exceptions 
#####################################

class Defeat(Exception):
    pass

class Victory(Exception):
    pass

HIDING_MSGS = [
    "You hide behind a dusty statue!",
    "You hide in a nearby closet!",
    "You crouch behind some dusty crates!",
    "You disguise yourself using dirt and vegetation!",
    "You crouch in the shadows.",
    "You carefully evade a patrolling guard!",
    "You take a quick nap in a nearby closet.",
    "You use your ninja skills to hang from the ceiling!",
    "You are almost caught, but the troll has bad eyesight and mistakes you for a wall.",
    "Hiding is for cowards!... and for people who like winning.",
]
