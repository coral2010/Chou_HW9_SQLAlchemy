import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def routes():
    return (
        f'Available Routes:<br>'
        f'/api/v1.0/precipitation<br>'
        f'/api/v1.0/stations<br>'
        f'/api/v1.0/tobs<br>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by((Measurement.date).desc()).\
        filter(Measurement.date >= '2016-01-01').filter(Measurement.date <= '2016-12-31').all()
    
    all_precipitation = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["precipitation"] = precipitation.prcp
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station).\
        group_by(Measurement.station).all()
        
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.date, Measurement.tobs).\
        order_by((Measurement.date).desc()).\
        filter(Measurement.date >= '2016-01-01').filter(Measurement.date <= '2016-12-31').all()
    
    all_tobs = []
    for tob in tobs:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["tobs"] = tobs.tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)
        