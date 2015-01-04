#####################################
# Enable/Disable student AI 
#####################################

USE_AI = False

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

# Defense
SHIELD_BASE_CHANCE = 0.75
SHIELD_LEVEL_BONUS = 0.05

# Event Probabilities
ITEM_DROP_PROBABILITY = 0.5
ENEMY_ENCOUNTER_CHANCE = 10 / 187.5

# Health
PLAYER_MAX_HEALTH = 100

#####################################
# Custom game exceptions 
#####################################

class Defeat(Exception):
    pass

class Victory(Exception):
    pass
