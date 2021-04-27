import cv2
import pytesseract
### Init variable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
## Read Img by name
img = cv2.imread("Test3.jpg")
## Convert to RBG since tesseract work with RBG, not BGR
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
## Read text from Image
str_test = pytesseract.image_to_string(img)
print(str_test)
## Read text's boxes from Iamge
boxes = pytesseract.image_to_boxes(img)

Himg,Wimg,_ = img.shape
for b in boxes.splitlines():
    b = b.split(' ')
    print(b)
    x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
    cv2.rectangle(img,(x,Himg-y),(w+2,Himg-h),(0,0,240),1)
    cv2.putText(img,b[0],(x,Himg-y+20),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,150,0),1)
# print(boxes)
## Show image
cv2.imshow('Img_1',img)
cv2.waitKey(0)