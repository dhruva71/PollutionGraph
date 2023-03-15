import datetime

import requests
import tomli
from matplotlib import pyplot as plt

from SafeLevels import SAFE_LEVELS


class PollutionGraph:
    def __init__(self):
        with open("toml/config.toml", "rb") as f:
            config = tomli.load(f)
        self.api_key = config["api_key"]
        self.lat = config["lat"]
        self.lon = config["lon"]

    def fetch_data(self, start, end, save_json=False):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={self.lat}" \
              f"&lon={self.lon}&start={start}&end={end}&appid={self.api_key}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if save_json:
            with open("response.json", "w") as f:
                f.write(response.text)
        return response.json()

    @staticmethod
    def load_data():
        # load data from response.json and return as json
        with open("response.json", "r") as f:
            data = f.read()
        return data

    def plot_data(self, data, start, end):
        # convert data to list
        # {"main":{"aqi":5},"components":{"co":807.76,"no":2.49,"no2":10.37,"o3":1.59,"so2":2.35,"pm2_5":78.55,"pm10":83.21,"nh3":7.47}
        aqi = [i["main"]["aqi"] for i in data["list"]]
        co = [i["components"]["co"] for i in data["list"]]
        no = [i["components"]["no"] for i in data["list"]]
        no2 = [i["components"]["no2"] for i in data["list"]]
        o3 = [i["components"]["o3"] for i in data["list"]]
        so2 = [i["components"]["so2"] for i in data["list"]]
        pm2_5 = [i["components"]["pm2_5"] for i in data["list"]]
        pm10 = [i["components"]["pm10"] for i in data["list"]]
        nh3 = [i["components"]["nh3"] for i in data["list"]]

        timestamps = [i["dt"] for i in data["list"]]
        # convert timestamps to datetime, and drop year
        timestamps = [datetime.datetime.fromtimestamp(i) for i in timestamps]

        # draw line plot as needed
        # plt.plot(aqi, label="aqi")
        # plt.plot(co, label="co")
        # plt.plot(no, label="no")
        # plt.plot(no2, label="no2")
        # plt.plot(o3, label="o3")
        # plt.plot(so2, label="so2")
        # plt.plot(timestamps, pm2_5, label="pm2_5")
        plt.plot(timestamps, pm10, label="pm10", color="r")
        # plt.plot(nh3, label="nh3")

        # draw scatter plot
        # plt.scatter(timestamps, pm10, label="pm10", color="r")

        # convert datetime to human-readable format
        start_date = datetime.datetime.fromtimestamp(start).strftime("%d-%b-%Y")
        end_date = datetime.datetime.fromtimestamp(end).strftime("%d-%b-%Y")
        plt.title(f'Air Pollution in Guwahati from {start_date} to {end_date}')
        plt.xlabel("Date")
        plt.ylabel("PM10 (ug/m3)")

        plt.xticks(fontsize=8)

        plt.axhline(y=SAFE_LEVELS['pm10'], color='g', linestyle='-', label="PM10 Safe Level by CPCB")

        plt.legend()
        plt.grid(True)

        # size of the figure
        plt.gcf().set_size_inches(15, 10)

        plt.savefig("output/graph.png")
        plt.show()
