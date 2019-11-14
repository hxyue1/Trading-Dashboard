from flask import Flask, request, render_template, redirect, flash, Response
#import alphavantage as av
import os
from flask_table import Table, Col
import sqlite3
import pandas as pd
from . import analytics as an
import random

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, DateField, validators, IntegerField
from wtforms.validators import DataRequired

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
        frequency = SelectField(u'Frequency', choices=[('intraday','Intraday'),
                                                       ('daily','Daily')])
        start = DateField('DatePicker',format='%m/%d/%Y', validators=(validators.Optional(),))
        end = DateField('DatePicker',format='%m/%d/%Y', validators=(validators.Optional(),))
        interval = SelectField(u'Interval', choices=[('1min','1 minute'),
                                                     ('5min','5 minute'),
                                                     ('15min','15 minute'),
                                                     ('30min','30 minute'),
                                                     ('60min','60 minute'),
                                                     ])
        submit = SubmitField('Get data')
        
    class ForecastForm(FlaskForm):
        ticker = StringField('Ticker', validators=[DataRequired()])   
        horizon = IntegerField('Number of days to forecast', validators=(validators.Optional(),))
        submit = SubmitField('Forecast')
        
    
    
    @app.route('/', methods=['GET','POST'])
    def describe():

        form=InputForm()
        ticker = form.ticker.data
        frequency = form.frequency.data
        if form.validate_on_submit():

            df = an.get_data(ticker, 
                             frequency=form.frequency.data,
                             interval=form.interval.data,
                             start=form.start.data,
                             end=form.end.data
                             )
            
            if frequency == 'intraday':
                x_coordinates = df['Timestamp'].dt.time
                y_coordinates = df['Close']
            else:
                x_coordinates = df['Timestamp']
                y_coordinates = df['Adjusted Close']
                
            graph1_url = an.build_line(x_coordinates, y_coordinates)
            graph2_url = an.build_hist(df)
            
            return render_template('index.html',
                                   #tables=[df.to_html(classes='data', index=False)],
                                   #titles=df.columns.values,
                                   form=form,
                                   graph1=graph1_url,
                                   graph2=graph2_url
                                   )
        else:
            df = pd.DataFrame({
                    'Timestamp':[1,2],
                    'Open':[1,2]})
            return render_template('index.html',
                                   tables=[df.to_html(classes='data',index=False)],
                                   titles=df.columns.values, form=form)
    
    @app.route('/forecast', methods=['GET','POST'])    
    def forecast():
        form=ForecastForm()
        ticker = form.ticker.data
        horizon = form.horizon.data
        
        if form.validate_on_submit():
            
            df = an.get_data(ticker)
            predictions = an.predict(df, horizon=horizon)
            graph1_url = an.build_line(predictions['Timestamp'],predictions['Returns'])
            graph2_url = an.build_line(predictions['Timestamp'],predictions['Standard Deviations'])
            
        return render_template('forecast.html',
                               form=form,
                               graph1=graph1_url,
                               graph2=graph2_url)

    return(app)


def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()



