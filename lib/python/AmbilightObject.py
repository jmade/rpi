import subprocess as sp
import numpy as np
# 
from led import *
from command import generateCommand


class AmbilightObject:

	def __init__(self,pixel_count=100):
		self.strip = stripInit(led_count=pixel_count,visuals=True)
		self.run = True
		self.name = 'ambi_obj'
		self.totalPixelCount = pixel_count
		self.data_shape = (1,pixel_count,3)
		self.buff_size = 1*pixel_count*3
		self.command = generateCommand()

	def describe(self):
		description = ''.join([
			'Name: ',self.name,
			'Pixel Count: ',str(self.totalPixelCount),
			'Run Value: ',str(self.run)
			])
		print(description)
		return description

	def stopAmbilight(self):
		self.run = False

	def startAmbilight(self):
		self.run_ambilight()

	# Help functions
	def colorize_frame(frame):
		for i in range(self.totalPixelCount):
			pixel = frame[0][i]
			self.strip.setPixelColor(i,Color(int(pixel[0]),int(pixel[1]),int(pixel[2])))
		self.strip.show()

	def turnStripOff(self):
		colorWipe(self.strip, Color(0, 0, 0),25)


	# Amilight Loop
	def run_ambilight(self):
		pipe = sp.Popen(self.command, stderr=sp.PIPE ,stdout=sp.PIPE, bufsize=self.buff_size)
		while self.run:
			raw_image = pipe.stdout.read(self.buff_size)
			# TODO:
			# handle 
			# ValueError: cannot reshape array of size 0 into shape (1,100,3)
			frame = np.fromstring(raw_image, dtype='uint8').reshape(self.data_shape)
			# 
			for i in range(self.totalPixelCount):
				pixel = frame[0][i]
				self.strip.setPixelColor(i,Color(int(pixel[0]),int(pixel[1]),int(pixel[2])))
			self.strip.show()
			# 
			pipe.stdout.flush()

		# turnStripOff()
