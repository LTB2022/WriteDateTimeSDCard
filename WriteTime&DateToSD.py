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


if False:   # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    #   t is a time object
    t = time.struct_time((2022,  03,   09,   15,  56,  15,    0,   -1,    -1))

    #print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    #print()

# while True:
#    t = rtc.datetime
#    #print(t)     # uncomment for debugging

#    print("The date is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mday, t.tm_mon, t.tm_year))
#    print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))

#    time.sleep(1) # wait a second

# Creates object that connects SPI bus and a digital output for the microSD card's CS line.
# The pin name should match our wiring.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# This is the chip select line on the M4 board.
cs = digitalio.DigitalInOut(board.D10)

# This creates the microSD card object and the filesystem object:
# Inputs are the spi and cs objects.
sdcard = adafruit_sdcard.SDCard(spi, cs)
# The microSD card object and the filesystem object are now
# being passed through Vfsfat class.
vfs = storage.VfsFat(sdcard)

# We can now make the path /sd on the CircuitPython
# filesystem read and write from the card:
storage.mount(vfs, "/sd")

# Creates a file and writes name inside a text file along the path.
with open("/sd/timestamp.txt", "w") as f:
    f.write("Val McGee\r\n")


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

