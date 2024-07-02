import os
import sys
import csv
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import brown,blue
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import black

path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/PDF"
os.chdir(path)
c = Canvas("Hello-world.pdf")
textobject = c.beginText()
textobject.setTextOrigin(2, 2.5*inch)
c.drawString(100, 750, "Welcome to Reportlab!")
c.save()
