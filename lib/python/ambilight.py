#!/usr/bin/env python3

import subprocess as sp
import numpy as np
from PIL import Image
from led import *

# 
LED_TOP_COUNT = 32
LED_LEFT_COUNT = 18
LED_RIGHT_COUNT = 18
LED_BOTTOM_LEFT = 16
LED_BOTTOM_RIGHT = 16
# 
LED_BOTTOM_COUNT = LED_BOTTOM_LEFT + LED_BOTTOM_RIGHT
TOTAL_PIXEL_COUNT = LED_TOP_COUNT + LED_LEFT_COUNT + LED_RIGHT_COUNT + LED_BOTTOM_COUNT
# 
LED_PIXEL_STRIP_HEIGHT = 1

DATA_SHAPE = (LED_PIXEL_STRIP_HEIGHT,TOTAL_PIXEL_COUNT,3)
BUFF_SIZE = LED_PIXEL_STRIP_HEIGHT*TOTAL_PIXEL_COUNT*3

BLUE = Color(0,0,255)
GREEN = Color(0,255,0)
RED = Color(255,0,0)
WHITE = Color(255,255,255)
BLACK = Color(0,0,0)

# 
COMMAND = ""
STRIP = None
RUN = True

# Ratio
def findHeight(width,rat1=16.0,rat2=9.0):
	ratio = width / rat1
	calculated_height = ratio * rat2
	return int(calculated_height)

# Image Functions
def analyseImage(arr):
	pixelateImage(Image.fromarray(arr.astype('uint8')))
	return

def pixelateImage(image,image_name='pixelate'):
	backgroundColor = (0,)*3
	pixelSize = 32 #9
	image = image.resize((image.size[0]/pixelSize, image.size[1]/pixelSize), Image.NEAREST)
	image = image.resize((image.size[0]*pixelSize, image.size[1]*pixelSize), Image.NEAREST)
	pixel = image.load()
	for i in range(0,image.size[0],pixelSize):
		for j in range(0,image.size[1],pixelSize):
			for r in range(pixelSize):
				pixel[i+r,j] = backgroundColor
				pixel[i,j+r] = backgroundColor
	image.save(image_name + '.jpeg')

def saveImage(img,name='default_image'):
	Image.fromarray(img.astype('uint8')).save(name + '.jpeg')


# def colorizeTopRow(top_row,strip):
# 	pixel_index = 0
# 	for i in range(34,68):
# 		pixel = top_row[0][i]
# 		color = Color(pixel[0],pixel[1],pixel[2])
# 		strip.setPixelColor(pixel_index,color)
# 		pixel_index += 1
# 	strip.show()


#  Auto Crop / Cropping 
def parseSize(crop_cmd):
	chopped = crop_cmd[len('chop='):len(crop_cmd)]
	numbers = chopped.split(':')
	return (numbers[0],numbers[1])

# add in scaling to this function too 
def getCropValue():
	limit=24
	rnd=16
	reset=0
	crop_cmd = 'cropdetect=' + str(limit) + ':' + str(rnd) + ':' + str(reset)
	print('crop_cmd:\n',crop_cmd)
	p = sp.Popen(["ffmpeg",
		'-i', '/dev/video0',
		'-t', '1',
		'-vf', crop_cmd,
		'-f', 'null',
		'awk \'/crop/ { print $NF }\'',
		], stdout=sp.PIPE, stderr=sp.PIPE)
	err, out = p.communicate()
	if(err) : print('error',err); return None;
	crops = getCropValues(out.split())
	return crops[0]

def getCropValues(output):
	crop_values = []
	for i in range(len(output)):
		if "crop=" in output[i]:
			crop_values.append(output[i])
	# maybe further analyse here? average all the values in the arrays?
	return crop_values

def getBlackBarCropValue():
	# crop_detect = getCropValue()
	# cropped_size = parseSize(crop_detect)
	# print('crop_detect:\n',crop_detect)
	# print('Cropped_size:',cropped_size)

	inset = 4
	cropped_inset = (688-inset,448-inset,22+inset,30+inset)
	return cropped_inset

def strip_init():
	# Create NeoPixel object with appropriate configuration.
	strip = stripInit(TOTAL_PIXEL_COUNT,True)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	return strip
	

def computeFilterGraph():
	print("Computing Filter Graph...")
	blk_bar_crop_value = getBlackBarCropValue()
	w_in = blk_bar_crop_value[0]
	h_in = blk_bar_crop_value[1]

	# Number of LEDs for the setup.
	ratio_height = findHeight(32,16,9) #18

	# How large the boxes around the edges are
	frame_width = 16
	crop_width = frame_width
	crop_height = frame_width

	flip_left = ',transpose=2' #Rotate 90 degrees counterclockwise.
	flip_right = ',transpose=1' #Rotate 90 degrees clockwise.

	# Scale Filters
	left_scale = ',scale='+str(LED_LEFT_COUNT)+':'+str(LED_PIXEL_STRIP_HEIGHT)
	right_scale = ',scale='+str(LED_RIGHT_COUNT)+':'+str(LED_PIXEL_STRIP_HEIGHT)
	top_scale = ',scale='+str(LED_TOP_COUNT)+':'+str(LED_PIXEL_STRIP_HEIGHT)
	bottom_scale = ',scale='+str(LED_BOTTOM_COUNT)+':'+str(LED_PIXEL_STRIP_HEIGHT)

	# Crop Filters
	left_crop_cmd = ''.join([
		'crop',
		'=w=',str(crop_width),
		':h=',str(h_in),
		':x=',str(0),
		':y=',str(0),
		flip_right,
		left_scale
		])

	right_crop_cmd = ''.join([
		'crop',
		'=w=',str(crop_width),
		':h=',str(h_in),
		':x=',str(w_in-crop_width),
		':y=',str(0),
		flip_left,
		right_scale
		])

	top_crop_cmd = ''.join([
		'crop',
		'=w=',str(w_in),
		':h=',str(crop_height),
		':x=',str(0),
		':y=',str(0),
		top_scale
		])

	bottom_crop_cmd = ''.join([
		'crop',
		'=w=',str(w_in),
		':h=',str(crop_height),
		':x=',str(0),
		':y=',str(h_in-crop_height),
		bottom_scale
		])

	left_bottom_crop_cmd = ''.join([
		'crop',
		'=w=',str(LED_BOTTOM_LEFT),
		':h=',str(LED_PIXEL_STRIP_HEIGHT),
		':x=',str(0),
		':y=',str(0),
		',hflip'
		])

	right_bottom_crop_cmd = ''.join([
		'crop',
		'=w=',str(LED_BOTTOM_RIGHT),
		':h=',str(LED_PIXEL_STRIP_HEIGHT),
		':x=',str(LED_BOTTOM_LEFT),
		':y=',str(0),
		',hflip'
		])

	black_bar_crop_cmd = ''.join([
		'crop',
		'=w=',str(getBlackBarCropValue()[0]),
		':h=',str(getBlackBarCropValue()[1]),
		':x=',str(getBlackBarCropValue()[2]),
		':y=',str(getBlackBarCropValue()[3]),
		])

	# Filter Graph Steps  
	splits_to_crops_cmd = ''.join([
		''.join(['[split_1]',top_crop_cmd,'[top_crop_out];']),
		''.join(['[split_2]',left_crop_cmd,'[left_crop_out];']),
		''.join(['[split_3]',right_crop_cmd,'[right_crop_out];']),
		''.join(['[split_4]',bottom_crop_cmd,'[bottom_crop_out];'])
		])

	bottom_chop_cmd = ''.join([
		'[bottom_crop_out]split[left_bottom][right_bottom];',
		''.join(['[left_bottom]',left_bottom_crop_cmd,'[left_bottom_crop_out];']),
		''.join(['[right_bottom]',right_bottom_crop_cmd,'[right_bottom_crop_out];']),
		])

	h_stack_cmd = ''.join([
		'[left_bottom_crop_out]', # hflip'd
		'[left_crop_out]', # might need vflipped or hflipped depending on transpose.
		'[top_crop_out]', # fine as is.
		'[right_crop_out]', # fine as is.
		'[right_bottom_crop_out]', # hflip'd
		'hstack=inputs=5'
		])

	#  we need to perform the Black bar cropping first, and split from there.
	graph_start = ''.join([
		'[0:v]',black_bar_crop_cmd,'[crop_out];',
		'[crop_out]split[split_a][split_b];',
		'[split_a]split[split_1][split_2];',
		'[split_b]split[split_3][split_4];'
		])

	frame_filter_graph = ''.join([
		splits_to_crops_cmd,
		bottom_chop_cmd,
		h_stack_cmd
		])

	prod_graph = ''.join([
		graph_start,
		frame_filter_graph,
		])
	# Prod Command Generated
	return prod_graph

def generateCommand():
	return['ffmpeg',
	'-loglevel', 'fatal',
	'-threads', '2',
	'-f', 'video4linux2',
	'-i', '/dev/video0',
	'-filter_complex', computeFilterGraph(),
	'-f', 'image2pipe',
	'-pix_fmt', 'rgb24',
	'-vcodec', 'rawvideo',
	'-']

#  Todo: make this a part of a init method just printing a few easily read input values...
def get_video_info():
	command = ['ffprobe',
	'-v', 'fatal',
	'-show_entries', 'stream=width,height,r_frame_rate,duration',
	'-of', 'default=noprint_wrappers=1:nokey=1',
	'/dev/video0', '-sexagesimal']
	ffmpeg = sp.Popen(command, stderr=sp.PIPE ,stdout = sp.PIPE)
	out, err = ffmpeg.communicate()
	if(err) : print(err)
	out = out.split('\n')
	return {'file' : '/dev/video0','width': int(out[0]),'height' : int(out[1]),'fps': float(out[2].split('/')[0])/float(out[2].split('/')[1]),'duration' : out[3] }

def turnStripOff():
	global STRIP
	print('[AMBILIGHT]: Turning Strip Off')
	colorWipe(STRIP,BLACK)

def colorize_frame(frame):
	def colorize(frame,strip):
		for i in range(TOTAL_PIXEL_COUNT):
			pixel = frame[0][i]
			strip.setPixelColor(i,Color(int(pixel[0]),int(pixel[1]),int(pixel[2])))
		strip.show()
	colorize(frame,STRIP)


def read_frame(command,strip,frame_count=1):
	global RUN

	pipe = sp.Popen(command, stderr=sp.PIPE ,stdout=sp.PIPE, bufsize=BUFF_SIZE)

	if frame_count == 0:
		print("[AMBILIGHT]: Frame Count is Zero, Running Loop Indefinitly...")
		while RUN:
			raw_image = pipe.stdout.read(BUFF_SIZE)
			# TODO:
			# handle 
			# ValueError: cannot reshape array of size 0 into shape (1,100,3)
			frame = np.fromstring(raw_image, dtype='uint8').reshape(DATA_SHAPE)
			colorize_frame(frame)
			pipe.stdout.flush()
		turnStripOff()
	else:
		print("[AMBILIGHT]: Running Loop for: ",frame_count)
		for i in range(frame_count):
			print(i)
			if i == (frame_count-1):
				turnStripOff()
				return
			raw_image = pipe.stdout.read(BUFF_SIZE)
			frame = np.fromstring(raw_image, dtype='uint8').reshape(DATA_SHAPE)
			colorize_frame(frame)
			pipe.stdout.flush()
		turnStripOff()
	print('[AMBILIGHT]: Finished Reading Frames.')
	return


def stop_ambilight_system(strip):
	global RUN
	print('[AMBILIGHT]: Stopping System.')
	RUN = False
	print("(RUN: "+str(RUN)+")")
	colorWipe(strip,BLACK)
	return


def start_ambilight_system(strip):
	print('[AMBILIGHT]: Starting System.')
	global STRIP
	global RUN
	RUN = True
	STRIP = strip
	command = generateCommand()
	print("[AMBILIGHT]: (RUN "+str(RUN)+")")
	read_frame(command,strip,frame_count=0)


# def run_main():
# 	global STRIP
# 	global COMMAND
# 	COMMAND = generateCommand()
# 	STRIP = strip_init()
# 	print("Setup Complete")
# 	print("Running Program")
# 	try:
# 		while True:
# 			read_frame(COMMAND,STRIP,0)
# 	except KeyboardInterrupt:
# 		turnStripOff()
# 		print("Goodbye")

# def main():
# 	run_main()

# main()