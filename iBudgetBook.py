import os
import sys
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas

fName = "aFile.txt"
path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/PDF"
os.chdir(path)
c = Canvas("Hello-world.pdf")
c.drawString(100, 750, "Welcome to Reportlab!")
c.save()
