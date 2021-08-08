# 28/02/2021
# Python script that generates a report with basic information of SGY files passed in the tuple file_list
# Written by Saulo Silva - saulocpp@gmail.com
import segyio
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext

def sgy_report(main_tk, file_list):
	sgyrep_window = tk.Toplevel(main_tk)
	sgyrep_window.title("Basic SEG-Y report")
	sgyrep_window.grab_set()
	text_report = scrolledtext.ScrolledText(sgyrep_window)
	text_report.pack(expand = True, fill = tk.BOTH)
	def save_file_as():
		save_file = tk.filedialog.asksaveasfilename(defaultextension = ".txt", filetypes = [("Text files", "*.txt *.TXT"), ("All files", "*.*")])
		if(save_file != ""):
			with open(save_file, "w") as report_out:
				report_out.write(text_report.get('1.0', 'end'))
			report_out.close()
	button_save = tk.Button(sgyrep_window, text = "Save to file", command = save_file_as).pack(side = tk.LEFT, padx = 20, pady = 20)
	button_close = tk.Button(sgyrep_window, text = "Close", command = sgyrep_window.destroy).pack(side = tk.RIGHT, padx = 20, pady = 20)
	for file_name in file_list:
		sgyfile = segyio.open(file_name, iline = segyio.tracefield.TraceField.SourceEnergyDirectionExponent, xline = segyio.tracefield.TraceField.CDP)
		sgyfile.mmap()
		inp = segyio.cube(sgyfile)
		inp = inp[:, :, :]
		ilines, xlines, samples = inp.shape
		text_report.insert(tk.END, file_name + "\n\n")
		text_report.insert(tk.END, "Number of inlines: " + str(ilines) + "\n")
		text_report.insert(tk.END, "Minimum and Maximum inline: [" + str(sgyfile.ilines[0]) + ", " + str(sgyfile.ilines[ilines - 1]) + "]\n")
		text_report.insert(tk.END, "Number of xlines: "  + str(xlines) + "\n")
		text_report.insert(tk.END, "Minimum and Maximum xline: [" + str(sgyfile.xlines[0]) + ", " + str(sgyfile.xlines[xlines - 1]) + "]\n")
		text_report.insert(tk.END, "Samples per trace: " + str(samples) + "\n")
		text_report.insert(tk.END, "Sampling rate: " + str(sgyfile.bin[segyio.BinField.Interval]) + "\n")
		text_report.insert(tk.END, "\n----------------------------------\n\n")
		sgyfile.close()
	text_report.config(state = tk.DISABLED)
