from time import sleep
import RPi.GPIO as GPIO

LOG = True
FILE_LOC = '/home/pi/volume.txt'

# Pins
DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
BLUE_WIRE = 13 # Microstepping
GREEN_WIRE = 19 # Microstepping
WHITE_WIRE = 26 # Microstepping
SLEEP = 16 #sleep/wakeup

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200  # Steps per Revolution (360 / 1.8)

# Microstep Resolution GPIO Pins
MODE = (BLUE_WIRE,GREEN_WIRE,WHITE_WIRE)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

step_count = SPR * 32
delay = .0208 / 32

ROATION_SCALE = 2.0

# Power
def wakeup():
  if LOG: print("~Good Morning!~")
  GPIO.output(SLEEP, GPIO.HIGH)

def goToSleep():
  if LOG: print("~Good Night!~")
  GPIO.output(SLEEP, GPIO.LOW)


# Direction
def setDirectionClockwise():
  if LOG: print("Direction Set to Clockwise |-> ")
  GPIO.output(DIR, CW)

def setDirectionCounterClockwise():
  if LOG: print("Direction Set to Clockwise <-|")
  GPIO.output(DIR, CCW)


# Main Operations
def setup():
  if LOG: print("GPIO SETUP")
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(DIR, GPIO.OUT)
  GPIO.setup(STEP, GPIO.OUT)
  GPIO.setup(MODE, GPIO.OUT)
  GPIO.setup(SLEEP, GPIO.OUT)
  GPIO.output(MODE, RESOLUTION['1/32'])

def cleanup():
  if LOG: print("GPIO Cleanup")
  goToSleep()
  GPIO.cleanup()

def spin(steps):
  wakeup()
  if LOG: print("Spinning: "+str(steps))
  for x in range(int(steps)):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

def rotate(clockwise=True,rotations=1.0):
  if clockwise:
    setDirectionClockwise()
  else:
    setDirectionCounterClockwise()
  rotationAmount = float(rotations) * step_count
  steps = int(rotationAmount)
  if LOG:
    print("Steps: "+str(steps))
  spin(steps)


# Volume Persistance
def calibrate():
  try:
    with open(FILE_LOC, 'w+') as f:
      f.write("0")
      rotate(clockwise=False,rotations=2.0)
      print("Calibration Complete.")
  except IOError as e:
    print("CALIBRATION FAILED")
    print("Couldn't open or write to file (%s)." % e)

def readVolume():
  try:
    with open(FILE_LOC) as f:
      first = f.readline()
      if LOG: print("Volume Read: "+str(int(first)))
      return int(first)
  except IOError as e:
    print("Couldn't Read Volume at (%s)." % e)
    print("Starting Calibration")
    calibrate()
    return 0

def saveVolume(level):
  try:
    with open(FILE_LOC, 'w+') as f:
      f.write(str(level))
      if LOG: print("Saved Volume: "+str(level))
  except IOError as e:
    print("ERROR Saving Volume")
    print("Couldn't open or write to file (%s)." % e)

# Volume Functions

def setVolume(volume):
  currentVol = readVolume()
  if currentVol < volume:
    turnUpAmout = volume - currentVol
    setVolumeTo(turnUpAmout,True)
  else: # we need to turn down
    turnDownAmount = currentVol - volume
    setVolumeTo(turnDownAmount,False)

def setVolumeTo(amt,isClockWise):
  print("Setting Volume to Level: "+str(amt))
  print("Direction "+str(isClockWise))

  if amt == 0:
    return
  rotAmt = (float(amt) * 0.01)
  percentage = (ROATION_SCALE * rotAmt)
  if LOG: print("Setting Volume to: "+str(percentage))
  rotate(clockwise=isClockWise,rotations=percentage)
  saveVolume(amt)

def setVolumeMax():
  rotate(clockwise=True,rotations=2.0)
  saveVolume(100)

def setVolumeMin():
  rotate(clockwise=False,rotations=2.0)
  saveVolume(0)




# app interface
def volumeUp():
  setup()
  rotate(clockwise=True,rotations=0.2)
  cleanup()

def volumeDown():
  setup()
  rotate(clockwise=False,rotations=0.2)
  cleanup()

def volumeDownMax():
  setup()
  rotate(clockwise=False,rotations=2.0)
  cleanup()

def volumeUpTriple():
  setup()
  rotate(clockwise=True,rotations=0.6)
  cleanup()

def volumeDownTriple():
  setup()
  rotate(clockwise=False,rotations=0.6)
  cleanup()


# need to find a way to check volume level?
# maybe store it in a text file and look it up to retrieve it?

def raiseVolume():
  volume = readVolume() # Get Volume
  volume += 10 # Raise Volume
  # Volme checks
  if volume > 90: volume = 100
  if volume < 10: volume = 10
  setVolume(volume)

def lowerVolume():
  volume = readVolume() # Get Volume
  volume -= 10 # lower Volume
  # Volme checks
  if volume > 90: volume = 90
  if volume < 10: volume = 0
  setVolume(volume)

# main funcs

def pause():
  sleep(1.5)

def backAndForth(rot=1.0):
  rotate(clockwise=True,rotations=rot)
  pause()
  rotate(clockwise=False,rotations=rot)
