import pygame
import random 
from enum import Enum
from collections import namedtuple
pygame.init()

#Direktionerna som är tillgänglig i spelet.
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x', 'y')

BLOCK_SIZE = 20

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
            self._place_foodfood()

    def play_step(self):
        pass

if __name__== '__main__':
    game = SnakeGame()

    #Spel loopen
    while True:
        game.play_step()



    pygame.quit() 