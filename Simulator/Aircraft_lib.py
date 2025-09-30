class Aircraft:
    
    def __init__(self):
        self.Aircraft_list = []

    def add_aircraft(self, 
                     Aircraft_type: str, 
                     Aircraft_STAR: str, 
                     Max_landing_weight: float, 
                     Max_weight: float, 
                     Max_payload: float, 
                     Surface: float, 
                     CD0app: float, 
                     CD2app: float, 
                     CD0clean: float, 
                     CD2clean: float,
                     hpdesc: int,
                     CTdesc_high: float,
                     CTdesc_low: float,
                     CTdsc_app: float,
                     CT1: float,
                     CT2: float,
                     CT3: float,
                     CF1: float,
                     CF2: float):
        
        try:
            Aircraft = {
                "type": Aircraft_type,
                "STAR": Aircraft_STAR,
                "Max_landing_weight": Max_landing_weight,
                "Max_weight": Max_weight,
                "Max_payload": Max_payload,
                "CD0app": CD0app,
                "CD2app": CD2app,
                "CD0clean": CD0clean,
                "CD2clean": CD2clean,
                "hpdesc": hpdesc,
                "CTdesc_high": CTdesc_high,
                "CTdesc_low": CTdesc_low,
                "CTdesc_app": CTdsc_app,
                "CT1": CT1,
                "CT2": CT2,
                "CT3": CT3,
                "CF1": CF1,
                "CF2": CF2
            }

            self.Aircraft_list.append(Aircraft)
            
            return True
        
        except Exception as e:
            print(f"Error at: {e}")

            return False
        
    def get_aircraft_value(self, aircraft_type, key):
        for aircraft in self.Aircraft_list:
            if aircraft.get("type") == aircraft_type:
                return aircraft.get(key, None)
        return None

class STAR:
    def __init__(self):
        self.STAR_list = []
    
    def Add_STAR(self,
                 name: str,
                 altitude: int):
        
        try:
            STAR_entry = {
                    "name": name,
                    "altitude": altitude
                }

            self.STAR_list.append(STAR_entry)
            
            return True
        
        except Exception as e:
                print(f"Error at: {e}")

                return False
        
    def get_STAR_value(self, star_name, key):
        for star in self.STAR_list:
            if star.get("name") == star_name:
                return star.get(key, None)
        return None
    
    
        
   


