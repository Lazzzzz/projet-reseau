import uuid

import pygame
import pymunk as pymunk


class Shape:
	def __init__(self, x, y, m):
		self.body = pymunk.Body(mass=m, moment=10)
		self.body.position = (x, y)
		self.shape = None
		self.uuid = uuid.uuid4()
	
	def add_to_zone(self, space):
		space.add(self.body)
		space.add(self.shape)


class Rect(Shape):
	def __init__(self, x, y, w, h, m):
		super().__init__(x, y, m)
		self.rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
		self.shape = pymunk.Poly.create_box(body=self.body, size=(w, h))
		self.shape.elasticity = 1


class Circle(Shape):
	def __init__(self, x, y, r, m):
		super().__init__(x, y, m)
		self.pos = (x - r // 2, y - r // 2)
		self.radius = r
		self.shape = pymunk.Circle(self.body, radius=self.radius)
		self.shape.elasticity = 1


class SimulationSpace:
	def __init__(self, size):
		self.size = size
		self.space = pymunk.Space()
		self.space.gravity = 0, 900
		
		segment1 = pymunk.Segment(self.space.static_body, (0, self.size[1]), (self.size[0], self.size[1]), 10)
		segment1.elasticity = 1
		
		segment2 = pymunk.Segment(self.space.static_body, (0, 0), (0, self.size[1]), 10)
		segment2.elasticity = 1
		
		segment3 = pymunk.Segment(self.space.static_body, (self.size[0], 0), self.size, 10)
		segment3.elasticity = 1
		
		segment4 = pymunk.Segment(self.space.static_body, (0, 0), (self.size[0], 0), 10)
		segment4.elasticity = 1
		
		self.space.add(segment1, segment2, segment3, segment4)
		
		self.shapes = {
			'rect': {},
			'circle': {}
		}
		
		self.mouse = {}
	
	def add_shape(self, shape):
		shape.add_to_zone(self.space)
		if isinstance(shape, Rect):
			self.shapes['rect'][shape.uuid] = shape
		if isinstance(shape, Circle):
			self.shapes['circle'][shape.uuid] = shape
	
	def update(self, dt):
		self.space.step(dt)
