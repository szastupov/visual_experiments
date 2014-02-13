from nodebox.graphics import *
from math import sin, pi

class Vis(object):
    def __init__(self):
        self.t = 0
        self.s = 8
        self.color = Color(77, 77, 255, 200, base=255)

    def draw(self, canvas):
        elapsed = canvas.elapsed
        self.w = canvas.width
        self.h = canvas.height

        if "r" in canvas.keys:
            self.t = 0
            self.s = 8

        self.t += elapsed*0.003
        if self.s > 1:
            speed = 0.9
            ns = self.s-elapsed*speed
            self.s = max(ns, 1)

        translate(self.w/2, self.h/2)
        s = round(self.s, 4)
        scale(s, s)
        n = 10
        for i in xrange(1, n):
            self.draw_shape(float(i)/n)

    def draw_shape(self, scale):
        n = 60
        s = 800*scale
        points = []

        nostroke()
        fill(self.color)
        for i in xrange(n):
            t = self.t+(2*pi*i/(n-1))
            x = cos(t)
            y = sin(t)#*cos(t)
            points.append((x*s, y*s))

        stroke(self.color)
        lp = points[0]
        for p in points[1:]:
            x1, y1 = lp
            x2, y2 = p
            lp = p
            m = (y2-y1)/(x2-x1)
            x1p = self.w/2
            y1p = m*(x1p-x1)-y1
            x2p = -self.w/2
            y2p = m*(x2p-x2)-y2
            line(x1, y1, x2, y2)
            line(x1p, y1p, x2p, y2p)

vis = Vis()

def draw(canvas):
    canvas.clear()
    background(0)
    def draw_scene():
        vis.draw(canvas)

    img = render(draw_scene, canvas.width, canvas.height)
    blur(img, kernel=2).draw()

SIZE = (1280, 768)
canvas.size = SIZE
canvas.name = "connected"
canvas.run(draw)