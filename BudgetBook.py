import os
import sys
import csv
from pathlib import Path
from datetime import datetime, date, timedelta
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import brown,blue, PCMYKColor, black, green, red, yellow, purple
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.validators import Auto

MyAccounts = []
categorynames = ['Frans', 'Applicaties', 'Optredens', 'Sjoelen', 'Kapper', 'Singels']
endmonth = []
startdate = date(1990,1,1)

class Account:
    def __init__(self, name, balance, endmonth):
        self.name = name
        self.balance = int(remove_decimal_num(balance))
        self.endmonth = endmonth

def print_myaccounts():
    for j in range(len(MyAccounts)):
        print("My accounts", MyAccounts[j].name, str(MyAccounts[j].balance))
    return

def days_since_1990(year, month, day):          
    d = date(year, month, day)
    delta = d - startdate
    return delta.days

def date_from_days(days): 
    delta = timedelta(days)    
    offset = startdate + delta               
    return offset

def begin_saldos(findata):
    for j in range(len(findata)):
        if findata[j][1] == "Transfer" and findata[j][3] == "Begin Saldos":
            endmonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            MyAccounts.append(Account(findata[j][4], findata[j][5], endmonth))
    print_myaccounts()
    return

def process_transactions(findata, d):
    delta = date_from_days(d)
    enddate = delta.strftime('%Y-%m-%d')
    endyear = int(enddate[:4])
    endmonth = int(enddate[5:7])
    endday = int(enddate[8:10])
    print("Process tranactions", len(findata), d)
    for j in range(len(findata)):
        bookdate = findata[j][0]
        bookday = int(bookdate[:2])
        bookmonth = int(bookdate[3:5])
        bookyear = int(bookdate[6:10])
        try:
            bd = days_since_1990(bookyear, bookmonth, bookday)
        except ValueError:
            print("ValueError", findata[j][0], findata[j][2]) 
        if bd <= d and findata[j][3] != "Begin Saldos":
            output_num = remove_decimal_num(findata[j][5])
            first = False
            second = False
            for i in range(len(MyAccounts)):
                if findata[j][3] == MyAccounts[i].name:
                    firstaccount = i
                    first = True
                if findata[j][4] == MyAccounts[i].name:
                    secondaccount = i
                    second = True
            if first and not second:
                if findata[j][4] == "Frans":
                    MyAccounts[firstaccount].balance = MyAccounts[firstaccount].balance + int(output_num)
                else:
                    MyAccounts[firstaccount].balance = MyAccounts[firstaccount].balance - int(output_num)
            if first and second:
                MyAccounts[firstaccount].balance = MyAccounts[firstaccount].balance -  int(output_num)      
                MyAccounts[secondaccount].balance = MyAccounts[secondaccount].balance +  int(output_num)   
            print(j, findata[j][0], findata[j][1], findata[j][2], findata[j][3], findata[j][4], findata[j][5])
    return

def remove_decimal_num(string_decimal):
    return ''.join(string_decimal.split('.'))

def create_bar_graph(data):
    d = Drawing()
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 85
    bar.width = 475
    accountsbalances = []
    bar.categoryAxis.categoryNames = []
    for obj in data:
        accountsbalances.append(obj.balance)
        bar.categoryAxis.categoryNames.append(obj.name)
    bar.data = []
    bar.data.append(accountsbalances)
    bar.bars[0, 0].fillColor = blue
    bar.bars[0, 1].fillColor = green
    bar.bars[0, 2].fillColor = brown
    d.add(bar, '')
    return d

def create_pie_chart(data):
    d = Drawing()
    pie = Pie()
    pie.x = 150
    pie.y = 65
    pie.data = []
    pie.labels = []
    for obj in data:
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

def BudgetBookPie(data):
    doc = SimpleDocTemplate('flowable_with_piechart.pdf')
    elements = []
    styles = getSampleStyleSheet()
    ptext = Paragraph('Text before the chart', styles["Normal"])
    elements.append(ptext)
    chart = create_pie_chart(data)
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
    d = days_since_1990(2023, 12, 31)
    process_transactions(findata, d)
    BudgetBookBar(MyAccounts)
    BudgetBookPie(MyAccounts)
    print_myaccounts()
    key = input("Wait")
