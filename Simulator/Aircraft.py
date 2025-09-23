class Aircrafts:
    
    def __init__(self):
        self.Aircraft_list = []

    def add_aircraft(self, Aircraft_type, Aircraft_STAR, Weight_at_IAF):
        
        try:
            Aircraft = {
                "type": Aircraft_type,
                "STAR": Aircraft_STAR,
                "Weight_at_IAF": Weight_at_IAF
            }

            self.Aircraft_list.append(Aircraft)
            
            return True
        
        except Exception as e:
            print(f"Error at: {e}")

            return False
        
    def get_aircraft_value(self, type, key):
        for aircraft in self.Aircraft_list:
            if aircraft[type] == type:
                return aircraft.get(key, None)
            
        return None


