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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    """
    首页加载
    """
    logger.debug("这是一个debug消息")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port= 9070)