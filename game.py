import pygame
import random 
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
 
#Omstart 

#Belöning 

#Spel(händelse) > direktion.

#spel_iteration

#kollison check




#Direktionerna som är tillgänglig i spelet.
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x, y')

BLOCK_SIZE = 20
SPEED = 40

#Färger
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        #bredd (w) & Höjd (h) variabler
        self.w = w
        self.h = h

        #init skärm
        #Anger skärmens begränsningar dessutom ytan för spel planen
        self.display = pygame.display.set_mode((self.w, self.h))

        #En liten namn som sidan kommer få
        pygame.display.set_caption('SNAKE')

        #En integrerad klocka som tillåter  elet ticka framåt.
        self.clock = pygame.time.Clock()
        
        self.reset()
        
        

    def reset(self):
        #Ormens påbörjande direktion när spelet startas
        self.direction = Direction.RIGHT

        #Anger vart huvudet på ormen kommer befinna sig, som är då i mitten. 
        self.head = Point(self.w/2, self.h/2)

        #Ger den en initiall storlek av 3 så 1 block i mitten och sedan två bakom den.
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        #Poäng
        self.score = 0

        #Mat i mappen
        self.food = None

        #Anroppar våran mat placerare
        self._place_food()

        self.frame_iteration = 0

    def _place_food(self):
        #Vi tar fram random koordinater, men som är begrännsande beroende på skräm storleken
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE

        #Anger maten denna koordinat
        self.food = Point(x, y)

        #Vi måste kolla om maten har kanske kommit fram på ormen, då behövs det att vi gör om det.
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        #a. få in inputs
        #Inväntar på inputs av användaren
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    

        #b. Ormen rör sig
        self._move(action) #updatterar huvudet av ormen
        self.snake.insert(0, self.head)

        #c. Kolla om ormen har dött = spelet är slut
        #Dessutom nu om ain har spelet för länge utan något nytt som händer.
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        #d. Placera nytt frukt eller röra sig 
        if self.head == self.food:
            self.score +=1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        #e. Updatera interna klockan och skörmen.¨
        self._update_ui()
        self.clock.tick(SPEED)

        #f. returnera spelet är över och poäng
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        #Träffar kanterna
        if pt.x > self.w-BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        #Träffar sig själv
        if pt in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE-2, BLOCK_SIZE-2))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        #[framåt, höger, vänster]

        clock_wise  = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] #Ingen förändring

        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] #Åker åt höger

        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] #Åker åt vänster

        self.driection = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x+= BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x-= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y+= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y-= BLOCK_SIZE

        self.head = Point(x, y)