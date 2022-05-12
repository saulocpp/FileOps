## LICENSE:

This independent project is licensed under the terms of the "Creative Commons - No Derivatives" license (https://creativecommons.org/licenses/by-nd/4.0/).

The program can be downloaded from the project page at Github (https://github.com/saulocpp/FileOps) and freely used, even for commercial purposes. The author owns the copyrights and intellectual property of the program and its sources. It is not allowed to sell, rent, lease, modify or include the source code, part or whole, into other programs, commercial or free.

## Main goals:

FileOps is a tool to assist those dealing with Geoscience-related files, such as faults, well data and SGY volumes, in converting between formats or getting useful information from the data. It is not intended to replace existing tools that interact with repositories which require proprietary API, but to complement them, since many operations are not easily done, or at all possible to do with such tools.

When it is the case that a program doesn't have a certain operation, chances are that it will need to be done manually and take longer to accomplish than the original end task. FileOps aims at automating some of these operations and save time of data management personnel with intermediate tasks, allowing for more time to be spent in QC.

The program is made to be as simple and straightforward as possible, with the description of operations and occasional extra parameters being self-explanatory. As for the main programming platform, Python was chosen for simplicity in deployment, though other tools such as AWK are employed when they provide a simpler and more efficient way of solving a problem.

## Requirements/Usage:

At the time of this writing, FileOps depends on the following packages: <b>pygubu, tkinter, pandas, os, segyio</b>. Some operations depend on AWK, which is native in *nix systems but not in Windows, so if the latter is your preferred system, an environment such as MingW64 or WSL will be required. The Python version used for development and testing is 3.6, with 2.7 no longer supporting some of the more modern syntax 3.x. Tested in Linux (x86-64 and ARM64), Windows 8.1/10 and macOS. The program is launched by "<b>python FileOps.py</b>" and the interface should show up.

![Main_Window](https://user-images.githubusercontent.com/82084498/168159438-7ecc54b3-3edf-4d8f-8f01-dff4c289514a.jpg)

The main window shows the standard 1-2-3 steps of selecting the file(s), operation and running. New features will expand the section 2 and, as appropriate, the "Extra parameters" fields. The following screen shows a report with basic information of the selected SGYs and allow for saving it to text file.

![SEGY_Report](https://user-images.githubusercontent.com/82084498/128628826-52ca206d-6d9b-4d39-b158-4c197a1bfa55.jpg)

Important to note that errors due to missing steps for a given operation, such as trying to run without selecting a file, or convert faults without providing survey and interpreter name, will show an error message, however, problems that happen out of the program will be reported by the Python interpreter in the terminal where it was launched. For example, trying to open a file that has no read permission, or writing to a directory that has no write permission or insufficient space left, are caught by Python and not by FileOps.

When exchanging data between OpenWorks and Deli, use Data Export with the horizon standard file format, "Landmark (all)", then split it to the CSV formnat as expected by Deli. Once the processing in Deli is finished, various CSV horizon files are generated and can then be joined with FileOps. The 6th column of some files is ignored and file names are used as horizon names, but are truncated to 60 characters as required by OW, so no changes to individual files are needed. In Data Import use the horizon file format "HorizonExportv1p0.afm.xml".

GPU-based operations, such as the conversion of AVF file from Vrms to Vint, have additional dependencies explained in its own documentation, which also contains benchmarks and direct comparisons to other applications that do velocity conversion (though not from an AVF file to another AVF file). In environments where it is impractical to fulfil all the CUDA requirements for Linux computers, the easiest way is to use Windows instead. As for Macs, Apple has long decided to drop OS support for nVidia cards on their computers and the existing ones will be made obsolete at some point. Since they are still functional and perfectly capable of performing computing-intensive tasks with the Geforce-M cards and outperforming CPU-based implementations, the .bundle dynamic library will be provided for as long as the author still has his Macbook Pro 2012 or the functions don't require a feature not present in a Kepler GPU.

## Bug report:

If you think you found a bug, report to the author, but notice a few important things before doing so:
- Is it a really bug, in the sense that the program is not doing what it is supposed to do? If so, chances are that the file you are trying to process has some peculiarity that the ones tested to implement an operation didn't. A sample file will probably be needed to apply a fix.
- Is it just something that you don't personally agree with and think it could be done another way? Then it is not a bug and may fit as an enhancement.

In both cases, refer to the Enhancement section for relevant information.

## Enhancement:

Enhancement requests are welcome but need to be well-founded and aligned with the objectives already mentioned. The proponent must clearly present a high and concrete demand as well as the benefits of a new operation. This means that "nice to have" features will be avoided in order to keep the code base compact and useful.

Operations present in other applications aren't candidates for implementation either. As mentioned before, FileOps is not intended to be the end-all tool for data handling or overlap with existing established applications, it is meant to complement them and serve as a time-saver for side tasks that are time-consuming for data management teams.
