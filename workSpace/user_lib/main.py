from machine import Pin,I2C
import time
import ssd1306
import socket
import network
import urequests
import MLX90614

WIDTH = const(128)
HEIGHT = const(64)
pscl = Pin(5, Pin.OUT)
psda = Pin(4, Pin.OUT)
i2c = I2C(scl=pscl, sda=psda)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensor = MLX90614.MLX90614(i2c)

button=Pin(14,Pin.IN, pull=None) 

wlan=0
SSID='High Hrothgar'
PSW='Skyrimbelongstothenords'
API_KEY='UTPMCCXIC9Q5R3CH'

def connectWiFi(ID,password):
  i=0
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ID, password)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    i=i+1
    oled.fill(0)
    oled.text('Makerfabs.com',10,0)
    oled.text('connecting WiFi',0,16)
    oled.text(SSID,0,32)
    oled.text('Countdown:'+str(20-i)+'s',0,48)
    oled.show()
    time.sleep(1)
    if(i>20):
      break
  oled.fill(0)
  oled.text('Makerfabs',25,0)
  oled.text('Python ESP32',0,32)
  if(i<20):
    oled.text('WIFI connected',0,16)
  else:
    oled.text('NOT connected!',0,16)
  oled.show()
  time.sleep(3)
  return True 

connectWiFi(SSID,PSW)

def Remind():
  oled.fill(0)
  oled.text('Measure Temp',10,5)
  oled.text('Please press',10,25)
  oled.text('the button',10,45)
  oled.show()
  
try:
  while True:
    if(button.value() == 0):
      Temp = sensor.getObjCelsius()
      oled.fill(0)
      oled.text('Temperature:',10,20)
      oled.text(str(Temp),20,40)
      print(Temp)
      oled.show() 
      
      URL="https://api.thingspeak.com/update?api_key="+API_KEY+"&field1="+str(Temp)
      res=urequests.get(URL)           
      print(res.text)
      
    else:
      Remind()
      
except KeyboardInterrupt:
            pass   
