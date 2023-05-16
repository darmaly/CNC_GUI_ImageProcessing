import serial
from time import sleep
import sys
import csv

MILLIMETERS_PER_PULSE   = 0.0125
SYSCLK                  = 40000000
TIMER_FREQUENCY         = 156250

COM                     = '/dev/cu.SLAB_USBtoUART'  # /dev/ttyACM0 (Linux)
BAUD                    = 115200
PIC32                   = serial.Serial(COM, BAUD, timeout=1)
CURRENT_POSITION_XYZ     = [0, 0]
CURRENT_POSITION_MM     = [0, 0]
PIXELS_PER_MM           = 3.77952755953
MM_PER_PIXEL            = 0.2645833333

def sendDataAndWait(message):
    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read() 


def drawSquare():
    # go down
    tdata = "".encode("ascii")
    PIC32.write("d,000,r,2000,x,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()

    # go right
    tdata = "".encode("ascii")
    PIC32.write("d,2000,r,000,u,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()

    # go up
    tdata = "".encode("ascii")
    PIC32.write("d,000,r,2000,u,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()

    # go left
    tdata = "".encode("ascii")
    PIC32.write("d,2000,l,000,u,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()
def drawTriangle():
    # up and to the right
    tdata = "".encode("ascii")
    PIC32.write("d,1000,r,2000,u,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()

    # down and to the right
    tdata = "".encode("ascii")
    PIC32.write("d,1000,r,2000,d,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()

    # close off the triangle
    tdata = "".encode("ascii")
    PIC32.write("d,2000,l,000,x,275000\n".encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()



def drawCircle(precision, timer, max_speed):
    motor_x_right = "r"
    motor_x_left = "l"
    motor_y_up = "u"
    motor_y_down = "x"
    comma = ","
    precis_count = precision
    x_speed = precis_count
    y_speed = max_speed + precis_count
    timer_value = timer
    if max_speed > 8000:
        maxSpeed = 8000
    else:
        maxSpeed = max_speed

    message = ""

    while (x_speed < maxSpeed):

        # up and to the right
        message = ""  # reset the message each time
        message = message + "d" + comma + str(x_speed) + comma + motor_x_right + comma + str(
            y_speed) + comma + motor_y_up + comma + str(timer_value) + "\n"
        y_speed = y_speed - precis_count
        x_speed = x_speed + precis_count
        print(message)
        tdata = "".encode("ascii")
        PIC32.write(message.encode("ascii"))
        while (tdata != "XX".encode("ascii")):
            tdata += PIC32.read()

    # down and to the right
    while (y_speed < maxSpeed):
        message = ""  # reset the message each time
        message = message + "d" + comma + str(x_speed) + comma + motor_x_right + comma + str(
            y_speed) + comma + motor_y_down + comma + str(timer_value) + "\n"
        y_speed = y_speed + precis_count
        x_speed = x_speed - precis_count
        print(message)
        tdata = "".encode("ascii")
        PIC32.write(message.encode("ascii"))
        while (tdata != "XX".encode("ascii")):
            tdata += PIC32.read()

    # down and to the left
    while (x_speed < maxSpeed):
        message = ""  # reset the message each time
        message = message + "d" + comma + str(x_speed) + comma + motor_x_left + comma + str(
            y_speed) + comma + motor_y_down + comma + str(timer_value) + "\n"
        y_speed = y_speed - precis_count
        x_speed = x_speed + precis_count
        print(message)
        tdata = "".encode("ascii")
        PIC32.write(message.encode("ascii"))
        while (tdata != "XX".encode("ascii")):
            tdata += PIC32.read()

    # up and to the left
    while (y_speed < maxSpeed):
        message = ""  # reset the message each time
        message = message + "d" + comma + str(x_speed) + comma + motor_x_left + comma + str(
            y_speed) + comma + motor_y_up + comma + str(timer_value) + "\n"
        y_speed = y_speed + precis_count
        x_speed = x_speed - precis_count
        print(message)
        tdata = "".encode("ascii")
        PIC32.write(message.encode("ascii"))
        while (tdata != "XX".encode("ascii")):
            tdata += PIC32.read()


def calc_distance_mm(distance_milliMeters, motorFrequency, timerPrescale):
    pulsesNeeded = distance_milliMeters / ((motorFrequency / TIMER_FREQUENCY) * MILLIMETERS_PER_PULSE)
    return pulsesNeeded


def goDown(distance_milliMeters, penState, motorFrequency, timerPrescale):
    timerValue = calc_distance_mm(distance_milliMeters, motorFrequency, timerPrescale)
    timerValue = timerValue
    message = ""
    message = message + penState + ",0,r," + str(motorFrequency) + ",x," + str(int((timerValue))) + "\n"

    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()


def goUp(distance_milliMeters, penState, motorFrequency, timerPrescale):
    timerValue = calc_distance_mm(distance_milliMeters, motorFrequency, timerPrescale)
    timerValue = timerValue
    message = ""
    message = message + penState + ",0,r," + str(motorFrequency) + ",u," + str(int((timerValue))) + "\n"

    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()


def goLeft(distance_milliMeters, penState, motorFrequency, timerPrescale):
    timerValue = calc_distance_mm(distance_milliMeters, motorFrequency, timerPrescale)
    timerValue = timerValue
    message = ""
    message = message + penState + "," + str(motorFrequency) + ",l,0,x," + str(int((timerValue))) + "\n"

    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()


def goRight(distance_milliMeters, penState, motorFrequency, timerPrescale):
    timerValue = calc_distance_mm(distance_milliMeters, motorFrequency, timerPrescale)
    timerValue = timerValue
    message = ""
    message = message + penState + "," + str(motorFrequency) + ",r,0,x," + str(int((timerValue))) + "\n"

    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()


def goxy(x2, y2, max_speed, pen_state):
    global CURRENT_POSITION_XYZ
    print("current position: " + str(CURRENT_POSITION_XYZ))
    x1, y1          = CURRENT_POSITION_XYZ
    # count the steps to get to x2 and y2 steps
    y_moveToPixel   = y2 - y1
    x_moveToPixel   = x2 - x1

    print(str(x_moveToPixel) + ',' + str(y_moveToPixel))
    if x_moveToPixel != 0 or y_moveToPixel != 0:
        goXY_mm(x_moveToPixel*MM_PER_PIXEL, y_moveToPixel*MM_PER_PIXEL, max_speed, pen_state)

    CURRENT_POSITION_XYZ = [x_moveToPixel+CURRENT_POSITION_XYZ[0], y_moveToPixel+CURRENT_POSITION_XYZ[1]]

# down and left directions are represented by negative values of X and Y
# the position is also the defined in millimeters
# penState is either "d" for draw or "m" for move
def goXY_mm(X_millimeter, Y_millimeter, max_speed, penState):
    message = ""
    tdata   = ""
    y_dir   = ""
    x_dir   = ""
    abs_y   = abs(Y_millimeter)
    abs_x   = abs(X_millimeter)

    if X_millimeter == 0 or Y_millimeter == 0:
        secondary_motor_speed = 0
    elif abs(X_millimeter) <= abs(Y_millimeter):
        secondary_motor_speed = abs(X_millimeter) / abs(Y_millimeter) * max_speed
    else:
        secondary_motor_speed = abs(Y_millimeter) / abs(X_millimeter) * max_speed

    # set direction based on sign
    if Y_millimeter < 0:
        y_dir = "n"
    else:
        y_dir = "u"

    if X_millimeter < 0:
        x_dir = "l"
    else:
        x_dir = "r"

    # set the "default speed" to the motor with a longer travel. this limits the frequency to the default speed

    if (abs_x >= abs_y):
        timerValue = calc_distance_mm(abs_x, max_speed, 256)
        message = message + penState + "," + str(max_speed) + "," + x_dir + "," + str(
            int((secondary_motor_speed))) + "," + y_dir + "," + str(int((timerValue))) + "\n"

    else:
        timerValue = calc_distance_mm(abs_y, max_speed, 256)
        message = message + penState + "," + str(int((secondary_motor_speed))) + "," + x_dir + "," + str(
            max_speed) + "," + y_dir + "," + str(int((timerValue))) + "\n"

    print(message)
    sendDataAndWait(message)

def liftPen():
    message = "m,0,l,200,r,10"
    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()

def lowerPen():
    message = "d,0,l,100,u,10"
    print(message)
    tdata = "".encode("ascii")
    PIC32.write(message.encode("ascii"))
    while (tdata != "XX".encode("ascii")):
        tdata += PIC32.read()
        
def markPaper(speed):
    # start with a go home macro
    goXY_mm(55, -55, speed, "m")

    sleep(1)

    #  this will draw the left vertical lines
    goDown(10, "d", speed, 256)
    goDown(259.4, "m", speed, 256)
    goDown(10, "d", speed, 256)
    sleep(1)

    # draws the bottom hoizontal lines
    goRight(10, "d", speed, 256)
    goRight(195.9, "m", speed, 256)
    goRight(10, "d", speed, 256)
    sleep(1)

    #  this will draw the Right vertical lines
    goUp(10, "d", speed, 256)
    goUp(259.4, "m", speed, 256)
    goUp(10, "d", speed, 256)
    sleep(1)

    # draws the top hoizontal lines
    goLeft(10, "d", speed, 256)
    goLeft(195.9, "m", speed, 256)
    goLeft(10, "d", speed, 256)
    sleep(1)

    goUp(55, "m", speed, 256)
    goLeft(55, "m", speed, 256)
# negative values of width and heigh will change the way it draws the rectangle
def draw_rectangle(width, height, speed):
    goXY_mm(width, 0, speed, "d")
    goXY_mm(0, (height * -1), speed, "d")
    goXY_mm((width * -1), 0, speed, "d")
    goXY_mm(0, height, speed, "d")
def goHome(speed):
    global CURRENT_POSITION_XYZ
    print(CURRENT_POSITION_XYZ)
    # home_x = CURRENT_POSITION_XYZ[0]*-1
    # home_y = CURRENT_POSITION_XYZ[1]*-1
    goxy(0, 0, speed, "m")

    CURRENT_POSITION_XYZ = [0, 0]

def setHome():
    global CURRENT_POSITION_XYZ
    CURRENT_POSITION_XYZ = [0,0]

def setXHome():
    global CURRENT_POSITION_XYZ
    CURRENT_POSITION_XYZ[0] = 0

def setYHome():
    global CURRENT_POSITION_XYZ
    CURRENT_POSITION_XYZ[1] = 0


# open our file
def traceImage(path):
    with open(path, 'r') as infile:
        reader = csv.reader(infile, delimiter=",")
        for row in reader:
            motor_x     = row[1]
            motor_y     = row[2]
            speed       = row[3]
            penState    = row[0]

            goxy(float(motor_x), float(motor_y), float(speed), penState)
            print(motor_x, motor_y, speed, penState)
    goHome(4000)


def main():
    

    path = "imagePathPoints.CNC"
    # goxy(100, 100, 1000, "d")
    # goxy(150, 200, 1000, "d")
    # goxy(100, 200, 1000, "d")
    traceImage(path)

    # goxy(50, 100, 2000, "m")

    goHome(1000)

if __name__ == "__main__":
    main()