import busio
import adafruit_pcf8523
import time
import board
import digitalio
import adafruit_sdcard
import storage

# Lights up LED for log on SD card:

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Creates object I2C that connects the I2C module to pins SCL and SDA
myI2C = busio.I2C(board.SCL, board.SDA)
# Creates an object that can access the RTC and communicate that information along using I2C.
rtc = adafruit_pcf8523.PCF8523(myI2C)


if False:   # Leave as False unless you want to reset the time that the RTC keeps!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    
    #   t is an instance of the struct_time class. It is being passed through the time function to collect and store time data of type integer!
    t = time.struct_time((2022,  03,   09,   15,  56,  15,    0,   -1,    -1))
    #   Here we are using the struct_time object "t" to write time keeping information to the RTC circuit. 
    rtc.datetime = t

# "spi" is created as an instance of class SPI and is passed through the busio function, which assigns the pins of the Serial Peripheral Interface. 
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# This is the chip select line on the M4 board.
cs = digitalio.DigitalInOut(board.D10)

# "sdcard" is an instance of the SDCard class, which is passed through the adafruit_sdcard function, which uses information from the "spi" and "cs" objects.
sdcard = adafruit_sdcard.SDCard(spi, cs)
# This sets up the file storage system, the FAT16. 
vfs = storage.VfsFat(sdcard)

# We can now make the path /sd on the CircuitPython
# filesystem read and write from the card:
storage.mount(vfs, "/sd")

# Creates a file and writes name inside a text file along the path.
with open("/sd/timestamp.txt", "w") as f:
    f.write("Profile Name\r\n")


print("Logging timestamp into filesystem")

# appending timestamp to file

with open("/sd/timestamp.txt", "a") as f:
    led.value = True
    # This is supposed to be the timestamp
    # Not sure if it updates every time
    t = rtc.datetime

    f.write( "%d/%d/%d" % (t.tm_mday, t.tm_mon, t.tm_year))
    f.write("%d:%02d:%02d " % (t.tm_hour, t.tm_min, t.tm_sec))
    led.value = False  # turn off LED to indicate we're done

