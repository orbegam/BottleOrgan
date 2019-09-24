from pyfirmata import Arduino, util
import time
import pygame.midi as midi
import traceback
import json

def pins_by_note(note):
	with open('servo_config.json', 'r') as f:
		pins_config = json.load(f)
		note = str(note)
		if note in pins_config:
			cfg = pins_config[note]
			return cfg[0], cfg[1], cfg[2]
		else:
			return None, None, None

def all_mute_angles():
	res = dict()
	with open('servo_config.json', 'r') as f:
		pins_config = json.load(f)
		for cfg in pins_config.values():
			res[cfg[0]] = cfg[1]

	return res

### ARDUINO

board = Arduino('COM7')
pins = [board.get_pin('d:{0}:s'.format(i)) for i in range(2, 10)]

def move_servo(pin, angle):	
	print 'Writing {0} to pin {1}'.format(angle, pin)
	pins[pin - 2].write(angle)

mute_angles = all_mute_angles()
for pin in mute_angles:
	board.servo_config(pin, mute_angles[pin])
	move_servo(pin, mute_angles[pin])

### MIDI

midi.init()
inp = midi.Input(1)

def play_note(note):
	pin, mute_angle, play_angle = pins_by_note(note)
	if pin is None:
		print "Error: No pin for note {0}".format(note)
		return

	move_servo(pin, play_angle)

def mute_note(note):
	pin, mute_angle, play_angle = pins_by_note(note)
	if pin is None:
		print "Error: No pin for note {0}".format(note)
		return

	move_servo(pin, mute_angle)

### MAIN LOOP

print "Setup done."

# Flush old messages
if inp.poll():
	inp.read(1000)

while True:
	if inp.poll():
		msgs = inp.read(1000)
		for msg in msgs:
			print 'MIDI message: ', msg
			if msg[0][0] != 144:
				continue

			note = msg[0][1]
			volume = msg[0][2]
			try:
				if volume > 0:
					play_note(note)
				else:
					mute_note(note)
			except Exception as ex:
				print "Error: "
				traceback.print_exc()
