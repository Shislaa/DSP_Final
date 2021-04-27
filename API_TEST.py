# export GOOGLE_APPLICATION_CREDENTIALS=kyourcredentials.json
import os,io
import cv2
from PIL import Image
# Imports the Google Cloud client library
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Google_Vision_API.json'
# Instantiates a client
client = vision_v1.ImageAnnotatorClient()
def detect_text(path):
    """Detects text in the file."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = ''
    counter = 0
    for text in texts:
        if counter != 0:
            string+=' ' + text.description
        counter += 1
    return string

# print(detect_text("Test3.jpg"))
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    file = 'live.png'
    cv2.imwrite( file,frame)

    cv2.imshow('frame', frame)

    # print OCR text
    p_frame = detect_text(file)
    if p_frame != '':
        print(p_frame)

    # Display the resulting frame

    keypressed = cv2.waitKey(1)
    if keypressed == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
os.remove("live.png")