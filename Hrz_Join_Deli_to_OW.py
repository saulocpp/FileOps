# 12/05/2022
# Python script to join multiple IL,XL,X,Y,Z horizon files from Deli into one OW horizon file for loading (based on the Landmark horizon default format in Data Export)
# Written by Saulo Silva - saulocpp@gmail.com

import os
import sys
import tkinter as tk
import pyarrow as pa
from tkinter import messagebox
from pyarrow import csv
from random import randint
from datetime import datetime

def hrz_deli2ow(file_list, interp, survey, domain, onset, attribute):
	with open("Deli2OW_" + datetime.now().strftime("%d-%m-%Y_%H%M%S") + ".dat", "w") as d2ow:
		for file_name in file_list:
			readoptions		= csv.ReadOptions(autogenerate_column_names = True)
			convertoptions	= csv.ConvertOptions(column_types = {"f0": pa.int32(), "f1": pa.int32(), "f2": pa.string(), "f3": pa.string(), "f4": pa.string()})
			deli			= csv.read_csv(file_name, read_options = readoptions, convert_options = convertoptions)
			LINE_COUNT		= deli.num_rows
			INTERP_NAME		= interp + " " * (9 - len(interp))
			DOMAIN			= domain + " " * (10 if len(domain) == 5 else 11)
			ATTRIBUTE		= attribute + " " * (40 - len(attribute))
			HRZ_NAME		= os.path.basename(os.path.splitext(file_name)[0])
			HRZ_NAME		= HRZ_NAME[:60] if len(HRZ_NAME) > 60 else HRZ_NAME + " " * (60 - len(HRZ_NAME))
			HRZ_ONSET		= onset + " " * (17 - len(onset))
			HRZ_RGB			= str(randint(0, 255)) + "-" + str(randint(0, 255)) + "-" + str(randint(0, 255))
			HRZ_VERSION		= "Deli_to_OW" + " " * 30
			SURVEY_NAME		= survey + " " * (60 - len(survey))
			print("3D Horizon, version 1.0", file = d2ow)
			print(INTERP_NAME + DOMAIN + ATTRIBUTE + HRZ_NAME + HRZ_ONSET + HRZ_RGB, file = d2ow)
			print(HRZ_VERSION + SURVEY_NAME, file = d2ow)
			for i in range(1, LINE_COUNT):
				ILINE = str(deli["f0"][i]) + " " * (16 - len(str(deli["f0"][i])))
				XLINE = str(deli["f1"][i]) + " " * (16 - len(str(deli["f1"][i])))
				VAL_X = str(deli["f2"][i]) + " " * (16 - len(str(deli["f2"][i])))
				VAL_Y = str(deli["f3"][i]) + " " * (16 - len(str(deli["f3"][i])))
				VAL_Z = str(deli["f4"][i]) + " " * (16 - len(str(deli["f4"][i])))
				print(ILINE, XLINE, VAL_X, VAL_Y, VAL_Z, file = d2ow)
	d2ow.close()
	tk.messagebox.showinfo("Deli to OW conversion finished", "Use the format file 'HorizonExportv1p0.afm.xml' in Data Import to load the result in OpenWorks.")
