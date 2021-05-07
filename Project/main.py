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

#Open template and get canny
template = cv2.imread(r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\coin.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 10, 25)
(height, width) = template.shape[:2]

#open the main image and convert it to gray scale image
main_image = cv2.imread(r'C:\Users\nicol\Documents\GitHub\OpenCV_Vehicle_Detection\Project\images\coinz.png')
(m_height, m_width) = main_image.shape[:2]

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
      if c_valMax < 14100000: # cvalmax do match q começou a dar erro
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

   # using top ranked score, fill in that area with green
   main_image[loc_max[1]:loc_max[1]+height+1:, loc_max[0]:loc_max[0]+width+1, 0] = 0    # blue channel
   main_image[loc_max[1]:loc_max[1]+height+1:, loc_max[0]:loc_max[0]+width+1, 1] = 255  # green channel
   main_image[loc_max[1]:loc_max[1]+height+1:, loc_max[0]:loc_max[0]+width+1, 2] = 0    # red channel

   #Draw rectangle around the template
   cv2.rectangle(main_image, (x_start, y_start), (x_end, y_end), (153, 22, 0), 5)
   cv2.imshow('Template Found', main_image)
   cv2.waitKey(0)
