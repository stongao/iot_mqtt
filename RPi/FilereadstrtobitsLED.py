import RPi.GPIO as GPIO
import time
from datetime import datetime
import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 6012
BUFFER_SIZE = 1

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

GPIO.setup(7,GPIO.OUT)

GPIO.output(7,0)
sleep = 1/250.000000
time.sleep(1/2.0)
#a = [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0]
#a = [0,0,0,0,1,1,1,1]

#a = string_to_bits("abcdef")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
except:
    print 'Socket Connection could not be setup'

GPIO.output(7,0)
time.sleep(8)

f = open('test.txt', 'r')
#while True:
	#GPIO.output(7,1)
	#time.sleep(sleep)
	#GPIO.output(7,0)
	#time.sleep(sleep)
#print datetime.now()
while True:
	#prev_time = datetime.now()
	a = string_to_bits(f.read(6))
        if len(a) == 0:
             break;
        #print a
        i = 0
	GPIO.output(7,1)
	time.sleep(sleep)
	for i in range (len(a)):
		GPIO.output(7, int(a[i]))
		time.sleep(sleep)
		#curr_time = datetime.now()
                #print curr_time - prev_time
                #prev_time = curr_time
	
	GPIO.output(7,0)
	time.sleep(10*sleep)
	#print a
	#time.sleep(2*sleep)
GPIO.output(7,0)
print datetime.now()	
time.sleep(1/2.0)






























































































































































