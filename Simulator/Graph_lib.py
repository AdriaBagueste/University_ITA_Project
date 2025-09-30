import matplotlib.pyplot as plt
from Calculator_lib import *
import os

class graph:
    def __init__(self):
        self.Data_list = []

    def add_data(self, Data: list):
                
        try:
            self.Data_list.append(Data)
            
            return True
        
        except Exception as e:
            print(f"Error at: {e}")

            return False
        
    def plot(self, filepath: str = None):
        try:
            print(f"[Graph] Starting plot with {len(self.Data_list)} series")
            for series in self.Data_list:
                label = None
                if isinstance(series, dict):
                    x = series.get("x")
                    h = series.get("h")
                    label = series.get("label")
                    if x is not None and h is not None:
                        print(f"[Graph] Series label={label}, points={len(x)}")
                        if label:
                            plt.plot(x, h, label=label)
                        else:
                            plt.plot(x, h)
                elif isinstance(series, (list, tuple)) and len(series) == 2:
                    plt.plot(series[0], series[1])
            plt.xlabel("x [m]")
            plt.ylabel("h [m]")
            plt.grid(True)
            if any(isinstance(s, dict) and s.get("label") for s in self.Data_list):
                plt.legend(loc='best')
            plt.tight_layout()
            if filepath:
                abs_path = os.path.abspath(filepath)
                print(f"[Graph] Saving figure to {abs_path}")
                plt.savefig(abs_path, dpi=150)
                print(f"[Graph] Saved figure to {abs_path}")
            else:
                plt.show()
            plt.close()
            return True
        except Exception as e:
            print(f"Error at: {e}")
            return False
