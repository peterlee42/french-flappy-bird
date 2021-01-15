from pygame.transform import scale
from pygame.image import load
import pygame

pygame.init()
bg = load('assets/bg.png')

bird_one = load('assets/bird1.png')
bird_two = load('assets/bird2.png')
bird_three = load('assets/bird3.png')

ground = load('assets/ground.png')
pipe = load('assets/pipe.png')

restart_button = load('assets/restart.png')

paris = load('assets/paris.png')

# foods


onion = scale(load('assets/onion.png'), (51, 51))
garlic = scale(load('assets/garlic.png'), (65, 72))
salt_pepp = scale(load('assets/salt_pepp.png'), (52, 52))
white_wine = scale(load('assets/butter.png'), (97, 65))
butter = scale(load('assets/white_wine.png'), (30, 108))
beef_stock = scale(load('assets/beef_stock.png'), (55, 97))
bag_of_sugar = scale(load('assets/bag_of_sugar.png'), (52, 52))

foods = [onion, garlic, salt_pepp, butter,
         white_wine, beef_stock, bag_of_sugar]
