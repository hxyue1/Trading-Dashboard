from flask import Flask, request, render_template, redirect, flash, Response
#import alphavantage as av
import os
from flask_table import Table, Col
import sqlite3
import pandas as pd
from . import alphavantage as av
import random

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'testing.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    class InputForm(FlaskForm):
        ticker = StringField('Ticker', validators=[DataRequired()])
        #frequency = StringField('Frequency', validators=[DataRequired()])   
        frequency = SelectField(u'Frequency', choices=[('daily','Daily'),
                                                       ('intraday','Intraday')])
        interval = SelectField(u'Interval', choices=[('1min','1 minute'),
                                                     ('5min','5 minute'),
                                                     ('15min','15 minute'),
                                                     ('30min','30 minute'),
                                                     ('60min','60 minute'),
                                                     ])
        submit = SubmitField('Get data')
        
    def build_graph(df, frequency):   
        
        if frequency == 'intraday':
            x_coordinates = df['Timestamp'].dt.time
        else:
            x_coordinates = df['Timestamp']
            
        y_coordinates = df['Close']
        
        img = io.BytesIO()
        plt.plot(x_coordinates, y_coordinates)
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return 'data:image/png;base64,{}'.format(graph_url)
    
    @app.route('/input', methods=['GET','POST'])
    def example_1():
        
        form=InputForm()
        ticker = form.ticker.data
        frequency = form.frequency.data
        
        if form.validate_on_submit():
            
            ticker = form.ticker.data
            df = av.get_data(ticker, 
                             frequency=form.frequency.data,
                             interval=form.interval.data)
            
            graph1_url = build_graph(df, frequency)
            
            return render_template('input.html',
                                   tables=[df.to_html(classes='data', index=False)],
                                   titles=df.columns.values,
                                   form=form,
                                   graph1=graph1_url
                                   )
        else:
            df = pd.DataFrame({
                    'Timestamp':[1,2],
                    'Open':[1,2]})
            return render_template('input.html',
                                   tables=[df.to_html(classes='data',index=False)],
                                   titles=df.columns.values, form=form)
        @app.route('/')
        def example_2():
            form=InputForm()
            con = sqlite3.connect('testdb.db')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM BHP')
            data = cursor.fetchall()
            return render_template('example_2.html', value=data, form=form)
        


    return(app)










 

def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()



