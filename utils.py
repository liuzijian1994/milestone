import quandl
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Select,RadioGroup
from bokeh.palettes import Spectral4
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource

def make_dataset(src, name):
    return(src[name])

def make_plot(src):
    y1 = list(src['High'])
    y2 = list(src['Low'])
    y3 = list(src['Close'])
    y4 = list(src['Open'])
    x = list(src['Date'])
    #output_file("lines.html")

    p = figure(title="Click on legend entries to hide", x_axis_label='date',x_axis_type='datetime', y_axis_label='price')

    p.line(x, y1, legend="High price", line_width=1,line_color="red")
    p.line(x, y2, legend="Low price", line_width=1,line_color="blue")
    p.line(x, y3, legend="Close price", line_width=1,line_color="yellow")
    p.line(x, y4, legend="Open price", line_width=1,line_color="orange")
    p.legend.click_policy="hide"

    #show(p)
    return(p)

def update_plot(attrname, old, new):
    current_stock = select_stock.value
    data_source= make_dataset(data_dict,current_stock)
    source = data_source
    full.children[0] = make_plot(source)
