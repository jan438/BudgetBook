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

def remove_decimal_num(string_decimal):
    return ''.join(string_decimal.split('.'))

def create_bar_graph(data):
    d = Drawing(600, 500)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 85
    bar.width = 475
    bar.data = data
    bar.categoryAxis.categoryNames = ['Microsoft', 'Google', 'Apple',
                                      'Cash', 'Sjoelen', 'Strippenkaart',
                                      'Begin Salos', 'Frans' ]
    bar.bars[0].fillColor   = PCMYKColor(0,100,100,40,alpha=85)
    bar.bars[1].fillColor   = PCMYKColor(23,51,0,4,alpha=85)
    bar.bars.fillColor       = PCMYKColor(100,0,90,50,alpha=85)
    d.add(bar, '')
    d.save(formats=['pdf'], outDir='./Data', fnRoot='bar1')

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
    d.save(formats=['pdf'], outDir='./Data', fnRoot='pie1')

def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

if __name__ == '__main__':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/Data"
    os.chdir(path)
    data = [[1,2,3,None,None,5,5,5],[1,2,3,4,5,6,7,8]]
    file_to_open = "BTRecords.csv"
    count = 0
    som = 0
    findata = []
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print("row", row)
            if count > 0:
                output_num = remove_decimal_num(row[5])
                print("row[5]",row[5], output_num, count)
                findata.append(row)
            count += 1
    print("Length", len(findata))
    data.pop()
    data.append([count,7,6,som,4,3,2,count])
    create_bar_graph(data)
    create_pie_chart(True)
    key = input("Wait")
