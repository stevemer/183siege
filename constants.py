MAP_WIDTH = 80
MAP_HEIGHT = 38

VISIBLE_TILES = ['X', ' ', '@']

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

class Defeat(Exception):
    pass

class Victory(Exception):
    pass

#####################################
# Probabilities and balancing factors
#####################################

# Items
POTION_HEALTH = 25
POTION_NUM = 5

# Enemies
ENEMY_DAMAGE_CONSTANT = 0.5

# Defense
SHIELD_BASE_CHANCE = 0.75
SHIELD_LEVEL_BONUS = 0.05

# Event Probabilities
ITEM_DROP_PROBABILITY = 0.5
ENEMY_ENCOUNTER_CHANCE = 10 / 187.5 #TBT, should be 5 though...

# Health
PLAYER_MAX_HEALTH = 100
