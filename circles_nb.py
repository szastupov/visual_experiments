from nodebox.graphics import *
from random import randint, choice, uniform

SIZE = (1024, 768)

class Circle(object):
	def __init__(self):
		self.x = randint(0, SIZE[0])
		self.y = randint(0, SIZE[1])
		self.color = [255, 204, 34, randint(20, 150)]
		self.d = randint(70, 160)
		self.r = self.d/2
		self.speed = randint(1, 20)
		self.dirx = choice((-1, 1))
		self.diry = choice((-1, 1))

	def draw(self, dt):
		if self.x < 0:
			self.dirx = 1
		elif self.x > SIZE[0]:
			self.dirx = -1

		if self.y < 0:
			self.diry = 1
		elif self.y > SIZE[1]:
			self.diry = -1

		self.x += self.dirx * self.speed * dt
		self.y += self.diry * self.speed * dt
		fill(*self.color, base=255)
		ellipse(self.x, self.y, self.d, self.d)

class Title(object):
	def __init__(self):
		self.txt = Text("summer", SIZE[0]/2, SIZE[1]/2)
		self.txt.fontsize = 64
		self.txt.fill = Color(255, 255, 204, 200, base=255)

	def draw(self, dt):
		self.txt.draw()


objects = [Circle() for i in range(150)]
objects.insert(len(objects)/2, Title())

def draw(canvas):
	canvas.clear()
	def draw_scene():
		background(238, 170, 0, 255, base=255)
		nostroke()
		for c in objects:
			c.draw(canvas.elapsed)
	img = render(draw_scene, SIZE[0], SIZE[1])
	blur(img).draw()

canvas.fps = 30
canvas.size = SIZE
canvas.run(draw)