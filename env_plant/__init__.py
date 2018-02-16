from gym.envs.registration import register

register(
    id='plant-v0',
    entry_point='env_plant.envs:SimpleEnv',
)