from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from DAO import *
from Models import *
import numpy as np
from PIL import Image
import pathlib
import logging
import time
import sys
import cv2
import csv
import os

class Ui_MainWindow(QMainWindow):
	
	def __init__(self):

		super().__init__()

		logging.basicConfig(filename='Logging.log', filemode='w', format='%(asctime)s : %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

		logging.info(f'Main Window Started')

		self.connection_manager = ConnectionManager("Database/database.db")

		self.student_dao = StudentDAO(self.connection_manager)
		self.professor_dao = ProfessorDAO(self.connection_manager)
		self.class_dao = ClassDAO(self.connection_manager)
		self.classroom_dao = ClassroomDAO(self.connection_manager)
		self.level_dao = LevelDAO(self.connection_manager)
		self.module_dao = ModuleDAO(self.connection_manager)
		self.presence_dao = PresenceDAO(self.connection_manager)
		self.seance_dao = SeanceDAO(self.connection_manager)

		self.class_ls = self.class_dao.ListClasses()
		self.classroom_ls = self.classroom_dao.ListClassrooms()
		self.module_ls = self.module_dao.ListModules()

		self.setObjectName("MainWindow")
		self.setFixedSize(480, 320)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
		self.setSizePolicy(sizePolicy)
		self.setMaximumSize(QtCore.QSize(480, 320))

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/logo_app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.setWindowIcon(icon)
		self.setStyleSheet("background-color: rgb(128, 163, 200);")

		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(170, 0, 140, 140))
		self.label.setText("")
		self.label.setPixmap(QtGui.QPixmap("icons/logo.png"))
		self.label.setScaledContents(True)
		self.label.setObjectName("label")

		self.new_seance = QtWidgets.QPushButton(self.centralwidget)
		self.new_seance.setGeometry(QtCore.QRect(50, 200, 72, 72))
		self.new_seance.setMaximumSize(QtCore.QSize(72, 72))
		self.new_seance.setMouseTracking(False)
		self.new_seance.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("icons/New.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.new_seance.setIcon(icon1)
		self.new_seance.setIconSize(QtCore.QSize(64, 64))
		self.new_seance.setObjectName("new_seance")
		self.new_seance.clicked.connect(self.AddSeance)

		self.export = QtWidgets.QPushButton(self.centralwidget)
		self.export.setGeometry(QtCore.QRect(204, 200, 72, 72))
		self.export.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("icons/Export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.export.setIcon(icon2)
		self.export.setIconSize(QtCore.QSize(64, 64))
		self.export.setObjectName("export")
		self.export.clicked.connect(self.Export)

		self.more = QtWidgets.QPushButton(self.centralwidget)
		self.more.setGeometry(QtCore.QRect(358, 200, 72, 72))
		self.more.setText("")
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap("icons/More.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.more.setIcon(icon3)
		self.more.setIconSize(QtCore.QSize(64, 64))
		self.more.setObjectName("more")
		self.more.clicked.connect(self.Options)

		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 20))
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)

		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)

		self.add_seance = None
		self.export_data = None
		self.options = None

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("MainWindow", "SmartAbsence"))
		self.new_seance.setToolTip(_translate("MainWindow", "Create new seance"))
		self.new_seance.setStatusTip(_translate("MainWindow", "Create new seance"))
		self.new_seance.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Create new seance</p></body></html>"))
		self.export.setToolTip(_translate("MainWindow", "Export Data"))
		self.export.setStatusTip(_translate("MainWindow", "Export Data"))
		self.export.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Export Data</p></body></html>"))
		self.more.setToolTip(_translate("MainWindow", "Go to more options"))
		self.more.setStatusTip(_translate("MainWindow", "Go to more options"))
		self.more.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Go to more options</p></body></html>"))

	def AddSeance(self):
		if self.add_seance is None:
			self.add_seance = Ui_Add_Seance(self)
			self.add_seance.show()
			self.hide()
		else:
			self.add_seance = None

	def Export(self):
		if self.export_data is None:
			self.export_data = Ui_Export_data(self)
			self.export_data.show()
			self.hide()
		else:
			self.export_data = None

	def Options(self):
		if self.options is None:
			self.options = Ui_Options(self)
			self.options.show()
			self.hide()
		else:
			self.options = None


class Ui_Add_Seance(QWidget):

	def __init__(self, mainwindow):

		logging.info(f'Add Seance window Started')

		super().__init__()
		self.setObjectName("Add_Seance")
		self.setFixedSize(480, 320)

		self.MainWindow = mainwindow

		self.class_dao = mainwindow.class_dao
		self.classroom_dao = mainwindow.classroom_dao
		self.module_dao = mainwindow.module_dao
		self.professor_dao = mainwindow.professor_dao
		self.detection = None

		self.class_ls = self.class_dao.ListClasses()
		self.classroom_ls = self.classroom_dao.ListClassrooms()
		self.module_ls = self.module_dao.ListModules()
		self.professor_ls = self.professor_dao.ListProfessors()


		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/New.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon)

		self.class_value = QtWidgets.QComboBox(self)
		self.class_value.setGeometry(QtCore.QRect(50, 40, 120, 26))
		self.class_value.setObjectName("class_value")
		self.class_value.setMaxVisibleItems(8)
		self.class_value.setStyleSheet("QComboBox { combobox-popup: 0; }")

		for clss in self.class_ls:
			self.class_value.addItem(clss.Label)

		self.class_value.setCurrentIndex(-1)

		self.classroom_value = QtWidgets.QComboBox(self)
		self.classroom_value.setGeometry(QtCore.QRect(310, 40, 120, 26))
		self.classroom_value.setObjectName("classroom_value")
		self.classroom_value.setMaxVisibleItems(8)
		self.classroom_value.setStyleSheet("QComboBox { combobox-popup: 0; }")

		for crm in self.classroom_ls:
			self.classroom_value.addItem(crm.Label)

		self.classroom_value.setCurrentIndex(-1)

		self.module_value = QtWidgets.QComboBox(self)
		self.module_value.setGeometry(QtCore.QRect(50, 100, 120, 26))
		self.module_value.setObjectName("module_value")
		self.module_value.setMaxVisibleItems(8)
		self.module_value.setStyleSheet("QComboBox { combobox-popup: 0; }")

		for mdl in self.module_ls:
			self.module_value.addItem(mdl.Label)

		self.module_value.setCurrentIndex(-1)

		self.professor_value = QtWidgets.QComboBox(self)
		self.professor_value.setGeometry(QtCore.QRect(310, 100, 120, 26))
		self.professor_value.setObjectName("professor_value")
		self.professor_value.setMaxVisibleItems(8)
		self.professor_value.setStyleSheet("QComboBox { combobox-popup: 0; }")

		for prf in self.professor_ls:
			self.professor_value.addItem(prf.Name)

		self.professor_value.setCurrentIndex(-1)

		self.date = QtWidgets.QDateEdit(self)
		self.date.setEnabled(False)
		self.date.setGeometry(QtCore.QRect(240, 150, 120, 26))
		self.date.setObjectName("date")
		self.date.setDateTime(QDateTime.currentDateTime())

		self.start_time = QtWidgets.QTimeEdit(self)
		self.start_time.setGeometry(QtCore.QRect(50, 210, 120, 26))
		self.start_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(8, 0, 0)))
		self.start_time.setMaximumTime(QtCore.QTime(18, 59, 59))
		self.start_time.setMinimumTime(QtCore.QTime(8, 0, 0))
		self.start_time.setObjectName("start_time")

		self.end_time = QtWidgets.QTimeEdit(self)
		self.end_time.setGeometry(QtCore.QRect(310, 210, 120, 26))
		self.end_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(10, 0, 0)))
		self.end_time.setMaximumTime(QtCore.QTime(18, 59, 59))
		self.end_time.setMinimumTime(QtCore.QTime(8, 0, 0))
		self.end_time.setObjectName("end_time")

		self.class_label = QtWidgets.QLabel(self)
		self.class_label.setGeometry(QtCore.QRect(50, 20, 120, 17))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.class_label.setFont(font)
		self.class_label.setAlignment(QtCore.Qt.AlignCenter)
		self.class_label.setObjectName("class_label")

		self.classroom_label = QtWidgets.QLabel(self)
		self.classroom_label.setGeometry(QtCore.QRect(310, 20, 120, 17))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.classroom_label.setFont(font)
		self.classroom_label.setAlignment(QtCore.Qt.AlignCenter)
		self.classroom_label.setObjectName("classroom_label")

		self.module_label = QtWidgets.QLabel(self)
		self.module_label.setGeometry(QtCore.QRect(50, 80, 120, 17))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.module_label.setFont(font)
		self.module_label.setAlignment(QtCore.Qt.AlignCenter)
		self.module_label.setObjectName("module_label")

		self.professor_label = QtWidgets.QLabel(self)
		self.professor_label.setGeometry(QtCore.QRect(310, 80, 120, 17))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.professor_label.setFont(font)
		self.professor_label.setAlignment(QtCore.Qt.AlignCenter)
		self.professor_label.setObjectName("professor_label")

		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setGeometry(QtCore.QRect(110, 150, 120, 26))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.date_label.setFont(font)
		self.date_label.setAlignment(QtCore.Qt.AlignCenter)
		self.date_label.setObjectName("date_label")

		self.end_hour_label = QtWidgets.QLabel(self)
		self.end_hour_label.setGeometry(QtCore.QRect(310, 190, 120, 17))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.end_hour_label.setFont(font)
		self.end_hour_label.setAlignment(QtCore.Qt.AlignCenter)
		self.end_hour_label.setObjectName("end_hour_label")

		self.start_hour_label = QtWidgets.QLabel(self)
		self.start_hour_label.setGeometry(QtCore.QRect(50, 190, 120, 17))
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(True)
		font.setUnderline(False)
		font.setWeight(75)
		font.setStrikeOut(False)
		self.start_hour_label.setFont(font)
		self.start_hour_label.setAlignment(QtCore.Qt.AlignCenter)
		self.start_hour_label.setObjectName("start_hour_label")

		self.start = QtWidgets.QPushButton(self)
		self.start.setGeometry(QtCore.QRect(380, 250, 89, 25))
		self.start.setObjectName("start")
		self.start.clicked.connect(self.Start)

		self.cancel = QtWidgets.QPushButton(self)
		self.cancel.setGeometry(QtCore.QRect(280, 250, 89, 25))
		self.cancel.setObjectName("cancel")
		self.cancel.clicked.connect(self.Cancel)

		self.msg = QMessageBox(self)
		self.msg.setIcon(QMessageBox.Warning)
		self.msg.setWindowTitle("Incomplete data")

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Add_Seance", "Add Seance"))
		self.start.setText(_translate("Add_Seance", "Start"))
		self.cancel.setText(_translate("Add_Seance", "Cancel"))
		self.date.setDisplayFormat(_translate("Add_Seance", "dd/MM/yyyy"))
		self.start_time.setDisplayFormat(_translate("Add_Seance", "hh:mm"))
		self.end_time.setDisplayFormat(_translate("Add_Seance", "hh:mm"))
		self.class_label.setText(_translate("Add_Seance", "Class"))
		self.classroom_label.setText(_translate("Add_Seance", "Calssroom"))
		self.module_label.setText(_translate("Add_Seance", "Module"))
		self.professor_label.setText(_translate("Add_Seance", "Professor"))
		self.date_label.setText(_translate("Add_Seance", "Date :"))
		self.end_hour_label.setText(_translate("Add_Seance", "End Hour"))
		self.start_hour_label.setText(_translate("Add_Seance", "Start Hour"))

	def Start(self):

		if self.class_value.currentIndex() == -1 :
			self.msg.setText("Please chose a class from the list !")
			self.msg.exec_()
		elif self.classroom_value.currentIndex() == -1:
			self.msg.setText("Please chose a classroom from the list !")
			self.msg.exec_()
		elif self.professor_value.currentIndex() == -1:
			self.msg.setText("Please chose a professor from the list !")
			self.msg.exec_()
		elif self.module_value.currentIndex() == -1:
			self.msg.setText("Please chose a module from the list !")
			self.msg.exec_()
		else :

			seance = Seance()
			seance_dao = self.MainWindow.seance_dao

			seance.ID_Seance = seance_dao.last_index + 1
			seance.ID_Class = self.class_ls[self.class_value.currentIndex()].ID_Class
			seance.ID_Classroom = self.classroom_ls[self.classroom_value.currentIndex()].ID_Classroom
			seance.ID_Professor = self.professor_ls[self.professor_value.currentIndex()].ID_Professor
			seance.ID_Module = self.module_ls[self.module_value.currentIndex()].ID_Module
			seance.Date = self.date.date().toString('dd-MM-yyyy')
			seance.Starting_hour = int(self.start_time.time().toString('hh'))
			seance.Ending_hour = int(self.end_time.time().toString('hh'))

			seance_dao.AddSeance(seance)

			if self.detection is None:
				self.detection = Ui_Detection(self.MainWindow, seance.ID_Seance)
				self.detection.show()
				self.hide()
			else:
				self.detection = None

	def Cancel(self):

		logging.info(f'Cancel clicked')

		self.hide()
		self.MainWindow.add_seance = None
		self.MainWindow.show()

class VideoThread(QThread):
	change_pixmap_signal = pyqtSignal(np.ndarray)

	def run(self):
		# capture from web cam
		cap = cv2.VideoCapture(0)
		while True:
			ret, cv_img = cap.read()
			if ret:
				self.change_pixmap_signal.emit(cv_img)

class Ui_Detection(QWidget):

	def __init__(self, mainwindow, id_snc):

		logging.info(f'Detection Window Started')

		super().__init__()

		# create the video capture thread
		self.thread = VideoThread()
		# connect its signal to the update_image slot
		self.thread.change_pixmap_signal.connect(self.update_image)
		# start the thread
		self.thread.start()

		self.capture = np.zeros((100,100,3), np.uint8)

		self.std_dao = mainwindow.student_dao
		self.class_dao = mainwindow.class_dao
		self.presence_dao = mainwindow.presence_dao

		self.detector = Detector(1000, 0)
		self.current_std = Student()
		self.presence = Presence(id_seance = id_snc)
		
		self.pics_ls = []
		self.pics_time = [0.0]
		self.detection_done = True
		self.on_detection = False
		self.presence_ls = []
		self.update_ls = []

		self.MainWindow = mainwindow

		self.setObjectName("Detection")
		self.setFixedSize(480, 320)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/logo_app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon)

		self.camera = QtWidgets.QLabel(self)
		self.camera.setGeometry(QtCore.QRect(8, 8, 220, 260))
		self.camera.setFrameShape(QtWidgets.QFrame.Box)
		self.camera.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.camera.setText("")
		self.camera.setObjectName("camera")

		self.name_label = QtWidgets.QLabel(self)
		self.name_label.setGeometry(QtCore.QRect(240, 20, 67, 20))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.name_label.setFont(font)
		self.name_label.setObjectName("name_label")

		self.cne_label = QtWidgets.QLabel(self)
		self.cne_label.setGeometry(QtCore.QRect(240, 70, 67, 20))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.cne_label.setFont(font)
		self.cne_label.setObjectName("cne_label")

		self.class_label = QtWidgets.QLabel(self)
		self.class_label.setGeometry(QtCore.QRect(240, 120, 67, 20))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.class_label.setFont(font)
		self.class_label.setObjectName("class_label")

		self.name_value = QtWidgets.QLineEdit(self)
		self.name_value.setGeometry(QtCore.QRect(310, 20, 156, 20))
		self.name_value.setReadOnly(True)
		self.name_value.setObjectName("name_value")

		self.cne_value = QtWidgets.QLineEdit(self)
		self.cne_value.setGeometry(QtCore.QRect(310, 70, 156, 20))
		self.cne_value.setReadOnly(True)
		self.cne_value.setObjectName("cne_value")

		self.class_value = QtWidgets.QLineEdit(self)
		self.class_value.setGeometry(QtCore.QRect(310, 120, 156, 20))
		self.class_value.setReadOnly(True)
		self.class_value.setObjectName("class_value")

		self.start_detection = QtWidgets.QPushButton(self)
		self.start_detection.setGeometry(QtCore.QRect(370, 170, 89, 25))
		self.start_detection.setObjectName("start_detection")
		self.start_detection.clicked.connect(self.StartDetection)

		self.correct_detection = QtWidgets.QPushButton(self)
		self.correct_detection.setGeometry(QtCore.QRect(250, 170, 89, 25))
		self.correct_detection.setObjectName("correct_detection")
		self.correct_detection.clicked.connect(self.Edit)

		self.end_detection = QtWidgets.QPushButton(self)
		self.end_detection.setGeometry(QtCore.QRect(310, 230, 89, 25))
		self.end_detection.setObjectName("end_detection")
		self.end_detection.clicked.connect(self.End)

		self.progress_bar = QtWidgets.QProgressBar(self)
		self.progress_bar.setGeometry(QtCore.QRect(140, 145, 200, 30))
		self.progress_bar.setValue(0)
		self.progress_bar.setVisible(False)
		
		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Detection", "Detection Window"))
		self.name_label.setText(_translate("Detection", "Name :"))
		self.cne_label.setText(_translate("Detection", "CNE	:"))
		self.class_label.setText(_translate("Detection", "Class  :"))
		self.correct_detection.setText(_translate("Detection", "Edit"))
		self.start_detection.setText(_translate("Detection", "Start"))
		self.end_detection.setText(_translate("Detection", "End"))

	def update_image(self, cv_img):
		"""Updates the image_label with a new opencv image"""
		qt_img = self.ImageEdits(cv_img)
		self.camera.setPixmap(qt_img)
	
	def ImageEdits(self, cv_img):
		""" Crop and add the green frame"""
		self.capture = cv_img[110:370,210:430]
		cv_img = cv_img[110:370,210:430].copy()
		
		#draw lines
		cv2.line(cv_img,(22,26),(80,26),(11,243,50),3)
		cv2.line(cv_img,(22,26),(22,84),(11,243,50),3)
		cv2.line(cv_img,(140,26),(198,26),(11,243,50),3)
		cv2.line(cv_img,(198,26),(198,84),(11,243,50),3)
		cv2.line(cv_img,(22,176),(22,234),(11,243,50),3)
		cv2.line(cv_img,(22,234),(80,234),(11,243,50),3)
		cv2.line(cv_img,(198,176),(198,234),(11,243,50),3)
		cv2.line(cv_img,(140,234),(198,234),(11,243,50),3)

		if not self.on_detection:
			cv2.putText(cv_img, "Press Start", (35, 130), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

		
		#detect face
		if 1 <= len(self.pics_time) < 6 and not self.detection_done:
			detected, (x,y,w,h) = self.detector.FaceDetect(cv_img)
			if detected:
				time_now = time.time()
				perecedent_time = self.pics_time[len(self.pics_time)-1]
				if len(self.pics_ls) <= 5 and time_now - perecedent_time > 0.5:
					self.pics_ls.append(self.capture)
					self.pics_time.append(time.time())
				cv2.rectangle(cv_img, (x,y), (x+w,y+h), (0,255,0), 2)
		elif len(self.pics_ls) == 5 and not self.detection_done:
			self.Recognize()
			self.detection_done = True

		return self.Convert_CV_QT(cv_img)
		
	def Convert_CV_QT(self, cv_img):
		"""Convert from an opencv image to QPixmap"""
		rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
		h, w, ch = rgb_image.shape
		bytes_per_line = ch * w
		convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
		p = convert_to_Qt_format.scaled(self.camera.size().width(), self.camera.size().height(), Qt.IgnoreAspectRatio)
		
		return QPixmap.fromImage(p)

	def SaveImages(self, cne, id_class):
		for i in range(5):
			try:
				cv2.imwrite(f'DataSet/{id_class}/{cne}/{cne}_{i}_1.png', self.pics_ls[i])
				cv2.imwrite(f'DataSet/{id_class}/{cne}/{cne}_{i}_2.png', cv2.flip(self.pics_ls[i], 1))
			except Exception as e:
				logging.warning(f'Error : {e}')
		
	def StartDetection(self):
		
		if self.cne_value.text():
			self.current_std = self.std_dao.GetStudentByCNE(self.cne_value.text())
			self.NewDetection()
		else:
			self.NewDetection()

	def NewDetection(self):
		if self.current_std.ID_Student not in self.presence_ls:
				self.presence_ls.append(self.current_std.ID_Student)
		self.on_detection = True
		self.ClearFields()
		self.detection_done = False
		self.pics_ls = []
		self.pics_time = [0.0]

	def ClearFields(self):
		self.name_value.setText("")
		self.cne_value.setText("")
		self.class_value.setText("")

	def Recognize(self):
		std_id_ls = []
		for im in self.pics_ls:
			std_id_ls.append(self.detector.FaceRecognize(im))

		std_id = max(set(std_id_ls), key = std_id_ls.count)
		self.current_std = self.std_dao.GetStudent(std_id)
		self.FillFields(self.current_std)
		self.on_detection = False

	def FillFields(self, std):
		self.name_value.setText(std.Name)
		self.cne_value.setText(std.CNE)
		self.class_value.setText(self.class_dao.GetClass(std.ID_Class).Label)

	def Edit(self):
		self.thread.exit()
		self.setDisabled(True)
		cne, state = QInputDialog.getText(self, 'Edit', 'Enter your CNE :')

		if state:
			self.current_std = self.std_dao.GetStudentByCNE(cne)
			self.camera.setPixmap(self.Convert_CV_QT(self.pics_ls[0]))
			self.FillFields(self.current_std)
			self.SaveImages(self.current_std.CNE, self.current_std.ID_Class)
			self.presence_ls.append(self.current_std.ID_Student)
			self.update_ls.append(self.current_std.ID_Student)
			self.setDisabled(False)
			self.NewDetection()
			self.thread.start()
		else:
			self.presence_ls.append(self.current_std.ID_Student)
			self.NewDetection()
			self.setDisabled(False)
			self.thread.start()

	def setDisabled(self, bol):
		self.camera.setEnabled(not bol)
		self.start_detection.setEnabled(not bol)
		self.correct_detection.setEnabled(not bol)
		self.end_detection.setEnabled(not bol)
		self.name_value.setEnabled(not bol)
		self.cne_value.setEnabled(not bol)
		self.class_value.setEnabled(not bol)
		self.name_label.setEnabled(not bol)
		self.cne_label.setEnabled(not bol)
		self.class_label.setEnabled(not bol)
		if bol:
			self.thread.exit()
		else:
			self.thread.start()

	def End(self):
		self.setDisabled(True)
		self.progress_bar.setVisible(True)
		self.NewDetection()
		for id_std in self.presence_ls:
			self.presence.ID_Student = id_std
			self.presence_dao.AddPresence(self.presence)
			self.progress_bar.setValue((50*self.presence_ls.index(id_std))//len(self.presence_ls))

		if len(self.update_ls) != 0:
			imgs_ls = []
			ids_ls = []

			for id_std in self.update_ls:
				std = self.std_dao.GetStudent(id_std)
				for i in range(5):
					path_1 = f'DataSet/{std.ID_Class}/{std.CNE}/{std.CNE}_{i}_1.png'
					path_2 = f'DataSet/{std.ID_Class}/{std.CNE}/{std.CNE}_{i}_2.png'
					imgs_ls.append(np.array(Image.open(path_1).convert('L'),'uint8'))
					imgs_ls.append(np.array(Image.open(path_2).convert('L'),'uint8'))
					ids_ls.append(std.ID_Student)
					ids_ls.append(std.ID_Student)
				self.progress_bar.setValue(((25*self.update_ls.index(id_std))//len(self.update_ls))+50)
			
			self.detector.UpdateModel(imgs_ls, np.array(ids_ls))

		for i in range(4):
			time.sleep(0.3)
			self.progress_bar.setValue(((25*i)//4)+75)

		logging.info(f'End of detection')
		self.progress_bar.setVisible(False)
		self.hide()
		self.MainWindow.show()

class Ui_Export_data(QWidget):

	def __init__(self, mainwindow):

		logging.info(f'Export Window Started')

		super().__init__()

		self.columns = ["Classroom","Class","Module","Professor","Start Hour","End Hour"]

		self.class_dao = mainwindow.class_dao
		self.classroom_dao = mainwindow.classroom_dao
		self.module_dao = mainwindow.module_dao
		self.professor_dao = mainwindow.professor_dao
		self.seance_dao = mainwindow.seance_dao
		self.student_dao = mainwindow.student_dao
		self.presence_dao = mainwindow.presence_dao

		self.class_ls = self.class_dao.ListClasses()
		self.classroom_ls = self.classroom_dao.ListClassrooms()
		self.module_ls = self.module_dao.ListModules()
		self.professor_ls = self.professor_dao.ListProfessors()
		self.seance_ls = self.seance_dao.ListSeances()

		self.current_seances = []

		self.MainWindow = mainwindow

		self.setObjectName("export_data")
		self.setFixedSize(480, 320)

		self.date_value = QtWidgets.QDateEdit(self)
		self.date_value.setGeometry(QtCore.QRect(80, 30, 110, 26))
		self.date_value.setCalendarPopup(True)
		self.date_value.setObjectName("date_value")
		self.date_value.dateChanged.connect(self.List_seances)

		self.seances_table = QtWidgets.QTableWidget(self)
		self.seances_table.setGeometry(QtCore.QRect(10, 70, 451, 181))
		self.seances_table.setObjectName("seances_table")
		self.seances_table.setColumnCount(6)

		for i in range(6):
			item = QtWidgets.QTableWidgetItem()
			self.seances_table.setHorizontalHeaderItem(i, item)

		self.class_value = QtWidgets.QComboBox(self)
		self.class_value.setGeometry(QtCore.QRect(300, 30, 161, 25))
		self.class_value.setObjectName("class_value")

		for clss in self.class_ls:
			self.class_value.addItem(clss.Label)

		self.class_value.setCurrentIndex(-1)
		self.class_value.currentIndexChanged.connect(self.List_seances)

		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setGeometry(QtCore.QRect(0, 30, 67, 26))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.date_label.setFont(font)
		self.date_label.setAlignment(QtCore.Qt.AlignCenter)
		self.date_label.setObjectName("date_label")

		self.class_label = QtWidgets.QLabel(self)
		self.class_label.setGeometry(QtCore.QRect(220, 30, 67, 26))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.class_label.setFont(font)
		self.class_label.setAlignment(QtCore.Qt.AlignCenter)
		self.class_label.setObjectName("class_value")

		self.export_data_button = QtWidgets.QPushButton(self)
		self.export_data_button.setGeometry(QtCore.QRect(370, 270, 89, 25))
		self.export_data_button.setObjectName("export_data")
		self.export_data_button.clicked.connect(self.Export_csv)

		self.cancel = QtWidgets.QPushButton(self)
		self.cancel.setGeometry(QtCore.QRect(260, 270, 89, 25))
		self.cancel.setObjectName("cancel")
		self.cancel.clicked.connect(self.Cancel)

		self.msg = QMessageBox(self)
		self.msg.setIcon(QMessageBox.Warning)
		self.msg.setWindowTitle("No seance selected")

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("export_data", "Export CSV"))
		self.date_value.setDisplayFormat(_translate("export_data", "dd/MM/yyyy"))
		self.date_label.setText(_translate("export_data", "Date :"))
		self.class_label.setText(_translate("export_data", "Class :"))
		self.export_data_button.setText(_translate("export_data", "Export"))
		self.cancel.setText(_translate("export_data", "Cancel"))
		self.seances_table.setHorizontalHeaderLabels(self.columns)

	def Cancel(self):
		logging.info(f'Cancel clicked')
		self.hide()
		self.MainWindow.export_data = None
		self.MainWindow.show()

	def AddItem(self, seance):
		lastRow = self.seances_table.rowCount()
		self.seances_table.insertRow(lastRow)
		for classroom in self.classroom_ls:
			if classroom.ID_Classroom == seance.ID_Classroom:
				self.seances_table.setItem(lastRow , 0, QtWidgets.QTableWidgetItem(classroom.Label))

		for clss in self.class_ls:
			if clss.ID_Class == seance.ID_Class:
				self.seances_table.setItem(lastRow , 1, QtWidgets.QTableWidgetItem(clss.Label))

		for module in self.module_ls:
			if module.ID_Module == seance.ID_Module:
				self.seances_table.setItem(lastRow , 2, QtWidgets.QTableWidgetItem(module.Label))

		for prf in self.professor_ls:
			if prf.ID_Professor == seance.ID_Professor:
				self.seances_table.setItem(lastRow , 3, QtWidgets.QTableWidgetItem(prf.Name))

		self.seances_table.setItem(lastRow , 4, QtWidgets.QTableWidgetItem(str(seance.Starting_hour)))
		self.seances_table.setItem(lastRow , 5, QtWidgets.QTableWidgetItem(str(seance.Ending_hour)))

	def List_seances(self):
		self.seances_table.setRowCount(0) #empty table
		self.current_seances = []

		if self.class_value.currentIndex() == -1:
			for seance in self.seance_ls:
				if seance.Date == self.date_value.date().toString('dd-MM-yyyy'):
					self.current_seances.append(seance)
					self.AddItem(seance)			
		else :
			self.seances_table.setRowCount(0)
			for seance in self.seance_ls:
				if seance.Date == self.date_value.date().toString('dd-MM-yyyy') and seance.ID_Class == self.class_ls[self.class_value.currentIndex()].ID_Class:
					self.current_seances.append(seance)
					self.AddItem(seance)

	def Export_csv(self):

		if len(self.seances_table.selectedIndexes()) != 0:
			filePath, _ = QFileDialog.getSaveFileName(self,"Path")
			if filePath:
				if ".csv" not in filePath:
					filePath += '.csv'
				file = open(filePath, 'a')
				file.write("Name,CNE,Presence\n")
				presence_ls = self.presence_dao.GetPresences(self.current_seances[self.seances_table.selectedIndexes()[0].row()].ID_Seance)
				present_ls = []
				students_ls = self.student_dao.ListStudentsByClass(self.current_seances[self.seances_table.selectedIndexes()[0].row()].ID_Class)
				for std in students_ls:
					for prs in presence_ls:
						if prs.ID_Student == std.ID_Student:
							present_ls.append(prs.ID_Student)

					if std.ID_Student in present_ls:
						file.write(f'{std.Name},{std.CNE},Present\n')
					else:
						file.write(f'{std.Name},{std.CNE},Absent\n')

				file.close()

			else:
				self.msg.setText("Please set a file path to export data !")
				self.msg.exec_()
		else:
			self.msg.setText("Please chose a seance from the list !")
			self.msg.exec_()

		file.close()

class Ui_Options(QWidget):

	def __init__(self, mainwindow):

		logging.info(f'Options Window Started')

		super().__init__()

		self.student_dao = mainwindow.student_dao
		self.professor_dao = mainwindow.professor_dao
		self.class_dao = mainwindow.class_dao
		self.classroom_dao = mainwindow.classroom_dao
		self.level_dao = mainwindow.level_dao
		self.module_dao = mainwindow.module_dao
		self.presence_dao = mainwindow.presence_dao
		self.seance_dao = mainwindow.seance_dao

		self.class_ls = self.class_dao.ListClasses()
		self.table_ls = mainwindow.connection_manager.List_tables()

		self.separators = [",",";","tab","|"]

		self.MainWindow = mainwindow
		self.setFixedSize(480, 320)

		self.tabs = QtWidgets.QTabWidget(self)
		self.tabs.setGeometry(QtCore.QRect(0, 0, 480, 280))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.tabs.setFont(font)
		self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
		self.tabs.setObjectName("tabs")

		self.training = QtWidgets.QWidget()
		self.training.setObjectName("training")

		self.path_label_training = QtWidgets.QLabel(self.training)
		self.path_label_training.setGeometry(QtCore.QRect(10, 60, 140, 25))
		self.path_label_training.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.path_label_training.setObjectName("path_label_training")

		self.path_value_training = QtWidgets.QLineEdit(self.training)
		self.path_value_training.setEnabled(True)
		self.path_value_training.setGeometry(QtCore.QRect(10, 100, 381, 26))
		self.path_value_training.setObjectName("path_value_training")

		call_for_training = partial(self.Browse, 0)

		self.browseButton_training = QtWidgets.QPushButton(self.training)
		self.browseButton_training.setGeometry(QtCore.QRect(400, 100, 64, 26))
		self.browseButton_training.setObjectName("browseButton_training")
		self.browseButton_training.clicked.connect(call_for_training)

		self.training_button = QtWidgets.QPushButton(self.training)
		self.training_button.setGeometry(QtCore.QRect(340, 210, 100, 26))
		self.training_button.setObjectName("training_button")
		self.training_button.clicked.connect(self.Training)
		
		self.data = QtWidgets.QWidget()
		self.data.setObjectName("data")

		self.table_grp = QtWidgets.QGroupBox(self.data)
		self.table_grp.setGeometry(QtCore.QRect(120, 30, 230, 80))
		self.table_grp.setCheckable(True)
		self.table_grp.setChecked(False)
		self.table_grp.setObjectName("table_grp")

		self.table_label = QtWidgets.QLabel(self.table_grp)
		self.table_label.setGeometry(QtCore.QRect(10, 40, 67, 26))
		self.table_label.setObjectName("table_label")

		self.table_value = QtWidgets.QComboBox(self.table_grp)
		self.table_value.setGeometry(QtCore.QRect(70, 40, 150, 26))
		self.table_value.setObjectName("table_value")

		for table in self.table_ls:
			self.table_value.addItem(table)

		self.table_value.setCurrentIndex(-1)

		self.separator_label = QtWidgets.QLabel(self.data)
		self.separator_label.setGeometry(QtCore.QRect(120, 150, 114, 26))
		self.separator_label.setObjectName("separator_label")

		self.separator_value = QtWidgets.QComboBox(self.data)
		self.separator_value.setGeometry(QtCore.QRect(240, 150, 100, 26))
		self.separator_value.setObjectName("separator_value")

		for sep in self.separators:
			self.separator_value.addItem(sep)

		self.separator_value.setCurrentIndex(-1)

		self.raw_checkBox = QtWidgets.QCheckBox(self.data)
		self.raw_checkBox.setGeometry(QtCore.QRect(30, 190, 140, 23))
		self.raw_checkBox.setObjectName("raw_checkBox")

		self.export_button_data = QtWidgets.QPushButton(self.data)
		self.export_button_data.setGeometry(QtCore.QRect(250, 210, 90, 25))
		self.export_button_data.setObjectName("export_button_data")
		self.export_button_data.clicked.connect(self.Export_data)

		self.import_button_data = QtWidgets.QPushButton(self.data)
		self.import_button_data.setGeometry(QtCore.QRect(360, 210, 90, 25))
		self.import_button_data.setObjectName("import_button_data")
		self.import_button_data.clicked.connect(self.Import_data)

		self.tabs.addTab(self.training, "")
		self.tabs.addTab(self.data, "")
		self.tabs.setCurrentIndex(0)

		self.cancel = QtWidgets.QPushButton(self)
		self.cancel.setGeometry(QtCore.QRect(20, 285, 90, 24))
		self.cancel.setObjectName("cancel")
		self.cancel.clicked.connect(self.Cancel)

		self.progress_bar = QtWidgets.QProgressBar(self)
		self.progress_bar.setGeometry(QtCore.QRect(140, 145, 200, 30))
		self.progress_bar.setValue(0)
		self.progress_bar.setVisible(False)

		self.msg = QMessageBox(self)
		self.msg.setIcon(QMessageBox.Warning)
		self.msg.setWindowTitle("Warning")

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Options", "Options"))
		self.training_button.setText(_translate("Options", "Training"))
		self.browseButton_training.setText(_translate("Options", "Browse"))
		self.path_label_training.setText(_translate("Options", "Path to Images :"))
		self.tabs.setTabText(self.tabs.indexOf(self.training), _translate("Options", "Training"))
		self.import_button_data.setText(_translate("Options", "Import"))
		self.separator_label.setText(_translate("Options", "Separated By :"))
		self.table_grp.setTitle(_translate("Options", "Process a unique table"))
		self.table_label.setText(_translate("Options", "Table :"))
		self.export_button_data.setText(_translate("Options", "Export"))
		self.tabs.setTabText(self.tabs.indexOf(self.data), _translate("Options", "Data"))
		self.raw_checkBox.setText(_translate("Options", "Import raw"))
		self.cancel.setText(_translate("Options", "Cancel"))

	def Cancel(self):
		logging.info(f'Cancel clicked')
		self.hide()
		self.MainWindow.options = None
		self.MainWindow.show()

	def Browse(self, state):
		directory = QFileDialog.getExistingDirectory(self, "Select Directory","",QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		if state == 0:
			self.path_value_training.setText(directory)
		elif state == 1:
			return directory

	def Training(self):
		logging.info(f'Training Started')
		path = self.path_value_training.text()
		if path:
			self.training.setEnabled(False)
			self.progress_bar.setVisible(True)
			cne_ls = os.listdir(path)
			imgs_ls = []
			ids_ls = []
			classes = {}

			#to orgnize folders by student's classes
			for cne in cne_ls:
				std = self.student_dao.GetStudentByCNE(cne)
				if std.ID_Class not in classes:
					classes[std.ID_Class] = [std]
				else:
					classes[std.ID_Class].append(std)

				self.progress_bar.setValue(((50*cne_ls.index(cne))//len(cne_ls)))

			keys = list(classes.keys()) #because of the progress bar
			for clss in keys:
				detector = Detector(clss, mode=1)
				for std in classes[clss]:
					student_path = path+"/"+std.CNE
					imgs_files = os.listdir(student_path)
					for im in imgs_files:
						imagePath = student_path+"/"+im
						imgs_ls.append(np.array(Image.open(imagePath).convert('L'),'uint8'))
						ids_ls.append(std.ID_Student)

				detector.TrainModel(imgs_ls, np.array(ids_ls))
				self.progress_bar.setValue(((50*keys.index(clss))//len(keys))+50)

			logging.info(f'Training ended')
			self.progress_bar.setVisible(False)
			self.training.setEnabled(True)
		else:
			self.msg.setText("Please enter a path !")
			self.msg.exec_()

	def Export_data(self):
		path = self.Browse(1)

		logging.info(f'Exporting data to {path}')
		
		if self.separator_value.currentIndex() == -1 or self.separator_value.currentText() == "tab":
			separator = "\t"
		else: 
			separator = self.separator_value.currentText()

		self.progress_bar.setVisible(True)
		
		if not self.table_grp.isChecked():
			time.sleep(0.3)
			self.Export_Students(separator, path)
			self.progress_bar.setValue(12)
			self.Export_Classes(separator, path)
			self.progress_bar.setValue(25)
			self.Export_Modules(separator, path)
			self.progress_bar.setValue(37)
			self.Export_Levels(separator, path)
			self.progress_bar.setValue(50)
			self.Export_Professors(separator, path)
			self.progress_bar.setValue(62)
			self.Export_Classrooms(separator, path)
			self.progress_bar.setValue(75)
			self.Export_Seances(separator, path)
			self.progress_bar.setValue(87)
			self.Export_Presences(separator, path)
			self.progress_bar.setValue(100)
			time.sleep(0.3)
		else:
			if self.table_value.currentText() == "Students" : 
				self.Export_Students(separator, path)
				self.progress_bar.setValue(100)

		self.progress_bar.setVisible(False)

	def Export_Students(self, separator, path):
		with open(path+"/"+"Students.csv", 'w') as students_csv:
			student_str = "ID_Student" + separator + "Name" + separator + "CNE" + separator + "ID_Class" + "\n"
			students_csv.write(student_str)
			csv_writer = csv.writer(students_csv, delimiter=separator)
			std_ls = self.student_dao.ListStudents()
			for std in std_ls:
				csv_writer.writerow(std)
		students_csv.close()

	def Export_Classes(self, separator, path):
		with open(path+"/"+"Classes.csv", "a") as class_csv:
			class_str = "ID_Class" + separator + "Label" + separator + "ID_Level" + "\n"
			class_csv.write(class_str)
			csv_writer = csv.writer(class_csv, delimiter=separator)
			class_ls = self.class_dao.ListClasses()
			for clss in class_ls:
				csv_writer.writerow(clss)		
		class_csv.close()

	def Export_Modules(self, separator, path):
		with open(path+"/"+"Modules.csv", "a") as module_csv:
			module_str = "ID_Module" + separator + "Label" + separator + "ID_Level" + "\n"
			module_csv.write(module_str)
			csv_writer = csv.writer(module_csv, delimiter=separator)
			module_ls = self.module_dao.ListModules()
			for mdl in module_ls:
				csv_writer.writerow(mdl)
		module_csv.close()

	def Export_Levels(self, separator, path):
		with open(path+"/"+"Levels.csv", "a") as level_csv:
			level_str = "ID_Level" + separator + "Label" + "\n"
			level_csv.write(level_str)
			csv_writer = csv.writer(level_csv, delimiter=separator)
			level_ls = self.level_dao.ListLevels()
			for lvl in level_ls:
				csv_writer.writerow(lvl)
		level_csv.close()

	def Export_Professors(self, separator, path):
		with open(path+"/"+"Professors.csv", "a") as professor_csv:
			professor_str = "ID_Professor" + separator + "Name" + "\n"
			professor_csv.write(professor_str)
			csv_writer = csv.writer(professor_csv, delimiter=separator)
			professor_ls = self.professor_dao.ListProfessors()
			for prf in professor_ls:
				csv_writer.writerow(prf)
		professor_csv.close()

	def Export_Classrooms(self, separator, path):
		with open(path+"/"+"Classrooms.csv", "a") as classroom_csv:
			classroom_str = "ID_Classroom" + separator + "Label" + "\n"
			classroom_csv.write(classroom_str)
			csv_writer = csv.writer(classroom_csv, delimiter=separator)
			classroom_ls = self.classroom_dao.ListClassrooms()
			for clssrm in classroom_ls:
				csv_writer.writerow(clssrm)
		classroom_csv.close()

	def Export_Seances(self, separator, path):
		with open(path+"/"+"Seances.csv", "a") as seance_csv:
			seance_str = "ID_Seance" + separator + "ID_Classroom" + separator + "Date" + separator + "Starting_hour" + separator + "Ending_hour" + separator + "ID_Module" + separator + "ID_Class" + separator + "ID_Professor" + "\n"
			seance_csv.write(seance_str)
			csv_writer = csv.writer(seance_csv, delimiter=separator)
			seance_ls = self.seance_dao.ListSeances()
			for snc in seance_ls:
				csv_writer.writerow(snc)
		seance_csv.close()

	def Export_Presences(self, separator, path):
		with open(path+"/"+"Presences.csv", "a") as presence_csv:
			presence_str = "ID_Presence" + separator + "ID_Student" + separator + "ID_Seance" + "\n"
			presence_csv.write(presence_str)
			csv_writer = csv.writer(presence_csv, delimiter=separator)
			presence_ls = self.presence_dao.ListPresences()
			for prnc in presence_ls:
				csv_writer.writerow(prnc)
		presence_csv.close()

	def Import_data(self):
		files, _ = QFileDialog.getOpenFileNames(self,"Select one or more files to import from","","CSV (*.csv)")
		logging.info(f'Importing data from {files}')
		for file in files:
			path = pathlib.Path(file)
			if path.name == "Students.csv":
				if self.raw_checkBox.isChecked():
					self.Import_Students(path, 1)
				else :
					self.Import_Students(path, 0)
			elif path.name == "Classes.csv":
				self.Import_Classes(path)
			elif path.name == "Professors.csv":
				self.Import_Professors(path)
			else:
				self.msg.setText('Please choose proper files !')
				self.msg.exec_()

	def Import_Students(self, path, state):
		with open(str(path), "r") as student_csv:
			dialect = csv.Sniffer().sniff(student_csv.read(1024), delimiters=";,|\t")
			student_csv.seek(0)
			csv_reader = csv.reader(student_csv, dialect)
			header = next(csv_reader)
			if header != None:
				for row in csv_reader:
					if self.student_dao.GetStudentByCNE(row[2]):
						print(f"student {row[1]} already exists !")
					else:
						if state == 0:
							self.student_dao.AddStudent(Student(row[0],row[1],row[2],row[3]))
						else :
							class_id = self.class_dao.GetClassByLabel(row[2]).ID_Class
							self.student_dao.AddStudent(Student(0,row[0],row[1],class_id))

	def Import_Classes(self, path):
		with open(str(path), "r") as class_csv:
			dialect = csv.Sniffer().sniff(class_csv.read(1024), delimiters=";,|\t")
			class_csv.seek(0)
			csv_reader = csv.reader(class_csv, dialect)
			header = next(csv_reader)
			if header != None:
				for row in csv_reader:
					if self.class_dao.GetClassByLabel(row[1]):
						print(f"class {row[1]} already exists !")
					else:
						self.class_dao.AddClass(Class(row[0],row[1],row[2]))

	def Import_Professors(self, path):
		with open(str(path), "r") as professor_csv:
			dialect = csv.Sniffer().sniff(professor_csv.read(1024), delimiters=";,|\t")
			professor_csv.seek(0)
			csv_reader = csv.reader(professor_csv, dialect)
			header = next(csv_reader)
			if header != None:
				for row in csv_reader:
					if self.professor_dao.GetProfessorByName(row[1]):
						print(f"professor {row[1]} already exists !")
					else:
						self.professor_dao.AddProfessor(Professor(row[0],row[1]))

	def Import_Modules(self, path):
		with open(str(path), "r") as module_csv:
			dialect = csv.Sniffer().sniff(module_csv.read(1024), delimiters=";,|\t")
			module_csv.seek(0)
			csv_reader = csv.reader(module_csv, dialect)
			header = next(csv_reader)
			if header != None:
				for row in csv_reader:
					if self.module_dao.GetModuleByLabel(row[1]):
						print(f"module {row[1]} already exists !")
					else:
						self.module_dao.AddModule(Module(row[0],row[1],row[2]))

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	ui = Ui_MainWindow()
	ui.show()
	sys.exit(app.exec_())