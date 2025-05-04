import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
import time
import io
# pip install flask-excel
# , static_url_path='/static'
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



import logging
import echarts_utils as utils

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    """
    首页加载
    """
    logger.debug("这是一个debug消息")

    return render_template("index.html")

@app.route("/stock/data")
def stock_data():
    res = utils.query_future("600519", "贵州茅台")
    return res.dump_options_with_quotes()

if __name__ == "__main__":
    app.run(debug=True, port= 9070)