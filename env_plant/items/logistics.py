
from env_plant.settings import LIMITS, SCREEN_WIDTH_PIXELS

class TransportBelt:
    def __init__(self, location, orientation):
        # tuple (x,y)
        self.location = location
        # tuple (dx, dy), signed, only in 4 directions:
        # north = (0,1), west = (-1, 0), south = (0, -1), east = (1, 0)
        self.orientation = orientation
        self.current_items_number = 0

    def has_free_place(self):

        if self.current_items_number + 1 > LIMITS['transport_belt']['max_throughput']:
            return False

        return True

    def get_next_location(self):

        return self.location + self.orientation


class Item:
    def __init__(self):
        self.belt = None


class Conveyor:
    """
    Is a helper class for a list of TransportBelts
    """
    def __init__(self):
        self.belts = {}
        self.items = []

    def add_belt(self, belt):
        index = belt.location[0] + belt.location[1] * SCREEN_WIDTH_PIXELS
        self.belts[index] = belt

    def find_belt(self, location):

        index = location[0] + location[1] * SCREEN_WIDTH_PIXELS

        if index in self.belts:
            return self.belts[index]

        return None

    def move_one_step(self):

        for item in self.items:

            next_belt = self.find_belt(item.belt.get_next_location())

            if next_belt:

                if not next_belt.has_free_place:
                    continue

                item.belt.current_items_number -= 1
                next_belt.current_items_number += 1
                item.belt = next_belt

            else:
                lkfdj









