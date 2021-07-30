import os
import pickle
import cv2
import logging

class Class:
	'''
		Class model class
	'''

	def __init__(self, id_class=0, label="", id_level=0):
		self.ID_Class = id_class
		self.Label = label
		self.ID_Level = id_level

	def __str__(self, separator=","):
		return f'{self.ID_Class}{separator}{self.Label}{separator}{self.ID_Level}\n'

	def __iter__(self):
		return iter([self.ID_Class, self.Label, self.ID_Level])

class Module:
	'''
		Module model class
	'''

	def __init__(self, id_module=0, label="", id_level=0):
		self.ID_Module = id_module
		self.Label = label
		self.ID_Level = id_level

	def __str__(self, separator=","):
		return f'{self.ID_Module}{separator}{self.Label}{separator}{self.ID_Level}\n'

	def __iter__(self):
		return iter([self.ID_Module, self.Label, self.ID_Level])

class Level:
	'''
		Level model class
	'''

	def __init__(self, id_level=0, label=""):
		self.ID_Level = id_level
		self.Label = label

	def __str__(self, separator=","):
		return f'{self.ID_Level}{separator}{self.Label}\n'

	def __iter__(self):
		return iter([self.ID_Level, self.Label])

class Professor:
	'''
		Professor model class
	'''

	def __init__(self, id_professor=0, name=""):
		self.ID_Professor = id_professor
		self.Name = name

	def __str__(self, separator=","):
		return f'{self.ID_Professor}{separator}{self.Name}\n'

	def __iter__(self):
		return iter([self.ID_Professor, self.Name])

class Seance:
	'''
		Seance model class
	'''

	def __init__(self, id_seance=0, id_classroom=0, date="", starting_hour=0, ending_hour=0, id_module=0, id_class=0, id_professor=0):
		self.ID_Seance = id_seance
		self.ID_Classroom = id_classroom
		self.Date = date
		self.Starting_hour = starting_hour
		self.Ending_hour = ending_hour
		self.ID_Module = id_module
		self.ID_Class = id_class
		self.ID_Professor = id_professor
		
	def __str__(self, separator=","):
		return f'{self.ID_Seance}{separator}{self.ID_Classroom}{separator}{self.Date}{separator}{self.Starting_hour}{separator}{self.Ending_hour}{separator}{self.ID_Module}{separator}{self.ID_Class}{separator}{self.ID_Professor}\n'

	def __iter__(self):
		return iter([self.ID_Seance, self.ID_Classroom, self.Date, self.Starting_hour, self.Ending_hour, self.ID_Module, self.ID_Class, self.ID_Professor])

class Student:
	'''
		Student model class
	'''

	def __init__(self, id_student=0, name="", cne="", id_class=0):
		self.ID_Student = id_student
		self.Name = name
		self.CNE = cne
		self.ID_Class = id_class

	def __str__(self, separator=","):
		return f'{self.ID_Student}{separator}{self.Name}{separator}{self.CNE}{separator}{self.ID_Class}\n'

	def __iter__(self):
		return iter([self.ID_Student, self.Name, self.CNE, self.ID_Class])

class Classroom:
	'''
		Classroom model class
	'''

	def __init__(self, id_classroom=0, label=""):
		self.ID_Classroom = id_classroom
		self.Label = label

	def __str__(self, separator=","):
		return f'{self.ID_Classroom}{separator}{self.Label}\n'

	def __iter__(self):
		return iter([self.ID_Classroom, self.Label])

class Presence:
	'''
		Presence model class
	'''

	def __init__(self, id_presence=0, id_student=0, id_seance=0):
		self.ID_Presence = id_presence
		self.ID_Student = id_student
		self.ID_Seance = id_seance

	def __str__(self, separator=","):
		return f'{self.ID_Presence}{separator}{self.ID_Student}{separator}{self.ID_Seance}\n'

	def __iter__(self):
		return iter([self.ID_Presence, self.ID_Student, self.ID_Seance])

class Detector:
	'''
		Class that manage detection/recognition and trainig methodes
	'''

	def __init__(self, id_class, mode=0):
		self.ID_Class = id_class
		self.Mode = mode
		self.Model = cv2.face.LBPHFaceRecognizer_create()

		try:
			self.face_detector = cv2.CascadeClassifier('Models/haarcascade_frontalface_default.xml')
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.models_folder = "Models/"

		self.class_model = self.models_folder + str(self.ID_Class) + ".yml"

		if self.Mode == 0:
			try:
				self.Model.read(self.class_model)
			except Exception as e:
				logging.warning(f'Error : {e}')

	def FaceDetect(self,img):

		# detectMultiScale(image, scalefactor, minNeighbors)
		#   	scalefactor the smaller scale will increase the number of layers

		face = self.face_detector.detectMultiScale(img, 1.9, 3)
		detected = False

		if len(face) != 0:
			detected = True
			(x,y,w,h) = face[0]
		else:
			(x,y,w,h) = (0,0,0,0)

		return detected,(x,y,w,h)

	def FaceRecognize(self, img):
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		id_std, c = self.Model.predict(gray)
		return id_std

	def UpdateModel(self, ls_img, ls_IDs):

		try:
			self.Model.update(ls_img, ls_IDs)
			self.Model.write(self.class_model)
		except Exception as e:
			logging.warning(f'Error : {e}')

	def TrainModel(self, ls_img, ls_IDs):

		try:
			self.Model.train(ls_img, ls_IDs)
			self.Model.write(self.class_model)
		except Exception as e:
			logging.warning(f'Error : {e}')

	def __str__(self, separator=","):
		if self.Mode == 0:
			return f'Detector for class : {self.ID_Class}\n'
		else :
			return f'Detector is in train mode'

