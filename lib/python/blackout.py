from led import *

def main():
	strip = stripInit(100,False)
	for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,0))
	strip.show()

main()