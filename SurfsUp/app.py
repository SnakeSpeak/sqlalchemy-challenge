# Import the dependencies.
from flask import Flask, jsonify
import numpy as np

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
import numpy as np
import pandas as pd
from pprint import pprint
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
metadata= MetaData()
metadata.reflect(bind = engine)
Base = automap_base(metadata = metadata)
# reflect the tables
Base.prepare()

# Save references to each table
tab_references = {}

for table_name in metadata.tables:
    tab_references[table_name] = Base.classes.get(table_name)

for table_name, table_class in tab_references.items():
    print(table_name,table_class)


Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
Session = sessionmaker(bind = engine)
session = Session()

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
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Percipitation route
@app.route("/api/v1.0/percipitation")
def percipitation():
    # Perform a query to retrieve the data and precipitation scores
    year_data = pd.read_sql("SELECT * FROM measurement WHERE date > '2016-08-15' and date < '2017-08-17'", conn)


    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    year_df = pd.DataFrame(year_data)
    year_df = year_df.rename(columns={'prcp':'percipitation'})
    year_df.sort_index()
    date_prcp_df = year_df.loc[:,['date','percipitation']]
    jsonified_df = date_prcp_df.to_json(orient='records')
    return jsonified_df

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    station_df = pd.read_sql("SELECT * FROM station", conn)
    station_json = station_df.to_json(orient = 'records')
    return station_json
    
#tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    most_active = pd.read_sql("SELECT date, tobs FROM measurement WHERE station = 'USC00519281'",conn)
    most_active = pd.DataFrame(most_active)
    active_json = most_active.to_json(orient= 'records')
    return active_json

if __name__ == "__main__":
    app.run(debug=True)
