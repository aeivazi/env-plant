import numpy as np

RECIPES = {
    'iron_plate': {'iron_ore': 1, 'time': 3.5},
    'stone_furnace': {'coal_consumption': 0.0225}
}

def resources_one_ts_iron_plate():
    needed_coal = RECIPES['stone_furnace']['coal_consumption']
    needed_iron_ore = RECIPES['iron_plate']['iron_ore']/RECIPES['iron_plate']['time']
    return needed_coal, needed_iron_ore


def resources_for_iron_plate():
    needed_coal = RECIPES['stone_furnace']['coal_consumption'] * RECIPES['iron_plate']['time']
    needed_iron_ore = RECIPES['iron_plate']['iron_ore']
    return needed_coal, needed_iron_ore

REWARDS = {
    'iron_ore': 1,
    'coal_ore': 1,
    'iron_plate': 2 * (np.sum(resources_for_iron_plate()))
}

LIMITS = {
    'transport_belt': {'max_throughput': 13.33}
}

SCREEN_WIDTH_PIXELS = 50
SCREEN_HEIGHT_PIXELS = 50

PIXEL_SIZE = 10
