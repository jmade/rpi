import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 34      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

def ambilightStripInit():
	return stripInit(led_count=100,visuals=False)

def largeStripInit(visuals=True):
	# Create NeoPixel object with appropriate configuration.
	led_count = 150
	strip = Adafruit_NeoPixel(led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	if visuals:
		colorWipe(strip,Color(255,255,255),10)
		colorWipe(strip,Color(0,0,0),25)	
	print("Large Strip 150 Intialized!")
	return strip


def megaTinyStripInit(visuals=True):
	# Create NeoPixel object with appropriate configuration.
	led_count = 144
	strip = Adafruit_NeoPixel(led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	if visuals:
		colorWipe(strip,Color(255,255,255),10)
		colorWipe(strip,Color(0,0,0),25)	
	print("MegaTiny 144 Strip Intialized!")
	return strip

def matrixInit(visuals=True):
	# Create NeoPixel object with appropriate configuration.
	led_count = 16
	strip = Adafruit_NeoPixel(led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	if visuals:
		colorWipe(strip,Color(255,255,255),50)
		colorWipe(strip,Color(0,0,0),25)	
	print("Matrix 16 Strip Intialized!")
	return strip

def ringInit(led_count=12,visuals=True):
		# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	print("Ring 12 Strip Intialized!")
	if visuals:
		colorWipe(strip,Color(255,255,255),50)
		colorWipe(strip,Color(0,0,0),25)
	return strip

def stripInit(led_count=1,visuals=True):
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	print('NeoPixel Strip Intialized with '+str(led_count)+' NeoPixels!')
	if visuals:
		colorWipe(strip,Color(255,255,255),25)
		colorWipe(strip,Color(0,0,0),25)
	return strip



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)


# Demos
def runDemo(strip,count=0):
	if count == 0:
		runDemoRepeat(strip)
	else:
		for i in range(count):
			print("Running Demo ["+str(i)+"]")
			runDemoOnce(strip)

def runDemoOnce(strip):
	print ('Color wipe animations.')
	colorWipe(strip, Color(255, 0, 0),25)  # Red wipe
	colorWipe(strip, Color(0, 255, 0),15)  # Blue wipe
	colorWipe(strip, Color(0, 0, 255),10)  # Green wipe
	print ('Theater chase animations.')
	theaterChase(strip, Color(127, 127, 127))  # White theater chase
	theaterChase(strip, Color(127,   0,   0))  # Red theater chase
	theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
	print ('Rainbow animations.')
	rainbow(strip)
	rainbowCycle(strip)
	theaterChaseRainbow(strip)

def runDemoRepeat(strip):
	while True:
		print ('Color wipe animations.')
		colorWipe(strip, Color(255, 0, 0),25)  # Red wipe
		colorWipe(strip, Color(0, 255, 0),15)  # Blue wipe
		colorWipe(strip, Color(0, 0, 255),10)  # Green wipe
		print ('Theater chase animations.')
		theaterChase(strip, Color(127, 127, 127))  # White theater chase
		theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		print ('Rainbow animations.')
		rainbow(strip)
		rainbowCycle(strip)
		theaterChaseRainbow(strip)


# Custom base functions
def convertToColorArray(arr):
	converted = []
	for item in arr:
		color = Color(int(item[0]),int(item[1]),int(item[2]))
		converted.append(color)
	return converted
