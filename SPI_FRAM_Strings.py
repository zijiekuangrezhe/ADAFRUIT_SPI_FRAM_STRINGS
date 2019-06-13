# SPI FRAM STRINGS STUFF
import board
import busio
import digitalio
import time
import adafruit_fram

# Create SPI Bus
spi_bus = busio.SPI(board.SCK, board.MOSI, board.MISO)

# Set Up Chip-Select
spi_cs = digitalio.DigitalInOut(board.D2)
spi_cs.direction = digitalio.Direction.OUTPUT
spi_cs.value = True

# Set Up SPI FRAM
fram = adafruit_fram.FRAM_SPI(spi_bus, spi_cs, write_protect=False, wp_pin=None, baudrate=12000000) # 12MHz

byteArrayRange = len(fram) # 8192 Bytes

def spiFramReset(startAddress, resetLength):
    if((startAddress < 0) or (startAddress > 8191)):
        print("-> ERROR: startAddress must be between 0 and {}.".format(byteArrayRange - 1), end="")
    else:
        if(resetLength > byteArrayRange):
            print("-> ERROR: Can't reset more than the space on the FRAM Chip, which is 8192 bytes...", end="")
        else:
            if(startAddress + resetLength > byteArrayRange):
                print("-> ERROR: Can't reset chosen space!"
                + " startAddress must be less than or equal to {}.".format(byteArrayRange - resetLength)
                + " Missing {} Byte(s).".format(startAddress + resetLength - byteArrayRange), end="")
            else:
                print("-> Performing {} Bytes Reset from Address {}...".format(resetLength, startAddress))
                startTime = time.time()
                for position in range(resetLength):
                    fram[startAddress + position] = 0xff
                elapsedTime = time.time() - startTime
                print("-> {} Bytes Reset in about {} Seconds.".format(resetLength, elapsedTime))
    return

def spiFramWrite(stringToWrite, startAddress, startSeparator, endSeparator): # Decide if string is short or long.
    if(len(stringToWrite) < 968): # Safe Short String Value
        spiFramWriteShortStrings(stringToWrite, startAddress, startSeparator, endSeparator)
    else:
        spiFramWriteLongStings(stringToWrite, startAddress, startSeparator, endSeparator)
    return

def spiFramWriteShortStrings(stringToWrite, startAddress, startSeparator, endSeparator):
    if(startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator) > byteArrayRange - 1):
        print("-> ERROR: Can't fit text into chosen space!"
        + " startAddress must be less than or equal to {}. Missing {} Byte(s)."
        .format(byteArrayRange - (len(startSeparator) + len(stringToWrite) + len(endSeparator)) - 1,
        startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator) + 1 - byteArrayRange), end="")
    else:
        print("-> Writing {} Bytes from FRAM Address {} to {}..."
        .format(len(startSeparator) + len(stringToWrite) + len(endSeparator), startAddress,
        startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator)))
        startTime = time.time()
        for position in range(len(startSeparator)):
            fram[startAddress + position] = bytearray(startSeparator[position])
        fram[startAddress + len(startSeparator)] = bytearray(stringToWrite)
        for position in range(len(endSeparator)):
            fram[startAddress + len(startSeparator) + len(stringToWrite) + position] = bytearray(endSeparator[position])
        fram[startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator)] = 0xff
        elapsedTime = time.time() - startTime
        print("-> {} Bytes Written in about {} Seconds.".format(len(stringToWrite), elapsedTime))
        del(stringToWrite)
    return

def spiFramWriteLongStings(stringToWrite, startAddress, startSeparator, endSeparator):
    if(startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator) > byteArrayRange - 1):
        print("-> ERROR: Can't fit text into chosen space!"
        + " startAddress must be less than or equal to {}. Missing {} Byte(s)."
        .format(byteArrayRange - (len(startSeparator) + len(stringToWrite) + len(endSeparator)) - 1,
        startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator) + 1 - byteArrayRange), end="")
    else:
        print("-> Writing {} Bytes from FRAM Address {} to {}..."
        .format(len(startSeparator) + len(stringToWrite) + len(endSeparator), startAddress,
        startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator)))
        startTime = time.time()
        for position in range(len(startSeparator)):
            fram[startAddress + position] = bytearray(startSeparator[position])
        for position in range(len(stringToWrite)):
            fram[startAddress + len(startSeparator) + position] = bytearray(stringToWrite[position])
        for position in range(len(endSeparator)):
            fram[startAddress + len(startSeparator) + len(stringToWrite) + position] = bytearray(endSeparator[position])
        fram[startAddress + len(startSeparator) + len(stringToWrite) + len(endSeparator)] = 0xff
        elapsedTime = time.time() - startTime
        print("-> {} Bytes Written in about {} Seconds.".format(len(stringToWrite), elapsedTime))
        del(stringToWrite)
    return

def spiFramRead(startAddress):
    print("-> Reading & Printing FRAM Until First Empty Byte:", end="\n\n")
    startTime = time.time()
    print("{START}", end="\n")
    stringToRead = ""
    position = 0
    while(fram[startAddress + position][0] != 0xff):
        print(chr(fram[startAddress + position][0]), end="")
        position += 1
    if(position == 0):
        print("{END}", end="")
    else:
        print("\n{END}", end="")
    elapsedTime = time.time() - startTime
    print("\n\n-> {} Bytes Read in about {} Seconds.".format(position, elapsedTime))
    del(stringToRead)
    return

def spiFramPrintWhole():
    print("-> Reading & Printing the Whole {} Bytes FRAM Data:".format(byteArrayRange), end="\n\n")
    startTime = time.time()
    print("{START}", end="\n")
    empty = True
    for position in range(len(fram)):
        if(fram[position][0] != 0xff):
            print(chr(fram[position][0]), end="")
            empty = False
        else:
            print("", end="")
    if(empty == True):
        print("{END}", end="")
    else:
        print("\n{END}", end="")
    elapsedTime = time.time() - startTime
    print("\n\n-> {} KB SPI FRAM Printed in about {} Seconds.".format(byteArrayRange, elapsedTime))
    return


stringToWrite = "Lorem ipsum dolor sit amet, quo oporteat nominati id, no meis disputationi eos, stet utroque vis at. Mel ferri adversarium no, illum consetetur pro ad, iusto commune mea ad. Errem voluptua vis at, eam malis aliquip imperdiet id. Simul partiendo sea ea, ne sed diam partem nostrud, eam dicat nonumes no. Duo impetus detraxit cu, doctus adipiscing ne vix.\n\nUsu cu modo malorum, eum no liber insolens temporibus. Ius no illud zril recteque, et ius mundi latine aperiri, at melius aperiam recusabo vix. Esse euismod eam te, zril civibus volumus ea nam, per eleifend indoctum an. At usu soluta comprehensam, no vix agam molestie, id sea wisi eripuit necessitatibus. Fugit appetere eum eu, ridens bonorum tractatos at has, est assentior pertinacia an. Eos eros omnesque et.\n\nUllum meliore at nec, ut erant fastidii his, cum cu causae aliquip recusabo. Option dolores ex eos, dicant neglegentur eam ei, ea quem vulputate contentiones vis. Ferri feugiat maiorum no vim. Id falli dicant pri. Has ei movet ceteros.\n\nIus case feugait te, integre sensibus in duo, per ad eirmod referrentur philosophia. Augue harum nullam te mei, diceret conceptam mea ut. Per cu illud perpetua torquatos. Ea usu atqui assueverit cotidieque. Te sit salutatus consulatu, vis graeci euripidis dissentiet id.\n\nSit quidam tamquam delicata eu, duo audiam perfecto eu. Sit ad harum fuisset gubergren. Ut dicit bonorum signiferumque est, pri scriptorem cotidieque persequeris ne. Eu quod dicant definitiones eam, ea vis graeco partiendo maiestatis."
#stringToWrite = "A"*500

print("-> SPI FRAM Size: {} Bytes = {} KB.".format(len(fram), len(fram) / 1024.0))
spiFramReset(startAddress=0, resetLength=8192)
spiFramWrite(stringToWrite, startAddress=0, startSeparator="", endSeparator="")
spiFramRead(0)
#spiFramPrintWhole()
# END OF SCRIPT
