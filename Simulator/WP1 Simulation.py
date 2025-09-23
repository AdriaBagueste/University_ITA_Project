from Aircraft_lib import Aircraft

Aircrafts = Aircraft()

#IAF altitude in ft
IAF_ALTITUDE = 5000

#Max landing weight (MLW) in t (tones)
MLW_B767 = 145.150
MLW_B777 = 237.680
MLW_B737 = 51.710
MLW_A320 = 64.500
MLW_A319 = 61.000

#// Adding all aircrafts in the project
Aircrafts.add_aircraft('B767-300ER', 'GRAUS3N', MLW_B767)
Aircrafts.add_aircraft('B777-300', 'MATEX4N', MLW_B777)
Aircrafts.add_aircraft('B737', 'LOBAR3N', 0.8 * MLW_B737)
Aircrafts.add_aircraft('A320-212', 'CASPE4N', MLW_A320)
Aircrafts.add_aircraft('A319-131', 'PUMAL5N', 0.8 * MLW_A319)
Aircrafts.add_aircraft('B767-300ER', 'ALBER3X', 0.8 * MLW_B767)

