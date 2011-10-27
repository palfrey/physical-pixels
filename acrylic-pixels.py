from PIL import Image
from sys import argv, exit
from OpenGL.GL import *

def main():
	if argv[-1].find(".png") == -1:
		raise Exception, "need a PNG as the last argument"
	im = Image.open(argv[-1])
	width = im.size[0]
	height = im.size[1]
	print "size", width, height
	all = list(im.getdata())
	pts = [[] for _ in range(width)]
	for x in range(width):
		pts[x] = [() for _ in range(height)]
		for y in range(height):
			pts[x][y] = all[(y*width)+x]

	depth = 20
	rodm = GLMaterial(emission = (1,1,1))
	rodw = 5

	size = 20
	spacing = 5
	largeSize = size+spacing

	for x in range(width):
		for y in range(height):
			if len(pts[x][y]) == 3:
				(r,g,b) = pts[x][y]
				a = 255
			else:
				(r,g,b,a) = pts[x][y]
			if a>0:
				c = (r/255.0,g/255.0,b/255.0)
				b = Box(
						pos = (largeSize*x,0,-largeSize*y),
						lx = size,
						ly = 3,
						lz = size,
						material = GLMaterial (
							ambient = c,
							diffuse = c,
							emission = c
							)
				)

				Box(
						pos = ((largeSize*x), (depth/2), (-largeSize*y)),
						lz = rodw,
						lx = rodw,
						ly = depth,
						material = rodm
				)
	
	totalheight = ((height-1)*largeSize) + size
	totalwidth = ((width-1)*largeSize) + size
	midwidth = (width-1)*(largeSize/2)
	midheight = (height-1)*(largeSize/2)
	print "total", totalwidth, totalheight
	b = Box (
			pos = (midwidth, depth, -midheight),
			lx = totalwidth,
			ly = 3,
			lz = -totalheight,
			material = GLMaterial (
				diffuse = (0,0,0,0.5),
				blend_factors = (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
			)
	)
main()
