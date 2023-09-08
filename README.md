# PDF Merger for One-Sided Scanners

This Python application allows you to merge PDFs from a one-sided scanner on Windows, Linux, and Mac. It utilizes Tkinter for the graphical user interface.

![Application Screenshot](https://github.com/Persie0/One_Sided_Scan_Merger_App/raw/master/2022-12-10_18-50.png)

## Features

- Merge two PDF files:
  - One containing the front pages of a scan (those are all odd pdf pages after the merge).
  - One containing the backsides of a scan **in reverse order** (those are all even pdf pages after the merge).

## Download

You can download the application for Windows from the following link:

[Download OneSidedScansMergerApp.exe](https://github.com/Persie0/One_Sided_Scan_Merger_App/releases/download/folderMerge/OneSidedScansMergerApp.exe)

## User Interface

- The application offers a simple and intuitive UI.
- Easily select the two PDFs you want to merge.

## Usage
0. Place your pages into the scanner/printer with all front pages facing up. Scan these front pages *(to get a PDF with all front pages in the right order)*, then remove the stack from the scanner, flip it around, and scan the back sides (to get a PDF with all back sides in the reversed order i.e. starting with th last page)*.
1. Download the `.exe` file.
2. Launch the application.
3. Select the two PDF files you want to merge.
4. Click the "Merge" button to generate the merged PDF.

## Build Instructions (for other platforms)

To build the application for other platforms, follow these steps:

1. Install Python if you haven't already.
2. Clone this repository.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the application using `python OneSidedScansMergerApp.py`.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to contribute, report issues, or suggest improvements! If you encounter any problems, please [open an issue](https://github.com/Persie0/One_Sided_Scan_Merger_App/issues).
