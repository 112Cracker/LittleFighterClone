import pygame
from pygame.locals import *
import pyganim

from Heroes import Heroes

class Electro(Heroes):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.rightData = 'characterImages/electro/electro_0.png'
		self.leftData = 'characterImages/electro/electro_0_mirror.png'
			
		self.rData = 'characterImages/electro/electro_1.png' # for right special attacks
		self.lData = 'characterImages/electro/electro_1_mirror.png' # left for special attacks

		self.rSuper0 = 'characterImages/electro/super_col2.png'
		self.lSuper0 = 'characterImages/electro/super_col2_mirror.png'

		self.rSuper1 = 'characterImages/electro/super_col.png'
		self.lSuper1 = 'characterImages/electro/super_col_mirror.png'


		self.specialAttackRect = [(3*80,  1*80, 80, 80),
								  (4*80,  1*80, 80, 80),
								  (5*80,  1*80, 80, 80),
								  (6*80,  1*80, 80, 80),
								  (7*80,  1*80, 80, 80),
								  (8*80,  1*80, 80, 80),
								  (9*80,  1*80, 80, 80),
								  (0*80,  2*80, 80, 80),
								  (1*80,  2*80, 80, 80),
								  (2*80,  2*80, 80, 80),]

		self.lspecialAttackRect = [(6*80, 1*80, 80, 80),
								  (5*80,  1*80, 80, 80),
								  (4*80,  1*80, 80, 80),
								  (3*80,  1*80, 80, 80),
								  (2*80,  1*80, 80, 80),
								  (1*80,  1*80, 80, 80),
								  (0*80,  1*80, 80, 80),
								  (9*80,  2*80, 80, 80),
								  (8*80,  2*80, 80, 80),
								  (7*80,  2*80, 80, 80),]

		self.kickAttackRect = [(4*80, 1*80, 80, 80),
							   (5*80, 1*80, 80, 80),
							   (6*80, 1*80, 80, 80),
							   (7*80, 1*80, 80, 80),]

		self.lkickAttackRect = [(5*80, 1*80, 80, 80),
							   (4*80, 1*80, 80, 80),
							   (3*80, 1*80, 80, 80),
							   (2*80, 1*80, 80, 80),]

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