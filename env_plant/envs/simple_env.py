import gym
from gym.utils import seeding
from gym.envs.classic_control import rendering

from env_plant.settings import REWARDS, SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS, PIXEL_SIZE
from env_plant.envs.state import State
from env_plant.utils import get_coords
from env_plant.items.logistics import TransportBelt

class SimpleEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self):

        self.seed()
        self.viewer = None
        self.state = State()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def calculate_reward(self):
        reward = 0.0
        iron_ore, coal_ore, iron_plates = self.state.count_items()
        reward += iron_ore * REWARDS['iron_ore']
        reward += coal_ore * REWARDS['coal_ore']
        reward += iron_plates * REWARDS['iron_plate']
        return reward

    def step(self, action):
        """
        Action is a triple of info for one piece of transport belt:
        ((x, y), orientation)

        :param action:
        :return:
        """

        belt = TransportBelt(action[0], action[1])
        self.state.add_belt(belt)

        self.state.one_step_time()

        return self.state, self.calculate_reward(), False, {}

    def reset(self):
        self.state.set_defaults()
        return self.state

    def render(self, mode='human'):

        if self.state is None:
            return None

        if self.viewer is None:
            self.viewer = rendering.Viewer(SCREEN_WIDTH_PIXELS*PIXEL_SIZE, SCREEN_HEIGHT_PIXELS*PIXEL_SIZE)

            # # create iron resources
            # l,r,b,t = 0, OBJECT_W, SCREEN_HEIGHT_PIXELS - OBJECT_H, SCREEN_HEIGHT_PIXELS
            # iron_resource = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            # iron_resource.set_color(1.000, 0.549, 0.000) #orange
            # self.viewer.add_geom(iron_resource)
            #
            # # create coal resources
            # l, r, b, t = 0, OBJECT_W, 0, OBJECT_H
            # coal_resource = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            # coal_resource.set_color(0.412, 0.412, 0.412)  # darkgray
            # self.viewer.add_geom(coal_resource)

            for ind, om in self.state.mines.items():
                coords = get_coords(om.location, PIXEL_SIZE)
                om_p = rendering.FilledPolygon(coords)
                om_p.set_color(0.184, 0.310, 0.310)  # black gray
                self.viewer.add_geom(om_p)

            # create stone furnace
            for ind, furnace in self.state.furnaces.items():
                coords = get_coords(furnace.location, PIXEL_SIZE)
                f_p = rendering.FilledPolygon(coords)
                f_p.set_color(1.000, 0.843, 0.000) #gold
                self.viewer.add_geom(f_p)

        for ind, belt in self.state.belts.items():
            coords = get_coords(belt.location, PIXEL_SIZE)
            b_p = rendering.FilledPolygon(coords)
            b_p.set_color(0.647, 0.165, 0.165) #brown
            self.viewer.add_geom(b_p)

        cap = rendering.Line(start = (10, 10), end = (50, 10))
        self.viewer.add_geom(cap)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
