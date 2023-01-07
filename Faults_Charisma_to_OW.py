# 06/01/2023
# Python script to convert fault file in Charisma format to OpenWorks for loading with Data Import
# The file can contain multiple faults, as exported by ErathNet or other apps, or one fault per file, as exported by Petrel
# Written by Saulo Silva - saulocpp@gmail.com
import os
import pandas
import numpy as np

def flt_charisma2ow(file_list, interp, survey, domain):
#========= Aux Functions ==========
	def Reset_xyz_pts():
		temp_xyz_pts	= np.empty(7, np.float)
		temp_xyz_pts[0]	= temp_xyz_pts[2] = temp_xyz_pts[4] = 9999999999.0
		temp_xyz_pts[1]	= temp_xyz_pts[3] = temp_xyz_pts[5] = 0.0
		temp_xyz_pts[6]	= 0
		return temp_xyz_pts

	def Write_Header(OW_FAULT_NAME, INTERP_NAME, SURVEY_NAME, DOMAIN, c2ow):
		print("New Fault Plane, version 1.10", file = c2ow)
		print(OW_FAULT_NAME + INTERP_NAME + SURVEY_NAME + "UNKNOWN     " + DOMAIN + "Y" + " " * 19, file = c2ow)

	def Write_Segment_Info(INTERP_NAME, DOMAIN, MIN_X, MAX_X, MIN_Y, MAX_Y, MIN_Z, MAX_Z, NUM_PTS, c2ow):
		print("Fault Segment", file = c2ow)
		print(INTERP_NAME + " " * 15 + "{:.0f}         {:.3f}{:.3f}{:.1f} {:.1f} {:.5f}{:.5f}".format(NUM_PTS, MIN_X, MAX_X, MIN_Y, MAX_Y, MIN_Z, MAX_Z), file = c2ow)
		print(DOMAIN + "0", file = c2ow)

	def Write_Segment_Data(SEGMENT_BEGIN, SEGMENT_END, c2ow):
		for data_idx in range(SEGMENT_BEGIN, SEGMENT_END):
			print("      {:.2f}     {:.2f}   {:.5f}".format(charisma.iloc[data_idx][3], charisma.iloc[data_idx][4], charisma.iloc[data_idx][5]), file = c2ow)
#======== End of Aux Functions and start of the main program =========
	for file_name in file_list:
		global charisma
		charisma = pandas.read_csv(file_name, header = None, delim_whitespace = True, dtype = {"txt":str, "il":float, "xl":float, "x":float, "y":float, "z":float, "flt":str, "seg":int})
		charisma.drop(charisma.columns[[0, 1, 2]], axis = "columns", inplace = True)
		INTERP_NAME	= interp + " " * (5 - len(interp))
		SURVEY_NAME	= survey + " " * (40 - len(survey))
		DOMAIN		= domain + " " * (8 if len(domain) == 4 else 7)
		c2ow_file, current_fault, xyz_pts, current_segment, file_line, segment_begin = "", "", "", 1, 0, 0

		for file_line in range(len(charisma.index)):
			if(current_fault != charisma.iloc[file_line, 3]):
				if(file_line == (len(charisma.index) - 1) or file_line > 1):
					Write_Segment_Info(INTERP_NAME, DOMAIN, xyz_pts[0], xyz_pts[1], xyz_pts[2], xyz_pts[3], xyz_pts[4], xyz_pts[5], xyz_pts[6], c2ow_file)
					Write_Segment_Data(file_line - int(xyz_pts[6]), file_line, c2ow_file)
				xyz_pts			= Reset_xyz_pts()
				current_segment	= 1
				current_fault	= charisma.iloc[file_line, 3]
				OW_FAULT_NAME	= current_fault + " " * (60 - len(current_fault)) if len(current_fault) <= 50 else current_fault[0 : 49] + " " * 10
				c2ow_file		= open(os.path.dirname(file_name) + "/Charisma2OW_" + os.path.basename(current_fault), "w")
				Write_Header(OW_FAULT_NAME, INTERP_NAME, SURVEY_NAME, DOMAIN, c2ow_file)
			if(current_segment != charisma.iloc[file_line, 4]):
				Write_Segment_Info(INTERP_NAME, DOMAIN, xyz_pts[0], xyz_pts[1], xyz_pts[2], xyz_pts[3], xyz_pts[4], xyz_pts[5], xyz_pts[6], c2ow_file)
				Write_Segment_Data(file_line - int(xyz_pts[6]), file_line, c2ow_file)
				current_segment	= charisma.iloc[file_line, 4]
				xyz_pts			= Reset_xyz_pts()

			xyz_pts[0], xyz_pts[1] = min(xyz_pts[0], charisma.iloc[file_line, 0]), max(xyz_pts[1], charisma.iloc[file_line, 0])
			xyz_pts[2], xyz_pts[3] = min(xyz_pts[2], charisma.iloc[file_line, 1]), max(xyz_pts[3], charisma.iloc[file_line, 1])
			xyz_pts[4], xyz_pts[5] = min(xyz_pts[4], charisma.iloc[file_line, 2]), max(xyz_pts[5], charisma.iloc[file_line, 2])
			xyz_pts[6] += 1
		Write_Segment_Info(INTERP_NAME, DOMAIN, xyz_pts[0], xyz_pts[1], xyz_pts[2], xyz_pts[3], xyz_pts[4], xyz_pts[5], xyz_pts[6], c2ow_file)
		Write_Segment_Data(file_line + 1 - int(xyz_pts[6]), file_line + 1, c2ow_file)

