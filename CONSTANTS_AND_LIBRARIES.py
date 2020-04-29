from graphics import *
from random import randint
from math import atan, sin, cos, pi

white = color_rgb(255, 255, 255)
red = color_rgb(255, 0, 0)
green = color_rgb(124, 252, 0)
yellow = color_rgb(247, 239, 1)
bg_color = color_rgb(50, 50, 50)

stateList = {"start": 1, "end": -1, "nothing": 0}

# def graph_reading():
#
#     w = WindowObject("window", 1000, 800)
#
#     auto = Graph()
#     auto.data_to_structure("input.txt")
#     auto.draw_graph(w)
#     w.unprint_message()
#
#     while True:
#         word = w.read_word()
#         if word is False:
#             break
#         result = auto.verify_word(word)
#         w.print_message(result)
