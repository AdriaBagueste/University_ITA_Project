import numpy as np
import matplotlib.pyplot as plt



g = 9.80665  # m/s^2
ft2m = 0.3048
m2ft = 1/ft2m

# ---------- parámetros (Annex B) ----------

aircraft_params = {
    "B767-300ER": {
        "MLW": 145150.0,    # kg (145.150 tons)
        "S": 283.50,        # m^2
        "CD0_app": 0.014000,
        "CD2_app": 0.049000,
        "CD0_clean": 0.017400,
        "CD2_clean": 0.045900,
        "hp_desc": 26418,   # ft
        "CT_desc_high": 0.064359,
        "CT_desc_low": 0.055988,
        "CT_desc_app": 0.12475,
        "CT1": 0.35167e6,   # N  (interpretado como .35167E+06)
        "CT2": 0.44673e5,   # ft ( .44673E+05 -> 44673 )
        "CT3": 0.10129e-9
    },
    "B777-300": {
        "MLW": 237680.0,    # kg
        "S": 428.04,
        "CD0_app": 0.017300,
        "CD2_app": 0.048400,
        "CD0_clean": 0.015700,
        "CD2_clean": 0.042000,
        "hp_desc": 36122,
        "CT_desc_high": 0.044239,
        "CT_desc_low": 0.041065,
        "CT_desc_app": 0.092921,
        "CT1": 0.42577e6,
        "CT2": 0.48987e5,
        "CT3": 0.66146e-10
    },
    "B737": {
        "MLW": 51710.0,     # kg
        "S": 124.65,
        "CD0_app": 0.027000,
        "CD2_app": 0.044100,
        "CD0_clean": 0.023500,
        "CD2_clean": 0.044500,
        "hp_desc": 30152,
        "CT_desc_high": 0.036336,
        "CT_desc_low": 0.053395,
        "CT_desc_app": 0.16440,
        "CT1": 0.14573e6,
        "CT2": 0.55638e5,
        "CT3": 0.14200e-10
    },
    "A320-212": {
        "MLW": 64500.0,     # kg
        "S": 122.60,
        "CD0_app": 0.024200,
        "CD2_app": 0.046900,
        "CD0_clean": 0.024000,
        "CD2_clean": 0.037500,
        "hp_desc": 12398,
        "CT_desc_high": 0.045711,
        "CT_desc_low": 0.027207,
        "CT_desc_app": 0.13981,
        "CT1": 0.13605e6,
        "CT2": 0.52238e5,
        "CT3": 0.26637e-10
    },
    "A319-131": {
        "MLW": 61000.0,     # kg
        "S": 122.60,
        "CD0_app": 0.028400,
        "CD2_app": 0.037600,
        "CD0_clean": 0.028000,
        "CD2_clean": 0.031000,
        "hp_desc": 27726,
        "CT_desc_high": 0.083084,
        "CT_desc_low": 0.051765,
        "CT_desc_app": 0.14767,
        "CT1": 0.13900e6,
        "CT2": 0.58900e5,
        "CT3": 0.57200e-14
    }
}