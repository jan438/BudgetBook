import os
import sys
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/PDF"
os.chdir(path)
c = Canvas("Hello-world.pdf")
textobject = c.beginText()
textobject.setTextOrigin(2, 2.5*inch)
c.drawString(100, 750, "Welcome to Reportlab!")
c.save()
