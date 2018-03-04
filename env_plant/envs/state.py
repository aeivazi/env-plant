
from env_plant.items.production import BurnerMiningDrill, StoneFurnace
from env_plant.settings import SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS
from env_plant.utils import to_ind
from env_plant.items.item import Item

import copy


class State:
    def __init__(self):

        self.mines = {}
        self.furnaces = {}
        self.belts = {}
        self.items = []

        self.set_defaults()

    def set_defaults(self):
        self.mines = {}
        self.furnaces = {}
        self.items = []

        iron_loc = (0., SCREEN_HEIGHT_PIXELS - 1)
        coal_loc = (0., 0.)

        om = BurnerMiningDrill(iron_loc)
        self.mines[to_ind(om.location)] = om

        cm = BurnerMiningDrill(coal_loc)
        self.mines[to_ind(cm.location)] = cm

        for i in range(10):
            self.items.append(Item(iron_loc, 'iron_ore'))
            self.items.append(Item(coal_loc, 'coal_ore'))

        f_loc = (0.75 * SCREEN_WIDTH_PIXELS, 0.5 * SCREEN_HEIGHT_PIXELS)
        f = StoneFurnace(f_loc)
        self.furnaces[to_ind(f.location)] = f

    def count_items(self):
        iron_ore = 0.
        coal_ore = 0.
        iron_plates = 0.

        for item in self.items:
            if item.type == 'iron_ore':
                iron_ore += 1.
            elif item.type == 'coal_ore':
                coal_ore += 1.

        for key, furnace in self.furnaces.items():
            iron_plates += furnace.iron_plate
            iron_ore += furnace.iron_ore
            coal_ore += furnace.coal_ore

        return iron_ore, coal_ore, iron_plates

    def __str__(self):

        iron_ore, coal_ore, iron_plate = self.count_items()

        output = 'Resources: '
        output += 'iron ore {}, '.format(iron_ore)
        output += 'coal ore {}, '.format(coal_ore)
        output += 'iron plates {}. '.format(iron_plate)

        return output

    def add_belt(self, belt):
        self.belts[to_ind(belt.location)] = belt

    def one_step_time(self):

        #TODO try to mine

        #try to move items
        self.items_one_step_time()

        #try to make iron_plates
        self.produce()

    def items_one_step_time(self):

        # to be able to delete items from the list
        temp_items = copy.copy(self.items)
        for item in temp_items:

            index = to_ind(item.location)

            if index in self.belts:

                belt = self.belts[index]
                item.location = belt.next_location()

            elif index in self.furnaces:
                furnace = self.furnaces[index]
                furnace.add_resource(item)
                self.items.remove(item)

    def produce(self):
        for ind, furnace in self.furnaces.items():
            furnace.produce_one_iron_plate()









