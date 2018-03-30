import sys
import os
sys.path.append(os.path.abspath('..'))

import pygame
from pygame.locals import *
import pyganim

from Heroes import Heroes

class Firen(Heroes):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.rightData = 'characterImages/firen/firen_0.png'
		self.leftData = 'characterImages/firen/firen_0_mirror.png'
		
		self.rData = 'characterImages/firen/firen_1.png' # for right special attacks
		self.lData = 'characterImages/firen/firen_1_mirror.png' # left for special attacks

		self.specialAttackRect = [(0*80, 0*80, 80, 80),
								  (1*80, 0*80, 80, 80),
								  (2*80, 0*80, 80, 80),
								  (3*80, 0*80, 80, 80),
								  (4*80, 0*80, 80, 80),
								  (5*80, 0*80, 80, 80),
								  (6*80, 0*80, 80, 80),
								  (7*80, 0*80, 80, 80),
								  (8*80, 0*80, 80, 80),
								  (9*80, 0*80, 80, 80),]

		self.lspecialAttackRect = [(9*80, 0*80, 80, 80),
								  (8*80, 0*80, 80, 80),
								  (7*80, 0*80, 80, 80),
								  (6*80, 0*80, 80, 80),
								  (5*80, 0*80, 80, 80),
								  (4*80, 0*80, 80, 80),
								  (3*80, 0*80, 80, 80),
								  (2*80, 0*80, 80, 80),
								  (1*80, 0*80, 80, 80),
								  (0*80, 0*80, 80, 80),]

		self.kickAttackRect = [(4*80, 1*80, 80, 80),
							   (5*80, 1*80, 80, 80),
							   (6*80, 1*80, 80, 80),
							   (7*80, 1*80, 80, 80),
							   (8*80, 1*80, 80, 80),
							   (9*80, 1*80, 80, 80),]

		self.lkickAttackRect = [(5*80, 1*80, 80, 80),
							   (4*80, 1*80, 80, 80),
							   (3*80, 1*80, 80, 80),
							   (2*80, 1*80, 80, 80),
							   (1*80, 1*80, 80, 80),
							   (0*80, 1*80, 80, 80),]

	def specialAttack(self):
		specialAttack = pyganim.getImagesFromSpriteSheet(self.rData, rects = self.specialAttackRect)
		specialAttackFrame = list(zip(specialAttack, [100] * len(specialAttack)))
		specialAttackAnim = pyganim.PygAnimation(specialAttackFrame)
		return specialAttackAnim

	def lspecialAttack(self):
		lspecialAttack = pyganim.getImagesFromSpriteSheet(self.lData, rects = self.lspecialAttackRect)
		lspecialAttackFrame = list(zip(lspecialAttack, [100] * len(lspecialAttack)))
		lspecialAttackAnim = pyganim.PygAnimation(lspecialAttackFrame)
		return lspecialAttackAnim

	def kick(self):
		kickAttack = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.kickAttackRect)
		kickAttackFrame = list(zip(kickAttack, [100] * len(kickAttack)))
		kickAnim = pyganim.PygAnimation(kickAttackFrame)
		return kickAnim

	def lkick(self):
		lkickAttack = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.lkickAttackRect)
		lkickAttackFrame = list(zip(lkickAttack, [100] * len(lkickAttack)))
		lkickAnim = pyganim.PygAnimation(lkickAttackFrame)
		return lkickAnim