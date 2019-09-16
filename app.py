from flask import Flask, render_template
import quandl
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Select,RadioGroup
from bokeh.palettes import Spectral4
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from utils import make_dataset,make_plot,update_plot
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8


app = Flask(__name__)

@app.route('/')
def bokeh():

    quandl.ApiConfig.api_key = "xMwhitoyQ___b7Mb9pAt"
    data_dict ={}
    stock_list= ['ATVI','AAPL','GOOG','CSCO']
    for i in stock_list:
        data_dict[i] = quandl.get("WIKI/%s" %i)
        useful_cols = ['Open','High','Low','Close']
    for i in data_dict.keys():
        data_dict[i] = data_dict[i][useful_cols].reset_index()

    current_stock = 'AAPL'
    select_stock = Select(title="stock selection", value=current_stock, options=stock_list)

    source = make_dataset(data_dict,current_stock)
    plot = make_plot(source)

    select_stock.on_change('value', update_plot)

    controls = column(select_stock)
    full = row(plot,controls)
    curdoc().add_root(full)

    curdoc().title = 'Stock demo'


    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(full)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
