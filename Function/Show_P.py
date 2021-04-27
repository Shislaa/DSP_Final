from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
import cv2
import sys
import os,io
# Imports the Google Cloud client library
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

### Initialize Environment
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

class Show_Capture_UI(QtWidgets.QDialog):
    def __init__(self):
        super(Show_Capture_UI,self).__init__()
        ##load UI from files
        loadUi('C:\\Users\\Lil Shil\\PycharmProjects\\DSP\\Show_P.ui',self)
        frame = cv2.imread("live.png")
        qformat = QImage.Format_Indexed8
        if len(frame.shape) == 3:
            if (frame.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        frame = QImage(frame, frame.shape[1], frame.shape[0], qformat)
        frame = frame.rgbSwapped()
        self.Cam_Feed.setPixmap(QPixmap.fromImage(frame))
        self.Cam_Feed.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.Retry.clicked.connect(self.Retry_Controller)
    def Retry_Controller(self):
        self.hide()



#### Run the UI
def Run_UI():
    print("Switch is done")
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Show_Capture_UI()
    window.show()
    # sys.exit(app.exec())
