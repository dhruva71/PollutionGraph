import streamlit as st
import pandas as pd
from pollution_graph import PollutionGraph


@st.cache_data
def cached_fetch_data(pollution_graph: PollutionGraph, start_timestamp: int, end_timestamp: int):
    """
    Uses Streamlit's caching to cache the data and save on API calls
    :param pollution_graph:
    :param start_timestamp:
    :param end_timestamp:
    :return:
    """
    api_data = pollution_graph.fetch_data(start_timestamp, end_timestamp)
    return api_data


# Load data
pg = PollutionGraph(config=st.secrets)

# Set start and end time
# get the first day of the current month
START = int(pd.to_datetime("today").replace(day=1).timestamp())
END = int(pd.to_datetime("today").timestamp())

# if you wish to let the users pick the start and end date, uncomment the following lines
# START = st.date_input("Start date", value=pd.to_datetime("2023-03-01"))
# END = st.date_input("End date", value=pd.to_datetime("today"))

# Fetch data
data = cached_fetch_data(pg, START, END)

# extract data
component_data = pg.extract_component_data(data, component="pm10")
timestamps = pg.extract_timestamps(data)

# convert timestamps to datetime
timestamps = [pd.to_datetime(i, unit="s") for i in timestamps]

# create dataframe
df = pd.DataFrame({"pm10": component_data, "timestamp": timestamps})

# add a column for safe levels
df["safe"] = 60

# display title
st.title("PM10 levels in {}".format(pg.city))
st.header("From {} to {}".format(pd.to_datetime(START, unit="s"), pd.to_datetime(END, unit="s")))
st.write("App by Dhruvajyoti Sarma")
st.write("Data from openweathermap.org")

# draw line chart using streamlit
st.line_chart(df, x="timestamp", y=["pm10", "safe"], height=500, width=0)
