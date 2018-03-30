import pygame
from pygame.locals import *
import pyganim

class Heroes():

	health = 100
	power = 0
	
	timerDelay = 0
	punch = 10
	kick = 10
	punch = 20

	punchDamage = 10
	specialDamage = 20
	

	def __init__(self, x, y):
		self.rightData = ''
		self.leftData = ''
		self.x = x
		self.y = y
		self.statusSets = ['stand', 'walk', 'run', 'defense', 
						   'punch', 'kick', 'specialAttack']
		self.currStatus = 'stand'
		self.max = False
		self.super = False
		self.specialPowerDecre = 20

		self.directionSets = ['up', 'down', 'right', 'left']
		self.currDirection = 'right'

		self.walkingDx = 3
		self.runningDx = 6

		self.walkingDy = 3
		self.runningDy = 6

		self.isGetHit = False
		self.winRounds = 0

		self.standRect = [(0, 0, 80, 80),
			 			  (1*80,0, 80, 80),
			 			  (2*80,0, 80, 80),
			 			  (3*80,0, 80, 80)]

		self.lstandRect = [(720, 0, 80, 80),
			 			   (640, 0, 80, 80),
			 			   (560, 0, 80, 80),
			 			   (480, 0, 80, 80)]

		self.walkRect = [(3*80, 0, 80, 80),
			 			 (4*80, 0, 80, 80),
			 			 (5*80, 0, 80, 80),
			 			 (6*80, 0, 80, 80),
			 			 (7*80, 0, 80, 80)]

		self.lwalkRect = [(400, 0, 80, 80),
			 			  (320, 0, 80, 80),
			 			  (240, 0, 80, 80),
			 			  (160, 0, 80, 80)]

		self.runRect = [(0, 2*80, 80, 80),
			 			(1*80,2*80, 80, 80),
			 			(2*80,2*80, 80, 80)]

		self.lrunRect = [(720, 2*80, 80, 80),
			 			 (640, 2*80, 80, 80),
			 			 (560, 2*80, 80, 80)]

		self.punchRect = [(0, 1*80, 80, 80),
			 			  (1*80,1*80, 80, 80),
			 			  (2*80,1*80, 80, 80),
			 			  (3*80,1*80, 80, 80)]

		self.lpunchRect = [(720, 1*80, 80, 80),
			 			   (640,1*80, 80, 80),
			 			   (560,1*80, 80, 80),
			 			   (480,1*80, 80, 80)]

		self.defenseRect = [(6*80,5*80, 80, 80),
			   				(7*80,5*80, 80, 80),]

		self.ldefenseRect = [(240,5*80, 80, 80),
			   				 (160,5*80, 80, 80),]


		self.specialAttackRect = [(3*80, 2*80, 80, 80),
								  (4*80, 2*80, 80, 80),
								  (5*80, 2*80, 80, 80),
								  (6*80, 2*80, 80, 80),
								  (7*80, 2*80, 80, 80),
								  (8*80, 2*80, 80, 80),]

		self.lspecialAttackRect = [(3*80, 2*80, 80, 80),
								  (4*80, 2*80, 80, 80),
								  (5*80, 2*80, 80, 80),
								  (6*80, 2*80, 80, 80),
								  (7*80, 2*80, 80, 80),
								  (8*80, 2*80, 80, 80),]

		self.getHitRect = [(3*80, 5*80, 80, 80),
						   (4*80, 5*80, 80, 80),
						   (5*80, 5*80, 80, 80)]

		self.lgetHitRect = [(6*80, 5*80, 80, 80),
							(5*80, 5*80, 80, 80),
							(4*80, 4*80, 80, 80)]

	def stand(self):
		standImages = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.standRect)
		standFrame = list(zip(standImages, [100] * len(standImages)))
		standAnim = pyganim.PygAnimation(standFrame)
		return standAnim

	def lstand(self):
		standImages = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.lstandRect)
		standFrame = list(zip(standImages, [100] * len(standImages)))
		lstandAnim = pyganim.PygAnimation(standFrame)
		return lstandAnim

	def walk(self):
		walkImages = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.walkRect)
		walkFrame = list(zip(walkImages, [100] * len(walkImages)))
		walkAnim = pyganim.PygAnimation(walkFrame)
		return walkAnim

	def lwalk(self):
		walkImages = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.lwalkRect)
		walkFrame = list(zip(walkImages, [100] * len(walkImages)))
		lwalkAnim = pyganim.PygAnimation(walkFrame)
		return lwalkAnim

	def run(self):
		runImages = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.runRect)
		runFrame = list(zip(runImages, [100] * len(runImages)))
		runAnim = pyganim.PygAnimation(runFrame)
		return runAnim

	def lrun(self):
		runImages = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.lrunRect)
		runFrame = list(zip(runImages, [100] * len(runImages)))
		lrunAnim = pyganim.PygAnimation(runFrame)
		return lrunAnim

	def defense(self):
		defenseImages = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.defenseRect)
		defenseFrame = list(zip(defenseImages, [100] * len(defenseImages)))
		defenseAnim = pyganim.PygAnimation(defenseFrame)
		return defenseAnim

	def ldefense(self):
		defenseImages = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.ldefenseRect)
		defenseFrame = list(zip(defenseImages, [100] * len(defenseImages)))
		ldefenseAnim = pyganim.PygAnimation(defenseFrame)
		return ldefenseAnim

	def punch(self):
		punchImages = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.punchRect)
		punchFrame = list(zip(punchImages, [100] * len(punchImages)))
		punchAnim = pyganim.PygAnimation(punchFrame)
		return punchAnim

	def lpunch(self):
		punchImages = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.lpunchRect)
		punchFrame = list(zip(punchImages, [100] * len(punchImages)))
		lpunchAnim = pyganim.PygAnimation(punchFrame)
		return lpunchAnim


	def getHit(self):
		getHitImages = pyganim.getImagesFromSpriteSheet(self.rightData, rects = self.getHitRect)
		getHitFrame = list(zip(getHitImages, [100] * len(getHitImages)))
		getHitAnim = pyganim.PygAnimation(getHitFrame)
		return getHitAnim

	def lgetHit(self):
		lgetHitImages = pyganim.getImagesFromSpriteSheet(self.leftData, rects = self.lgetHitRect)
		lgetHitFrame = list(zip(lgetHitImages, [100] * len(lgetHitImages)))
		lgetHitAnim = pyganim.PygAnimation(lgetHitFrame)
		return lgetHitAnim









