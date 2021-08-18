import numpy as np
import cv2
import imutils

carros = 0

car_classifier = cv2.CascadeClassifier(r'Project\haarcascade_car.xml')
cap = cv2.imread(r'Project\images#\carrosDia1.jpg')
(height, width) = cap.shape[:2]
gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

taxa = 35
parou = False
while taxa >= 25:
    cars = car_classifier.detectMultiScale(gray, 1.004, taxa) #35
    for (x,y,w,h) in cars:
        carros = carros + 1
        cv2.rectangle(cap, (x, y), (x+w, y+h), (0, 0, 255), 2)
        gray_exib = imutils.resize(cap, width = int(1000))
    if(carros <= 25):
        parou = True
        break
    print(carros)
    taxa = taxa - 5

if(not parou):
    carros = round(carros / 3)

print('Carros: ' + str(carros))
cv2.imshow('Cars', gray_exib)
cv2.waitKey()

#Taxa de erro: ~10% (3 em 32)