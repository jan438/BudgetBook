from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.validators import Auto
from reportlab.lib.formatters import DecimalFormatter

class PieChart01(_DrawingEditorMixin,Drawing):
    def __init__(self,width=540,height=177,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        self._colors = PCMYKColor(100,55,0,55), PCMYKColor(55,24,0,9), PCMYKColor(0,70,60,5), PCMYKColor(10,0,49,28), PCMYKColor(47,64,28,0), PCMYKColor(10,10,73,0), PCMYKColor(22,3,0,0), PCMYKColor(22,0,100,8), PCMYKColor(0,64,100,0), PCMYKColor(0,100,99,4), PCMYKColor(0,30,72,11), PCMYKColor(50,0,25,30), PCMYKColor(64,100,0,14), PCMYKColor(75,0,7,0), PCMYKColor(23,2,0,77), PCMYKColor(30,56,100,37), PCMYKColor(0,4,22,32), PCMYKColor(0,30,100,0),
        fontSize = 7
        fontName = 'Times-Roman'
        self._add(self,Pie(),name='chart',validate=None,desc=None)
        self.chart.width             = self.chart.height = 148
        self.chart.sameRadii         = 1
        self.chart.x                 = 1
        self.chart.y                 = 18
        self.chart.slices.strokeColor  = PCMYKColor(0,0,0,0)
        self.chart.slices.strokeWidth  = 0.5
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self._add(self,Legend(),name='legendHeader',validate=None,desc=None)
        self.legendHeader.x         = 160
        self.legendHeader.y         = self.height
        self.legendHeader.fontSize  = fontSize
        self.legendHeader.fontName  = 'Times-Bold'
        self.legendHeader.subCols[0].minWidth = 240
        self.legendHeader.subCols[0].align = 'left'
        self.legendHeader.subCols[1].minWidth = 60
        self.legendHeader.subCols[1].align = 'left'
        self.legendHeader.subCols[2].minWidth = 50
        self.legendHeader.subCols[2].align = 'left'
        self.legendHeader.subCols[3].minWidth = 50
        self.legendHeader.subCols[3].align = 'left'
        black = PCMYKColor(0,0,0,100)
        self.legendHeader.colorNamePairs = [(black, ('Company','Previous Year','This Year','Change'))]
        self.legend.x                = 160
        self.legend.y                = 163
        self.legend.fontSize         = fontSize
        self.legend.fontName         = fontName
        self.legend.dx               = 6
        self.legend.dy               = 6
        self.legend.dxTextSpace      = 5
        self.legend.yGap             = 0
        self.legend.deltay           = 12
        self.legend.strokeColor      = PCMYKColor(0,0,0,0)
        self.legend.strokeWidth      = 0
        self.legend.columnMaximum    = 99
        self.legend.alignment        = 'right'
        self.legend.variColumn       = 0
        self.legend.dividerDashArray = None
        self.legend.dividerWidth     = 0.5
        self.legend.dividerOffsX     = (0, 0)
        self.legend.dividerLines     = 7
        self.legend.dividerOffsY     = 6
        self.legend.subCols[0].align = 'left'
        self.legend.subCols[0].minWidth = 230
        self.legend.subCols[1].align = 'left'
        self.legend.subCols[1].align='numeric'
        self.legend.subCols[1].dx = -45
        self.legend.subCols[1].minWidth = 60
        self.legend.subCols[2].align = 'left'
        self.legend.subCols[2].align='numeric'
        self.legend.subCols[2].dx = -40
        self.legend.subCols[2].minWidth = 50
        self.legend.subCols[3].align='numeric'
        self.legend.subCols[3].dx = -10
        self.legend.subCols[3].dx = -15
        self._seriesNames = 'BP', 'Shell Transport & Trading', 'Liberty International', 'Persimmon', 'Royal Bank of Scotland', 'Land Securities', 'BT', 'Standard Chartered', 'Bovis Homes', 'HSBC Holdings', 'Natwest', 'Barclays', 'Sainsburys'
        self._seriesData1 = 27.40, 0, 10.33, 0.6, 27.38, 0, 0, 8.21, 9.30, 3.65, 0, 0, 10.37, 2.4, 2.5, 2.4, 2.55, 1.6
        self._seriesData2 = 37.89, 0, 12.73, 0.74, 24.71, 0, 0, 6.94, 7.87, 0, 0, 0, 3.4, 1.79, 1.8, 1.81, 1.82, 0.5
        self._seriesData3 = [x-y for (x,y) in zip(self._seriesData1, self._seriesData2)]
        formatter = DecimalFormatter(places=2,thousandSep=',',decimalSep='.',suffix='%')
        names = list(zip(self._seriesNames,
        map(formatter, self._seriesData1),
        map(formatter, self._seriesData2),
        map(formatter, self._seriesData3)))
        self.legend.colorNamePairs = list(zip(self._colors, names))
        self.chart.data  = self._seriesData1
        for i, v in enumerate(self.chart.data): self.chart.slices[i].fillColor = self._colors[i]
        self.legend.deltax         = 75
        self.width        = 450
        self.height       = 200
        self.width        = 400
        self.legendHeader.subCols[0].minWidth = 100
        self.legend.subCols[0].minWidth = 90
        self.chart.height           = 125
        self.chart.width            = 120
        self.chart.height           = 120
        self.chart.y                = 40
        self.chart.x                = 12
        self.legend.x              = 150
        self.legendHeader.x              = 150

if __name__=="__main__":
    PieChart01().save(formats=['pdf'],outDir='./Data',fnRoot=None)
    key = input("Wait")