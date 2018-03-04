from env_plant.settings import resources_one_ts_iron_plate, RECIPES


class StoneFurnace:
    def __init__(self, location):
        self.location = location
        self.ts_count = 0.0

        self.coal_ore = 0.0
        self.iron_ore = 0.0
        self.iron_plate = 0.0

    def add_resource(self, item):
        if item.type == 'coal_ore':
            self.coal_ore += 1.
        elif item.type == 'iron_ore':
            self.iron_ore += 1.

    def produce_one_iron_plate(self):
        """
        Recipe:
        1 iron_ore + 3.5 time = 1 iron plate

        """

        # check needed resources for one step:
        needed_coal, needed_iron_ore = resources_one_ts_iron_plate()

        if self.coal_ore < needed_coal or self.iron_ore < needed_iron_ore:
            return

        self.ts_count += 1.
        self.coal_ore -= needed_coal
        self.iron_ore -= needed_iron_ore

        if self.ts_count > RECIPES['iron_plate']['time']:
            self.iron_plate += 1

        return


class BurnerMiningDrill:
    def __init__(self, location):
        self.location = location