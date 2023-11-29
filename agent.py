import torch 
import random
import numpy as np
from collections import deque 
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #slump
        self.gamma = 0 
        self.memory = deque(maxlen=MAX_MEMORY) #Om vi får över bord minnet så kommer systemet ta bort element från vänster.
        self.model = None
        self.trainer = None
        #MODEL

    def get_state(self,game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            #Framåt
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            #Höger
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            #Vänster
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),

            #Rörelse direktion
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #Matens position
            game.food.x < game.head.x, #mat åt vänster
            game.food.x > game.head.x, #mat åt höger
            game.food.y < game.head.y, #mat åvanför
            game.food.y > game.head.y #mat under
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #Om det går över max memory så popar vi ormen

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #Kommer ge tillbaks en lista av ormarna
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #Ain ska utföra slumpmässiga rörelser för att utforska sin omgivning, sedam utföra det mest optimiserade dragen.
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move [move] = 1
        else:
            state = torch.tensor(state, dtype= torch.float)
            prediction = self.model.predict (state0)
            move = torch.argmax(prediction).item()
            final_move [move] = 1


        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = agent()
    game = SnakeGameAI()
    while  True:
        #Få ut dåvarande position
        state_old = agent.get_state(game)

        #inmata det nya positionen
        final_move = agent.get_action(state_old)

        #Utföra det och lokalisera na positionen
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #utföra i korta minnes lagringen
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #Komma ihåg allt 
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #träna lång minnes lagringen (så att ain kan förbätra sig själv från alla sina minnen)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score

            print("GAME", agent.n_names, "SCORE:", score, "RECORD:", record)

if __name__ == '__main__':
    train()


