import sys
from PyQt5.QtGui import QColor, QIcon, QImage,QBrush
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QDialog,QApplication, QGraphicsDropShadowEffect,QMessageBox,QAbstractItemView
from PyQt5 import QtCore
import cv2,imutils,time,csv,os,datetime,glob
import numpy as np
from PIL import Image
import pandas as pd

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
counter=0

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("Ui/Loading.ui",self)
        #QTimer ==> Start
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.progressfunc)
        #Time in Millisecond
        self.timer.start(35)
        #Change Loading Labels Value
        self.label_Loading.setText("Loding...")
        # Dynamic Text
        QtCore.QTimer.singleShot(1500,lambda: self.label_Loading.setText("<strong>Loading</strong> User Interface"))
        QtCore.QTimer.singleShot(3000,lambda: self.label_Loading.setText("<strong>Connecting</strong> Database"))
        QtCore.QTimer.singleShot(4500,lambda: self.label_Loading.setText("<strong>Let's</strong> Enjoy"))

    def progressfunc(self):
        global counter
        #Set value to progress bar
        self.progressBar.setValue(counter)
        #Close splash screen and open app
        if counter>100:
            self.timer.stop()
            self.close()
            #Show Main Application
            # self.login=Login()
            # self.login.show()
            log=Login()
            widget.setFixedHeight(800)
            widget.setFixedWidth(1200)
            widget.setWindowTitle("Attendance Management System")
            widget.setWindowIcon(QIcon('Pic/Icon.png'))
            widget.addWidget(log)
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.show()
        counter+=1

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("Ui/Login.ui",self)
        # self.txtUserId.setFocus()
        self.btnLogin.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user=self.txtUserId.text()
        password=self.txtPassword.text()
        status=self.comboBoxStatus.currentText()
        if len(user)==0 or len(password)==0:
            self.lblerror.setText("Please input all fields..")
        else:
            # Database Code
            if user=="admin@gmail.com" and password=="admin":
                if status=="New Registration":
                    Reg=Registration()
                    widget.addWidget(Reg)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif status=="Take Attendance":
                    Att=Attendance()
                    widget.addWidget(Att)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.lblerror.setText("Invalid username or password..")

class Registration(QDialog):
    def __init__(self):
        super(Registration,self).__init__()
        loadUi("Ui/Registration.ui",self)
        self.comboBoxCourse.addItem('Select One',['Select One'])
        self.comboBoxCourse.addItem('B.Tech',['CSE','ECE','Machenical','Civil'])
        self.comboBoxCourse.addItem('MBA',['Finance','Management'])
        self.comboBoxCourse.addItem('Diploma',['CSE','ECE','Machenical','Civil'])
        self.comboBoxCourse.currentIndexChanged.connect(lambda: self.indexChanged(self.comboBoxCourse.currentIndex()))
        self.btnCapture.clicked.connect(self.captureimage)
        self.btnBack.clicked.connect(self.back)
        self.btnRegister.clicked.connect(self.saveData)
        # Haeding Writing in Student.csv File
        if not os.path.isfile("StudentDetails\Student.csv"):
            with open('StudentDetails\Student.csv', 'a+') as csvFile:
                writer = csv.DictWriter(csvFile, fieldnames=['Stu_ID','Stu_Name','Stu_Email','Stu_Contact','Stu_Course','Stu_Branch','Stu_Pass','Date','Time'])
                writer.writeheader()
            csvFile.close()
        self.started = False
    
    def back(self):
        log=Login()
        widget.addWidget(log)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def indexChanged(self,index):
        print(index)
        self.comboBoxBranch.clear()
        branches=self.comboBoxCourse.itemData(index)
        if branches:
            self.comboBoxBranch.addItems(branches)

    def captureimage(self):
        stuID=self.txtStuID.text()
        stuName=self.txtStuName.text()
        if self.started:
            self.started=False
            self.btnCapture.setText('Click To Capture')
        else:
            self.started=True
            self.btnCapture.setText('Stop')
        sampleNum=0
        vid = cv2.VideoCapture(0)
        # vid = cv2.VideoCapture(f'http://192.168.43.1:8080/video')
        while(vid.isOpened()):
            img, self.image = vid.read()
            self.image  = imutils.resize(self.image ,height = 480)
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.15,minNeighbors=7,minSize=(80, 80),flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (10, 228,220), 5)
                sampleNum=sampleNum+1
                cv2.imwrite("TrainingImage\ "+stuID + "." + stuName +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
            self.setPhoto(self.image)
            cv2.waitKey(1)                                      # Import for working code
            if self.started==False:     #No Use
                break
            elif sampleNum>=10:
                self.started=False      #No use
                self.btnCapture.setText('Click To Capture')     # break if the sample number is morethan 10
                break

    def saveData(self):
        stuID=self.txtStuID.text()
        stuName=self.txtStuName.text()
        stuEmail=self.txtEmailID.text()
        stuContact=self.txtContact.text()
        stuCourse=self.comboBoxCourse.currentText()
        stuBranch=self.comboBoxBranch.currentText()
        stuPass=self.txtPass.text()
        stuCPass=self.txtPass.text()
        date = datetime.datetime.fromtimestamp(time.time()).strftime('%d %B %Y')
        timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M:%S %p')
        row = [stuID,stuName,stuEmail,stuContact,stuCourse,stuBranch,stuPass,date,timeStamp]
        with open('StudentDetails\Student.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

        # Train Data
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        imagePaths=[os.path.join("TrainingImage",f) for f in os.listdir("TrainingImage")]
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,dtype='uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[0])
            print(Id)
            print(imageNp)
            faces.append(imageNp)
            Ids.append(Id)

        recognizer.train(faces, np.array(Ids))
        recognizer.save("TrainingImageLabel\Trainner.yml")

        msg=QMessageBox()
        msg.setWindowTitle("Confirmation Message")
        msg.setText("Your Information Has Been Recorded...")
        msg.setInformativeText("Images Saved for ID: " + stuID +" & Name: " +stuName)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        msg.exec()

    def setPhoto(self,image):
        self.tmp = image
        image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.lblImage.setPixmap(QtGui.QPixmap.fromImage(image))

class Attendance(QDialog):
    def __init__(self):
        super(Attendance,self).__init__()
        loadUi("Ui/Attendance.ui",self)
        self.btnStart.clicked.connect(self.trackImages)
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(10)
        self.started = False
        self.btnBack.clicked.connect(self.backWidget)
        self.btnViewA.clicked.connect(self.viewAttendance)

    def viewAttendance(self):
        attR=AttendanceRecord()
        widget.addWidget(attR)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def backWidget(self):
        log=Login()
        widget.addWidget(log)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def displayTime(self):
        self.lblTime.setText("Current Date & Time : "+QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.DefaultLocaleLongDate))

    def trackImages(self):
        if self.started:
            self.started=False
            self.btnStart.setText('Start')
        else:
            self.started=True
            self.btnStart.setText('Stop')

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Student_ID', 'Student_Name','Stu_Contact','Stu_Course','Stu_Branch', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)
        df = pd.read_csv("StudentDetails\Student.csv")
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img, self.image = vid.read()
            self.image  = imutils.resize(self.image ,height = 480)
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.15,minNeighbors=7,minSize=(80, 80),flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (36,255,12), 5)
                self.Id, self.conf = recognizer.predict(gray[y:y + h, x:x + w])
                if (self.conf < 50):
                    date = datetime.datetime.fromtimestamp(time.time()).strftime('%d %B %Y')
                    timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M:%S %p')
                    name = df.loc[df['Stu_ID'] == self.Id]['Stu_Name'].values
                    contact = df.loc[df['Stu_ID'] == self.Id]['Stu_Contact'].values
                    course = df.loc[df['Stu_ID'] == self.Id]['Stu_Course'].values
                    branch = df.loc[df['Stu_ID'] == self.Id]['Stu_Branch'].values
                    name = str(name)[2:-2]
                    contact = str(contact)[1:-1]
                    course = str(course)[2:-2]
                    branch = str(branch)[2:-2]
                    tt = str(self.Id) + "-" + name
                    nameShow = str(tt)
                    attendance.loc[len(attendance)] = [self.Id, name, '+91 '+contact, course, branch, date, timeStamp]
                else:
                    self.Id = 'Unknown'
                    # noOfFile = len(os.listdir("ImagesUnknown")) + 1
                    # cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", self.image[y:y + h, x:x + w])
                    nameShow = str(self.Id)
                cv2.putText(self.image, str(nameShow), (x, y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255))
            attendance = attendance.drop_duplicates(subset=['Student_ID'], keep='first')
            self.setPhoto(self.image)
            key = cv2.waitKey(1) & 0xFF
            if self.started==False:
                self.lblAttendance.setText("Click On Start To Take Attendance....")
                break

        date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        fileName = "Attendance/Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
        attendance.to_csv(fileName, index=False)

    def setPhoto(self,image):
        self.tmp = image
        image = imutils.resize(image,width=1100)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.lblAttendance.setPixmap(QtGui.QPixmap.fromImage(image))

class AttendanceRecord(QDialog):
    def __init__(self):
        super(AttendanceRecord,self).__init__()
        loadUi('Ui/AttendanceRecord.ui',self)
        self.btnBack.clicked.connect(self.backWindow)

        # self.tblAttendance.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.tblAttendance.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.tblAttendance.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tblAttendance.horizontalHeader().setVisible(False)
        # self.tblAttendance.setStyleSheet("background-color: black; selection-background-color: #353535; border-radius: 10px")
        # self.tblAttendance.setObjectName("tableWidget")
        # self.tblAttendance.setRowCount(0)
        # self.tblAttendance.horizontalHeader().resizeSection(0, 188)
        # self.tblAttendance.horizontalHeader().resizeSection(1, 155)
        # self.tblAttendance.horizontalHeader().resizeSection(2, 250)
        # self.tblAttendance.horizontalHeader().resizeSection(3, 66)
        # self.tblAttendance.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.tblAttendance.setSortingEnabled(True)
        self.tblAttendance.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblAttendance.verticalHeader().setVisible(False)
        self.tblAttendance.setShowGrid(False)
        self.tblAttendance.horizontalHeader().setStretchLastSection(True)
        self.tblAttendance.setColumnWidth(0,80)
        self.tblAttendance.setColumnWidth(1,80)
        self.tblAttendance.setColumnWidth(2,220)
        self.tblAttendance.setColumnWidth(3,170)
        self.tblAttendance.setColumnWidth(4,90)
        self.tblAttendance.setColumnWidth(5,100)
        self.tblAttendance.setColumnWidth(6,200)
        self.tblAttendance.setColumnWidth(7,120)
        self.loadData()
    
    def loadData(self):
        # Find last recorded .csv file
        folder_path = r'Attendance'
        file_type = '\*csv'
        files = glob.glob(folder_path + file_type)
        lastFile = max(files, key=os.path.getctime)

        df = pd.read_csv(lastFile)
        self.tblAttendance.setRowCount(len(df))
        for row in range(len(df)):
            self.tblAttendance.setItem(row,0,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tblAttendance.setItem(row,1,QtWidgets.QTableWidgetItem(str(df.loc[row,'Student_ID'])))
            self.tblAttendance.setItem(row,2,QtWidgets.QTableWidgetItem(df.loc[row,'Student_Name']))
            self.tblAttendance.setItem(row,3,QtWidgets.QTableWidgetItem(str(df.loc[row,'Stu_Contact'])))
            self.tblAttendance.setItem(row,4,QtWidgets.QTableWidgetItem(df.loc[row,'Stu_Course']))
            self.tblAttendance.setItem(row,5,QtWidgets.QTableWidgetItem(df.loc[row,'Stu_Branch']))
            self.tblAttendance.setItem(row,6,QtWidgets.QTableWidgetItem(df.loc[row,'Date']))
            self.tblAttendance.setItem(row,7,QtWidgets.QTableWidgetItem(df.loc[row,'Time']))
        
    def backWindow(self):
        Att=Attendance()
        widget.addWidget(Att)
        widget.setCurrentIndex(widget.currentIndex()+1)

# Main
app=QApplication(sys.argv)
welcome=Main()
widget=QtWidgets.QStackedWidget()
welcome.setFixedHeight(400)
welcome.setFixedWidth(600)
welcome.setWindowFlags(QtCore.Qt.FramelessWindowHint)
welcome.setAttribute(QtCore.Qt.WA_TranslucentBackground)

#Drop Shadow Effect
shadow=QGraphicsDropShadowEffect()
shadow.setBlurRadius(20)
shadow.setXOffset(0)
shadow.setYOffset(0)
shadow.setColor(QColor(0,0,0,60))
welcome.setGraphicsEffect(shadow)
welcome.show()
try:
   sys.exit(app.exec())
except:
   print("Exiting")