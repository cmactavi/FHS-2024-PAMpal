from pms_a003 import Sensor 
from oled_091 import SSD1306 
from time import sleep 
from os import path 
from serial import SerialException 
import board 
import adafruit_ens160 
from gpiozero import LED 
 
# Set pins 18, 23 and 24 to be LEDs 
red = LED(18) 
blue = LED(23) 
 
DIR_PATH = path.abspath(path.dirname(__file__)) 
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf") 
 
i2c = board.I2C()  # uses board.SCL and board.SDA 
 
ens = adafruit_ens160.ENS160(i2c) 
 
# Set the temperature compensation variable to the ambient temp 
# for best sensor calibration 
ens.temperature_compensation = 25 
# Same for ambient relative humidity 
ens.humidity_compensation = 50 
 
def info_print(): 
    oled_display.DirImage(path.join(DIR_PATH, "Images/SB.png")) 
    oled_display.DrawRect() 
    oled_display.ShowImage() 
    sleep(1) 
    oled_display.PrintText("  Waiting....", FontSize=14) 
    oled_display.ShowImage() 
 
 
oled_display = SSD1306() 
air_mon = Sensor() 
air_mon.connect_hat(port="/dev/ttyS0", baudrate=9600) 
 
 
if __name__ == "__main__": 
    info_print() 
try: 
    while True: 
        values = air_mon.read()

        #Threshold limits for sensors; LEDS will turn on if sensor goes above threshold
        if (values.pm25_cf1 > 50): 
            red.on() 
        elif (values.pm25_cf1 < 50): 
            red.off() 
        if (ens.TVOC > 60): 
            blue.on() 
        elif (ens.TVOC < 60): 
            blue.off() 
        print("PM 1.0 : {} \tPM 2.5 : {} \tPM 10 : {}".format( 
            values.pm10_cf1, values.pm25_cf1, values.pm100_cf1)) 
 
        #Print outputs of sensors to OLED screen
        oled_display.PrintText("PM1.0= {:2d}".format(values.pm10_cf1), 
                               cords=(2, 2), FontSize=10) 
        oled_display.PrintText("PM2.5= {:2d}".format(values.pm25_cf1), 
                               cords=(65, 2), FontSize=10) 
        oled_display.PrintText("PM10= {:2d}".format(values.pm100_cf1), 
                               cords=(25, 20), FontSize=13) 
        oled_display.ShowImage() 
        sleep(2) 
        oled_display.PrintText("AQI= {:2d}".format(ens.AQI), 
                               cords=(2, 2), FontSize=10) 
        oled_display.PrintText("TVOC= {:2d}".format(ens.TVOC), 
                               cords=(65, 2), FontSize=10) 
        oled_display.PrintText("eCO2= {:2d}".format(ens.eCO2), 
                               cords=(25, 20), FontSize=13) 
 
 
        oled_display.ShowImage() 
        sleep(2) 
        print("AQI (1-5):", ens.AQI) 
        print("TVOC (ppb):", ens.TVOC) 
        print("eCO2 (ppm):", ens.eCO2) 
        print() 
 
except KeyboardInterrupt: 
    air_mon.disconnect_hat() 

 

 