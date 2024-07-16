from reportlab.lib.colors import PCMYKColor, red, Color, CMYKColor, yellow
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace, Font, registerFont
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.validators import Auto

class BarChart01(_DrawingEditorMixin,Drawing):

    def __init__(self,width=298,height=165,*args,**kw):
        Drawing.__init__(self, width, height, *args, **kw)
        fontName = 'Times-Roman'
        self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
        self.chart.width = 280
        self.chart.height = 106
        self.chart.x = 15
        self.chart.y = 50 
        self._colors = (PCMYKColor(100, 67, 0, 23), PCMYKColor(60, 40, 0, 13), PCMYKColor(100,0,46,46), PCMYKColor(70,0,36,36))
        self.chart.bars.strokeColor = None
        self.chart.bars.strokeWidth = 0
        for i, color in enumerate(self._colors): self.chart.bars[i].fillColor = color
        self.chart.barSpacing = 4
        self.chart.barWidth = 14
        self.chart.barLabelFormat   = '%s'
        self.chart.barLabels.nudge           = 5
        self.chart.barLabels.angle           = 90
        self.chart.barLabels.fontName        = fontName
        self.chart.barLabels.fontSize        = 5
        self.chart.categoryAxis.categoryNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']
        self.chart.categoryAxis.labelAxisMode='low'
        self.chart.categoryAxis.labels.angle = 0
        self.chart.categoryAxis.labels.boxAnchor = 'n'
        self.chart.categoryAxis.labels.dy = -6
        self.chart.categoryAxis.labels.fillColor = PCMYKColor(0,0,0,100)
        self.chart.categoryAxis.labels.fontName = fontName
        self.chart.categoryAxis.labels.fontSize = 6
        self.chart.categoryAxis.labels.textAnchor='middle'
        self.chart.categoryAxis.tickShift=1
        self.chart.categoryAxis.visibleTicks = 0
        self.chart.categoryAxis.strokeWidth     = 0
        self.chart.categoryAxis.strokeColor         = None
        self.chart.data = [(0.27, 2.17, 3.66, 5.2, -1.33, -3.12, -6.36, 4.4), (1.34, 1.11, 3.53, 4.55, -3.36, -6.64, -7.41, -6.22),(1.37, 2.17, 3.77, 5.12, -1.22, -3.22, -5.36, 4.14), (0.33, 1.21, 3.52, 4.77, -1.36, -6.64, -8.1, -7.52)]
        self.chart.groupSpacing = 15
        self.chart.valueAxis.avoidBoundFrac     = None
        self.chart.valueAxis.gridStrokeWidth    = 0.25
        self.chart.valueAxis.labels.fontName    = fontName
        self.chart.valueAxis.labels.fontSize    = 6
        self.chart.valueAxis.rangeRound         = 'both'
        self.chart.valueAxis.strokeWidth        = 0
        self.chart.valueAxis.visibleGrid        = 1
        self.chart.valueAxis.visibleTicks       = 0
        self.chart.valueAxis.visibleAxis        = 0
        self.chart.valueAxis.gridStrokeColor    = PCMYKColor(70,0,36,36)
        self.chart.valueAxis.gridStrokeWidth    = 0.25
        self.chart.valueAxis.valueStep          = None#3
        self.chart.valueAxis.labels.dx          = -3
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.alignment = 'right'
        self.legend.autoXPadding = 6
        self.legend.boxAnchor = 'sw'
        self._seriesNames = 'BP', 'Shell Transport & Trading', 'Liberty International', 'Royal Bank of Scotland'
        self.legend.columnMaximum = 3
        self.legend.dx = 8
        self.legend.dxTextSpace = 4
        self.legend.dy = 6
        self.legend.fontSize = 6
        self.legend.fontName = fontName
        self.legend.strokeColor = None
        self.legend.strokeWidth = 0
        self.legend.subCols.minWidth = 55
        self.legend.variColumn = 1
        self.legend.x = 6
        self.legend.y = 1
        self.legend.deltay = 10
        self._add(self,Label(),name ='XLabel',validate=None,desc="The label on the horizontal axis")
        self.XLabel._text = ""
        self.XLabel.fontSize = 6
        self.XLabel.height = 0
        self.XLabel.maxWidth = 100
        self.XLabel.textAnchor ='middle'
        self.XLabel.x = 140
        self.XLabel.y = 10
        self._add(self,Label(),name='YLabel',validate=None,desc="The label on the vertical axis")
        self.YLabel._text = ""
        self.YLabel.angle = 90
        self.YLabel.fontSize = 6
        self.YLabel.height = 0
        self.YLabel.maxWidth = 100
        self.YLabel.textAnchor ='middle'
        self.YLabel.x = 12
        self.YLabel.y = 80
        self.legend.autoXPadding     = 65

    def getContents(self):
        self.legend.colorNamePairs = list(zip(self._colors, self._seriesNames))
        return Drawing.getContents(self)

if __name__=="__main__":
    BarChart01().save(formats=['pdf'],outDir='./Data',fnRoot=None)