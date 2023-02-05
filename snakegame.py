import pygame
import sys
from pygame.math import Vector2
import random
import time

game_active = True

class Fruit:
    def __init__(self):
        self.reset()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255,0,0), fruit_rect)
    
    def randomize(self):
        self.x = random.randint(1,cell_number-1)
        self.y = random.randint(1,cell_number-1)
        self.pos = Vector2(self.x, self.y) 

    def reset(self):
        self.x = random.randint(1,cell_number-1)
        self.y = random.randint(1,cell_number-1)
        self.pos = Vector2(self.x, self.y) 


class Snake:
    def __init__(self, snake_colour):
        self.reset(snake_colour)

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, self.snake_colour, block_rect)

    def move_snake(self): 
        if self.new_block == True:
            body_copy = self.body[:] 
            body_copy.insert(0, body_copy[0]+self.direction) 
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] 
            body_copy.insert(0, body_copy[0]+self.direction) 
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self, snake_colour):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.snake_colour = snake_colour



class Snake2(Snake):
    def __init__(self, snake_colour):
        self.reset(snake_colour)

        
    def reset(self, snake_colour):
        self.body = [Vector2(8, 10), Vector2(9, 10), Vector2(10, 10)]
        self.direction = Vector2(0,1)
        self.new_block = False
        self.snake_colour = snake_colour

class Button:
    def __init__(self, text, width, height, pos, elevation):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos,(width, height))
        self.top_color = (88, 24, 69)

        self.bottom_rect = pygame.Rect(pos,(width, elevation))
        self.bottom_color = (88, 24, 69)

        self.text_surface = game_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)
    
    def draw_button(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation 
        self.text_rect.center = self.top_rect.center
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = 12)
        screen.blit(self.text_surface, self.text_rect) 
        self.check_click()
        pygame.display.update()
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.dynamic_elevation = 0
            self.pressed = True
        elif self.pressed == True:
            action = True
            self.dynamic_elevation = self.elevation
            self.pressed = False
            return action
            
class Main:
    def __init__(self):
        self.snake = Snake((127, 0, 255))
        self.snake2 = Snake2((0,128,128))
        self.fruit = Fruit()
        self.button = Button('QUIT', 200, 40, (500, 500), 6) 
        self.retry = Button('RETRY', 200, 40, (100, 500), 6)
    
    def update(self):
        if game_active == True:
            self.snake.move_snake()
            self.snake2.move_snake()
            self.check_collision()
           
            if self.check_fail():
                self.game_over()
         
         
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.snake2.draw_snake()
        self.draw_score()
        self.draw_score2()
    
            
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
        
        if self.fruit.pos == self.snake2.body[0]:
            self.fruit.randomize()
            self.snake2.add_block()

    def check_fail(self):
        if not (0 <= self.snake.body[0].x < cell_number) or not (0 <= self.snake.body[0].y < cell_number):
            return True
        
        for block in self.snake.body[1:]: #
            if block == self.snake.body[0] or block == self.snake2.body[0]:
                return True
            
        
        if not (0 <= self.snake2.body[0].x < cell_number) or not (0 <= self.snake2.body[0].y < cell_number):
            return True
        
        for block in self.snake2.body[1:]: #
            if block == self.snake2.body[0] or block == self.snake.body[0]:
                return True
            
    def game_over(self):
        game_over_text = 'GAME OVER'
        game_over_surface = game_over_font.render(game_over_text, True, pygame.Color('black'))
        go_x = cell_size * cell_number / 2
        go_y = cell_size * cell_number / 2
        game_over_rect = game_over_surface.get_rect(center = (go_x, go_y))
        screen.blit(game_over_surface, game_over_rect)
        self.button.draw_button()
        self.retry.draw_button()
        global game_active
        game_active = False
        

    def draw_score(self):
        score_text ='P1: '+ str(len(self.snake.body) - 3)  
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)
    
    def draw_score2(self):
        score_text = 'P2: '+str(len(self.snake2.body) - 3)  
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = 60
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)
    
    
    
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 25)
game_over_font = pygame.font.Font(None, 100)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
pygame.display.set_caption("Snake wars")

main_game = Main()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == SCREEN_UPDATE:
            main_game.update()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main_game.snake2.direction.y != 1:
                    main_game.snake2.direction = Vector2(0, -1)
            if event.key == pygame.K_s:
                if main_game.snake2.direction.y != -1:
                    main_game.snake2.direction = Vector2(0, 1)
            if event.key == pygame.K_a:
                if main_game.snake2.direction.x != 1:
                    main_game.snake2.direction = Vector2(-1, 0)
            if event.key == pygame.K_d:
                if main_game.snake2.direction.x != -1:
                    main_game.snake2.direction = Vector2(1, 0)
    
    if main_game.button.check_click() == True:
        pygame.quit()
        sys.exit()
    
    if main_game.retry.check_click() == True:
       game_active = True
       main_game.fruit.reset()
       main_game.snake.reset((127, 0, 255))
       main_game.snake2.reset((0,128,128))
        
    screen.fill((200, 150, 200)) 
    main_game.draw_elements()
    if game_active == True:
        pygame.display.update()
    clock.tick(60)


