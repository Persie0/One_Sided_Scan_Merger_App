# import components from tkinter library
from tkinter import Tk, Label, Button, Checkbutton, BooleanVar
import os
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
# import filedialog module
from tkinter import filedialog
from pathlib import Path
import webbrowser
import glob
from PIL import Image

filename1 = ""
filename2 = ""
directory = ""


# function for opening the file explorer window
def browseDirectory():
    dire = filedialog.askdirectory(initialdir=str(Path.home() / "Downloads"),
                                   title="Select a directory", )
    global directory
    directory = dire
    # change label contents
    filename_label3.configure(text="Directory Selected:\n" + dire)


# function for opening the file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir=str(Path.home() / "Downloads"),
                                       title="Select a File",
                                       filetypes=(("Pdfs", "*.pdf"),
                                                  ("all files", "*.*")))
    global filename1
    filename1 = filename
    # change label contents
    filename_label.configure(text="File Selected:\n" + filename)


def browseFiles2():
    filename = filedialog.askopenfilename(initialdir=str(Path.home() / "Downloads"),
                                          title="Select a File",
                                          filetypes=(("Text files", "*.pdf*"),
                                                     ("all files", "*.*")))
    global filename2
    filename2 = filename
    # change label contents
    filename_label2.configure(text="File Selected:\n" + filename)


def ReadPdfFile(fName):
    found = False
    while not found:
        try:
            with open(fName, 'rb') as f:
                found = True
                print(PdfFileReader)
                return PdfFileReader(f)
        except FileNotFoundError:
            print("File not found: ", fName)
        fName = input("Enter filename :> ")


def ReversePdf(pdfFile):
    revPdf = PdfFileWriter()
    endPage = pdfFile.getNumPages()
    for i in reversed(range(endPage)):
        revPdf.addPage(pdfFile.getpage(i))
    return revPdf


# detect if merged file already exists
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    if (not os.path.exists(path)):
        path = filename + "0001" + extension

    while os.path.exists(path):
        path = filename + str(counter).zfill(4) + extension
        counter += 1

    return path


def createPDF():
    try:
        pdf1 = PdfFileReader(open(filename1, 'rb'))
        pdf2 = PdfFileReader(open(filename2, 'rb'))
    except Exception as e:
        error_label.configure(text="Error:" + str(e) + "\nno files chosen or one of your PDFs might be damaged")
    else:
        outfile = str(Path.home() / "Downloads" / "MERGED.pdf")
        outfile = uniquify(outfile)
        outputStream = open(outfile, 'wb')

        revPdf = PdfFileWriter()
        endPage2 = pdf2.getNumPages()
        endPage1 = pdf1.getNumPages()

        for i in reversed(range(endPage2)):
            revPdf.addPage(pdf2.getPage(i))
        pdf2 = revPdf

        outPdf = PdfFileWriter()
        if endPage1==endPage2:
            for i in range(endPage2):
                outPdf.addPage(pdf1.getPage(i))
                outPdf.addPage(pdf2.getPage(i))
        else:
            exeption_label.configure(text="Files dont have the same length: " + filename1 + " and " + filename2)


        # pdf2 = revPdf.write(outputStream)
        outPdf.write(outputStream)
        outputStream.close()
        global initial_state
        if initial_state.get():
            # Set the path to the PDF file
            pdf_path = outfile

            # Convert the PDF to images
            images = convert_from_path(pdf_path)
            # Create a PdfFileReader object for the input PDF
            input_reader = PdfFileReader(pdf_path)

            # Create a PdfFileWriter object for the output PDF
            output_writer = PdfFileWriter()

            # Iterate through the images and save them to a folder
            for i, image in enumerate(images):
                file_name = 'image_{}.jpg'.format(i)
                image.save(file_name, 'JPEG')

                # Set the path to the image
                image_path =file_name

                # Open the image
                image = Image.open(image_path)

                # Convert the image to grayscale
                gray_image = image.convert('L')

                # Get the width and height of the image
                width, height = gray_image.size

                # Iterate through the pixels in the image
                num_white_pixels = 0
                for x in range(width):
                    for y in range(height):
                        # Get the pixel at the current position
                        pixel = gray_image.getpixel((x, y))
                        # Check if the pixel is white (i.e. has a value of 255)
                        if pixel >250:
                            num_white_pixels += 1

                # Calculate the percentage of white  pixels in the image
                # Calculate the percentage of white  pixels in the image
                percent_white = (num_white_pixels / (width * height))*100
                print(file_name,percent_white)
                # Check if the image is mostly white
                os.remove(file_name)
                if percent_white > 98.3:
                    print('The image is mostly white.')
                else:
                    output_writer.addPage(input_reader.getPage(i))
            # Write the output PDF
            with open(outfile, "wb") as output_file:
                output_writer.write(output_file)
        error_label.configure(text="Merged PDF successfully exported with filename: " + outfile)



def loopFiles():
    files = glob.glob(directory + "/*.pdf")
    print(files)
    if len(files)%2!=0:
        exeption_label.configure(text="Uneven number of files!")
        return
    for file in files:
        i = files.index(file)
        if i % 2 == 1:
            continue
        else:
            global filename1
            filename1 = files[i]
            global filename2
            filename2 = files[i + 1]
        createPDF()
    exeption_label.configure(text="Successfully merged all")


def open_github():
    webbrowser.open_new("https://github.com/Persie0/One_Sided_Scan_Merger_App")


if __name__ == "__main__":
    # create root window
    window = Tk()

    # set window title
    window.title("One Sided Scan Merger")

    # set window size
    window.geometry("1350x400")

    # set window background color
    window.config(background="#272727")
    # Create a BooleanVar
    initial_state = BooleanVar(value=True)

    # create a file explorer label
    prompt_label = Label(window, text="Front Pages of scanned documents (Page 1,3,5,...)", height=4, fg="white",
                         background="#272727")
    filename_label = Label(window, text="", height=4, fg="white",
                           background="#272727")
    prompt_label.grid(column=1, row=1, padx=(30, 10), pady=(0, 0), rowspan=2)
    filename_label.grid(column=3, row=1, padx=(30, 10), pady=(0, 0), rowspan=2)

    # create browse button
    browse_button = Button(window, text="Select", command=browseFiles)
    browse_button.grid(column=2, row=1, padx=(0, 40), pady=(20, 5), ipadx=15)

    # create a file explorer label
    prompt_label2 = Label(window, text="Back Pages in Reversed Order of scanned documents (Page n,n-2,...,6,4,2):",
                          height=4, fg="white",
                          background="#272727")
    filename_label2 = Label(window, text="", height=4, fg="white",
                            background="#272727")
    prompt_label2.grid(column=1, row=3, padx=(30, 10), pady=(0, 0), rowspan=2)
    filename_label2.grid(column=3, row=3, padx=(30, 10), pady=(0, 0), rowspan=2)

    # create browse button
    browse_button2 = Button(window, text="Select", command=browseFiles2)
    browse_button2.grid(column=2, row=3, padx=(0, 40), pady=(20, 5), ipadx=15)

    # folder select
    prompt_label3 = Label(window, text="Or select a folder", height=4, fg="white", background="#272727")
    filename_label3 = Label(window, text="", height=4, fg="white",
                            background="#272727")
    prompt_label3.grid(column=1, row=10, padx=(30, 10), pady=(0, 0), rowspan=2)
    filename_label3.grid(column=3, row=10, padx=(30, 10), pady=(0, 0), rowspan=2)

    # create browse button
    browse_button3 = Button(window, text="Select", command=browseDirectory)
    browse_button3.grid(column=2, row=10, padx=(0, 40), pady=(20, 5), ipadx=15)

    merge_folder_button = Button(window, text="Merge folder", command=loopFiles)
    merge_folder_button.grid(column=9, row=10, padx=(0, 40), pady=(20, 5), ipadx=15)

    link1 = Button(text="Github", command=open_github, fg="blue", background="#272727", borderwidth=0)
    link1.grid(column=1, row=16)

    error_label = Label(window, text="", height=4, fg="white",
                        background="#272727")
    error_label.grid(column=1, row=5, padx=(30, 10), pady=(0, 0), rowspan=2)

    exeption_label = Label(window, text="", height=4, fg="red",
                        background="#272727")
    exeption_label.grid(column=1, row=18, padx=(30, 10), pady=(0, 0), rowspan=2)

    merge_button = Button(window, text="Merge", command=createPDF)
    merge_button.grid(column=9, row=5, padx=(0, 40), pady=(20, 5), ipadx=15)
        # Create a Label widget

    # Create a Checkbutton widget
    checkbox = Checkbutton(window, text="remove empty/white pages (takes longer)",
                        onvalue=True, offvalue=False,
                        variable=initial_state)

    # Set the initial state of the checkbox
    initial_state.set(True)

    # Add the label and checkbox to the window
    checkbox.grid(row=3, column=10)

    window.mainloop()
