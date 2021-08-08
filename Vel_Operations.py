# 08/08/2021
# Velocity-related operations executed with GPU
# Written by Saulo Silva - saulocpp@gmail.com
import os
import ctypes
import platform
from ctypes import *
import tkinter as tk
from tkinter import messagebox

def avf_vrms2vint(file_list):
	lib_name = ""
	current_os = platform.system()
	if(current_os == "Linux"):
		current_machine = platform.machine()
		if(current_machine == "x86_64"):
			lib_name = "./FileOps_GPU_Operations-x86_64.so"
		elif(current_machine == "aarch64"):
			lib_name = "./FileOps_GPU_Operations-aarch64.so"
	elif(current_os == "Windows"):
		lib_name = "./FileOps_GPU_Operations.dll"
	elif(current_os == "Darwin"):
		lib_name = "./FileOps_GPU_Operations.bundle"
	lib_gpuops = cdll.LoadLibrary(lib_name)
	if(lib_gpuops.has_CUDA30_GPU() == 0):
		for file_name in file_list:
			if(lib_gpuops.Vrms2Vint((file_name).encode('utf-8'), (os.path.splitext(file_name)[0] + "_converted_to_Vint.avf").encode('utf-8')) != 0):
				tk.messagebox.showerror("Vrms -> Vint", "Unable to process file " + file_name + ", check the terminal for more information on the error.")
	else:
		tk.messagebox.showerror("GPU error", "No CUDA 3.0+ NVidia card present. Unable to run GPU operations.")
	
