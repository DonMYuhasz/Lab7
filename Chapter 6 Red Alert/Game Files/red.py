# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 21:54:08 2022

@author: chris.pham
"""

import pgzrun
import pygame
import pgzero
import random
import asyncio
from pgzero.builtins import Actor
from random import randint

#Declare constants
FONT_COLOR = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FINAL_LEVEL = 6
START_SPEED = 10
COLORS = ["green", "blue","orange"]

#Declare global variables
game_over = False
game_complete = False
game_lose_try = False
Warn = True
current_level = 1
tries = 4
#Keep track of the stars on the screen
stars = []
animations = []

#Draw the stars
def draw():
    global stars, current_level, game_over, game_complete,tries,game_lose_try,Warn
    screen.clear()
    screen.blit("space", (0,0)) #add a background image to the game window
    if game_over:
        display_message("GAME OVER!", "Try again.")
    elif game_lose_try:
        screen.clear()
        screen.fill("red")
        asyncio.sleep(1)
        game_lose_try = False
    elif Warn:
        display_message("Epilepsy Warning\n", "I added sicc flashy lights which may be dangerous\nclick to continue")
    elif game_complete:
        display_message("YOU WON!", "Those were pretty fast.")
    else:
        for star in stars:
            star.draw()
    screen.draw.text("Tries", (0,0 ), color = "black", background = "white")
    screen.draw.text(str(tries), (0,20 ), color = "black", background = "white")

def update():
    global stars, Warn
    if len(stars) == 0 and Warn == False:
        stars = make_stars(current_level)

def make_stars(number_of_extra_stars):
    colors_to_create = get_colors_to_create(number_of_extra_stars)
    new_stars = create_stars(colors_to_create)
    layout_stars(new_stars)
    animate_stars(new_stars)
    return new_stars

def get_colors_to_create(number_of_extra_stars):
    #return[]
    colors_to_create = ["red"]
    for i in range(0, number_of_extra_stars):
        random_color = random.choice(COLORS)
        colors_to_create.append(random_color)
    return colors_to_create

def create_stars(colors_to_create):
    #return[]
    new_stars = []
    for color in colors_to_create:
        star = Actor(color + "-star")
        new_stars.append(star)
    return new_stars

def layout_stars(stars_to_layout):
    #pass
    number_of_gaps = len(stars_to_layout) + 1
    gap_size = WIDTH / number_of_gaps
    random.shuffle(stars_to_layout)
    for index, star in enumerate(stars_to_layout):
        new_x_pos = (index + 1) * gap_size
        star.x = new_x_pos

def animate_stars(stars_to_animate):
    #pass
    for star in stars_to_animate:
        duration = START_SPEED /((current_level+1)*1)
        star.anchor = ("center", "bottom")
        animation = animate(star, duration=duration, on_finished=handle_game_over, y=HEIGHT)
        animations.append(animation)
        
def handle_game_over():
    global game_over, tries,game_lose_try,stars
    if(tries>0):
        tries = tries-1
        game_lose_try = True
        stars = []
    elif(game_complete != True):
        game_over = True
    
    
def on_mouse_down(pos):
    global stars, current_level,tries,game_lose_try, Warn
    Warn = False
    for star in stars:
        if star.collidepoint(pos):
            if "red" in star.image:
                red_star_click()
            else:
                handle_game_over()
    

def red_star_click():
    global current_level, stars, animations, game_complete 
    stop_animations(animations)
    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level = current_level + 1
        stars = []
        animations = []
        
def stop_animations(animations_to_stop):
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()
            
def display_message(heading_text, sub_heading_text):
    screen.draw.text(heading_text, fontsize=60, center=CENTER, color=FONT_COLOR)
    screen.draw.text(sub_heading_text,
                     fontsize=30,
                     center=(CENTER_X, CENTER_Y+30),
                     color=FONT_COLOR)


pgzrun.go()