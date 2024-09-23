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
MyCategories = []
endmonth = []
processed = []
startdate = date(1990,1,1)

class Account:
    def __init__(self, name, balance, endmonth):
        self.name = name
        self.balance = int(remove_decimal_marker(balance))
        self.endmonth = endmonth

class Category:
    def __init__(self, name):
        self.name = name
        self.total = 0

def print_myaccounts(i):
    for j in range(len(MyAccounts)):
        print(i, "My accounts", MyAccounts[j].name, str(MyAccounts[j].balance))
    return

def print_mycategories(i):
    for j in range(len(MyCategories)):
        print(i, "My categories", MyCategories[j].name, str(MyCategories[j].total))
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
        if findata[j][0] == "Transfer" and findata[j][4][:12] == "Begin Saldos":
            account = findata[j][4][17:len(findata[j][4])-1]
            endmonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            MyAccounts.append(Account(account, findata[j][3], endmonth))
            processed.append(findata[j])
    return

def init_categories(findata):
    for j in range(len(findata)):
        category = findata[j][0]
        if category != "Transfer" and category != "Frans":
            categoryindex = -1
            for i in range(len(MyCategories)):
                if category == MyCategories[i].name:
                    categoryindex = i
                    break
            if categoryindex < 0:
                MyCategories.append(Category(category))
    return

def process_transfers(findata):
    for j in range(len(findata)):
        if findata[j][0] == "Transfer" and findata[j][4][:12] != "Begin Saldos":
            account1 = findata[j][4][:4]
            account2 = findata[j][4][9:len(findata[j][4])-1]
            amount = int(remove_decimal_marker(findata[j][3]))
            firstaccount = -1
            secondaccount = -1
            for i in range(len(MyAccounts)):
                if account1 == MyAccounts[i].name:
                    firstaccount = i
            for i in range(len(MyAccounts)):
                if account2 == MyAccounts[i].name:
                    secondaccount = i
            MyAccounts[firstaccount].balance = MyAccounts[firstaccount].balance - amount
            MyAccounts[secondaccount].balance = MyAccounts[secondaccount].balance + amount
            processed.append(findata[j])
    return

def process_frans(findata):
    for j in range(len(findata)):
        if findata[j][0] == "Frans":
            account = findata[j][4][:-1]
            amount = int(remove_decimal_marker(findata[j][3]))
            firstaccount = -1
            for i in range(len(MyAccounts)):
                if account == MyAccounts[i].name:
                    firstaccount = i
            MyAccounts[firstaccount].balance = MyAccounts[firstaccount].balance + amount
            processed.append(findata[j])
    return

def process_transactions(findata):
    for j in range(len(findata)):
        category = findata[j][0]
        if category != "Transfer" and category != "Frans":
            categoryindex = -1
            for i in range(len(MyCategories)):
                if category == MyCategories[i].name:
                    categoryindex = i
                    break
            if categoryindex < 0:
                break
            account = findata[j][4][:-1]
            amount = int(remove_decimal_marker(findata[j][3]))
            firstaccount = -1
            for i in range(len(MyAccounts)):
                if account == MyAccounts[i].name:
                    firstaccount = i
            MyAccounts[firstaccount].balance = MyAccounts[firstaccount].balance + amount
            MyCategories[categoryindex].total = MyCategories[categoryindex].total - amount
            processed.append(findata[j])
    return

def remove_decimal_marker(string_decimal):
    return ''.join(string_decimal.split(','))

def create_bar_graph(data):
    d = Drawing()
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 30
    bar.width = 300
    bar.height = 150
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
    bar.bars[0, 3].fillColor = yellow
    bar.bars[0, 4].fillColor = red
    bar.bars[0, 5].fillColor = purple
    d.add(bar, '')
    return d

def create_pie_chart(data):
    d = Drawing()
    pie = Pie()
    pie.x = 225
    pie.y = 0
    pie.width = 250
    pie.height = 150
    pie.data = []
    pie.labels = []
    for obj in data:
        pie.data.append(obj.balance)
        pie.labels.append(obj.name)
    pie._seriesCount = len(pie.data)
    add_legend(d, pie, pie.data)
    pie.slices.strokeWidth = 0.5
    pie.slices[3].popout = 20
    pie.slices[0].fillColor = blue
    pie.slices[1].fillColor = green
    pie.slices[2].fillColor = brown
    pie.slices[3].fillColor = yellow
    pie.slices[4].fillColor = red
    pie.slices[5].fillColor = purple
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
    if sys.platform[0] == 'l':
        path = '/home/jan/git/BudgetBook/Data'
    if sys.platform[0] == 'w':
        path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook/Data"
    os.chdir(path)
    file_to_open = "OurBudgetBookExport.csv"
    count = 0
    som = 0
    findata = []
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file, delimiter = ';')
        for row in csvreader:
            if count > 0:
                findata.append(row)
            count += 1
    print("Length", len(findata))
    begin_saldos(findata)
    init_categories(findata)
    process_transfers(findata)
    process_frans(findata)
    #d = days_since_1990(2023, 12, 31)
    process_transactions(findata)
    print("Count processed", len(processed))
    BudgetBookBar(MyAccounts)
    BudgetBookPie(MyAccounts)
    print_myaccounts(0)
    print_mycategories(0)
    key = input("Wait")
