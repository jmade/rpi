from led import *

def main():
	strip = stripInit(100,False)
	strip.begin()
	try:
		while True:
			runDemoRepeat(strip)
	except KeyboardInterrupt:
		print("Shutting Down.")
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,0))
		strip.show()

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