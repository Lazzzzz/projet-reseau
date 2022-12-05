import pymunk as pymunk


class SimulationSpace:
	def __init__(self):
		space = pymunk.Space()  # Create a Space which contain the simulation
		space.gravity = 0, -981  # Set its gravity
		
		body = pymunk.Body()  # Create a Body
		body.position = 50, 100  # Set the position of the body
		
		poly = pymunk.Poly.create_box(body)  # Create a box shape and attach to body
		poly.mass = 10  # Set the mass on the shape
		space.add(body, poly)  # Add both body and shape to the simulation
		
		while True:  # Infinite loop simulation
			space.step(0.02)  # Step the simulation one step forward
