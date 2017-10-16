import pandas as pd

DATA_FILE = "../../data/restaurants.csv"

class FileIO():
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.data_file = self.load_file()

    #######################################################
    # Load a specific JSON file from inside the the DATA_DIR
    #######################################################
    def load_file(self):
        print "loading {}".format(DATA_FILE)
        with open(DATA_FILE) as data_file:
            data = pd.read_csv(data_file, sep='\t', encoding='utf-8')
        return data

