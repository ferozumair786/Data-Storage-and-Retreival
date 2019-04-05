import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value"""
    # Query all dates for precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

     all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of Stations from the dataset"""
    # Query all stations
    results = session.query(Station.name).all()


    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures by date for a year from the last date from the dataset"""
    
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    import datetime as dt
    today = dt.date.today()
    
    #get last year's date
    lstdt = last_date[0].split('-', maxsplit=3)
    lastdate = dt.date(int(lstdt[0]), int(lstdt[1]), int(lstdt[2]))
    lastyear = lastdate - dt.timedelta(days=365)
   
    # Query all measurements
    results = session.query(Measurement.date,\
                             Measurement.tobs).\
                            filter(Measurement.date >= lastyear).\
                            filter(Measurement.date <= lastdate).\
                            all()

    
    all_temps = []
    for date, temp in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = temp
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>")
def dates(start_date, end_date):
    """Return a list of temperatures by date for a range"""
    
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    import datetime as dt
    
    
    if end_date is None and start_date is not None:
       # Query all measurements
        results = session.query(Measurement.date,\
                             Measurement.tobs).\
                            filter(Measurement.date >= start_date).\
                            all() 
    elif start_date is not None:
        # Query all measurements
        results = session.query(Measurement.date,\
                             Measurement.tobs).\
                            filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date).\
                            all()
    
    all_dates = []
    for date, tobs in results:
        date_dict = {}
        date_dict["date"] = date
        date_dict["tobs"] = tobs
        all_dates.append(date_dict)

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)
