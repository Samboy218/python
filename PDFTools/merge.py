#this tool will concatenate 2 pdf documents together
from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse

# Creating a routine that appends files to the output file
def append_pdf(input, output):
    for pageNum in range(input.numPages):
        output.addPage(input.getPage(pageNum))

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs='+', help="List of input files to be merged")
parser.add_argument("-o", "--output", help="name of file to write results to", default="out.pdf")

args = parser.parse_args()

# Creating an object where pdf pages are appended to
output = PdfFileWriter()

# Appending two pdf-pages from two different files
for i in range(len(args.input)):
    append_pdf(PdfFileReader(open(args.input[i], "rb")), output)

# Writing all the collected pages to a file
output.write(open(args.output,"wb"))
