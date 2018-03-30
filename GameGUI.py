import pygame
from GameSettings import*

pygame.font.init()
# display message to the screen
# default value -> center in the screen
# CITATION:  messageToScreen from https://www.youtube.com/watch?v=D69T-pfI6LY&index=46&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
def messageToScreen(msg, color, surface, xDisplace = 0, yDisplace = 0, font = "medium"):
    textSurf, textRect = textObjects(msg, color, font)
    textRect.center = (halfScreenWidth + xDisplace, halfScreenHeight + yDisplace)
    surface.blit(textSurf, textRect)

# define text objects
# CITATION: textObjects from https://www.youtube.com/watch?v=D69T-pfI6LY&index=46&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
def textObjects(text, color, font = "small"):
    if font == "small":
        textSurface = smallfont.render(text, True, color)
    elif font == "medium":
        textSurface = medfont.render(text, True, color)
    elif font == "large":
        textSurface = largefont.render(text, True, color)
    elif font == "blazed":
        textSurface = blazedfont.render(text, True, color)

    return textSurface, textSurface.get_rect()