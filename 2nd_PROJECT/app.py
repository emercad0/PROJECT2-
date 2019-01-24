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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/tableForBB.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.billboard100
Samples = Base.classes.billboard_listing
namesOf = Base.classes.billboard100
topArtist = Base.classes.topArtist


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Display the Columns in the generate view panel .
    We want to look over dates and weeks based on sample 
    """

    # Use Pandas to perform the sql query
    stmt = db.session.query(namesOf).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    ##return jsonify(list(df.columns)[7:10])
    return jsonify(list(df.songs))
    #return jsonify(list(df.columns)[:1])


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.index,
        Samples_Metadata.artist,
        Samples_Metadata.songs,
        Samples_Metadata.weekPosition,
        Samples_Metadata.entryPosition,
        Samples_Metadata.totalWeeks,
        Samples_Metadata.peakPosition,
        #Samples_Metadata.previousPosition,

    ]

    results = db.session.query(
        *sel).filter(Samples_Metadata.songs == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["Number of Weeks in the Top 100 Chart"] = result[5]
        sample_metadata["Entry Spot"] = result[4]
        sample_metadata["Average Weekly Spot"] = result[3]
        sample_metadata['Peak Spot'] = result[6]
        sample_metadata["Artist Name"] = result[1]
        sample_metadata["Song's Name"] = result[2]

        #sample_metadata["entryDate"] = result[6]
        #sample_metadata["entryPosition"] = result[7]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/listofpositions")
def listofpositions():
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[7:10])


@app.route("/positions/<positions>")
def samples(positions):
    """Return `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    sm_stmt = db.session.query(Samples_Metadata).statement
    sm_df = pd.read_sql_query(sm_stmt, db.session.bind)

    stmt_ta = db.session.query(topArtist).statement
    ta_df = pd.read_sql_query(stmt_ta, db.session.bind)

    # Filter the data based on the view to generate
    # (sample number) and
    sample_smdata = sm_df.loc[sm_df[positions] > 1, [
        "previousPosition", "weekPosition", "songs", "artist", positions]]
    sample_data = df.loc[df[positions] <= 5, [
        "weekPosition", "artist", "WeekOf", "songs", positions]]
    topArtist_data = ta_df.loc[ta_df[positions] > 0, [
        "artist", "previousPosition", "weekPosition", positions]]
    # Format the data to send as json
    data = {
        "weekPosition": sample_data.weekPosition.values.tolist(),
        "WeekOf": sample_data.WeekOf.values.tolist(),
        "sample_values": sample_data[positions].values.tolist(),
        "songs": sample_data.songs.values.tolist(),
        "artist": sample_data.artist.values.tolist(),

        "sample_smdata": sample_smdata[positions].values.tolist(),
        "sampleMeanWeeksP": sample_smdata.weekPosition.values.tolist(),
        "sampleMeanPP": sample_smdata.previousPosition.values.tolist(),
        "sampleArtist": sample_smdata.artist.values.tolist(),
        "sampleSongs": sample_smdata.songs.values.tolist(),

        "topArtist_values": topArtist_data[positions].values.tolist(),
        "topArtist_artist": topArtist_data.artist.values.tolist(),
        "topArtist_pp": topArtist_data.previousPosition.values.tolist(),
        "topArtist_wP": topArtist_data.weekPosition.values.tolist(),


    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
