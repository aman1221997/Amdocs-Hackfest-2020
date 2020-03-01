import numpy as np
import cv2
import cv2.aruco as aruco
import math

####################### Define Utility Functions Here ##########################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
    with np.load('System.npz') as X:
        camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
    return camera_matrix, dist_coeff

"""
Function Name : sin()
Input: angle (in degrees)
Output: value of sine of angle specified
Purpose: Returns the sine of angle specified in degrees
"""
def sin(angle):
    return math.sin(math.radians(angle))

"""
Function Name : cos()
Input: angle (in degrees)
Output: value of cosine of angle specified
Purpose: Returns the cosine of angle specified in degrees
"""
def cos(angle):
    return math.cos(math.radians(angle))



################################################################################


"""
Function Name : detect_markers()
Input: img (numpy array), camera_matrix, dist_coeff
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""
def detect_markers(img, camera_matrix, dist_coeff):
    markerLength = 100
    aruco_list = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    with np.load('System.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
    rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeff)
    center = []
    for i in range(len(corners)):
        center_x, center_y = 0, 0
        for x, y in corners[i][0]:
            center_x += x
            center_y += y
        center.append((center_x / 4, center_y / 4))
    if (ids is not None):
            for x in range(len(ids)):
                aruco_list.append((ids[x], center[x], rvec[x:(x + 1)], tvec[x:(x + 1)]))
    return aruco_list

"""
Function Name : drawAxis()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws 3 mutually
         perpendicular axes on the specified aruco marker in the image and
         returns the modified image.
"""
def drawAxis(img, aruco_list, aruco_id, camera_matrix, dist_coeff):
    for x in aruco_list:
        if aruco_id == x[0]:
            rvec, tvec = x[2], x[3]
    markerLength = 100
    m = markerLength/2
    pts = np.float32([[-m,m,0],[m,m,0],[-m,-m,0],[-m,m,m]])
    pt_dict = {}
    imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
    for i in range(len(pts)):
         pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
    src = pt_dict[tuple(pts[0])];   dst1 = pt_dict[tuple(pts[1])];
    dst2 = pt_dict[tuple(pts[2])];  dst3 = pt_dict[tuple(pts[3])];

    img = cv2.line(img, src, dst1, (0,255,0), 4)
    img = cv2.line(img, src, dst2, (255,0,0), 4)
    img = cv2.line(img, src, dst3, (0,0,255), 4)
    return img

"""
Function Name : drawCube()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws a cube
         on the specified aruco marker in the image and returns the modified
         image.
"""
def drawCube(img, ar_list, ar_id, camera_matrix, dist_coeff):
    for x in ar_list:
        if ar_id == x[0]:
            rvec, tvec = x[2], x[3]
    markerLength = 100
    m = markerLength/2
    pts = np.float32([[-m, m, 0], [m, m, 0], [m, -m, 0], [-m, -m, 0], [-m, m, 2 * m], [m, m, 2 * m], [m, -m, 2 * m], [-m, -m, 2 * m]])
    pt_dict = {}
    imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
    for i in range(len(pts)):
        pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
    src1 = pt_dict[tuple(pts[0])]
    src2 = pt_dict[tuple(pts[1])]
    src3 = pt_dict[tuple(pts[2])]
    src4 = pt_dict[tuple(pts[3])]
    dest1 = pt_dict[tuple(pts[4])]
    dest2 = pt_dict[tuple(pts[5])]
    dest3 = pt_dict[tuple(pts[6])]
    dest4 = pt_dict[tuple(pts[7])]
    img = cv2.line(img, src1, src2, (0, 0, 255), 4)
    img = cv2.line(img, src2, src3, (0, 0, 255), 4)
    img = cv2.line(img, src1, src4, (0, 0, 255), 4)
    img = cv2.line(img, src3, src4, (0, 0, 255), 4)
    img = cv2.line(img, src1, dest1, (0, 0, 255), 4)
    img = cv2.line(img, src2, dest2, (0, 0, 255), 4)
    img = cv2.line(img, src3, dest3, (0, 0, 255), 4)
    img = cv2.line(img, src4, dest4, (0, 0, 255), 4)
    img = cv2.line(img, dest1, dest2, (0, 0, 255), 4)
    img = cv2.line(img, dest2, dest3, (0, 0, 255), 4)
    img = cv2.line(img, dest1, dest4, (0, 0, 255), 4)
    img = cv2.line(img, dest3, dest4, (0, 0, 255), 4)
    
    return img

"""
Function Name : drawCylinder()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws a cylinder
         on the specified aruco marker in the image and returns the modified
         image.
"""
def drawCylinder(img, ar_list, ar_id, camera_matrix, dist_coeff):
    center = ()
    for x in ar_list:
        if ar_id == x[0]:
            center, rvec, tvec = x[1], x[2], x[3]
    markerLength = 100
    radius = markerLength/2; height = markerLength*1.5
    r = radius; h = height
    pts = np.float32([[r, 0, 0],
                      [r * cos(30), r * sin(30), 0],
                      [r * cos(60), r * sin(60), 0],
                      [0, r, 0],
                      [r * cos(120), r * sin(120), 0],
                      [r * cos(150), r * sin(150), 0],
                      [-r, 0, 0],
                      [r * cos(210), r * sin(210), 0],
                      [r * cos(240), r * sin(240), 0],
                      [0, -r, 0],
                      [r * cos(300), r * sin(300), 0],
                      [r * cos(330), r * sin(330), 0],
                      [r, 0, h],
                      [r * cos(30), r * sin(30), h],
                      [r * cos(60), r * sin(60), h],
                      [0, r, h],
                      [r * cos(120), r * sin(120), h],
                      [r * cos(150), r * sin(150), h],
                      [-r, 0, h],
                      [r * cos(210), r * sin(210), h],
                      [r * cos(240), r * sin(240), h],
                      [0, -r, h],
                      [r * cos(300), r * sin(300), h],
                      [r * cos(330), r * sin(330), h]
                      ])
    pt_dict = {}
    imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
    for i in range(len(pts)):
        pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
    center = pt_dict[tuple(pts[0])]
    s1, s2, s3, s4 = pt_dict[tuple(pts[0])], pt_dict[tuple(pts[1])], pt_dict[tuple(pts[2])], pt_dict[tuple(pts[3])]
    s5, s6, s7, s8 = pt_dict[tuple(pts[4])], pt_dict[tuple(pts[5])], pt_dict[tuple(pts[6])], pt_dict[tuple(pts[7])]
    s9, s10, s11, s12 = pt_dict[tuple(pts[8])], pt_dict[tuple(pts[9])], pt_dict[tuple(pts[10])], pt_dict[tuple(pts[11])]
    d1, d2, d3, d4 = pt_dict[tuple(pts[12])], pt_dict[tuple(pts[13])], pt_dict[tuple(pts[14])], pt_dict[tuple(pts[15])]
    d5, d6, d7, d8 = pt_dict[tuple(pts[16])], pt_dict[tuple(pts[17])], pt_dict[tuple(pts[18])], pt_dict[tuple(pts[19])]
    d9, d10, d11, d12 = pt_dict[tuple(pts[20])], pt_dict[tuple(pts[21])], pt_dict[tuple(pts[22])], pt_dict[tuple(pts[23])]
    img = cv2.line(img, s1, s7, (255, 0, 0), 4)
    img = cv2.line(img, s2, s8, (255, 0, 0), 4)
    img = cv2.line(img, s3, s9, (255, 0, 0), 4)
    img = cv2.line(img, s4, s10, (255, 0, 0), 4)
    img = cv2.line(img, s5, s11, (255, 0, 0), 4)
    img = cv2.line(img, s6, s12, (255, 0, 0), 4)
    img = cv2.line(img, d1, d7, (255, 0, 0), 4)
    img = cv2.line(img, d2, d8, (255, 0, 0), 4)
    img = cv2.line(img, d3, d9, (255, 0, 0), 4)
    img = cv2.line(img, d4, d10, (255, 0, 0), 4)
    img = cv2.line(img, d5, d11, (255, 0, 0), 4)
    img = cv2.line(img, d6, d12, (255, 0, 0), 4)
    img = cv2.line(img, s1, d1, (255, 0, 0), 4)
    img = cv2.line(img, s2, d2, (255, 0, 0), 4)
    img = cv2.line(img, s3, d3, (255, 0, 0), 4)
    img = cv2.line(img, s4, d4, (255, 0, 0), 4)
    img = cv2.line(img, s5, d5, (255, 0, 0), 4)
    img = cv2.line(img, s6, d6, (255, 0, 0), 4)
    img = cv2.line(img, s7, d7, (255, 0, 0), 4)
    img = cv2.line(img, s8, d8, (255, 0, 0), 4)
    img = cv2.line(img, s9, d9, (255, 0, 0), 4)
    img = cv2.line(img, s10, d10, (255, 0, 0), 4)
    img = cv2.line(img, s11, d11, (255, 0, 0), 4)
    img = cv2.line(img, s12, d12, (255, 0, 0), 4)
    img = cv2.line(img, s1, s2, (255, 0, 0), 4)
    img = cv2.line(img, s2, s3, (255, 0, 0), 4)
    img = cv2.line(img, s3, s4, (255, 0, 0), 4)
    img = cv2.line(img, s4, s5, (255, 0, 0), 4)
    img = cv2.line(img, s5, s6, (255, 0, 0), 4)
    img = cv2.line(img, s6, s7, (255, 0, 0), 4)
    img = cv2.line(img, s7, s8, (255, 0, 0), 4)
    img = cv2.line(img, s8, s9, (255, 0, 0), 4)
    img = cv2.line(img, s9, s10, (255, 0, 0), 4)
    img = cv2.line(img, s10, s11, (255, 0, 0), 4)
    img = cv2.line(img, s11, s12, (255, 0, 0), 4)
    img = cv2.line(img, s12, s1, (255, 0, 0), 4)
    img = cv2.line(img, d1, d2, (255, 0, 0), 4)
    img = cv2.line(img, d2, d3, (255, 0, 0), 4)
    img = cv2.line(img, d3, d4, (255, 0, 0), 4)
    img = cv2.line(img, d4, d5, (255, 0, 0), 4)
    img = cv2.line(img, d5, d6, (255, 0, 0), 4)
    img = cv2.line(img, d6, d7, (255, 0, 0), 4)
    img = cv2.line(img, d7, d8, (255, 0, 0), 4)
    img = cv2.line(img, d8, d9, (255, 0, 0), 4)
    img = cv2.line(img, d9, d10, (255, 0, 0), 4)
    img = cv2.line(img, d10, d11, (255, 0, 0), 4)
    img = cv2.line(img, d11, d12, (255, 0, 0), 4)
    img = cv2.line(img, d12, d1, (255, 0, 0), 4)

    # height, width, channels = img.shape
    # blank_image = np.zeros((height,width,3), np.uint8)
    # cv2.imshow("blank", blank_image)
#     # (x,y), radius = cv2.minEnclosingCircle(cnt)
#     # center = (int(x),int(y))
#     # radius = int(radius)
#     # cv2.circle(img,center,radius,(0,255,0),2)

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(gray,127,255,0)
    # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0,255,0), 3)
    return img

"""
MAIN CODE
This main code reads images from the test cases folder and converts them into
numpy array format using cv2.imread. Then it draws axis, cubes or cylinders on
the ArUco markers detected in the images.
"""


if __name__=="__main__":
    cam, dist = getCameraMatrix()
    img = cv2.imread("..\\TestCases\\image_5.jpg")
    aruco_list = detect_markers(img, cam, dist)
    for i in aruco_list:
        img = drawAxis(img, aruco_list, i[0], cam, dist)
        img = drawCube(img, aruco_list, i[0], cam, dist)
        img = drawCylinder(img, aruco_list, i[0], cam, dist)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
