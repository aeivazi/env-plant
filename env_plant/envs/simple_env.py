import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class SimpleEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = (self.masspole + self.masscart)
        self.length = 0.5 # actually half the pole's length
        self.polemass_length = (self.masspole * self.length)
        self.force_mag = 10.0
        self.tau = 0.02  # seconds between state updates

        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds
        high = np.array([
            self.x_threshold * 2,
            np.finfo(np.float32).max,
            self.theta_threshold_radians * 2,
            np.finfo(np.float32).max])

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-high, high)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        state = self.state
        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action==1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta* temp) / (self.length * (4.0/3.0 - self.masspole * costheta * costheta / self.total_mass))
        xacc  = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        x  = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        self.state = (x,x_dot,theta,theta_dot)
        done =  x < -self.x_threshold \
                or x > self.x_threshold \
                or theta < -self.theta_threshold_radians \
                or theta > self.theta_threshold_radians
        done = bool(done)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        screen_width = 500
        screen_height = 500

        resource_w, resource_h = 100, 100

        furnace_w, furnace_h = 100, 100
        furnace_center_x, furnace_center_y = 0.75 * screen_width, 0.5 * screen_height

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            # create iron resources
            l,r,b,t = 0, resource_w, screen_height-resource_h, screen_height
            iron_resource = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            iron_resource.set_color(1.000, 0.549, 0.000) #orange
            self.viewer.add_geom(iron_resource)

            # create coal resources
            l,r,b,t = 0, resource_w, 0, resource_h
            coal_resource = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            coal_resource.set_color(0.412, 0.412, 0.412) #darkgray
            self.viewer.add_geom(coal_resource)

            # create stone furnace
            l, r, b, t = furnace_center_x - 0.5 * furnace_w, furnace_center_x + 0.5 * furnace_w, \
                         furnace_center_y - 0.5 * furnace_h, furnace_center_y + 0.5 * furnace_h
            furnace = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            furnace.set_color(1.000, 0.843, 0.000) #gold
            self.viewer.add_geom(furnace)

        if self.state is None: return None

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer: self.viewer.close()