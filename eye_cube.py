from pyprocessing import *
from random import randrange

SIZE = (800, 400)

def setup():
	size(*SIZE)

ANGLE = 0.0
eyeBall = 800
retina = 420
sretina = 200
eyeColor = 200

def draw():
	global ANGLE
	background(255, 255, 255)

	# Translate coordinates to center
	translate(SIZE[0]/2, SIZE[1]/2, 0)

	# Draw eyeball
	fill(250)
	ellipse(0, 0, eyeBall, eyeBall)

	hint(DISABLE_DEPTH_TEST)

	# Look
	lmax = 40
	tx = map(mouse.x, 0, SIZE[0], -lmax, lmax)
	ty = map(mouse.y, 0, SIZE[1], -lmax, lmax)
	translate(tx, ty)

	fill(eyeColor)
	ellipse(0, 0, retina, retina)
	fill(0)
	ellipse(0, 0, sretina, sretina)

	pushMatrix()
	rotateX(-0.3)
	rotateY(ANGLE)
	ANGLE += 0.05
	fill(randrange(255), randrange(255), randrange(255), randrange(255))
	box(80)
	popMatrix()

	rsize = 100
	#fill(eyeColor)
	for i in range(12):
		fill(i*(255/12))
		pushMatrix()
		rotateZ(i*PI/6 - ANGLE/10)
		translate(100, 0, 0)
		rect(0, -rsize/2, rsize, rsize)
		popMatrix()

run()