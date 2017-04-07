#this tool will concatenate 2 pdf documents together
from pyPdf import PdfFileWriter, PdfFileReader
import argparse

# Creating a routine that appends files to the output file
def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


parser = argparse.ArgumentParser()
parser.add_argument("Input1")
parser.add_argument("Input2")
parser.add_argument("Output")

args = parser.parse_args()

# Creating an object where pdf pages are appended to
output = PdfFileWriter()

# Appending two pdf-pages from two different files
append_pdf(PdfFileReader(open(args.Input1,"rb")),output)
append_pdf(PdfFileReader(open(args.Input2,"rb")),output)

# Writing all the collected pages to a file
output.write(open(args.Output,"wb"))
