from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint,QRect
from PyQt5.uic import loadUi
import cv2
import sys
import os,io
# Imports the Google Cloud client library
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.cloud import translate_v2
from pathlib import Path as PA

### Initialize Environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'E:\Study Stuff\3rd year\ESD ( 29-4)\API_KEY.json'
# Instantiates a client
client = vision_v1.ImageAnnotatorClient()
client_2 = translate_v2.Client()
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
#######################################################################################
### Side Functions:
### Declare global variable
cap = cv2.VideoCapture(0)
prev_wid = ""
PATH = ""
lang_list = client_2.get_languages()
### Close the Webcam Protocal
def close_Cam():
    print("Close Cam worked")
    cap.release()
    cv2.destroyAllWindows()

def lang_annotation(name):
    global lang_list
    for i in lang_list:
        if i['name'] == name:
            return i['language']
def lang_name(anno):
    global lang_list
    for i in lang_list:
        if i['language'] == anno:
            return i['name']
#######################################################################################

class Start_Up_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(Start_Up_UI,self).__init__()
        #Load UI from Files
        loadUi('C:\\Users\\Lil Shil\\PycharmProjects\\DSP\\StartUp.ui',self)
        #Set Button connection
        self.Take_Pic.clicked.connect(self.To_Show_Cam)
        self.From_File.clicked.connect(self.To_Browse)
    def To_Show_Cam(self):
        Show_Cam = Show_Cam_UI()
        widget.addWidget(Show_Cam)
        widget.setFixedSize(800, 800)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def To_Browse(self):
        Br_F = Browse_File_UI()
        widget.addWidget(Br_F)
        widget.setFixedSize(800, 275)
        widget.setCurrentIndex(widget.currentIndex() + 1)
#######################################################################################
class Browse_File_UI(QtWidgets.QDialog):
    def __init__(self):
        super(Browse_File_UI,self).__init__()
        #Load UI from Files
        loadUi('C:\\Users\\Lil Shil\\PycharmProjects\\DSP\\Browse_File.ui',self)
        #Set Button connection
        self.counter = 0
        self.Browse.clicked.connect(self.browse_F)
        self.Ok.clicked.connect(self.To_Show_Txt)
    def browse_F(self):
        src = ''
        if self.counter == 0:
            src = 'C:/'
            self.counter += 1
        else:
            src = ''
        fname = QtWidgets.QFileDialog.getOpenFileName(self,'Open File',src,'Images (*.png;*.jpg;*.xmp;*.jfif)')
        self.Path.setText(fname[0])
    def To_Show_Txt(self):
        if self.Path.text() == '':
            self.Notice.setText("No File Chosen Yet")
        else:
            global prev_wid,PATH
            prev_wid = str(widget.currentWidget())
            PATH = self.Path.text()
            Show_Txt = Show_Txt_UI()
            h = Show_Txt.height()
            w = Show_Txt.width()
            widget.addWidget(Show_Txt)
            widget.setFixedSize(w, h)
            widget.setCurrentIndex(widget.currentIndex() + 1)
    def Put_Notice(self):
        self.Notice.setText("No File Chosen Yet!")


#######################################################################################

### Loading UI
class Show_Cam_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(Show_Cam_UI,self).__init__()
        #Load UI from Files
        loadUi('C:\\Users\\Lil Shil\\PycharmProjects\\DSP\\Show_Cam.ui',self)
        #Set Button connection
        self.Show_Cam.clicked.connect(self.CamF)
        self.Take_Pic.clicked.connect(self.TakePic)
        self.counter = 0

###  Function to show Camera
    def CamF(self):
        self.counter +=1
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if self.counter % 2 != 0:
                self.showCam(frame)
            else:
                self.Cam_Feed.clear()
                break
            cv2.waitKey(1)

#### Display Frame to Image Label
    def showCam(self,frame):
        qformat = QImage.Format_Indexed8
        if len(frame.shape) == 3:
            if(frame.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        frame = QImage(frame, frame.shape[1],frame.shape[0],qformat)
        frame = frame.rgbSwapped()
        self.Cam_Feed.setPixmap(QPixmap.fromImage(frame))
        self.Cam_Feed.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
#### Capture Image Function
    def TakePic(self):
        Cam_Is_On = self.Cam_Feed.pixmap()
        if Cam_Is_On is None:
            print("Deo co gi de xem ca")
        else:
            ret, frame = cap.read()
            file = 'live.png'
            cv2.imwrite(file, frame)

            Show_Cap = Show_Capture_UI()
            widget.addWidget(Show_Cap)
            widget.setFixedSize(850,550)
            widget.setCurrentIndex(widget.currentIndex()+1)

            # # print OCR text
            # p_frame = detect_text(file)
            # if p_frame != '':
            #     print(p_frame)
            # else:
            #     print("No text detected!")
#######################################################################################


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
        self.Ok.clicked.connect(self.Ok_Controller)
    def Retry_Controller(self):
        Show_Cam = Show_Cam_UI()
        widget.addWidget(Show_Cam)
        widget.setFixedSize(800, 800)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def Ok_Controller(self):
        global prev_wid
        prev_wid = str(widget.currentWidget())
        print(prev_wid)
        Show_Txt = Show_Txt_UI()
        h = Show_Txt.height()
        w = Show_Txt.width()
        widget.addWidget(Show_Txt)
        widget.setFixedSize(w, h)
        widget.setCurrentIndex(widget.currentIndex() + 1)
#######################################################################################

class Show_Txt_UI(QtWidgets.QDialog):
    def __init__(self):
        super(Show_Txt_UI,self).__init__()
        ## Load UI from files
        loadUi('C:\\Users\\Lil Shil\\PycharmProjects\\DSP\\Show_Txt.ui', self)
        global PATH,prev_wid,lang_list



        # print("prev_Wid in txt",prev_wid)
        if "Show_Capture_UI" in prev_wid:
            PATH = "live.png"
        w = self.Cam_Feed.width()
        h = self.Cam_Feed.height()
        frame_2 = QPixmap(PATH)

        self.Src_Lang.addItem("[Detect Language]")
        for i in lang_list:
            self.Src_Lang.addItem(i['name'])
            self.Des_Lang.addItem(i['name'])


        self.Cam_Feed.setPixmap(frame_2.scaled(w,h,QtCore.Qt.KeepAspectRatio))
        self.Cam_Feed.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # print("Debug TXT")
        self.To_SC.clicked.connect(self.To_SC_Controller)
        self.To_Br.clicked.connect(self.To_Br_Controller)
        self.Trans.clicked.connect(self.Translate)

        self.p_frame = detect_text(PATH)
        if self.p_frame != '':
            ### Get text method ToPlainText
            self.Txt_Img.setText(self.p_frame)
            print(self.p_frame)
            self.have_txt = True
        else:
            self.Txt_Img.setText("{{{ No Text can be Extracted from your Image, you might want to choose another one }}}")
            print("No text detected!")
            self.have_txt = False

        self.start_point, self.des_point = QPoint(),QPoint()

    # def paintEvent(self, event):
    #     pixmp = QPixmap(self.Cam_Feed.size())
    #     pixmp.fill(Qt.transparent)
    #     painter = QPainter(pixmp)
    #     painter.drawPixmap(QPoint(),pixmp)
    #     if not self.start_point.isNull() and not self.des_point.isNull():
    #         rect = QRect(self.start_point,self.des_point)
    #         painter.drawRect(rect.normalized())
    # def mousePressEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.start_point = event.pos()
    #         self.des_point = self.start_point()
    #         self.update()
    # def mouseMoveEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.des_point = self.start_point()
    #         self.update()
    # def mouseReleaseEvent(self, event):
    def To_SC_Controller(self):
        Show_Cam = Show_Cam_UI()
        widget.addWidget(Show_Cam)
        widget.setFixedSize(800, 800)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def To_Br_Controller(self):
        Br_F = Browse_File_UI()
        widget.addWidget(Br_F)
        widget.setFixedSize(800, 275)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Translate(self):
        if self.p_frame != '':
            target = lang_annotation(self.Des_Lang.currentText())

            if self.Src_Lang.currentIndex() == 0:
                out = client_2.translate(self.Txt_Img.toPlainText(), target_language=target)
                temp = str("Detected Language: " + lang_name(out['detectedSourceLanguage']))
                self.Notice.setText(temp)
            else:
                src = lang_annotation(self.Src_Lang.currentText())
                out = client_2.translate(self.Txt_Img.toPlainText(), target_language=target,source_language=src)
                self.Notice.setText(" ")
            print(out)
            self.Tran_Txt.setText(out["translatedText"])

        else:
            self.Notice.setText("No text detected!")

#######################################################################################

#### Run the UI
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
app.lastWindowClosed.connect(close_Cam)
window = Start_Up_UI()
widget.addWidget(window)
widget.setFixedSize(618,543)
widget.setWindowTitle("TransT")
widget.show()
sys.exit(app.exec())

