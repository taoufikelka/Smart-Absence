from Models import *
import sqlite3
import logging

class ConnectionManager:

	def __init__(self, db_file):
		
		self.connection = None
		try:
			self.connection = sqlite3.connect(db_file)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.cursor = self.connection.cursor()


	def List_tables(self):
		cursor = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = [
			v[0] for v in cursor.fetchall()
			if v[0] != "sqlite_sequence"
		]
		return tables

class ClassDAO:
	'''
		Class data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Class) FROM Classes").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddClass(self, clss):
		self.last_index += 1
		insert_query = "INSERT INTO Classes (ID_Class, Label, ID_Level) VALUES (?, ?, ?)"
		values = (self.last_index, clss.Label, clss.ID_Level)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteClass(self, c_ind):
		delete_query = "DELETE FROM Classes WHERE ID_Class = ?"
		search_query = "SELECT ID_Class FROM Classes WHERE ID_Class > ?"

		try:
			self.cursor.execute(delete_query, (c_ind,))
			self.conman.connection.commit()
			next_classes = self.cursor.execute(search_query, (c_ind,)).fetchall()
			for i in next_classes:
				new_id = i[0] - 1
				update_query = "UPDATE Classes SET ID_Class = ? WHERE ID_Class = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateClass(self, clss):
		update_query = "UPDATE Classes SET Label = ?, ID_Level = ? WHERE ID_Class = ?"
		values = (clss.Label, clss.ID_Level, clss.ID_Class)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def GetClass(self, id_class):
		search_query = "SELECT * FROM Classes WHERE ID_Class = ?"

		try:
			clss = self.cursor.execute(search_query,(id_class,)).fetchall()[0]
		except:
			logging.warning(f'Error : {e}')

		return Class(id_class, clss[1], clss[2])

	def GetClassByLabel(self, label):
		search_query = "SELECT  * FROM Classes WHERE Label = ?"

		try:
			cursor_result = self.cursor.execute(search_query,(label,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')
		
		if cursor_result != []:
			cl = cursor_result[0]
			return Class(cl[0], cl[1], cl[2])
		else:
			return False

	def ListClasses(self):
		select_query = "SELECT * FROM Classes"
		cls_obj_ls = []

		try:
			classes_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for cl in classes_list:
			cls_obj_ls.append(Class(cl[0], cl[1], cl[2]))

		return cls_obj_ls

class LevelDAO:
	'''
		Level data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Level) FROM Levels").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddLevel(self, lvl):
		self.last_index += 1
		insert_query = "INSERT INTO Levels (ID_Level, Label) VALUES (?, ?)"
		values = (self.last_index, lvl.Label)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteLevel(self, l_ind):
		delete_query = "DELETE FROM Levels WHERE ID_Level = ?"
		search_query = "SELECT ID_Level FROM Levels WHERE ID_Level > ?"

		try:
			self.cursor.execute(delete_query, (l_ind,))
			self.conman.connection.commit()
			next_levels = self.cursor.execute(search_query, (l_ind,)).fetchall()
			for i in next_levels:
				new_id = i[0] - 1
				update_query = "UPDATE Levels SET ID_Level = ? WHERE ID_Level = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateLevel(self, lvl):
		update_query = "UPDATE Levels SET Label = ? WHERE ID_Level = ?"
		values = (lvl.Label, lvl.ID_Level)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def ListLevels(self):
		select_query = "SELECT * FROM Levels"
		lvl_obj_ls = []

		try:
			levels_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for lvl in levels_list:
			lvl_obj_ls.append(Level(lvl[0], lvl[1]))


		return lvl_obj_ls

class ModuleDAO:
	'''
		Module data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Module) FROM Modules").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddModule(self, mdl):
		self.last_index += 1
		insert_query = "INSERT INTO Modules (ID_Module, Label, ID_Level) VALUES (?, ?, ?)"
		values = (self.last_index, mdl.Label, mdl.ID_Level)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteModule(self, m_ind):
		delete_query = "DELETE FROM Modules WHERE ID_Module = ?"
		search_query = "SELECT ID_Module FROM Modules WHERE ID_Module > ?"

		try:
			self.cursor.execute(delete_query, (m_ind,))
			self.conman.connection.commit()
			next_modules = self.cursor.execute(search_query, (m_ind,)).fetchall()
			for i in next_modules:
				new_id = i[0] - 1
				update_query = "UPDATE Modules SET ID_Module = ? WHERE ID_Module = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateModule(self, mdl):
		update_query = "UPDATE Modules SET Label = ?, ID_Level = ? WHERE ID_Module = ?"
		values = (mdl.Label, mdl.ID_Level, mdl.ID_Module)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def GetModuleByLabel(self, label):
		search_query = "SELECT  * FROM Modules WHERE Label = ?"

		try:
			cursor_result = self.cursor.execute(search_query,(label,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')
		
		if cursor_result != []:
			mdl = cursor_result[0]
			return Module(mdl[0], mdl[1], mdl[2])
		else:
			return False

	def ListModules(self):
		select_query = "SELECT * FROM Modules"
		mdl_obj_ls = []

		try:
			modules_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for md in modules_list:
			mdl_obj_ls.append(Module(md[0], md[1], md[2]))

		return mdl_obj_ls

class PresenceDAO:
	'''
		Presence data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Presence) FROM Presences").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddPresence(self, prs):
		self.last_index += 1
		insert_query = "INSERT INTO Presences (ID_Presence, ID_Student, ID_Seance) VALUES (?, ?, ?)"
		values = (self.last_index, prs.ID_Student, prs.ID_Seance)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeletePresence(self, p_ind):
		delete_query = "DELETE FROM Presences WHERE ID_Presence = ?"
		search_query = "SELECT ID_Presence FROM Presences WHERE ID_Presence > ?"

		try:
			self.cursor.execute(delete_query, (p_ind,))
			self.conman.connection.commit()
			next_presences = self.cursor.execute(search_query, (p_ind,)).fetchall()
			for i in next_presences:
				new_id = i[0] - 1
				update_query = "UPDATE Presences SET ID_Presence = ? WHERE ID_Presence = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdatePresence(self, prs):
		update_query = "UPDATE Presences SET ID_Student = ?, ID_Seance = ? WHERE ID_Presence = ?"
		values = (prs.ID_Student, prs.ID_Seance, prs.ID_Presence)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def GetPresences(self, seance_id):
		select_query = "SELECT * FROM Presences WHERE ID_Seance = ?"
		prs_obj_ls = []
		
		try:
			presences_list = self.cursor.execute(select_query, (seance_id,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for prs in presences_list:
			prs_obj_ls.append(Presence(prs[0], prs[1], prs[2]))

		return prs_obj_ls

	def ListPresences(self):
		select_query = "SELECT * FROM Presences"
		prs_obj_ls = []

		try:
			presences_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for prs in presences_list:
			prs_obj_ls.append(Presence(prs[0], prs[1], prs[2]))

		return prs_obj_ls

class SeanceDAO:
	'''
		Seance data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Seance) FROM Seances").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddSeance(self, snc):
		self.last_index += 1
		insert_query = "INSERT INTO Seances (ID_Seance, ID_Classroom, Date, Starting_hour, Ending_hour, ID_Module, ID_Class, ID_Professor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
		values = (self.last_index, snc.ID_Classroom, snc.Date, snc.Starting_hour, snc.Ending_hour, snc.ID_Module, snc.ID_Class, snc.ID_Professor)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteSeance(self, s_ind):
		delete_query = "DELETE FROM Seances WHERE ID_Seance = ?"
		search_query = "SELECT ID_Seance FROM Seances WHERE ID_Seance > ?"

		try:
			self.cursor.execute(delete_query, (s_ind,))
			self.conman.connection.commit()
			next_seances = self.cursor.execute(search_query, (s_ind,)).fetchall()
			for i in next_seances:
				new_id = i[0] - 1
				update_query = "UPDATE Seances SET ID_Seance = ? WHERE ID_Seance = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateSeance(self, snc):
		update_query = "UPDATE Seances SET ID_Classroom = ?, Date = ?, Starting_hour = ?, Ending_hour = ?, ID_Module = ?, ID_Class = ?, ID_Professor = ? WHERE ID_Seance = ?"
		values = (snc.ID_Classroom, snc.Date, snc.Starting_hour, snc.Ending_hour, snc.ID_Module, snc.ID_Class, snc.ID_Professor, snc.ID_Seance)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def ListSeances(self):
		select_query = "SELECT * FROM Seances"
		snc_obj_ls = []

		try:
			seances_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for scn in seances_list:
			snc_obj_ls.append(Seance(scn[0],scn[1],scn[2],scn[3],scn[4],scn[5],scn[6],scn[7]))

		return snc_obj_ls

class StudentDAO:
	'''
		Student data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Student) FROM Students").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddStudent(self, std):
		self.last_index += 1
		insert_query = "INSERT INTO Students (ID_Student, Name, CNE, ID_Class) VALUES (?, ?, ?, ?)"
		values = (self.last_index, std.Name, std.CNE, std.ID_Class)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteStudent(self, s_ind):
		delete_query = "DELETE FROM Students WHERE ID_Student = ?"
		search_query = "SELECT ID_Student FROM Students WHERE ID_Student > ?"

		try:
			self.cursor.execute(delete_query, (s_ind,))
			self.conman.connection.commit()
			next_students = self.cursor.execute(search_query, (s_ind,)).fetchall()
			for i in next_students:
				new_id = i[0] - 1
				update_query = "UPDATE Students SET ID_Student = ? WHERE ID_Student = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateStudent(self, std):
		update_query = "UPDATE Students SET Name = ?, CNE = ?, ID_Class = ? WHERE ID_Student = ?"
		values = (std.Name, std.CNE, std.ID_Class, std.ID_Student)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def GetStudent(self, s_ind):
		search_query = "SELECT * FROM Students WHERE ID_Student = ?"

		try:
			std = self.cursor.execute(search_query,(s_ind,)).fetchall()[0]
		except Exception as e:
			logging.warning(f'Error : {e}')
		
		return Student(s_ind, std[1], std[2], std[3])

	def GetStudentByCNE(self, cne):
		search_query = "SELECT * FROM Students WHERE CNE = ?"

		try:
			cursor_result = self.cursor.execute(search_query,(cne,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')
		
		if cursor_result != []:
			std = cursor_result[0]
			return Student(std[0], std[1], cne, std[3])
		else:
			return False

	def ListStudentsByClass(self, class_id):
		select_query = "SELECT * FROM Students WHERE ID_Class = ?"
		std_obj_ls = []

		try:
			students_list = self.cursor.execute(select_query, (class_id,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for std in students_list:
			std_obj_ls.append(Student(std[0], std[1], std[2], std[3]))

		return std_obj_ls

	def ListStudents(self):
		select_query = "SELECT * FROM Students"
		std_obj_ls = []

		try:
			students_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for std in students_list:
			std_obj_ls.append(Student(std[0], std[1], std[2], std[3]))

		return std_obj_ls

class ProfessorDAO:
	'''
		Professor data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Professor) FROM Professors").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddProfessor(self, prf):
		self.last_index += 1
		insert_query = "INSERT INTO Professors (ID_Professor, Name) VALUES (?, ?)"
		values = (self.last_index, prf.Name)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteProfessor(self, pr_ind):
		delete_query = "DELETE FROM Professors WHERE ID_Professor = ?"
		search_query = "SELECT ID_Professor FROM Professors WHERE ID_Professor > ?"

		try:
			self.cursor.execute(delete_query, (pr_ind,))
			self.conman.connection.commit()
			next_professors = self.cursor.execute(search_query, (pr_ind,)).fetchall()
			for i in next_professors:
				new_id = i[0] - 1
				update_query = "UPDATE Professors SET ID_Professor = ? WHERE ID_Professor = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateProfessor(self, prf):
		update_query = "UPDATE Professors SET Name = ? WHERE ID_Professor = ?"
		values = (prf.Name, prf.ID_Professor)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def GetProfessorByName(self, name):
		search_query = "SELECT  * FROM Professors WHERE Name = ?"

		try:
			cursor_result = self.cursor.execute(search_query,(label,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')
		
		if cursor_result != []:
			prf = cursor_result[0]
			return Professor(prf[0], prf[1])
		else:
			return False

	def ListProfessors(self):
		select_query = "SELECT * FROM Professors"
		prf_obj_ls = []

		try:
			professors_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for prf in professors_list:
			prf_obj_ls.append(Professor(prf[0], prf[1]))

		return prf_obj_ls

class ClassroomDAO:
	'''
		Classroom data access object
	'''

	def __init__(self, connection_manager):

		self.conman = connection_manager
		self.cursor = self.conman.cursor
		max_id = None

		try :
			max_id = self.cursor.execute("SELECT MAX(ID_Classroom) FROM Classrooms").fetchall()[0][0]
		except Exception as e:
			logging.warning(f'Error : {e}')

		if max_id is None:
			max_id = 999

		self.last_index = max_id

	def AddClassroom(self, crm):
		self.last_index += 1
		insert_query = "INSERT INTO Classrooms (ID_Classroom, Label) VALUES (?, ?)"
		values = (self.last_index, crm.Label)
		try:
			self.cursor.execute(insert_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def DeleteClassroom(self, cr_ind):
		delete_query = "DELETE FROM Classrooms WHERE ID_Classroom = ?"
		search_query = "SELECT ID_Classroom FROM Classrooms WHERE ID_Classroom > ?"

		try:
			self.cursor.execute(delete_query, (cr_ind,))
			self.conman.connection.commit()
			next_classrooms = self.cursor.execute(search_query, (cr_ind,)).fetchall()
			for i in next_classrooms:
				new_id = i[0] - 1
				update_query = "UPDATE Classrooms SET ID_Classroom = ? WHERE ID_Classroom = ?"
				self.cursor.execute(update_query, (new_id, i[0]))
				self.conman.connection.commit()
		except Exception as e:
			logging.warning(f'Error : {e}')

	def UpdateClassroom(self, crm):
		update_query = "UPDATE Classrooms SET Label = ? WHERE ID_Classroom = ?"
		values = (crm.Label, crm.ID_Classroom)

		try:
			self.cursor.execute(update_query, values)
		except Exception as e:
			logging.warning(f'Error : {e}')

		self.conman.connection.commit()

	def GetClassByLabel(self, label):
		search_query = "SELECT  * FROM Classrooms WHERE Label = ?"

		try:
			cursor_result = self.cursor.execute(search_query,(label,)).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')
		
		if cursor_result != []:
			clrm = cursor_result[0]
			return Classroom(clrm[0], clrm[1])
		else:
			return False

	def ListClassrooms(self):
		select_query = "SELECT * FROM Classrooms"
		crm_obj_ls = []

		try:
			classrooms_list = self.cursor.execute(select_query).fetchall()
		except Exception as e:
			logging.warning(f'Error : {e}')

		for crm in classrooms_list:
			crm_obj_ls.append(Classroom(crm[0], crm[1]))

		return crm_obj_ls