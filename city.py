from __future__ import division, print_function
from nodebox.graphics import *
from random import randint, getrandbits, uniform
from collections import deque

SIZE = (1280, 800)
LAYERS = 20
STARS_COLOR = Color(189, 155, 0, 255, base=255)
WINDOWS_COLOR = Color(189, 155, 0, 255, base=255)

NAMES = deque(("Google", "Microsoft", "Facebook", "Apple", "IBM",
    "Dropbox", "Samsung", "Sony", "HTC", "Nokia", "Toyota", "Honda",
    "Yamaha", "Suzuki", "Kawasaki", "Nissan", "GE", "Motorolla", "Siemens"))

# TODO: signs pallete, side-logos, different rooftops, projectors, blocky buildings

class Antena(object):
    def __init__(self, rx, ry, bw, bh):
        ah = randint(2, 2+int(bh//8))
        self.line = (rx, ry, rx, ry+ah)
        self.width = 3

    def draw(self):
        stroke(1.0, 0.2)
        strokewidth(3)
        line(*self.line)

        stroke(0.2, 1)
        strokewidth(2)
        line(*self.line)
        strokewidth(1)

class Sign(object):
    def __init__(self, x, y, w):
        name = NAMES.popleft()
        NAMES.append(name)
        self.txt = Text(name, x, y)
        self.txt.fill = Color(uniform(0, 1), uniform(0, 1), uniform(0, 1), 0.9)
        self.txt.fontsize = w*0.15
        self.txt.fontweight = BOLD

    def draw(self):
        self.txt.draw()

def one_of(n):
    return randint(1, n) == n

class Building(object):
    def __init__(self, x, y, w, h, z):
        self.rect = (x, y, w, h)
        self.ws = int(z*10)
        self.darken = (1-z)*0.5
        self.strokewidth = z

        self.objects = []
        nantenas = randint(0, min(4, int(w)))
        ox = x+w/2
        for i in xrange(nantenas):
            o = Antena(ox, y+h, w, h)
            self.objects.append(o)
            ox += o.width

        if getrandbits(1) and h > 300:
            self.objects.append(Sign(x, y+h, w))

    def draw_windows(self):
        x, y, w, h = self.rect
        ws = self.ws
        if ws == 0:
            return
        strokewidth(ws*0.45)
        color = darker(WINDOWS_COLOR, step=self.darken)
        off = ws+randint(0, 1)
        for wy in xrange(off, int(h-ws), ws):
            stroke(color)
            line(2+x, y+wy, x+w-2, y+wy)
            stroke(darker(color, step=0.4))
            # Dimmed windows
            for wx in xrange(off, int(w-ws), ws):
                nx = 2+x+wx
                if one_of(5):
                    line(nx, y+wy, nx+ws, y+wy)
        strokewidth(1)

    def draw(self):
        stroke(0)
        strokewidth(self.strokewidth)
        fill(darker(Color(0.3), step=self.darken))
        rect(*self.rect)

        # Objects on roof
        for o in self.objects:
            o.draw()

        # Windows
        self.draw_windows()

def make_layer(z):
    x = (1-z)*SIZE[0]/2
    y = (1-z)
    count = 15
    hc = count/2.0
    height_dist = 1+(1-z)*8
    for i in xrange(count):
        center_dist = 1-abs((i-hc)/hc)*(1-z)
        w = randint(50, 100)*z
        h = randint(100, 250)*center_dist*height_dist*z
        yield Building(x, y, w, h, z)
        x += w+w*0.35

def make_scene():
    for n in xrange(LAYERS):
        z = (n+1)/LAYERS
        rects = list(make_layer(z))
        yield rects

scene = list(make_scene())

def render_city():
    for i, s in enumerate(scene):
        for r in s:
            r.draw()

def render_stars():
    nostroke()
    for i in xrange(100):
        fill(STARS_COLOR, alpha=uniform(0.1, 0.9))
        x = randint(0, SIZE[0])
        y = randint(0, SIZE[1])
        rect(x, y, 1, 1)


stars = render(render_stars, SIZE[0], SIZE[1])
img = render(render_city, SIZE[0], SIZE[1])
shadow1 = dropshadow(img, amount=100, alpha=0.01)
shadow2 = dropshadow(img, amount=10)
shadow1.color.rgb = (0.3, 0.3, 0.3)
shadow2.color.rgb = (1, 1, 1)

def draw(canvas):
    canvas.clear()
    background(0.1)
    stars.draw()
    shadow1.draw(y=70)
    shadow2.draw()
    img.draw()

canvas.size = SIZE
canvas.name = "City"
canvas.run(draw)
