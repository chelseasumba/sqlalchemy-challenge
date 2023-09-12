# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
measurement= Base.classes.measurement
station= Base.classes.station

# Create our session (link) from Python to the DB


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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    previous_year= dt.date(2017,8,23)-dt.timedelta(days=365)
    results= session.query(measurement.date, measurement.prcp).filter(measurement.date>=previous_year).all()
    session.close()

    precipitation_results= {date:prcp for prcp in results}
    return jsonify(precipitation_results)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

previous_year= dt.date(2017,8,23)-dt.timedelta(days=365)
results= session.query(measurement.tobs)\
    .filter(measurement.station=='USC00519281')\
    .filter(measurement.date>=previous_year).all()
session.close()

    # Convert list of tuples into normal list
date_temp = [t[0]for t in results]

return jsonify(date_temp)

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

results= session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
    .filter(measurement.date >= start).all()

session.close()

    # Convert list of tuples into normal list
 start = list(np.ravel(results))

return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results= session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
    .filter(measurement.date >= start)\
    .filter(measurement.date<=end)\
    .all()

    session.close()

    # Convert list of tuples into normal list
   start_end = list(np.ravel(results))

    return jsonify(start_end)



if __name__ == '__main__':
    app.run(debug=True)