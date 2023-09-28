import pygame
import random 
from enum import Enum
from collections import namedtuple
pygame.init()
font = pygame.font.Font('arial.ttf', 25)

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

class SnakeGame:
    def __init__(self, w=640, h=480):
        #bredd (w) & Höjd (h) variabler
        self.w = w
        self.h = h

        #init skärm
        #Anger skärmens begränsningar dessutom ytan för spel planen
        self.display = pygame.display.set_mode((self.w, self.h))
        #En liten namn som sidan kommer få
        pygame.display.set_caption('SNAKE')
        #En integrerad klocka som tillåter spelet ticka framåt.
        self.clock = pygame.time.Clock()

        #init spel läge
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

    def _place_food(self):
        #Vi tar fram random koordinater, men som är begrännsande beroende på skräm storleken
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE

        #Anger maten denna koordinat
        self.food = Point(x, y)
        #Vi måste kolla om maten har kanske kommit fram på ormen, då behövs det att vi gör om det.
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        #a. få in inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT    
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #b. Ormen rör sig
        self._move(self.direction) #updatterar huvudet av ormen
        self.snake.insert(0, self.head)

        #c. Kolla om ormen har dött = spelet är slut

        #d. Placera nytt frukt eller röra sig 

        #e. Updatera interna klockan och skörmen.¨
        self._update_ui()
        self.clock.tick(SPEED)

        #f. returnera spelet är över och poäng

        game_over = False
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE-2, BLOCK_SIZE-2))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, direction):
        x = self.head.x
        y = self.head.y

if __name__== '__main__':
    game = SnakeGame()

    #Spel loopen
    while True:
        game_over, score = game.play_step()

        if game_over == True :
            break

    print("Score:", score)

    pygame.quit() 