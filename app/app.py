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
		self.cooldown = 200
	
	def update(self, network):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.selected = 'rect'
		if keys[pygame.K_c]:
			self.selected = 'circle'
		
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
				
				self.cooldown = 20
		else:
			self.cooldown -= 1
	
	def render(self, screen):
		self.surface = pygame.Surface((self.size, self.size))
		self.surface.fill((0, 0, 0))
		self.surface.set_colorkey((0, 0, 0))
		self.surface.set_alpha(100)
		
		if self.selected == 'rect':
			pygame.draw.rect(self.surface, (0, 0, 255), pygame.Rect(0, 0, self.size, self.size))
		if self.selected == 'circle':
			pygame.draw.circle(self.surface, (0, 255, 0), (self.size // 2, self.size // 2), self.size // 2)
		
		screen.blit(self.surface, pygame.mouse.get_pos())


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
			
			self.screen.fill((120, 120, 120))
			
			for rect_uuid in self.objects['rect']:
				pygame.draw.rect(self.screen, (0, 0, 255), self.objects['rect'][rect_uuid].rect)
			
			for circle_uuid in self.objects['circle']:
				pygame.draw.circle(self.screen, (0, 255, 0), self.objects['circle'][circle_uuid].pos,
				                   self.objects['circle'][circle_uuid].radius)
			
			self.shower.render(self.screen)
			for mouse_uuid in self.mouse_pos:
				if mouse_uuid != self.networkConnector.uuid:
					pygame.draw.circle(self.screen, (255, 0, 0), self.mouse_pos[mouse_uuid], 2)
			
			pygame.display.flip()
		
		pygame.quit()
