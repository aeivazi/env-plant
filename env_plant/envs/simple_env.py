import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

from env_plant.settings import *
from env_plant.items.production import BurnerMiningDrill, StoneFurnace


def render_get_coords(location, w, h):
    l, r, b, t = location[0] - 0.5 * w, location[0] + 0.5 * w, \
                 location[1] - 0.5 * h, location[1] + 0.5 * h
    return [(l, b), (l, t), (r, t), (r, b)]


class State:
    def __init__(self):
        self.iron_ore = 0
        self.coal_ore = 0
        self.iron_plates = 0

        self.iron_mines = []
        self.coal_mines = []
        self.furnaces = []
        self.belts = []

        self.set_defaults()

    def set_defaults(self):
        self.iron_ore = 10
        self.coal_ore = 10

        ore_mine = BurnerMiningDrill(400, 100)
        self.iron_mines.append(ore_mine)

        coal_mine = BurnerMiningDrill(100, 100)
        self.coal_mines.append(coal_mine)

        furnace = StoneFurnace(0.75 * SCREEN_WIDTH, 0.5 * SREEN_HEIGHT)
        self.furnaces.append(furnace)

    def __str__(self):

        output = 'Resources: '
        output += 'iron ore {}, '.format(self.iron_ore)
        output += 'coal ore {}, '.format(self.coal_ore)
        output += 'iron plates {}. '.format(self.iron_plates)

        return output


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
        reward += self.state.iron_ore * REWARDS['iron_ore']
        reward += self.state.coal_ore * REWARDS['coal_ore']
        reward += self.state.iron_plates * REWARDS['iron_plate']
        return reward

    def step(self, action):
        """
        Action is a triple of info for one piece of transport belt:
        (x, y, orientation)

        :param action:
        :return:
        """

        #assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))





        state = self.state

        for furnace in state.furnaces:
            furnace.produce_one_iron_plate()

        return self.state, self.calculate_reward(), False, {}

    def reset(self):
        self.state.set_defaults()
        return self.state

    def render(self, mode='human'):

        if self.state is None:
            return None

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(SCREEN_WIDTH, SREEN_HEIGHT)

            # create iron resources
            l,r,b,t = 0, OBJECT_W, SREEN_HEIGHT - OBJECT_H, SREEN_HEIGHT
            iron_resource = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            iron_resource.set_color(1.000, 0.549, 0.000) #orange
            self.viewer.add_geom(iron_resource)

            for om in self.state.iron_mines:
                om_p = rendering.FilledPolygon(render_get_coords(om.location, OBJECT_W, OBJECT_H))
                om_p.set_color(0.184, 0.310, 0.310)  # black gray
                self.viewer.add_geom(om_p)

            # create coal resources
            l,r,b,t = 0, OBJECT_W, 0, OBJECT_H
            coal_resource = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            coal_resource.set_color(0.412, 0.412, 0.412) #darkgray
            self.viewer.add_geom(coal_resource)

            # create stone furnace
            for furnace in self.state.furnaces:
                l, r, b, t = furnace.location[0] - 0.5 * OBJECT_H, furnace.location[0] + 0.5 * OBJECT_W, \
                             furnace.location[1] - 0.5 * OBJECT_H, furnace.location[1] + 0.5 * OBJECT_W
                furnace = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
                furnace.set_color(1.000, 0.843, 0.000) #gold
                self.viewer.add_geom(furnace)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()


# stone = StoneFurnace()
# state = State
# state.iron_ore_count = 2
# state.coal_ore_count = 10
#
# stone.add_resources(iron_ore=1., coal_ore=1.)
# plate = stone.produce_one_iron_plate()
#
# print(rewards)
#
# print(plate)
# print(stone.coal_ore, stone.iron_ore)


