class Laser:
	def __init__(self):
		self.color = color

	def __str__(self):
		return "Laser(" + str(color) + ")"

	def collideswith(self, obj):
		return True

class AlienLaser(Laser):
	def __init__(self, color):
		super().__init__(color)
	def __str__(self):
		return "AlienLaser(" + super().__str(self) + ")"
	def collideswith(self, obj):
		return type(obj).__name__ != "Alien"

class ShipLaser(Laser):
	def __init__(self, color):
		super().__init__(color)

	def __str__(self):
		return "ShipLaser(" + super().__str__(self) + ")"


class Alien
	def __init__(self, ...):
		self.last = pygame.time.get_ticks()
		self.often = random.randint(...)

	def fire_laser(...):
		now = self.time.get_ticks()
		if now - last > randomnum:
			self.fire_last(..)
			self.last = now
