import cv2
import numpy as np
import urllib.request

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
#im = Image.open(requests.get("https://visionofsid.files.wordpress.com/2022/01/1.png?w=150", stream=True).raw)
#im.show()

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
text=input("Enter the text to encrypt: ")
while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    whitebg = urllib.request.urlopen("https://visionofsid.files.wordpress.com/2022/01/white.jpg?w=200&zoom=2")
    array= np.array(bytearray(whitebg.read()), dtype=np.uint8)
    Im1 = cv2.imdecode(array, -1)
    blackbg = urllib.request.urlopen("https://visionofsid.files.wordpress.com/2022/01/blackbg.jpg?w=200&zoom=2")
    array= np.array(bytearray(blackbg.read()), dtype=np.uint8)
    Im2 = cv2.imdecode(array, -1)
    credit = urllib.request.urlopen("https://visionofsid.files.wordpress.com/2022/01/1.png?w=300")
    array= np.array(bytearray(credit.read()), dtype=np.uint8)
    Im3 = cv2.imdecode(array, -1)
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    xen=len(faces)
    lmao=str(xen)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    result = ""
    for i in range(len(text)):
        char = text[i]
        if (char.isupper()):
            result += chr((ord(char) + xen - 65) % 26 + 65)
        else:
            result += chr((ord(char) + xen - 97) % 26 + 97)
    creditt = cv2.resize(Im3, (500, 500))
    whitebgg = cv2.resize(Im1, (500, 500))
    blackbgg = cv2.resize(Im2, (500, 500))
    cv2.putText(whitebgg,"Original: ",(0,60),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),3)
    cv2.putText(whitebgg,text,(0,120),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),3)
    cv2.putText(whitebgg,"Cipher text:",(0,260), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 150, 0), 3)
    cv2.putText(whitebgg,result, (0,320), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 150, 0),3)
    cv2.putText(blackbgg,"Number of faces: ", (0,200),cv2.FONT_HERSHEY_COMPLEX, 2, (177, 128, 19), 3)
    cv2.putText(blackbgg,lmao, (0,250),cv2.FONT_HERSHEY_COMPLEX, 2, (177, 128, 19), 3)
    imgstack=stackImages(0.6,([creditt,whitebgg],[img,blackbgg]))
    cv2.imshow('img', imgstack)
    if cv2.waitKey(1) & 0xff==ord("a"):
        break
cap.release()

