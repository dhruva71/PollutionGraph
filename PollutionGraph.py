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
        self.city = config["city"]

    def fetch_data(self, start, end, save_json=False):
        """
        Fetch data from openweathermap.org
        :param start: Start time in unix timestamp
        :param end: End time in unix timestamp
        :param save_json: Whether to save the response as json or not
        :return: json response
        """
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
        """
        Load data from response.json
        :return:
        """
        # load data from response.json and return as json
        with open("response.json", "r") as f:
            data = f.read()
        return data

    @staticmethod
    def extract_component_data(data, component: str = "pm10") -> list:
        """
        Extract component data from json response
        :param data: data from json response from openweathermap.org
        :param component: component to extract data for. Can be one of the following: co, no, no2, o3, so2, pm2_5, pm10, nh3. Default: pm10
        :return: list of component data
        """
        # convert data to list
        # {"main":{"aqi":5},"components":{"co":807.76,"no":2.49,"no2":10.37,"o3":1.59,"so2":2.35,"pm2_5":78.55,"pm10":83.21,"nh3":7.47}
        component_data = [i["components"][component] for i in data["list"]]
        return component_data

    def plot_data(self, data, start, end, component: str = "pm10"):
        """
        Plots the data for the given component using matplotlib
        :param data: data from json response from openweathermap.org
        :param start: Start time in unix timestamp
        :param end: End time in unix timestamp
        :param component: component to extract data for. Can be one of the following: co, no, no2, o3, so2, pm2_5, pm10, nh3. Default: pm10
        :return: None
        """
        component_data = self.extract_component_data(data, component)

        timestamps = [i["dt"] for i in data["list"]]
        # convert timestamps to datetime, and drop year
        timestamps = [datetime.datetime.fromtimestamp(i) for i in timestamps]

        # draw line plot as needed
        plt.plot(timestamps, component_data, label=component, color="r")

        # convert datetime to human-readable format
        start_date = datetime.datetime.fromtimestamp(start).strftime("%d-%b-%Y")
        end_date = datetime.datetime.fromtimestamp(end).strftime("%d-%b-%Y")
        plt.title(f'Air Pollution in {self.city} from {start_date} to {end_date}')
        plt.xlabel("Date")
        plt.ylabel(f"{component.capitalize()} (ug/m3)")

        plt.xticks(fontsize=8)

        plt.axhline(y=SAFE_LEVELS[component], color='g', linestyle='-',
                    label=f"{component.capitalize()} Safe Level by CPCB")

        plt.legend()
        plt.grid(True)

        # size of the figure
        plt.gcf().set_size_inches(15, 10)

        plt.savefig("graph.png")
        plt.show()
