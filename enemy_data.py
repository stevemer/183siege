enemy_freqs = [0.6, 0.3, 0.1]

enemies = [
    {
        "name": "Cave Goblin",
        "image": "GOBLIN",
        "health": {
            "min": 1,
            "max": 5,
        },
        "items": [
            {"name": "Smelly Dagger","type": "SWORD", "strength": 1},
            {"name": "Slimy Bow", "type": "BOW", "strength": 1},
            {"name": "Old Shield", "type": "SHIELD", "strength": 1},
        ]
    },
    {
        "name": "Skeleton",
        "image": "SKELETON",
        "health": {
            "min": 3,
            "max": 8,
        },
        "items": [
            {"name": "Rusty Sword","type": "SWORD", "strength": 2},
            {"name": "Rusty Bow", "type": "BOW", "strength": 2},
            {"name": "Buckler", "type": "SHIELD", "strength": 2},
        ]
    },
    {
        "name": "Mud Troll",
        "image": "TROLL",
        "health": {
            "min": 5,
            "max": 15,
        },
        "items": [
            {"name": "Club","type": "CLUB", "strength": 3},
            #{"name": "Big Bow", "type": "BOW", "strength": 3},
            {"name": "Solid Shield", "type": "SHIELD", "strength": 3},
        ]
    },
]
