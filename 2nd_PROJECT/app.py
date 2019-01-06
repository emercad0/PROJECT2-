import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/chartsBB.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
#Samples_Metadata
chart_table= Base.classes.billboard_listing
Samples = Base.classes.billboard_listing


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():

    """Display the Columns of the generate view panel .
    We  look over dates and weeks based on view 
    """

    # query of the sql that was created for the project
    
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return of what's going to be selected for view
    return jsonify(list(df.columns)[3:7])


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Select and Return the chart Data for given view ."""
    select = [
        chart_table.currentWeekPosition,
        chart_table.previousWeekPosition,
        chart_table.peakPosition,
        chart_table.Artist,
        #chart_table.entryDate,
        #chart_table.entryPosition,
    ]
    results = db.session.query(*select).all()

    # dic viewing rows of columns
    sample_metadata = {}
    for result in results:
        sample_metadata["Current Week Position "] = result[0]
        sample_metadata["Previous Week Position "] = result[1]
        sample_metadata["Peak Position "] = result[2]
        #sample_metadata[" Artist "] = result[3]
        #sample_metadata["entryDate"] = result[4]
        #sample_metadata["entryPosition"] = result[5]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # (sample data)
    # Filter the data based on the view to generate

    sample_data = df.loc[df[sample], ["peakPosition", 
    "entryPosition", 
    "entryDate",
    "currentWeekPosition",
     "Artist",sample]]

    # data as a json 
    data = {
        "entryDate": sample_data.entryDate.values.tolist(),
        "entryPosition": sample_data.entryPosition.values.tolist(),
        "peakPosition": sample_data.peakPosition.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "artist": sample_data.Artist.values.tolist(),
        "currentWeekPosition": sample_data.currentWeekPosition.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
