import pandas as pd

DATA_FILE = "../data/restaurants.csv"
data_file = None
print "loading {}".format(DATA_FILE)
with open(DATA_FILE) as data_file:
    data_file = pd.read_csv(data_file, sep='\t', encoding='utf-8')


class FileIO():
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.data_file = data_file

    #######################################################
    # Load a specific JSON file from inside the the DATA_DIR
    #######################################################


    def update_dataset(self):
        self.data_handler.send({"fake_update": True})
