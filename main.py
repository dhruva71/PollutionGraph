import datetime

from PollutionGraph import PollutionGraph

if __name__ == "__main__":
    # create object
    pg = PollutionGraph()

    # set start and end time
    START = int(datetime.datetime(2023, 3, 1, 0, 0, 0).timestamp())
    END = int(datetime.datetime.today().timestamp())

    # fetch data
    data = pg.fetch_data(START, END)
    pg.plot_data(data, START, END)
