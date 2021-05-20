import imutils
import cv2
import numpy as np

l_xStart = -1
l_yStart = -1
l_xEnd = -1
l_yEnd = -1
l_height = -1
l_width = -1
contador = 0
l_valMax = -1
c_valMax = -1
imagensTemplate = [r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\carUnicoJojo1.png', 
                   r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\carUnicoJojo2.png',
                   r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\carUnicoJojo3.png',
                   r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\carUnicoJojo4.png',
                   r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\carUnicoJojo5.png']
# t1 - vals_maxs = [41602273, 48509457, 66520257, 39139037, 46415409]
vals_maxs = [42961905, 57359841, 57067197, 1, 1]

#open the main image and convert it to gray scale image
main_image = cv2.imread(r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\carJojo2.jpg')
(m_height, m_width) = main_image.shape[:2]

i = 0
while(i < len(imagensTemplate)):
   #Open template and get canny
   template = cv2.imread(imagensTemplate[i])
   template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
   template = cv2.Canny(template, 10, 25)
   (height, width) = template.shape[:2]
   
   while True:   
      gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
      temp_found = None

      for scale in np.linspace(0.2, 1.0, 20)[::-1]:
         #resize the image and store the ratio
         resized_img = imutils.resize(gray_image, width = int(gray_image.shape[1] * scale))
         ratio = gray_image.shape[1] / float(resized_img.shape[1])
         if resized_img.shape[0] < height or resized_img.shape[1] < width:
            break
         
         #Convert to edged image for checking
         e = cv2.Canny(resized_img, 10, 25)
         match = cv2.matchTemplate(e, template, cv2.TM_CCOEFF)
         (_, val_max, _, loc_max) = cv2.minMaxLoc(match)


         if temp_found is None or val_max>temp_found[0]:
            temp_found = (val_max, loc_max, ratio)
            c_valMax = val_max
      
      print(f'c_valMax: {c_valMax}') #VALMAX É A COMPATIBILIDADE COM O TEMPLATE
      if l_valMax >= 0:
         """l_valMax"""
         if c_valMax < vals_maxs[i]: # 14100000        cvalmax do match q começou a dar erro      41602177|46261429
            print(f'Quantidade: {contador}')
            break

      l_valMax = c_valMax
      contador = contador + 1

      #Get information from temp_found to compute x,y coordinate
      (_, loc_max, r) = temp_found
      (x_start, y_start) = (int(loc_max[0]), int(loc_max[1]))
      (x_end, y_end) = (int((loc_max[0] + width)), int((loc_max[1] + height)))

      l_xStart = x_start
      l_yStart = y_start
      l_xEnd = x_end
      l_yEnd = y_end

      #Draw elipse around the template
      x_coordinate = (x_end-x_start)/2 + x_start
      y_coordinate = (y_end-y_start)/2 + y_start
      x_coordinate = round(x_coordinate)
      y_coordinate = round(y_coordinate)

      main_image = cv2.ellipse(main_image, (x_coordinate, y_coordinate), (round((x_end - x_start)/1.7), round((y_end - y_start)/1.7)), 0.0, 0.0, 360.0, (255, 0, 0), -1)
      
      main_image_resized = imutils.resize(main_image, width = int(500))
      cv2.imshow('Template Found', main_image_resized)
      cv2.waitKey(0)
      
   i = i + 1
cv2.waitKey(0)

