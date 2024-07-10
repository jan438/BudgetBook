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

MyAccounts = []
accountnames = ['Microsoft', 'Google', 'Apple','Cash', 'Sjoelen', 'Strippenkaart','Begin Salos', 'Frans' ]
categorynames = ['Frans', 'Applicaties', 'Optredens', 'Sjoelen', 'Singels']

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = int(remove_decimal_num(balance))

def begin_saldos(findata):
    print("Begin saldos", len(findata))
    for j in range(len(findata)):
        if findata[j][1] == "Transfer" and findata[j][3] == "Begin Saldos":
            print(j, findata[j])
            MyAccounts.append(Account(findata[j][4], findata[j][5]))
    return 0

def process_transactions(findata):
    print("Process tranactions", len(findata))
    accountsbalances = [0,0,0,0,0,0,0,0]
    data = []
    for j in range(len(findata)):
        output_num = remove_decimal_num(findata[j][5])
        if findata[j][1] == "Transfer":
            for i in range(len(accountnames)):
                if findata[j][4] == accountnames[i]:
                    accountsbalances[i] = accountsbalances[i] + int(output_num)
    data.append([accountsbalances[0],accountsbalances[1],accountsbalances[2],accountsbalances[3],accountsbalances[4],accountsbalances[5],accountsbalances[6],accountsbalances[7]])
    return data

def remove_decimal_num(string_decimal):
    return ''.join(string_decimal.split('.'))

def create_bar_graph(data):
    d = Drawing()
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
    return d

def create_pie_chart(MyAccounts):
    d = Drawing()
    pie = Pie()
    pie.x = 150
    pie.y = 65
    pie.data = []
    pie.labels = []
    for obj in MyAccounts:
        pie.data.append(obj.balance)
        pie.labels.append(obj.name)
    pie._seriesCount = len(pie.data)
    add_legend(d, pie, pie.data)
    pie.slices.strokeWidth = 0.5
    pie.slices[3].popout = 20
    d.add(pie)
    return d

def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

def BudgetBookBar(data):
    doc = SimpleDocTemplate('flowable_with_barchart.pdf')
    elements = []
    styles = getSampleStyleSheet()
    ptext = Paragraph('Text before the chart', styles["Normal"])
    elements.append(ptext)
    chart = create_bar_graph(data)
    elements.append(chart)
    ptext = Paragraph('Text after the chart', styles["Normal"])
    elements.append(ptext)
    doc.build(elements)
    return 0

def BudgetBookPie(MyAccounts):
    doc = SimpleDocTemplate('flowable_with_piechart.pdf')
    elements = []
    styles = getSampleStyleSheet()
    ptext = Paragraph('Text before the chart', styles["Normal"])
    elements.append(ptext)
    chart = create_pie_chart(MyAccounts)
    elements.append(chart)
    ptext = Paragraph('Text after the chart', styles["Normal"])
    elements.append(ptext)
    doc.build(elements)
    return 0

if __name__ == '__main__':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/Data"
    os.chdir(path)
    file_to_open = "BTRecords.csv"
    count = 0
    som = 0
    findata = []
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if count > 0:
                findata.append(row)
            count += 1
    print("Length", len(findata))
    begin_saldos(findata)
    data = process_transactions(findata)
    BudgetBookBar(data)
    BudgetBookPie(MyAccounts)
    print("MyAccounts", len(MyAccounts))
    for j in range(len(MyAccounts)):
        print("Name", MyAccounts[j].name, MyAccounts[j].balance)
    key = input("Wait")
