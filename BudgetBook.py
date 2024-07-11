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

countaccounts = 7
countcategories = 6
MyAccounts = []
accountnames = ['Microsoft', 'Google', 'Apple','Cash', 'Sjoelen', 'Strippenkaart','Begin Salos']
categorynames = ['Frans', 'Applicaties', 'Optredens', 'Sjoelen', 'Kapper', 'Singels']
endmonth = []

class Account:
    def __init__(self, name, balance, endmonth):
        self.name = name
        self.balance = int(remove_decimal_num(balance))
        self.endmonth = endmonth

def begin_saldos(findata):
    print("Begin saldos", len(findata))
    for j in range(len(findata)):
        if findata[j][1] == "Transfer" and findata[j][3] == "Begin Saldos":
            endmonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            print(j, findata[j], len(endmonth))
            MyAccounts.append(Account(findata[j][4], findata[j][5], endmonth))
    return 0

def process_tranfer(first, second, amount):
    MyAccounts[first].balance = MyAccounts[first].balance + int(amount)
    MyAccounts[second].balance = MyAccounts[second].balance - int(amount)
    return

def process_transactions(findata):
    print("Process tranactions", len(findata))
    accountsbalances = [0,0,0,0,0,0,0]
    data = []
    for j in range(len(findata)):
        output_num = remove_decimal_num(findata[j][5])
        if not (findata[j][1] == "Transfer" and findata[j][3] != "Begin Saldos"):
            for i in range(countaccounts):
                if findata[j][3] == accountnames[i]:
                    secondaccount = False
                    for k in range(countaccounts):
                        if findata[j][4] == accountnames[k]:
                            secondaccount = True
                            process_tranfer(i, k, output_num)
                    if not secondaccount:
                        print("Category", findata[j][4] )
                    print(j, accountnames[i], "2e", secondaccount, findata[j][0], accountnames[i], "Desc", findata[j][2],)
                    amount = int(output_num)
                    accountsbalances[i] = accountsbalances[i] + amount
            #print(j, findata[j][0], findata[j][1],findata[j][2],findata[j][3],findata[j][4], findata[j][5])
        else:
            print(j, findata[j][0], findata[j][1],findata[j][2],findata[j][3],findata[j][4], findata[j][5])
    data.append(accountsbalances)
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
