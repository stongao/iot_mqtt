import mraa

print (mraa.getVersion())

lightStatus = mraa.Gpio(36) #edisonPin -> 14
lightStatus.dir(mraa.DIR_OUT)
lightStatus.write(0)

statusArduino = mraa.Gpio(47) #edisonPin -> 49
statusArduino.dir(mraa.DIR_OUT)
statusArduino.write(0)

statusRaspPi = mraa.Gpio(46) #edisonPin -> 47
statusRaspPi.dir(mraa.DIR_OUT)
statusRaspPi.write(0)

lightStatus.write(1)
statusArduino.write(1)
statusRaspPi.write(1)

