
#import components from tkinter library
from tkinter import Tk, Label, Button
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
#import filedialog module
from tkinter import filedialog
from pathlib import Path
import webbrowser

filename1=""
filename2=""

#function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = str(Path.home() / "Downloads"),
                                          title = "Select a File",
                                          filetypes = (("Text files", "*.pdf*"),
                                                       ("all files", "*.*")))
    global filename1
    filename1 = filename
    #change label contents
    filename_label.configure(text="File Selected:\n" + filename)

def browseFiles2():
    filename = filedialog.askopenfilename(initialdir = str(Path.home() / "Downloads"),
                                          title = "Select a File",
                                          filetypes = (("Text files", "*.pdf*"),
                                                       ("all files", "*.*")))
    global filename2
    filename2 = filename
    #change label contents
    filename_label2.configure(text="File Selected:\n" + filename)

def ReadPdfFile( fName ):
    found = False
    while( not found ):
        try:
            with open( fName, 'rb' ) as f:
                found = True
                print(PdfFileReader)
                return PdfFileReader(f)
        except FileNotFoundError:
            print( "File not found: " , fName )
        fName = input( "Enter filename :> ")

def ReversePdf( pdfFile ):
    revPdf = PdfFileWriter()
    endPage = pdfFile.getNumPages()
    for i in reversed(range(endPage)):
        revPdf.addPage(pdfFile.getpage(i))
    return revPdf

#detect if merged file already exists
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    if(not os.path.exists(path)):
        path = filename + "0001" + extension

    while os.path.exists(path):
        path = filename + str(counter).zfill(4) + extension
        counter += 1

    return path

def createPDF():
    try:
        pdf1 = PdfFileReader(open(filename1, 'rb' ))
        pdf2 = PdfFileReader(open(filename2, 'rb' ))
    except Exception as e:
        error_label.configure(text="Error:" + str(e) + "\nno files chosen or one of your PDFs might be damaged")
    else:
        outfile = str(Path.home() / "Downloads" / "MERGED.pdf")
        outfile=uniquify(outfile)
        outputStream = open(outfile, 'wb')

        revPdf = PdfFileWriter()
        endPage2 = pdf2.getNumPages()
        endPage1 = pdf1.getNumPages()

        for i in reversed(range(endPage2)):
            revPdf.addPage(pdf2.getPage(i))
        pdf2 = revPdf

        outPdf = PdfFileWriter()
        for i in range(endPage2):
            outPdf.addPage(pdf1.getPage(i))
            outPdf.addPage(pdf2.getPage(i))

        #pdf2 = revPdf.write(outputStream)
        outPdf.write(outputStream)
        error_label.configure(text="Merged PDF successfully exported with filename: "+outfile)
        outputStream.close()

def open_github():
    webbrowser.open_new("https://github.com/Persie0/One_Sided_Scan_Merger_App")

if __name__ == "__main__":        
    
    #create root window
    window = Tk()
        
    #set window title
    window.title("One Sided Scan Merger")
    
    #set window size
    window.geometry("1150x250")
    
    #set window background color
    window.config(background = "#272727")
    
    #create a file explorer label
    prompt_label = Label(window, text = "Front Pages of scanned documents (Page 1,3,5,...)", height = 4, fg = "white", background = "#272727")
    filename_label = Label(window, text="", height=4, fg="white",
                         background="#272727")
    prompt_label.grid(column=1, row=1, padx=(30,10), pady=(0,0), rowspan=2)
    filename_label.grid(column=3, row=1, padx=(30, 10), pady=(0, 0), rowspan=2)

    #create browse button
    browse_button = Button(window, text = "Select", command = browseFiles)
    browse_button.grid(column=2, row=1, padx=(0,40), pady=(20,5), ipadx=15)

    # create a file explorer label
    prompt_label2 = Label(window, text="Back Pages in Reversed Order of scanned documents (Page n,n-2,...,6,4,2):", height=4, fg="white",
                         background="#272727")
    filename_label2 = Label(window, text="", height=4, fg="white",
                           background="#272727")
    prompt_label2.grid(column=1, row=3, padx=(30, 10), pady=(0, 0), rowspan=2)
    filename_label2.grid(column=3, row=3, padx=(30, 10), pady=(0, 0), rowspan=2)

    # create browse button
    browse_button2 = Button(window, text="Select", command=browseFiles2)
    browse_button2.grid(column=2, row=3, padx=(0, 40), pady=(20, 5), ipadx=15)

    link1  = Button(text="Github page", command=open_github, fg="blue", background="#272727", borderwidth=0)
    link1.grid(column=1, row=7)

    error_label = Label(window, text="", height=4, fg="white",
                            background="#272727")
    error_label.grid(column=1, row=5, padx=(30, 10), pady=(0, 0), rowspan=2)

    merge_button = Button(window, text="Merge", command=createPDF)
    merge_button.grid(column=7, row=5, padx=(0, 40), pady=(20, 5), ipadx=15)


    window.mainloop()

