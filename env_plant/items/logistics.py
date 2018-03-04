
from env_plant.settings import LIMITS


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

    def next_location(self):

        return self.location + self.orientation








