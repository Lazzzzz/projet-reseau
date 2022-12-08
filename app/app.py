import random
import uuid

import pygame

from logic.simulation import Rect, Circle
from protocol.handler.clientNetworkHandler import ClientNetworkHandler
from protocol.packets.createcirclepacket import CreateCirclePacket
from protocol.packets.createrectpacket import CreateRectPacket
from protocol.packets.sendmousepospacket import MousePosPacket
from register.initPacket import initPackets

pygame.init()


class Shower:
	def __init__(self):
		self.selected = 'rect'
		self.size = 10
		self.mass = 10
		self.surface = pygame.Surface((self.size, self.size))
		self.cooldown = 0
	
	def update(self, network):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.selected = 'rect'
		if keys[pygame.K_c]:
			self.selected = 'circle'
		if keys[pygame.K_UP]:
			self.size += 1
			self.mass += 1
		if keys[pygame.K_DOWN]:
			self.size -= 1
			self.mass -= 1
			self.mass = max(10, self.mass)
			self.size = max(0, self.size)
		
		if self.cooldown == 0:
			if keys[pygame.K_s]:
				if self.selected == 'rect':
					mouse_pos = pygame.mouse.get_pos()
					rect = Rect(mouse_pos[0], mouse_pos[1], self.size, self.size, self.mass)
					packet = CreateRectPacket(rect)
					network.sendPacket(packet)
				
				if self.selected == 'circle':
					mouse_pos = pygame.mouse.get_pos()
					circle = Circle(mouse_pos[0], mouse_pos[1], self.size // 2, self.mass)
					packet = CreateCirclePacket(circle)
					network.sendPacket(packet)
				
				self.cooldown = 10
		else:
			self.cooldown -= 1
	
	def render(self, screen):
		self.surface = pygame.Surface((self.size, self.size))
		self.surface.fill((0, 0, 0))
		self.surface.set_colorkey((0, 0, 0))
		self.surface.set_alpha(100)
		
		if self.selected == 'rect':
			pygame.draw.rect(self.surface, (0, 0, 255), pygame.Rect(0, 0, self.size, self.size))
			pos = pygame.mouse.get_pos()[0] - self.size // 2, pygame.mouse.get_pos()[1] - self.size // 2
		if self.selected == 'circle':
			pygame.draw.circle(self.surface, (0, 255, 0), (self.size // 2, self.size // 2), self.size // 2)
			pos = pygame.mouse.get_pos()[0] - self.size // 2, pygame.mouse.get_pos()[
				1] - self.size // 2
		
		screen.blit(self.surface, pos)


class App:
	def __init__(self, ip='localhost', port=5000):
		initPackets()
		self.size = 640, 640
		self.screen = pygame.display.set_mode(self.size)
		
		self.networkConnector = ClientNetworkHandler(ip, port, uuid.uuid4(), self)
		self.shower = Shower()
		
		self.objects = {
			'rect': {},
			'circle': {}
		}
		
		self.mouse_pos = {}
		self.colors = {}
		self.clock = pygame.time.Clock()
	
	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			
			mouse_pos = MousePosPacket(pygame.mouse.get_pos(), self.networkConnector.uuid)
			self.networkConnector.sendPacket(mouse_pos)
			
			self.shower.update(self.networkConnector)
			self.networkConnector.update()
			
			self.screen.fill((170, 120, 170))
			
			for rect_uuid in self.objects['rect']:
				pygame.draw.rect(self.screen, (0, 0, 255), self.objects['rect'][rect_uuid].rect)
			
			for circle_uuid in self.objects['circle']:
				radius = self.objects['circle'][circle_uuid].radius
				posX = self.objects['circle'][circle_uuid].pos[0] + radius // 2
				posY = self.objects['circle'][circle_uuid].pos[1] + radius // 2
				
				pygame.draw.circle(self.screen, (0, 255, 0), (posX, posY), radius)
			
			self.shower.render(self.screen)
			for mouse_uuid in self.mouse_pos:
				if mouse_uuid != self.networkConnector.uuid:
					if mouse_uuid in self.colors:
						color = self.colors[mouse_uuid]
					else:
						color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
						self.colors[mouse_uuid] = color
					
					pygame.draw.circle(self.screen, color, self.mouse_pos[mouse_uuid], 4)
			
			pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((0, 0), self.size), 6)
			
			self.clock.tick(60)
			pygame.display.flip()
		
		pygame.quit()
		self.networkConnector.cl
