# PollutionGraph

PollutionGraph is a simple tool to visualize pollution data from the OpenWeatherMap API.

## Usage

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Rename `toml/sample.toml` to `toml/config.toml`, and plug in necessary info.
4. Run `python main.py`
5. The graph will be saved to `output/graph.png`

### OpenWeatherMap API Key
* This takes 24-48 hours to be approved. You can get one [here](https://openweathermap.org/api).

## License

This project is licensed under the MIT License.

## Streamlit

PollutionGraph is also available as a Streamlit app [here](https://dhruva71-pollutiongraph-streamlit-app-6az7av.streamlit.app/).
To deploy, use the streamlit_app.py as a starting point. Specify the config details in the "advanced" section of the Streamlit app.