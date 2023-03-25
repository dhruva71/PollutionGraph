import streamlit as st
import pandas as pd
from pollution_graph import PollutionGraph

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
data = pg.fetch_data(START, END)

# extract data
component_data = pg.extract_component_data(data, component="pm10")
timestamps = pg.extract_timestamps(data)

# create dataframe
df = pd.DataFrame({"pm10": component_data, "timestamp": timestamps})

# draw line chart using streamlit
st.line_chart(df)
