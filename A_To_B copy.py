import pygame
import random
import time
import sys
#import room2


black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 237,   47,   47)
blue     = (   0,   0, 255)
light_blue     = (   23,   130, 239)
yellow   = (241, 244, 66)


pygame.init()





screen_width = 880
screen_height = 650

screen = pygame.display.set_mode([screen_width, screen_height])


pygame.display.set_caption("A_to_B")


clock = pygame.time.Clock()

############################################

def intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = pygame.display.set_mode([screen_width,screen_height])

                    start.fill(black)

                    font = pygame.font.Font(None, 60)
                    text = font.render("Level 1", True, white)
                    start.blit(text, [380, 290])
                    pygame.display.flip()
                    clock.tick(30)
                    time.sleep(2)
                    main()
        
        start = pygame.display.set_mode([screen_width,screen_height])

        start.fill(black)

        pygame.draw.rect(screen, white, [300,272,280,60], 4)

        font = pygame.font.Font(None, 40)
        text = font.render("Press Space Bar", True, white)
        start.blit(text, [330, 290])

        pygame.display.flip()
        pygame.display.update()                       
        clock.tick(10)

############################################


all_block_list = pygame.sprite.Group()

player_list = pygame.sprite.Group()

wall_list = pygame.sprite.Group()

obstacle_list = pygame.sprite.Group()
moving_ver_list = pygame.sprite.Group()
moving_hor_list = pygame.sprite.Group()
blinking_obs_list = pygame.sprite.Group()

coin_list = pygame.sprite.Group()


coin_count = 0

death_count = 0

max_coin = 0

def make_wall(x,y, width, height, colour):

    wall = Wall(x,y, width, height, colour)
    wall_list.add(wall)
    all_block_list.add(wall)



def make_moving_ver(x,y, width, height, colour):

    obstacle = Obstacle(x,y, width, height, colour)
    obstacle_list.add(obstacle)
    moving_ver_list.add(obstacle)
    all_block_list.add(obstacle)

def make_moving_hor(x,y, width, height, colour):

    obstacle = Obstacle(x,y, width, height, colour)
    obstacle_list.add(obstacle)
    moving_hor_list.add(obstacle)
    all_block_list.add(obstacle)



def make_coin(x,y):
    
    global coin_count
    global death_count
    global max_coin
    
    coin = Coin(x,y)
    coin_list.add(coin)
    all_block_list.add(coin)

    if death_count > 0:
        coin_count = max_coin
    else:
        coin_count += 1
        max_coin += 1


############################################



class Wall(pygame.sprite.Sprite):

    change_x = 5
    change_y = 5
    
    def __init__(self, x,y, width, height, colour):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(colour)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Obstacle(Wall):

    def move_vertical(self, obstacle):
        
        self.rect.y += self.change_y
        
        block_hit_list = pygame.sprite.spritecollide(self,obstacle,False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y *= -1
                self.rect.y += self.change_y
            else:
                self.rect.top = block.rect.bottom
                self.change_y *= -1
                self.rect.y += self.change_y


    def move_sideway(self, obstacle):

        self.rect.x += self.change_x
        
        block_hit_list = pygame.sprite.spritecollide(self,obstacle,False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x *= -1
                self.rect.x += self.change_x
            else:
                self.rect.left = block.rect.right
                self.change_x *= -1
                self.rect.x += self.change_x


        
    
    def collision(self, lst):
        pygame.sprite.spritecollide(self,lst,True)
            
        
                
############################################
  


class Coin(pygame.sprite.Sprite):

    def __init__(self, x,y):

        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((13,13))
        self.image.fill(yellow)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y





class Player(pygame.sprite.Sprite):

    
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([22,22])
        self.image.fill(white)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        player_list.add(self)
        all_block_list.add(self)

        

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def collision(self, wall):
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self,wall,False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

                
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self,wall,False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def die(self, obs):

        global death_count
        
        if pygame.sprite.spritecollide(self,obs,False):

            death_count += 1
            
            for block in obs:
                block.collision(player_list)
                
            gameover()


    def collect(self, coin):

        global coin_count
        
        if pygame.sprite.spritecollide(self,coin, True):
            coin_count -= 1


    def reach_end(self, x,y, height):

        global coin_count
        
        if self.rect.x + 22 > x:
            if self.rect.y >= y and self.rect.y + 22 <= height + y:
                if coin_count == 0:
    #                room2.room2()
                    success()
                else:
                    pass


def gameover():

    over = False
    while not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

        
        screen.fill(black)
        font = pygame.font.Font(None, 60)
        text = font.render("Game Over", True, white)
        screen.blit(text, [320, 300])

        font = pygame.font.Font(None,25)
        text = font.render("R to Restart", True, white)
        screen.blit(text, [380,400])



        pygame.display.flip()

        clock.tick(30)

    


def success():
    over = False
    global death_count
    while not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(white)
        font = pygame.font.Font(None,60)
        text = font.render("Completed!", True, black)
        screen.blit(text, [345,290])

        font = pygame.font.Font(None, 33)
        text1 = font.render("Death Count  = ", True, black)
        text2 = font.render(str(death_count), True, black)
        screen.blit(text1, [640, 590])
        screen.blit(text2, [810, 590])

        pygame.display.flip()

        clock.tick(30)

              



def main():
    
    make_coin(180,500)
    make_coin(450,240)
    make_coin(570,300)
    make_coin(450,360)
    make_coin(570,420)
    make_coin(450,480)
    make_coin(34,360)
    make_coin(206,310)


    player = Player(10,590)
    
    done = False
    
    while not done:
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-6,0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(6,0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0,-6)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0,6)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(6,0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(-6,0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0,6)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0,-6)

#        if player.changespeed > 0:
#            if current_room == 1:
                

        player.collect(coin_list)
        
        player.collision(wall_list)

        for obstacle in moving_ver_list:
            obstacle.move_vertical(wall_list)

        for obstacle in moving_hor_list:
            obstacle.move_sideway(wall_list)

        player.reach_end(860, 20, 60)

#        for obstacle in blinking_obs_list:
#            obstacle.blink(blinking_obs_list)

        screen.fill(black)

        all_block_list.draw(screen)

        player.die(obstacle_list)
        
        pygame.display.flip()
        


        clock.tick(30)

        
    pygame.quit()
    sys.exit()



make_wall(0,0,20,570,light_blue)
make_wall(20,0,860,20,light_blue)
make_wall(0,630,880,20,light_blue)
make_wall(860,80,20,570,light_blue)
make_wall(20,500,120,20,light_blue)
make_wall(230, 103,20, 530, light_blue)
make_wall(-5,570,5,80,light_blue)
make_wall(350,20,20,535,light_blue)


make_moving_ver(120,520,20,50,red)
make_moving_ver(510,120,20,510,red)
make_moving_ver(630,20,20,510,red)
make_moving_ver(750,120,20,510,red)
make_moving_ver(20,20,230,20,red)
make_moving_ver(250,20,100,20,red)


make_moving_hor(20,330,147,20,red)
make_moving_hor(370,387,200,20,red)
make_moving_hor(860,447,200,20,red)
make_moving_hor(370,507,200,20,red)
make_moving_hor(860,327,200,20,red)
make_moving_hor(370,267,200,20,red)
make_moving_hor(860,207,200,20,red)


pygame.mouse.set_visible(True)

intro()



