###################################################################################################################################################################################################################################################################################
#######copyright 2019 Tanner Cormier, this progam is distributed under the terms of GNU GPLv3########################################################################################################################################################################################
###################################################################################################################################################################################################################################################################################
#imports the pygame modules needed to create the game
import pygame
from pygame.locals import *

#module that provides an interface with the operating system
import os

#module that allows you to launch and communicate with other files and programs
import sys

#module to provide extra math functions
import math

#module to generate random numbers
import random

#creates an instance of the pygame modules
pygame.init() 


###################################################################################################################################################################################################################################################################################


#width and height variables for the game window
W, H = 1120, 465

#variable for the game window
win = pygame.display.set_mode((W, H))

#sets the name displayed of the title bar
pygame.display.set_caption('Of The Abyss') 


###################################################################################################################################################################################################################################################################################


#variable for the game music
music = pygame.mixer.music.load(os.path.join('Music', 'backgroundMusic.mp3'))

#variable for the enemy's hit sound
hitSound = pygame.mixer.Sound(os.path.join('Music', 'enemyHit.ogg'))

#function that plays the music for the game on a loop
pygame.mixer.music.play(-1)


###################################################################################################################################################################################################################################################################################


#list variables that hold the images for the player walking animations
walkRight = [pygame.image.load(os.path.join('walking', '01.png')), pygame.image.load(os.path.join('walking', '02.png')), pygame.image.load(os.path.join('walking', '03.png')), pygame.image.load(os.path.join('walking', '04.png'))]
walkLeft = [pygame.image.load(os.path.join('walking', '05.png')), pygame.image.load(os.path.join('walking', '06.png')), pygame.image.load(os.path.join('walking', '07.png')), pygame.image.load(os.path.join('walking', '08.png'))]

#list variables that hold the images for the player attack animations
attackRight = [pygame.image.load(os.path.join('attack', '1.png')), pygame.image.load(os.path.join('attack', '2.png')), pygame.image.load(os.path.join('attack', '3.png')), pygame.image.load(os.path.join('attack', '4.png'))]
attackLeft = [pygame.image.load(os.path.join('attack', '5.png')), pygame.image.load(os.path.join('attack', '6.png')), pygame.image.load(os.path.join('attack', '7.png')), pygame.image.load(os.path.join('attack', '8.png'))]

#variable that holds the background image for the game
bg = pygame.image.load(os.path.join('City Background', 'Ruined City.png')).convert()


###################################################################################################################################################################################################################################################################################


#create player class
class player(object):

    #function to initialize what attributes the player object will need
    def __init__(self, x, y, width, height):
        self.x = x #attribute for horizontal position on the map
        self.y = y #attribute for vertical position on the map
        self.width = width #attribute for the width of player character
        self.height = height #attribute for the height of player character
        self.vel = 5 #attribute for movement speed
        self.walkCount = 0 #attribute that counts what image the player needs to be at in their walking animation
        self.left = False #attribute that says whether the player is going left or not
        self.right = False #attribute that says whether the player is going right or not
        self.standing = True #attribute that says whether the player is moving or not
        self.isJump = False #attribute that says whether the player is jumping or not
        self.jumpCount = 8 #attribute that counts how long the player is in the air while they're jumping
        self.attack = False #attribute that says whether the player is attacking or not
        self.attackCount = 0 #attribute that counts what image the player needs to be at in their attack animation

#function that draws the player class to the game window
    def draw(self, win):
        if self.walkCount + 1 >= 12: #if walk the walk count plus 1 is greater than 12
            self.walkCount = 0 #resets the walkcount to zero

        if self.attackCount + 1 >= 12: #if the attack count plus 1 is greater than 12
            self.attackCount = 0 #reset the attack count to zero
            self.attack = False #reset the attack variable to false

        if not(self.standing): #if the player is moving
            if self.left: #if the player is moving left
                if self.attack == True: #and is also attacking
                    win.blit(attackLeft[self.attackCount//3], (self.x, self.y)) #call the image the player is at in their attack animation
                    self.attackCount += 1 #increase the attack counter by 1
                else: #the player is just walking left
                    win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) #call whatever image the player is at in their walk animation
                    self.walkCount += 1 #increase the walk counte by 1
            else: #or else if the player is moving right
                if self.attack == True: #and is also attacking
                    win.blit(attackRight[self.attackCount//3], (self.x, self.y)) #call the image for the player attack animation
                    self.attackCount += 1 #increase the attack counter by 1
                else: #the player is just walking right
                    win.blit(walkRight[self.walkCount//3], (self.x, self.y)) #call the image for the player walking animation
                    self.walkCount += 1#
        else: #the player is standing
                if self.right: #if the player is looking right
                    if self.attack == True: #and also attacking
                        win.blit(attackRight[self.attackCount//3], (self.x, self.y)) #call the image for attack right animation
                        self.attackCount += 1 #increase attack count by 1
                    else: #the player is just standing
                        win.blit(walkRight[0], (self.x, self.y)) #draw the player standing right
                else: #the player is looking left
                    if self.attack == True: #and is also attacking
                        win.blit(attackLeft[self.attackCount//3], (self.x, self.y)) #call the image for the attack left animation
                        self.attackCount += 1 #increase attack counter by 1
                    else: #the player is just walking left
                        win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y, 40, 52) #draw the player hitbox on the game window


###################################################################################################################################################################################################################################################################################


#class for our enemy
class victim(object):
    #list variables that hold the images for the enemy's walking animations
    walkRight = [pygame.image.load(os.path.join('Victims', 'en1_5.png')), pygame.image.load(os.path.join('Victims', 'en1_6.png')), pygame.image.load(os.path.join('Victims', 'en1_7.png')), pygame.image.load(os.path.join('Victims', 'en1_8.png'))]
    walkLeft = [pygame.image.load(os.path.join('Victims', 'en1_1.png')), pygame.image.load(os.path.join('Victims', 'en1_2.png')), pygame.image.load(os.path.join('Victims', 'en1_3.png')), pygame.image.load(os.path.join('Victims', 'en1_4.png'))]

#function to define what variables the enemy object will need to have
    def __init__(self, x, y, width, height, end):
        self.x = x #attribute for enemy's horizontal position
        self.y = y #attribute for enemy's vertical position
        self.width = width #attribute for the width of enemy character
        self.height = height #attribute for the height of enemy character
        self.path = [x, end] #attribute that defines where enemy starts and finishes
        self.walkCount = 0 #attribute to count what image the player needs to be at in their walking animation
        self.vel = 3 #attribute for the speed at which the player moves
        self.hitbox = (self.x, self.y, 31, 57) #attribute for the size & position of enemy hit box
        self.health = 10 #attribute for the health of the enemy
        self.visible = True #attribute that says whether or not the enemy is visible on the screen

#function that draws the enemy animation to the game window
    def draw(self, win):
        self.move() #calls the enemy's move function and draws it to the window
        if self.visible: #if the enemy is visible on the screen
            if self.walkCount + 1 >= 12: #if the walk counter plus 1 is greater than 12
                self.walkCount = 0 #reset the walk counter to zero
            if self.vel > 0: #if the enemy's movement is greater than where it started
                win.blit(self.walkLeft[self.walkCount//3], (self.x ,self.y))#call the image needed for the enemy's left walking animation
                self.walkCount += 1 #increase walk count by one
            else: #else the enemy is moving right
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y)) #call the image needed for the enemy's right walking animation
                self.walkCount += 1 #increase walk count by one

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #draw the enemy health box
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x, self.y + 2, 25,57) #draw the enemies hitbox

#function for the enemy's movement
    def move(self):
        if self.vel > 0:  #if movement is greater than zero
            if self.x < self.path[1] + self.vel: #and if our x position is not greater than the end of our path
                self.x += self.vel #increase movement to right of the screen
            else: #when the enemy reaches the end of their path
                self.vel = self.vel * -1 #turn movement to negative which moves us left
                self.x += self.vel #move enemy x position in the other direction
                self.walkCount = 0 #set walkCount back to zero
        else: #if the enemy is moving left
            if self.x > self.path[0] - self.vel: # If the enemy has not reached where it spawned
                self.x += self.vel #move enemy x position to the left
            else:  #once they reach their starting point
                self.vel = self.vel * -1 #turn the velocity back to positive which moves us right
                self.x += self.vel #move enemy x position right
                self.walkCount = 0 #reset walk count back to 0

#function to call when the enemy is hit
    def hit(self):
        hitSound.play() #play the death wav file for our enemy
        if self.health > 0: #if the enemy's health is greater than zero
            self.health -= 5 #take 5 away from enemy health when hit
        else: #the enemy has no health left
            self.visible = False #make the enemy invisible on the screen
        print('hit') #print hit to the interactive interpreter


###################################################################################################################################################################################################################################################################################


#draw to window function
def redrawWindow():
    win.blit(bg, (0,0)) #draw the background image to the game window
    text = font.render('Score: ' + str(score), 1, (0,0,0)) #variable to render the font for the score
    win.blit(text, (1000, 10)) #draw everything in the text variable to the screen
    man.draw(win) #draw the player object to the game window
    for e in enemies: #for each enemy object in the list of enemies
        e.draw(win) #draw the enemy object to the game window
    pygame.display.update() #function to update the game window constantly


###################################################################################################################################################################################################################################################################################


###////main loop variables\\\\###

#variable for the player object
man = player(200, 414, 64, 64)

#list variable that holds all the enemy objects on the screen
enemies = []

font = pygame.font.SysFont('comicsans', 30, True)

#variable for the speed of the game
gameSpeed = 18

#variable for the timing of the game
clock = pygame.time.Clock()

#variable to keep track of how many npc's you've killed
score = 0

#sets a timer for the enemy spawn event
pygame.time.set_timer(USEREVENT+1, 3000) #sets a timer for 3 seconds

###////main loop for the game\\\\###

#variable that tells the loop whether to run or stop
run = True 
while run:

    #calls function to redraw game window
    redrawWindow()

    #calls function to start game clock
    clock.tick(gameSpeed)

    for enemy in enemies: #for each enemy in the list of enemys
        if enemy.visible == True: #if that enemies visible attribute is equal to true
            #and if the player hit box overlaps with enemy hitbox
            if man.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > enemy.hitbox[1]: 
                if man.hitbox[0] + man.hitbox[2] > enemy.hitbox[0] and man.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                    if man.attack == True: #and if the player objects attack attribute equals true
                        enemy.hit() #call the function to hit and cause damage to the enemy
        else: #or else the enemy is no longer visible
            enemies.pop(enemies.index(enemy)) #remove the enemy object from the list of enemies in the game loop
            score += 1 #add 1 to the player score
                    
###///player controls\\\###
    
    keys = pygame.key.get_pressed() #variable to run the function to check if a key has been pressed

#if the space key is pressed
    if keys[pygame.K_SPACE]:
        #bulletSound.play()
        man.attack = True #make the player objects attack attribute equal true
        if man.left: #if the left attribute is true
            facing = -1 #make the player face left
        else: #the right attribute is true
            facing = 1 #make the player face right

    if keys[pygame.K_LEFT] and man.x > man.vel: #if left key is pressed and the player isnt outside of the screen
        #move player to the left
        man.x -= man.vel 
        man.left = True 
        man.right = False
        man.standing =  False
    elif keys[pygame.K_RIGHT] and man.x < 1120 - man.width - man.vel: #if right key is pressed and the player isnt outside of the screen
        #move player to the right
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else: #if no keys are being pressed
        man.standing = True #player stand still
        man.walkCount = 0 #set walk counter to zero

    if not(man.isJump): #if the player isnt jumping
        if keys[pygame.K_UP]: #and the up keys is pressed
            #make jump equal true and stop player left and right movement
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else: #the player is jumping
        if man.jumpCount >= -8: #if jumpcount is greater than negative 8
            neg = 1 
            if man.jumpCount < 0: #if jump count is less than 0
                neg = -1 #variable to decrement jump height
            man.y -= int((man.jumpCount ** 2) * 0.5) * neg
            man.jumpCount -= 1
        else: #if the player isnt jumping
            man.isJump = False #set jump variable to false
            man.jumpCount = 8 #reset jumpcount to 8


###///Game events\\\###

            
    for event in pygame.event.get(): #loops through list of game events
        if event.type == pygame.QUIT: #checks if exit button has been clicked
            run = False #set game loop run variable to false
            pygame.quit() #quit pygame module
            quit()#ends game loop

        #event to spawn enemies randomly
        if event.type == USEREVENT+1: #if the timer goes off
            if len(enemies) < 4: #and enemies in the list is less than 4
                start_range = [50, 250, 450] #list of possible starting positions
                end_range = [600, 800, 1100] #list of possible ending positions
                s_range = random.randrange(0,3) #random number to choose from the list of start ranges
                e_range = random.randrange(0,3) #random number to choose from the list of end ranges
                start_path = 0 #initialize variable to be used for the enemy objects starting position
                end_path = 0 #initialize variable to be used for the enemy objetcs end position
                #randomly choose the starting position from the list of starting positions and put the result in start_path
                if s_range == 0:
                    start_path = start_range[0]
                elif s_range == 1:
                    start_path = start_range[1]
                else:
                    start_path = start_range[2]

                #randomly choose from the list of ending positions and put the result in end_path
                if e_range == 0:
                    end_path = end_range[0]
                elif e_range == 1:
                    end_path = end_range[1]
                else:
                    end_path = end_range[2]
                #add enemy to the list of enemies on the map  
                enemies.append(victim(start_path, 442, 64, 64, end_path))
