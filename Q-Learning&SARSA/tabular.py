from concurrent.futures import wait
import numpy as np
from tqdm import tqdm

ALPHA = 0.1
GAMMA = 0.9
EPSILON_MIN = 0
EPSILON_MAX = 0.4
DECAY_RATE = 1


class tabular:
    # base class for tabular methods
    def __init__(self,
                 env,                           # an instance of a open-ai environment
                 alpha=ALPHA,                   # learning rate
                 gamma=GAMMA,                   # discout factor
                 epsilon_min=EPSILON_MIN,       # epsilon min value
                 epsilon_max=EPSILON_MAX,       # epsilon max value
                 decay_rate=DECAY_RATE,       # epsilon decay rate
                 ) -> None:
        self.size = [env.observation_space.n, env.action_space.n]
        self.env = env
        self.table = np.zeros([env.observation_space.n, env.action_space.n])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max
        self.decay_rate = decay_rate
    
    def reset(self):
        self.table = np.zeros(self.size)

    def train(self, episodes, debug=False):
        # Training for $episodes times
        if debug:
            rewards_list = []
            count_list = []
            epsilon_list = []
        for i in range(episodes):
            rewards, count = self.update(i/episodes)
            if debug:
                epsilon = max(
                    self.epsilon_max*np.exp(-self.decay_rate*i/episodes),
                    self.epsilon_min
                )
                rewards_list.append(rewards)
                count_list.append(count)
                epsilon_list.append(epsilon)
        if debug:
            return rewards_list, epsilon_list, count_list

    def action_decayed_e_greedy(self, state, decay):
        # return an action based on decayed ε-greedy
        rng = np.random.uniform(0, 1)
        epsilon = max(
            self.epsilon_max*np.exp(-self.decay_rate*decay),
            self.epsilon_min
        )
        # expotenial decay
        if rng < epsilon:
            # random action
            return self.env.action_space.sample()
        else:
            # greedy policy
            return np.argmax(self.table[state])

    def update(self):
        # This method run an new episode of self.env and returns cumulative rewards
        # Must be overrided by subclass
        pass

    def evaluate(self):
        # run an episode only take the greedy action
        state = self.env.reset()
        terminal = False
        reward_episode = 0
        while not terminal:
            action = np.argmax(self.table[state])
            state, reward, terminal, _ = self.env.step(action)
            reward_episode += reward
        return reward_episode


class q_learning(tabular):
    def update(self, decay=0):
        # run an episode
        state = self.env.reset()    # intialize environment
        terminal = False            # assume the initiate state is not termial
        reward_episode = 0          # reward of this episode
        count = 0
        while not terminal:
            count += 1
            # choose action based on ε-greedy
            action = self.action_decayed_e_greedy(state, decay)
            # take action, observe reward and new_state
            new_state, reward, terminal, _ = self.env.step(action)
            # update Q(s, a)
            self.table[state, action] = self.table[state, action] \
                + self.alpha * (
                reward + self.gamma
                * np.max(self.table[new_state])
                - self.table[state, action]
            )
            state = new_state
            reward_episode += reward
        return reward_episode, count


class sarsa(tabular):
    def update(self, decay=0):
        state = self.env.reset()
        # choose action based on ε-greedy
        action = self.action_decayed_e_greedy(state, decay)
        terminal = False
        reward_episode = 0
        count = 0
        while not terminal:
            count += 1
            new_state, reward, terminal, _ = self.env.step(action)
            new_action = self.action_decayed_e_greedy(new_state, decay)
            self.table[state, action] = self.table[state, action] \
                + self.alpha * (
                reward
                + self.gamma
                * self.table[new_state, new_action]
                - self.table[state, action]
            )
            state, action = new_state, new_action
            reward_episode += reward
        return reward_episode, count



if __name__ == "__main__":
    import gym
    env = gym.make('Taxi-v3')
    q = q_learning(env)
    q.train(100)
    s = sarsa(env)
    s.train(100)
