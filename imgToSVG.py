import cv2
import numpy as np
# if gameboard is 400x400 mm

GAMEBOARD_LIMIT_MM      = [300, 300]
PIXELS_PER_MM           = 3.77952755953
CURRENT_POSITION_XY     = [0, 0]
CURRENT_POSITION_MM     = [0, 0]

# calculates the slope of the provided contour
def calculate_steps_per_motor(contours, width, height, speed):
    scaleFactor = normalizeBoard(width, height)
    scaleFactor = scaleFactor/PIXELS_PER_MM
    f = open('imagePath.CNC', 'w+')
    cnt = sorted(contours, key=cv2.contourArea)
    
    for i in reversed(range(len(cnt))):
        for j in range(len(cnt[i])):
            if cv2.contourArea(cnt[i]) > 80:
                x,y         = cnt[i][j][0]

                if j < len(cnt[i]) - 1:
                    x2, y2  = cnt[i][j+1][0]
                    mx, my  = [(x2-x), (y2-y)]
                    f.write('d,' + str(scaleFactor*mx) + ',' + str(scaleFactor*my) + str(speed) + '\n')
               
                elif j == len(cnt[i]) - 1 and i < len(cnt) - 1:
                    x2, y2  = cnt[i][0][0]
                    mx, my  = [(x2-x), (y2-y)]
                    f.write('d,' + str(scaleFactor*mx) + ',' + str(scaleFactor*my) + str(speed) + '\n')
                    x, y    = cnt[i][0][0]
                    x2, y2  = cnt[i+1][0][0]
                    mx, my  = [(x2-x), (y2-y)]
                    f.write('m,' + str(scaleFactor*mx) + ',' + str(scaleFactor*my) + str(speed) + '\n')
    
    f.write('m,' + str(-50) + ',' + str(150) + str(speed) + '\n')    
    f.close()


def print_pixel_path(edges,speed, hierarchy):
    f           = open('imagePathPoints.CNC', 'w+')
    cnt         = sorted(edges, key=cv2.contourArea)
    set_speed   = speed
    # print(hierarchy[0])
    for i in reversed(range(len(cnt))):
        if hierarchy[0][i][3] != -999:
            for j in range(len(cnt[i]) + 1):
                if cv2.contourArea(cnt[i]) > 80:
                    if j < len(cnt[i]):
                        x2, y2  = cnt[i][j][0]
                        f.write('d,' + str(x2) + ',' + str(y2) + ',' + str(set_speed) + '\n')
                    elif j == len(cnt[i]) and i > 1:
                        x2, y2  = cnt[i][0][0]
                        f.write('d,' + str(x2) + ',' + str(y2) + ',' + str(set_speed) + '\n')
                        x2, y2  = cnt[i-1][0][0]
                        f.write('m,' + str(x2) + ',' + str(y2) + ',' + str(set_speed) + '\n')
                    global CURRENT_POSITION_XY
                    CURRENT_POSITION_XY = [x2, y2]
    f.close()


def detectContours(path,thresh=80):
    # find and draw contours of image
    img                 = cv2.imread(path)
    # flip pngs
    img                 = cv2.flip(img, 0)
    # img                 = cv2.rotate(img, cv2.ROTATE_180)
    img                 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    IMG_WIDTH           = img.shape[0]
    IMG_HEIGHT          = img.shape[1]
    gray                = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh         = cv2.threshold(gray, thresh,255,0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def detectEdges_sobel(path,thresh=80):
    # find and draw contours of image
    img                 = cv2.imread(path)
    # flip pngs
    img                 = cv2.flip(img, 0)
    # img                 = cv2.rotate(img, cv2.ROTATE_180)
    img                 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    IMG_WIDTH           = img.shape[0]
    IMG_HEIGHT          = img.shape[1]
    gray                = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    
    img_blur            = cv2.GaussianBlur(gray, (3,3), 0) 
    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    # Display Sobel Edge Detection Images
    # cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
    # cv2.waitKey(0)


def detectEdges_canny(img, thresh_min=100, thresh_max=200):
    assert img is not None, "file could not be read, check with os.path.exists()"
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    edges   = cv2.Canny(blur,thresh_min,thresh_max)
    print(len(edges))
    return(edges)
    #cv2.imshow('canny', edges)
    #cv2.waitKey(0)
    
    

# this function returns the distance to travel, scaled so the motor will not travel off the board 
# it relies on the GAMEBOARD_LIMIT_MM define for the limiting size
#
##
###
# if you want to constrain this to the size of a paper
# example usage: 
################   
#
# GAMEBOARD_LIMIT_MM            = [215.9, 279.4]                            <------ 8.5in x 11in  converted to mm
# img_width, img_height, ret    = img.shape                                 <------ shape returns [width, height, channel]
# scale_factor                  = normalizeBoard(img_width, img_height)     <------ returns the scale_factor multiplier
#
################
def normalizeBoard(width, height):
    GAMEBOARD_SIZE_MM   = [width/PIXELS_PER_MM, height/PIXELS_PER_MM]
    scaleFactor         = 1
    # constrain by image height or width, depending on which is 
    if GAMEBOARD_SIZE_MM[0] > GAMEBOARD_LIMIT_MM[0] or GAMEBOARD_SIZE_MM[1] > GAMEBOARD_LIMIT_MM[1]:
        if (GAMEBOARD_SIZE_MM[0] - GAMEBOARD_LIMIT_MM[0] >= GAMEBOARD_SIZE_MM[1] - GAMEBOARD_LIMIT_MM[1]):
            scaleFactor = GAMEBOARD_LIMIT_MM[0] / GAMEBOARD_SIZE_MM[0]
        else:
            scaleFactor = GAMEBOARD_LIMIT_MM[1] / GAMEBOARD_SIZE_MM[1]
    # print("Gameboard Limit = (" + str(GAMEBOARD_LIMIT_MM[0]) + ", " + str(GAMEBOARD_LIMIT_MM[1]) + ")")
    # print("Gameboard Size  = (" + str(GAMEBOARD_SIZE_MM[0]) + ", " + str(GAMEBOARD_SIZE_MM[1]) + ")")
    # print("New Size        = (" + str(GAMEBOARD_SIZE_MM[0]*scaleFactor) + ", " + str(GAMEBOARD_SIZE_MM[1]*scaleFactor) + ")")
    return scaleFactor
    




def path_mm(edges, scaleFactor):
    # open and save image as an svg file
    f = open('imagePath.CNC', 'w+')
    
    iMax = len(edges)
    # calculate pixels per inc
    for i in range(len(edges)):
        if i < len(edges) - 1:                   # seperate paths
            f.write('m,')
        for j in range(len(edges[i])):
            x = edges[i][j][0][0] / PIXELS_PER_MM
            y = edges[i][j][0][1] / PIXELS_PER_MM
            jMax = len(edges[i])
            if j < len(edges[i]) - 1:
                x2 = edges[i][j + 1][0][0] / PIXELS_PER_MM
                y2 = edges[i][j + 1][0][1] / PIXELS_PER_MM
                mx, my = [x2 - x, y2 - y]
            if j == jMax - 1 and i < iMax - 1:
                X2, Y2 = edges[i+1][0][0] / PIXELS_PER_MM
                mx, my = [X2 - x, Y2 - y]
                print('<path d="M ' + str(mx) + ', ' + str(my) + '/>')


def resizeImage(path, scale=60):
    img             = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    scale_percent   = scale             
    width           = int(img.shape[1] * scale_percent / 100)
    height          = int(img.shape[0] * scale_percent / 100)
    dim             = (width, height)
    # resize image
    resized         = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized


# contours, hierarchy = detectContours('pokemon.jpg', 80)

# calculate_steps_per_motor(contours)
# scaleFactor         = normalizeBoard(IMG_WIDTH, IMG_HEIGHT)
# calculate_steps_per_motor(contours, IMG_WIDTH, IMG_HEIGHT, 2000)
# print_pixel_path(contours, 1000, hierarchy)

# blank = np.zeros(img.shape, dtype='uint8')
# cv2.drawContours(blank, contours=contours, contourIdx=-1, color=(0, 255, 255), thickness=1)
# cv2.imshow('Contours', blank)
# cv2.waitKey(0)

# print(scaleFactor)


# detectEdges_sobel("tiger.png",thresh=80)
# ImagePath = 'leaf.jpg'
# ImagePath2 = 'building.jpg'

#resized_image = resizeImage(ImagePath, 80)
#detectEdges_canny(resized_image,thresh_min=20, thresh_max=100)
