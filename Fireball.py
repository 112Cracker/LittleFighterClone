import pygame
from pygame.locals import *
import pyganim

class Fireball(object):

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.movingSpeed = 10 # in the x direction
		self.movingDirection = "right"

		self.rdata = "characterImages/fireBall.png"
		self.ldata = "characterImages/fireBall_mirror.png"

		self.ballRect = [(0*82, 0*83, 82, 83),
						 (1*82, 0*83, 82, 83),
						 (2*82, 0*83, 82, 83),
						 (3*82, 0*83, 82, 83)]

		self.lballRect = [(3*82, 0*83, 82, 83),
						 (2*82, 0*83, 82, 83),
						 (1*82, 0*83, 82, 83),
						 (0*82, 0*83, 82, 83)]

	def ball(self):
		fireBall = pyganim.getImagesFromSpriteSheet(self.rdata, rects = self.ballRect)
		ballFrame = list(zip(fireBall, [100] * len(fireBall)))
		ballAnim = pyganim.PygAnimation(ballFrame)
		return ballAnim

	def lball(self):
		lfireBall = pyganim.getImagesFromSpriteSheet(self.ldata, rects = self.lballRect)
		lballFrame = list(zip(lfireBall, [100] * len(lfireBall)))
		lballAnim = pyganim.PygAnimation(lballFrame)
		return lballAnim