import os
import pickle
from data import SaveData

class DataManager:
    def __init__(self):
        pass

    def load_data(self, file_path : str="data.GAMEDATA"):
        if not os.path.exists(file_path):
            self.create_data_file(file_path=file_path)

        with open(file_path, "rb") as file:
            return pickle.load(file)
    
    def create_data_file(self, data : SaveData=None, file_path : str="data.GAMEDATA"):
        with open(file_path, "wb") as file:
            if data == None:
                pickle.dump(SaveData(), file)
            else:
                pickle.dump(data, file)
    
    def save_data(self, data, file_path : str="data.GAMEDATA"):
        with open(file_path, "wb") as file:
            pickle.dump(data, file)