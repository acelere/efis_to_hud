#!/usr/bin/env python

import math, os, sys, random
import argparse, pygame
from operator import add

#############################################
## Function: initDisplay
def initDisplay(debug):
    pygame.init()
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        # if False:
        print("default to XDisplay {0}".format(disp_no))
        size = 480, 720
        # size = 320, 240
        screen = pygame.display.set_mode(size)
    else:
        drivers = ["directfb", "fbcon", "svgalib"]
        found = False
        for driver in drivers:
            if not os.getenv("SDL_VIDEODRIVER"):
                os.putenv("SDL_VIDEODRIVER", driver)
            try:
                pygame.display.init()
            except pygame.error:
                print("Driver: {0} failed.".format(driver))
                continue

            found = True
            break

        if not found:
            raise Exception("No video driver found.  Exiting.")

        if sys.platform.startswith('win'):
            size = 480, 720
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
       
        else:
            size = pygame.display.Info().current_w, pygame.display.Info().current_h
            screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    return screen, size


#############################################
## Function: generateHudReferenceLineArray
## create array of horz lines based on pitch, roll, etc.
def hud_generateHudReferenceLineArray(
    screen_width, screen_height, ahrs_center, pxy_div, pitch=0, roll=0, deg_ref=0, line_mode=1,
):


    if line_mode == 1:
        if deg_ref == 0:
            length = screen_width * 1.25
        elif (deg_ref % 10) == 0:
            length = screen_width * 0.85
        elif (deg_ref % 5) == 0:
            length = screen_width * 0.85
    else:
        if deg_ref == 0:
            length = screen_width * 0.5
        elif (deg_ref % 10) == 0:
            length = screen_width * 0.85
        elif (deg_ref % 5) == 0:
            length = screen_width * 0.85

    ahrs_center_x, ahrs_center_y = ahrs_center
    px_per_deg_y = screen_height / pxy_div
    pitch_offset = px_per_deg_y * (-pitch + deg_ref)

    center_x = ahrs_center_x - (pitch_offset * math.cos(math.radians(90 - roll)))
    center_y = ahrs_center_y - (pitch_offset * math.sin(math.radians(90 - roll)))

    x_len = length * math.cos(math.radians(roll))
    y_len = length * math.sin(math.radians(roll))
    
    start_x = center_x - (x_len / 0.75)
    end_x = center_x + (x_len / 0.75)
    start_y = center_y + (y_len / 0.75)
    end_y = center_y - (y_len / 0.75)
    
    oneThird = (end_x - start_x)/4
    st_qt_x = start_x + oneThird*1.25
    st_3qt_x = abs(end_x - oneThird)

    end_XY = center_y

    if roll < -5 and roll > -30:
        end_XY = center_y-25
    elif roll <= -30 and roll >-45:
        end_XY = center_y-35
        #st_qt_x = st_qt_x-15
    elif roll <= -45 and roll >-55:
        end_XY = center_y-45
    elif roll <= -45 and roll >-65:
        end_XY = center_y-55
        st_qt_x = st_qt_x-30
    elif roll <= -65 and roll >-75:
        end_XY = center_y-25
        st_qt_x = st_qt_x-35
    elif roll <= -75 and roll >-100:
        end_XY = center_y-45
        st_qt_x = st_qt_x-25
    elif roll <= -100 and roll >-105:
        end_XY = center_y-45
        st_qt_x = st_qt_x-25
    elif roll <= -105 and roll >-110:
        end_XY = center_y-45
        st_qt_x = st_qt_x-35
    elif roll <= -110 and roll >-125:
        end_XY = center_y-40
        st_qt_x = st_qt_x-40
    elif roll <= -125 and roll >-135:
        end_XY = center_y-50
        st_qt_x = st_qt_x-65
    elif roll <= -135 and roll >-145:
        end_XY = center_y-50
        st_qt_x = st_qt_x-65
    elif roll <= -145 and roll >-165:
        end_XY = center_y-50
        st_qt_x = st_qt_x-65
    elif roll <= -165 and roll >=-180:
        end_XY = center_y-50
        st_qt_x = st_qt_x-65          
    
    elif roll > 5 and roll <30:
        end_XY = center_y-25
    elif roll >= 30 and roll <45:
        end_XY = center_y-35
    elif roll >= 45 and roll <55:
        end_XY = center_y-45
    elif roll >= 55 and roll <65:
        end_XY = center_y-25
        st_qt_x = st_qt_x-15
    elif roll >= 65 and roll <75:
        end_XY = center_y-45
        st_qt_x = st_qt_x-5
    elif roll >= 75 and roll <100:
        end_XY = center_y-45
        st_qt_x = st_qt_x-25
    elif roll >= 100 and roll <125:
        end_XY = center_y-35
        st_qt_x = st_qt_x-55
    elif roll >=125 and roll < 135:
        end_XY = center_y-35
        st_qt_x = st_qt_x-70
    elif roll >=135 and roll < 145:
        end_XY = center_y-40
        st_qt_x = st_qt_x-60
    elif roll >= 145 and roll <165:
        end_XY = center_y-40
        st_qt_x = st_qt_x-65
    elif roll >=165 and roll <=180:
        end_XY = center_y-40
        st_qt_x = st_qt_x-65          
    elif roll >= -5 and roll <= 5:
        end_XY = center_y-40

    xRot = center_x + math.cos(math.radians(-10)) * (start_x - center_x) - math.sin(math.radians(-10)) * (start_y - center_y)
    yRot = center_y + math.sin(math.radians(-10)) * (start_x - center_x) + math.cos(math.radians(-10)) * (start_y - center_y)
    xRot1 = center_x + math.cos(math.radians(+10)) * (end_x - center_x) - math.sin(math.radians(+10)) * (end_y - center_y)
    yRot1 = center_y + math.sin(math.radians(+10)) * (end_x - center_x) + math.cos(math.radians(+10)) * (end_y - center_y)

    xRot2 = center_x + math.cos(math.radians(-10)) * (end_x - center_x) - math.sin(math.radians(-10)) * (end_y - center_y)
    yRot2 = center_y + math.sin(math.radians(-10)) * (end_x - center_x) + math.cos(math.radians(-10)) * (end_y - center_y)
    xRot3 = center_x + math.cos(math.radians(+10)) * (start_x - center_x) - math.sin(math.radians(+10)) * (start_y - center_y)
    yRot3 = center_y + math.sin(math.radians(+10)) * (start_x - center_x) + math.cos(math.radians(+10)) * (start_y - center_y)
    
    return [[xRot, yRot],[start_x, start_y],[end_x, end_y],[xRot1, yRot1],[xRot2, yRot2],[xRot3, yRot3], [st_qt_x, end_XY], [st_3qt_x, end_XY]]


#############################################
## Class: Point
## used for graphical points.
class Point:
    # constructed using a normal tupple
    def __init__(self, point_t=(0, 0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])

    # define all useful operators
    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Point((self.x * scalar, self.y * scalar))

    def __div__(self, scalar):
        return Point((self.x / scalar, self.y / scalar))

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    # get back values in original tuple format
    def get(self):
        return (self.x, self.y)


#############################################
## Function: draw_dashed_line
def hud_draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement / length

    for index in range(0, length / dash_length, 2):
        start = origin + (slope * index * dash_length)
        end = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)


#############################################
## Function: hud_draw_text
def hud_draw_text(screen, font, text, color, x, y):
    screen.blit(font.render(text, 1, color), (x, y))


#############################################
## Function: hud_draw_box_text
def hud_draw_box_text(
    screen, font, text, textcolor, x, y, width, height, linecolor, thickness
):
    pygame.draw.rect(screen, linecolor, (x, y, width, height), thickness)
    screen.blit(font.render(text, 1, textcolor), (x, y))


#############################################
## Function draw horz lines
def hud_draw_horz_lines(
    pygamescreen,
    surface,
    width,
    height,
    ahrs_center,
    ahrs_line_deg,
    aircraft,
    color,
    line_thickness,
    line_mode,
    font,
    pxy_div,
    Nadir_Circ,
    Zenith_Star,
    black_gap,
):

    for l in range(-90, 91, ahrs_line_deg):
        line_coords = hud_generateHudReferenceLineArray(
            width,
            height,
            ahrs_center,
            pxy_div,
            pitch=aircraft.pitch,
            roll=aircraft.roll,#
            deg_ref=l,
            line_mode=line_mode,
        )
        if l > 85:
            surface.blit(
            Nadir_Circ, (line_coords[6][0], line_coords[6][1]
                         )
                        )

        elif l <-85:
            surface.blit(
            Zenith_Star, (line_coords[6][0], line_coords[6][1]
                         )
                        )
          
        if abs(l) > 45:
            if l % 5 == 0 and l % 10 != 0:
                continue
        # draw below or above the horz
        if l < 0 and l > -81:
            z=1+1            
            hud_draw_dashed_line(
                surface,
                color,
                line_coords[1],
                line_coords[2],
                width=line_thickness,
                dash_length=5,
            )
            pygame.draw.lines(surface,
                color,
                False,
                (line_coords[2],
                line_coords[4]),
                line_thickness
            )
            pygame.draw.lines(surface,
                color,
                False,
                (line_coords[1],
                line_coords[5]),
                line_thickness
            )
            surface.blit(black_gap, (line_coords[6][0], line_coords[6][1]))
                    
        elif l == 0:
            pygame.draw.lines(
                surface,
                color,
                False,
                (line_coords[0],
                line_coords[1]),
                line_thickness
            )
            pygame.draw.lines(
                surface,
                color,
                False,
                (line_coords[1],
                line_coords[2]),
                line_thickness
            )
            pygame.draw.lines(
                surface,
                (0, 0, 0),
                False,
                (line_coords[2],
                line_coords[3]),
                line_thickness
            )
           
            pygame.draw.lines(
                surface,
                color,
                False,
                (line_coords[2],
                line_coords[3]),
                line_thickness
            )
            
        elif l > 0 and l < 81:
            pygame.draw.lines(
                surface,
                color,
                False,
                (line_coords[0],
                line_coords[1]),
                line_thickness
            )
            pygame.draw.lines(
                surface,
                color,
                False,
                (line_coords[1],
                line_coords[2]),
                line_thickness
            )
            pygame.draw.lines(
                surface,
                (0, 0, 0),
                False,
                (line_coords[2],
                line_coords[3]),
                line_thickness
            )
           
            pygame.draw.lines(
                surface,
                color,
                False,
                (line_coords[2],
                line_coords[3]),
                line_thickness
            )
            surface.blit(black_gap, (line_coords[6][0], line_coords[6][1]))            
#             black_gap_draw_neg = pygame.transform.rotate(black_gap, aircraft.roll)            
#             surface.blit(black_gap_draw_neg, (line_coords[6][0], line_coords[6][1]))
#         elif l >= 3 and l < 81:
#             pygame.transform.rotate(black_gap, aircraft.roll*2)
#             pygame.transform.scale(black_gap, (100, 100))
#             surface.blit(
#             black_gap, (line_coords[6][0], line_coords[6][1]
#                          )
#                         ) 
#             pygame.draw.lines(
#                 surface,
#                 color,
#                 False,
#                 (line_coords[4],
#                 line_coords[5]),
#                 line_thickness
#             )            
            
#         else:
#             pygame.draw.lines(
#                 surface,
#                 color,
#                 False,
#                 (line_coords[0],
#                 line_coords[1],
#                 line_coords[2],
#                 line_coords[3]),
#                 line_thickness
#             )

        # draw degree text
        if l != 0 and l % 5 == 0:
            text = font.render(str(abs(l)), False, color)
            text_width, text_height = text.get_size()
            left = int(line_coords[1][0]) - (text_width + int(width / 100))
            top = int(line_coords[1][1]) - text_height / 2
            right = int(line_coords[2][0]) + (int(width / 100))#text_width +
            top_ri = int(line_coords[2][1]) - text_height / 2            
            middle_x = (line_coords[2][0]-line_coords[1][0])
            middle_y = (line_coords[1][0])
            surface.blit(text, (left, top))
            surface.blit(text, (right, top_ri))
            if l < -80 or l > 80:
                text = font.render(str(abs(l)), False, (0, 0, 0))
                text_width, text_height = text.get_size()
                left = int(line_coords[1][0]) - (text_width + int(width / 100))
                top = int(line_coords[1][1]) - text_height / 2
                right = int(line_coords[2][0]) + (int(width / 100))#text_width +
                top_ri = int(line_coords[2][1]) - text_height / 2
                surface.blit(text, (left, top))
                surface.blit(text, (right, top_ri))
                top_left = (
        -(surface.get_width() - width) / 2,
        -(surface.get_height() - height) / 2,
    )
    pygamescreen.blit(surface, top_left)
