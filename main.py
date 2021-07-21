import sys
from FileReader import FileReader
from MatrixPrinter import MatrixPrinter

with open(sys.argv[1]) as file:
  lines = file.readlines()

reader = FileReader(lines)
MatrixPrinter(reader.matrix)