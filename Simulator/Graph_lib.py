import matplotlib as plt
from Calculator_lib import *

class graph:
    def __init__(self):
        Data_list = []

    def add_data(self, Data: list):
                
        try:
            self.Data_list.append(Data)
            
            return True
        
        except Exception as e:
            print(f"Error at: {e}")

            return False
        
