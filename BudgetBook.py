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
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.validators import Auto

accountnames = ['Microsoft', 'Google', 'Apple','Cash', 'Sjoelen', 'Strippenkaart','Begin Salos', 'Frans' ]
categorynames = ['Frans', 'Applicaties', 'Optredens', 'Sjoelen', 'Singels']
accountsbalances = [0,0,0,0,0,0,0,0]

def begin_saldos():
    print("Begin saldos")
    return 0

def remove_decimal_num(string_decimal):
    return ''.join(string_decimal.split('.'))

def create_bar_graph(data):
    d = Drawing(600, 500)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 85
    bar.width = 475
    bar.data = data
    bar.categoryAxis.categoryNames = accountnames
    bar.bars[0].fillColor   = PCMYKColor(0,100,100,40,alpha=85)
    bar.bars[1].fillColor   = PCMYKColor(23,51,0,4,alpha=85)
    bar.bars.fillColor       = PCMYKColor(100,0,90,50,alpha=85)
    d.add(bar, '')
    d.save(formats=['pdf'], outDir='./Data', fnRoot='bar1')

def create_pie_chart(legend=False):
    data = [10, 20, 30, 40]
    d = Drawing()
    pie = Pie()
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

def pie_chart_with_legend():
    data = list(range(15, 105, 15))
    drawing = Drawing(width=400, height=200)
    my_title = String(170, 40, 'My Pie Chart', fontSize=14)
    pie = Pie()
    pie.sideLabels = True
    pie.x = 150
    pie.y = 65
    pie.data = data
    pie.labels = accountnames
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data)
    return drawing

def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

def BudgetBookPie():
    doc = SimpleDocTemplate('flowable_with_chart.pdf')
    elements = []
    styles = getSampleStyleSheet()
    ptext = Paragraph('Text before the chart', styles["Normal"])
    elements.append(ptext)
    chart = pie_chart_with_legend()
    elements.append(chart)
    ptext = Paragraph('Text after the chart', styles["Normal"])
    elements.append(ptext)
    doc.build(elements)
    return 0

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
            #print(count, row)
            #key = input("Wait")
            if count > 0:
                findata.append(row)
            count += 1
    print("Length", len(findata))
    data.pop()
    for j in range(len(findata)):
        output_num = remove_decimal_num(findata[j][5])
        if findata[j][1] == "Transfer":
            if findata[j][4] == "Microsoft":
                accountsbalances[0] = accountsbalances[0] + int(output_num)
            if findata[j][4] == "Google":
                accountsbalances[1] = accountsbalances[1] + int(output_num)
            if findata[j][4] == "Apple":
                accountsbalances[2] = accountsbalances[2] + int(output_num)
            if findata[j][4] == "Cash":
                accountsbalances[3] = accountsbalances[3] + int(output_num)
            if findata[j][4] == "Sjoelen":
                accountsbalances[4] = accountsbalances[4] + int(output_num)
            if findata[j][4] == "Strippenkaart":
                accountsbalances[5] = accountsbalances[5] + int(output_num)
            if findata[j][4] == "Begin Saldos":
                accountsbalances[6] = accountsbalances[6] + int(output_num)
            if findata[j][4] == "Frans":
                accountsbalances[7] = accountsbalances[7] + int(output_num)
    data.append([accountsbalances[0],accountsbalances[1],accountsbalances[2],accountsbalances[3],accountsbalances[4],accountsbalances[5],accountsbalances[6],accountsbalances[7]])
    create_bar_graph(data)
    create_pie_chart(True)
    #BudgetBookPie()
    begin_saldos()
    key = input("Wait")
