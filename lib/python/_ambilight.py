import subprocess as sp
import numpy as np
from led import *

from command import generateCommand

TOTAL_PIXEL_COUNT = 100
LED_PIXEL_STRIP_HEIGHT = 1

DATA_SHAPE = (LED_PIXEL_STRIP_HEIGHT,TOTAL_PIXEL_COUNT,3)
BUFF_SIZE = LED_PIXEL_STRIP_HEIGHT*TOTAL_PIXEL_COUNT*3

def main():
	strip = stripInit(100,False)
	command = generateCommand()
	pipe = sp.Popen(command, stderr=sp.PIPE ,stdout=sp.PIPE, bufsize=BUFF_SIZE)

	try:
		while True:
			raw_image = pipe.stdout.read(BUFF_SIZE)
			frame = np.fromstring(raw_image, dtype='uint8').reshape(DATA_SHAPE)

			for i in range(strip.numPixels()):
				pixel = frame[0][i]
				strip.setPixelColor(i,Color(int(pixel[0]),int(pixel[1]),int(pixel[2])))
			strip.show()

			pipe.stdout.flush()

	except KeyboardInterrupt:

		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,0))
		strip.show()

		pipe.stdout.flush()
		# pipe.wait()

		try:
		    sys.stdout.close()
		except:
		    pass
		try:
		    sys.stderr.close()
		except:
		    pass
	else:
		try:
		    sys.stdout.close()
		except:
		    pass
		try:
		    sys.stderr.close()
		except:
		    pass

main()