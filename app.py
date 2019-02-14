
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# Use FLASK to create your routes.

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from datetime import timedelta

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

# /api/v1.0/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

oneyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= oneyear).all()
    return jsonify(dict(precip))


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

station = [Measurement.station, 
           func.count(Measurement.station)]

@app.route("/api/v1.0/stations")
def stations():
    count_station = session.query(*station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    return jsonify(dict(count_station))


# /api/v1.0/tobs
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_dates = session.query(Measurement.date, Measurement.tobs).all()
    return jsonify(dict(tobs_dates))


# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


@app.route("/api/v1.0/<start>")
def tobs():
    tobs_dates = session.query(Measurement.date, Measurement.tobs).all()
    return jsonify(dict(tobs_dates))


@app.route("/api/v1.0/<start>/<end>")
def tobs():
    tobs_dates = session.query(Measurement.date, Measurement.tobs).all()
    return jsonify(dict(tobs_dates))


if __name__ == "__main__":
    app.run(debug=True)
