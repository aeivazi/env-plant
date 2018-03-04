
from env_plant.settings import SCREEN_WIDTH_PIXELS


def to_ind(location):
    return location[0] + location[1] * SCREEN_WIDTH_PIXELS


def get_coords(location, pixel_size=1.):
    l, r, b, t = location[0], location[0] + 1, \
                 location[1], location[1] + 1
    l *= pixel_size
    r *= pixel_size
    b *= pixel_size
    t *= pixel_size
    return [(l, b), (l, t), (r, t), (r, b)]
