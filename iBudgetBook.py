import os
import sys
import csv
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import brown,blue, PCMYKColor, black
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.validators import Auto

def create_bar_graph():
    d = Drawing(280, 250)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 85
    data = [[1,2,3,None,None,None,5],
            [10,5,2,6,8,3,5],
            [5,7,2,8,8,2,5],
            [2,10,2,1,8,9,5],
            ]
    bar.data = data
    bar.categoryAxis.categoryNames = ['Year1', 'Year2', 'Year3',
                                      'Year4', 'Year5', 'Year6',
                                      'Year7']
    bar.bars[0].fillColor   = PCMYKColor(0,100,100,40,alpha=85)
    bar.bars[1].fillColor   = PCMYKColor(23,51,0,4,alpha=85)
    bar.bars.fillColor       = PCMYKColor(100,0,90,50,alpha=85)
    d.add(bar, '')
    d.save(formats=['pdf'], outDir='./PDF', fnRoot='test')

def create_pie_chart(legend=False):
    data = [10, 20, 30, 40]
    d = Drawing()
    pie = Pie()
    # required by Auto
    pie._seriesCount = 4
    if legend:
        add_legend(d, pie, data)
    pie.x = 150
    pie.y = 65
    pie_data = data
    pie.labels = [letter for letter in 'abcd']
    pie.slices.strokeWidth = 0.5
    pie.slices[3].popout = 20
    d.add(pie)
    d.save(formats=['pdf'], outDir='./PDF', fnRoot='test-pie')

def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

if __name__ == '__main__':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/PDF"
    os.chdir(path)
    create_bar_graph()
    create_pie_chart(True)