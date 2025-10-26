# CDO & Arrival Sequencing Simulator

## Description
This program simulates aircraft arrival trajectories for Continuous Descent Operations (CDO) at Josep Tarradellas Barcelona–El Prat Airport (LEBL).  
It is used to analyse and compare multiple CDO-based arrival scenarios to study the feasibility of implementing continuous descent procedures in congested airspace.

The simulation is developed in Python and models the descent of several aircraft types from 40,000 ft to 5,000 ft.  
It calculates altitude and distance values based on aerodynamic parameters, engine idle thrust, and air density following the International Standard Atmosphere (ISA).

---

## Aircraft Models
The following aircraft are included in the simulation:
- Boeing 767-300ER  
- Boeing 777-300  
- Boeing 737  
- Airbus A320-212  
- Airbus A319-131  

Each aircraft is simulated at 100% and 80% of its Maximum Landing Weight (MLW).

---

## Main Function
The main function of the program calculates the continuous descent trajectory for each aircraft type and configuration.  
It computes the minimum descent velocity and rate of descent (ROD) at each iteration according to:

```
V_minimum_descent = sqrt( (1 / (3 * ρ * S * CD0)) * (T + sqrt(T^2 + 12 * CD2 * (m * g)^2 * CD0)) )
```

The algorithm runs backwards from the IAF (Initial Approach Fix) altitude of 5,000 ft up to FL400, updating altitude and horizontal distance every second.

---

## Scenarios Simulated
Two scenarios are analysed with the simulator:

**Scenario 1:**  
All aircraft start their STAR (Standard Arrival Route) at the same time.  
This produces uneven arrival times and unsafe separations at the IAF.

**Scenario 2:**  
Aircraft arrive at the IAF with a fixed 2-minute separation.  
This produces a safer and more orderly flow but requires timing adjustments and higher fuel consumption.

---

## Output
The program provides:
- Altitude vs. distance trajectories for each aircraft model.  
- Time and altitude data at STAR waypoints and the IAF.  
- Comparative results for different arrival sequencing scenarios.

---

## Purpose
The results obtained with this program are used to determine:
- The operational feasibility of CDOs at Barcelona Airport.  
- Compliance with altitude restrictions at STAR waypoints.  
- Potential environmental and efficiency improvements through continuous descent procedures.
