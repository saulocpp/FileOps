import os
import pygubu
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import Faults_Charisma_to_OW as c2ow
import Segy_Report as sgyrep
import Vel_Operations as vel
import Hrz_Join_Deli_to_OW as d2ow

class FileOps_GUI:
	def __init__(self):
		self.builder = builder = pygubu.Builder()								#1: Create a builder
		builder.add_from_file("FileOps.ui")										#2: Load an ui file
		self.main_tk				= builder.get_object("main_tk")				#3: Create the Toplevel/mainwindow, and objects go in a main frame
		self.button_fileopen		= builder.get_object("button_fileopen")
		self.button_clear			= builder.get_object("button_clear")
		self.button_run				= builder.get_object("button_run")
		self.button_about			= builder.get_object("button_about")
		self.button_quit			= builder.get_object("button_quit")
		self.listbox_files			= builder.get_object("listbox_files")
		self.scrollh				= builder.get_object("scrollh")
		self.scrollv				= builder.get_object("scrollv")
		self.radio_flt_charisma2ow	= builder.get_object("radio_flt_charisma2ow")
		self.radio_split_td_well	= builder.get_object("radio_split_td_well")
		self.radio_sgy_report		= builder.get_object("radio_sgy_report")
		self.radio_vrms2vint_avf	= builder.get_object("radio_vrms2vint_avf")
		self.radio_vrms2vint_xytv	= builder.get_object("radio_vrms2vint_xytv")
		self.radio_split_ow_deli	= builder.get_object("radio_split_ow_deli")
		self.radio_join_deli_ow		= builder.get_object("radio_join_deli_ow")
		self.frame_extraparams		= builder.get_object("frame_extraparams")
		self.entry_interp			= builder.get_object("entry_interp")
		self.entry_survey			= builder.get_object("entry_survey")
		self.dropdown_domain		= builder.get_object("dropdown_domain")
		self.dropdown_onset			= builder.get_object("dropdown_onset")
		self.operation				= builder.get_variable("operation")
		self.interp					= builder.get_variable("interp")
		self.survey					= builder.get_variable("survey")
		self.domain					= builder.get_variable("domain")
		self.onset					= builder.get_variable("onset")

	file_list = ""

	def open_file(self):
		self.file_list = filedialog.askopenfilenames(filetypes = [("Data files", "*.dat *.DAT"), ("CSV files", "*.csv, *.CSV"), ("Text files", "*.txt *.TXT"), \
			("SEG-Y files", "*.segy *.sgy *.SGY *.SEGY"), ("Velocity files", "*.avf *.AVF *.xytv *.XYTV"), ("All files", "*")])
		if(len(self.file_list) != 0):
			self.listbox_files.delete(0, END)
			for item in self.file_list:
				self.listbox_files.insert(END, item)

	def clear_all(self):
		self.file_list = ""
		self.listbox_files.delete(0, END)

	def run_operation(self):
		if(len(self.file_list) == 0):
			tk.messagebox.showerror("Error...", "No file(s) selected.")
			return
		if(self.operation.get() == 1):
			if(self.entry_interp.get() != "" and self.entry_survey.get() != ""):
				c2ow.flt_charisma2ow(self.file_list, self.entry_interp.get(), self.entry_survey.get(), self.domain.get())
				tk.messagebox.showinfo("Charisma faults to OW faults", "Conversion complete. Check the \"Charisma2OW_*\" output file(s).")
			else:
				tk.messagebox.showerror("Missing information for fault conversion", "Fill in the fields for interpreter and survey name.")
		elif(self.operation.get() == 2):
			for file_name in self.file_list:
				os.system("awk -f Split_OW_TD_files.awk " + file_name)
			tk.messagebox.showinfo("Split T/D to individual files", "T/D tables in the input file(s) split in the form \"WellName_TDName.txt\".")
		elif(self.operation.get() == 3):
			sgyrep.sgy_report(self.main_tk, self.file_list)
		elif(self.operation.get() == 4):
			vel.vrms2vint('A', self.file_list)
		elif(self.operation.get() == 5):
			vel.vrms2vint('X', self.file_list)
		elif(self.operation.get() == 6):
			for file_name in self.file_list:
				os.system("awk -f Split_OW_Hrz_to_Deli.awk " + file_name)
		elif(self.operation.get() == 7):
			d2ow.hrz_deli2ow(self.file_list, self.entry_interp.get(), self.entry_survey.get(), self.domain.get(), self.onset.get())
		else:
			tk.messagebox.showerror("Unable to run operation", "Strange error occurred. Invalid operation value passed, please contact the developer.")

	# Change to a switch-case structure when Python 3.10 is available
	def extra_params(self):
		oper = self.operation.get()
		if(oper == 1):
			for child in self.frame_extraparams.winfo_children():
				child.config(state = "normal")
			self.dropdown_domain.config(state = "readonly")
			self.dropdown_onset.config(state = "disable")
		elif(oper == 7):
			for child in self.frame_extraparams.winfo_children():
				child.config(state = "normal")
			self.dropdown_domain.config(state = "readonly")
			self.dropdown_onset.config(state = "readonly")
		else:
			for child in self.frame_extraparams.winfo_children():
				child.config(state = "disable")
			self.dropdown_domain.config(state = "disable")
			self.dropdown_onset.config(state = "disable")

	def limit_interp(self, entry_interp):
		if len(self.entry_interp.get()) > 0:
			self.interp.set(self.entry_interp.get()[:5])

	def limit_survey(self, entry_survey):
		if len(self.entry_survey.get()) > 0:
			self.survey.set(self.entry_survey.get()[:40])

	def config_objects(self):
		self.main_tk.tk.call("wm", "iconphoto", self.main_tk._w, tk.PhotoImage(file = "FileOps.png"))
		ttk.Style().theme_use("alt")		# "alt", "clam", "classic", "default"
		self.builder.connect_callbacks(self)
		self.interp.trace("w", lambda *args: self.limit_interp(self.entry_interp))
		self.survey.trace("w", lambda *args: self.limit_survey(self.entry_survey))
		self.operation.set(1)
		self.domain.set("TIME")
		self.onset.set("MINIMUM")
		self.scrollh.config(command = self.listbox_files.xview)
		self.scrollv.config(command = self.listbox_files.yview)
		self.listbox_files.config(yscrollcommand = self.scrollv.set, xscrollcommand = self.scrollh.set)
		self.button_run.config(height = 2, font = tkfont.Font(weight = "bold", size = 14))
		self.button_about.config(command = lambda: tk.messagebox.showinfo("About FileOps", "Developed by: Saulo Silva\n\
Geophysics Consultant, saulocpp@gmail.com"))
		self.button_quit.config(command = self.main_tk.destroy)

	def run(self):
		self.main_tk.mainloop()

if __name__ == '__main__':
	fileops = FileOps_GUI()
	fileops.config_objects()
	fileops.extra_params()
	fileops.run()
