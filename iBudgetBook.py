import os
import sys
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas

fName = "aFile.txt"
path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook"
os.chdir(path)
with open(fName, 'r') as f:
    line = f.read()
    print(line)

