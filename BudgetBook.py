import os
import sys
import csv
from pathlib import Path
from datetime import datetime, date, timedelta
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import LETTER, A4, landscape, portrait
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import blue, green, black, red, pink, gray, brown, purple, orange, yellow, white, lightgrey
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import brown,blue, PCMYKColor, black, green, red, yellow, purple
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.validators import Auto

bbfont = "LiberationSerif"

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

def print_myaccounts():
    print("Count accounts", len(MyAccounts))
    for j in range(len(MyAccounts)):
        print(j, MyAccounts[j].name, str(MyAccounts[j].balance))
    return

def print_mycategories():
    print("Count categories", len(MyCategories))
    for j in range(len(MyCategories)):
        print(j, MyCategories[j].name, str(MyCategories[j].total))
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
  
def BBAccountLegends(draw_obj, x, y):
    legend = Legend()
    legend.alignment = 'right'
    legend.fontName = bbfont
    legend.fontSize = 10
    legend.x = x
    legend.y = y
    legend.colorNamePairs = [
        (blue, (MyAccounts[0]. name, "€ {:.2f}".format(MyAccounts[0].balance / 100))), 
        (green, (MyAccounts[1].name, "€ {:.2f}".format(MyAccounts[1].balance / 100))),
        (brown, (MyAccounts[2].name, "€ {:.2f}".format(MyAccounts[2].balance / 100))),
        (yellow, (MyAccounts[3].name, "€ {:.2f}".format(MyAccounts[3].balance / 100))), 
        (red, (MyAccounts[4].name, "€ {:.2f}".format(MyAccounts[4].balance / 100))), 
        (purple, (MyAccounts[5].name, "€ {:.2f}".format(MyAccounts[5].balance / 100)))]
    draw_obj.add(legend)
   
def BBCategoryLegends(draw_obj, x, y):
    legend = Legend()
    legend.alignment = 'right'
    legend.fontName = bbfont
    legend.fontSize = 10
    legend.x = x
    legend.y = y
    legend.colorNamePairs = [
        (blue, (MyCategories[0]. name, "€ {:.2f}".format(MyCategories[0].total / 100))), 
        (green, (MyCategories[1].name, "€ {:.2f}".format(MyCategories[1].total / 100))),
        (brown, (MyCategories[2].name, "€ {:.2f}".format(MyCategories[2].total / 100))),
        (yellow, (MyCategories[3].name, "€ {:.2f}".format(MyCategories[3].total / 100))), 
        (red, (MyCategories[4].name, "€ {:.2f}".format(MyCategories[4].total / 100))), 
        (purple, (MyCategories[5].name, "€ {:.2f}".format(MyCategories[5].total / 100)))]
    draw_obj.add(legend)

def BudgetBookCharts(categories, accounts):
    d = Drawing(595, 842)
    d.add(String(75, 825, "Account Bar Report", fontSize = 20, fillColor = purple))
    bar = VerticalBarChart()
    bar.categoryAxis.labels.fontName = bbfont
    bar.categoryAxis.labels.fontSize = 12
    bar.x = 75
    bar.y = 645
    bar.width = 475
    bar.height = 170
    accountbalances = []
    bar.categoryAxis.categoryNames = []
    for obj in accounts:
        accountbalances.append(obj.balance)
        bar.categoryAxis.categoryNames.append(obj.name)
    bar.data = []
    bar.data.append(accountbalances)
    bar.bars[0, 0].fillColor = blue
    bar.bars[0, 1].fillColor = green
    bar.bars[0, 2].fillColor = brown
    bar.bars[0, 3].fillColor = yellow
    bar.bars[0, 4].fillColor = red
    bar.bars[0, 5].fillColor = purple
    d.add(bar, '')
    d.add(String(75, 610, "Category Bar Report", fontSize = 20, fillColor = purple))
    bar = VerticalBarChart()
    bar.categoryAxis.labels.fontName = bbfont
    bar.categoryAxis.labels.fontSize = 12
    bar.x = 75
    bar.y = 430
    bar.width = 475
    bar.height = 170
    categorytotals = []
    bar.categoryAxis.categoryNames = []
    for obj in categories:
        categorytotals.append(obj.total)
        bar.categoryAxis.categoryNames.append(obj.name)
    bar.data = []
    bar.data.append(categorytotals)
    bar.bars[0, 0].fillColor = blue
    bar.bars[0, 1].fillColor = green
    bar.bars[0, 2].fillColor = brown
    bar.bars[0, 3].fillColor = yellow
    bar.bars[0, 4].fillColor = red
    bar.bars[0, 5].fillColor = purple
    d.add(bar, '')
    d.add(String(75, 390, "Account Pie Report", fontSize = 20, fillColor = purple))
    pie = Pie()
    pie.x = 100
    pie.y = 50
    pie.width = 175
    pie.height = 175
    pie.data = []
    pie.labels = []
    legends = []
    for obj in accounts:
        pie.data.append(obj.balance)
        pie.labels.append(obj.name)
    pie._seriesCount = len(pie.data)
    BBAccountLegends(d, 50, 330)
    pie.slices.strokeWidth = 0.5
    pie.slices[3].popout = 20
    pie.slices.fontName = bbfont
    pie.slices.fontSize = 12
    pie.slices[0].fillColor = blue
    pie.slices[1].fillColor = green
    pie.slices[2].fillColor = brown
    pie.slices[3].fillColor = yellow
    pie.slices[4].fillColor = red
    pie.slices[5].fillColor = purple
    d.add(pie)
    d.add(String(340, 390, "Category Pie Report", fontSize = 20, fillColor = purple))
    pie = Pie()
    pie.x = 340
    pie.y = 50
    pie.width = 175
    pie.height = 175
    pie.data = []
    pie.labels = []
    for obj in categories:
        pie.data.append(obj.total)
        pie.labels.append(obj.name)
    pie._seriesCount = len(pie.data)
    BBCategoryLegends(d, 340, 330)
    pie.slices.strokeWidth = 0.5
    pie.slices.fontName = bbfont
    pie.slices.fontSize = 12
    pie.slices[0].fillColor = blue
    pie.slices[1].fillColor = green
    pie.slices[2].fillColor = brown
    pie.slices[3].fillColor = yellow
    pie.slices[4].fillColor = red
    pie.slices[5].fillColor = purple
    d.add(pie)
    renderPDF.drawToFile(d, 'PDF/BugetBook.pdf')
    return

def BudgetBookBar(data):
    d = create_bar_graph(data)
    renderPDF.drawToFile(d, 'PDF/flowable_with_barchart.pdf')
    return

def BudgetBookAccountsPie(data):
    d = create_pie_accounts(data)
    renderPDF.drawToFile(d, 'PDF/accounts.pdf')
    return

def BudgetBookCategoriesPie(data):
    d = create_pie_categories(data)
    renderPDF.drawToFile(d, 'PDF/categories.pdf')    
    return

if __name__ == '__main__':
    if sys.platform[0] == 'l':
        path = '/home/jan/git/BudgetBook'
    if sys.platform[0] == 'w':
        path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook"
    os.chdir(path)
    pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
    count = 0
    som = 0
    findata = []
    file_to_open = "Data/CSV Export 2023.csv"
    with open(file_to_open, 'r', encoding ='utf-8-sig') as file:
        csvreader = csv.reader(file, delimiter = ';')
        for row in csvreader:
            findata.append(row)
            count += 1
    file_to_open = "Data/CSV Export 2024.csv"
    with open(file_to_open, 'r', encoding = 'utf-8-sig') as file:
        csvreader = csv.reader(file, delimiter = ';')
        for row in csvreader:
            findata.append(row)
            count += 1
    file_to_open = "Data/CSV Export 2025.csv"
    with open(file_to_open, 'r', encoding ='utf-8-sig') as file:
        csvreader = csv.reader(file, delimiter = ';')
        for row in csvreader:
            findata.append(row)
            count += 1
    print("Length", len(findata))
    begin_saldos(findata)
    print("Begin saldos")
    print_myaccounts()
    init_categories(findata)
    print("\nInit categries")
    print_myaccounts()
    print_mycategories()
    process_transfers(findata)
    print("\nProcess transfers")
    print_myaccounts()
    process_frans(findata)
    print("\nProcess Frans")
    print_myaccounts()
    process_transactions(findata)
    print("\nProcess transactions")
    print("Count processed", len(processed))
    BudgetBookCharts(MyCategories, MyAccounts)
    print_myaccounts()
    print_mycategories()
    key = input("Wait")
