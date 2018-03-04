import gym

from env_plant.envs import simple_env


env = gym.make('plant-v0')

print(env.state)

env.render(mode='human')

n_episodes = 1 #20
n_timesteps = 10 #100

for i_episode in range(n_episodes):
    env.reset()

    for t in range(20):

        env.render()

        #choose a random action
        action = ((t, t), (0, 1))

        state, reward, done, info = env.step(action)

        print(state, reward, done, info)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

input("Press Enter to close...")
env.close()