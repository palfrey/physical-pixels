from PIL import Image
from sys import argv, exit
from OpenGL.GL import *
from cgkit.cmds import load
from cgkit.all import *
from viewer import Viewer

class PixelsViewer(Viewer):
	def setOptions(self, optparser):
		Viewer.setOptions(self, optparser)
		optparser.add_option("--rod-length", help = "Length of spacing rods", dest="depth", default = 20, type = "float")
		optparser.add_option("--rod-width", help = "Width of spacing rods", dest="rodw", default = 5, type = "float")
		optparser.add_option("--pixel-size", help = "Size of individual display pixels", dest="size", default = 20, type = "float")
		optparser.add_option("--pixel-spacing", help = "Gap between pixels", dest="spacing", default = 5, type = "float")

	# run
	def run(self):
		"""Run the tool.

		This method calls the init() and action() method.
		"""

		# Custom initialization
		self.init()

		# No input file given? Then print the help page and exit
		if len(self.args)==0:
			self.optparser.print_help()
			return
		
		self.drawImage(self.args[0])

		# Load plugins
		#self.loadPlugins()

		# Convert global settings into command line options
		self.setOptionsFromGlobals()

		self.cam = self.getCamera()

		self.action()

		getScene().clear()

	def drawImage(self,name):
		im = Image.open(name)
		width = im.size[0]
		height = im.size[1]
		print "image dimensions = %d x %d " % (width, height)
		all = list(im.getdata())
		pts = [[] for _ in range(width)]
		for x in range(width):
			pts[x] = [() for _ in range(height)]
			for y in range(height):
				pts[x][y] = all[(y*width)+x]

		depth = self.options.depth
		rodw = self.options.rodw
		size = self.options.size
		spacing = self.options.spacing

		rodm = GLMaterial(emission = (1,1,1))
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
		print "backplate size %.2fmm x %.2fmm" %(totalwidth, totalheight)
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

if __name__ == "__main__":
	pv = PixelsViewer()
	pv.run()
