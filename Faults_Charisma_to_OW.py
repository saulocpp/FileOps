# 25/02/2021
# Python script to convert fault file in Charisma format to OpenWorks for loading with Data Import
# Written by Saulo Silva - saulocpp@gmail.com
import os
import pandas
import numpy as np

def flt_charisma2ow(file_list, interp, survey, domain):
	for file_name in file_list:
		charisma = pandas.read_csv(file_name, header = None, delim_whitespace = True)
		ROW_COUNT = len(charisma.index)
		flt = charisma.iloc[0, 6]
		FAULT_NAME = flt + " " * (60 - len(flt)) if len(flt) <= 50 else flt[0 : 49] + " " * 10
		INTERP_NAME = interp + " " * (5 - len(interp))
		SURVEY_NAME = survey + " " * (40 - len(survey))
		DOMAIN = domain + " " * (8 if len(domain) == 4 else 7)
		FAULT_COUNT = 1
		fault_num = charisma.iloc[0, 7]
		for i in range(1, ROW_COUNT):
			if(fault_num != charisma.iloc[i, 7]):
				fault_num = charisma.iloc[i, 7]
				FAULT_COUNT += 1
		xyz_pts = np.empty((FAULT_COUNT, 7), np.float)
		for i in range(0, FAULT_COUNT):
			xyz_pts[i][0] = xyz_pts[i][2] = xyz_pts[i][4] = 9999999999.0
			xyz_pts[i][1] = xyz_pts[i][3] = xyz_pts[i][5] = 0.0
			xyz_pts[i][6] = 0
		fault_num = charisma.iloc[0, 7]
		j = 0
		for i in range(0, ROW_COUNT):
			if(fault_num != charisma.iloc[i][7]):
				fault_num = charisma.iloc[i][7]
				j += 1
			xyz_pts[j][0] = min(charisma.iloc[i, 3], xyz_pts[j][0])
			xyz_pts[j][1] = max(charisma.iloc[i, 3], xyz_pts[j][1])
			xyz_pts[j][2] = min(charisma.iloc[i, 4], xyz_pts[j][2])
			xyz_pts[j][3] = max(charisma.iloc[i, 4], xyz_pts[j][3])
			xyz_pts[j][4] = min(charisma.iloc[i, 5], xyz_pts[j][4])
			xyz_pts[j][5] = max(charisma.iloc[i, 5], xyz_pts[j][5])
			xyz_pts[j][6] += 1
		with open(os.path.dirname(file_name) + "/Charisma2OW_" + os.path.basename(file_name), "w") as c2ow:
			data_idx = 0
			print("New Fault Plane, version 1.10", file = c2ow)
			print(FAULT_NAME + INTERP_NAME + SURVEY_NAME + "UNKNOWN     " + DOMAIN + "Y" + " " * 19, file = c2ow)
			for i in range(0, FAULT_COUNT):
				print("Fault Segment", file = c2ow)
				print(INTERP_NAME + " " * 15 + "{:.0f}         {:.3f}{:.3f}{:.1f} {:.1f} {:.5f}{:.5f}".format(xyz_pts[i][6], xyz_pts[i][0], xyz_pts[i][1], xyz_pts[i][2], xyz_pts[i][3], xyz_pts[i][4], xyz_pts[i][5]), file = c2ow)
				print(DOMAIN + "0", file = c2ow)
				for j in range(0, np.int(xyz_pts[i][6])):
					if(data_idx >= ROW_COUNT):
						break
					print("      {:.2f}     {:.2f}   {:.5f}".format(charisma.iloc[data_idx][3], charisma.iloc[data_idx][4], charisma.iloc[data_idx][5]), file = c2ow)
					data_idx += 1
		c2ow.close()
