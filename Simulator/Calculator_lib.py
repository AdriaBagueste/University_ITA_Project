from typing import Tuple, List
from Aircraft_lib import Aircraft


DELTA_T = 1.0  # seconds

# ISA constants (SI)
T0 = 288.15  # K
p0 = 101325.0  # Pa
g0 = 9.80665  # m/s^2
R = 287.05287  # J/(kg·K)
L = 0.0065  # K/m (troposphere lapse rate)
H_TROP = 11000.0  # m


def isa_temperature(h_m: float) -> float:
    if h_m <= H_TROP:
        return T0 - L * h_m
    else:
        return T0 - L * H_TROP


def isa_pressure(h_m: float) -> float:
    if h_m <= H_TROP:
        return p0 * (1.0 - (L * h_m) / T0) ** (g0 / (R * L))
    else:
        T11 = T0 - L * H_TROP
        p11 = p0 * (1.0 - (L * H_TROP) / T0) ** (g0 / (R * L))
        return p11 * pow(2.718281828, -g0 * (h_m - H_TROP) / (R * T11))


def isa_density(h_m: float) -> float:
    T = isa_temperature(h_m)
    p = isa_pressure(h_m)
    return p / (R * T)


class Calculate:

    # Define IAF altitude locally to avoid circular import (5000 ft to meters)
    IAF_Altitude = 5000.0 * 0.3048

    @staticmethod
    def _select_aircraft(aircrafts: Aircraft, aircraft_model: str):
        for a in aircrafts.Aircraft_list:
            if a.get("type") == aircraft_model:
                return a
        return None

    @staticmethod
    def getCDO(aircrafts: Aircraft, aircraft_model: str, mlw_percent: float) -> Tuple[List[float], List[float]]:
        """Compute a backward CDO trajectory using V_min RoD and idle thrust.

        Assumptions:
        - hp in ft for thrust model; T in N
        - Clean aerodynamics throughout (no configuration schedule provided)
        - No wind; dx/dt ≈ V, dh/dt = V*(T-D)/W
        - Mass constant (fuel burn ignored without confirmed FF units)
        """
        ac = Calculate._select_aircraft(aircrafts, aircraft_model)
        if not ac:
            return [], []

        # Geometry and masses
        S = ac.get("Surface") if ac.get("Surface") is not None else 1.0
        CD0 = ac.get("CD0clean") if ac.get("CD0clean") is not None else 0.02
        CD2 = ac.get("CD2clean") if ac.get("CD2clean") is not None else 0.4
        MLW = ac.get("Max_landing_weight") if ac.get("Max_landing_weight") is not None else 1.0
        m = max(1.0, (mlw_percent / 100.0) * MLW)  # kg

        # Thrust model parameters
        hpdesc_ft = ac.get("hpdesc") if ac.get("hpdesc") is not None else 0
        CTdesc_high = ac.get("CTdesc_high") if ac.get("CTdesc_high") is not None else 0.4
        CTdesc_low = ac.get("CTdesc_low") if ac.get("CTdesc_low") is not None else 0.3
        CT1 = ac.get("CT1") if ac.get("CT1") is not None else 0.0
        CT2 = ac.get("CT2") if ac.get("CT2") is not None else 1.0
        CT3 = ac.get("CT3") if ac.get("CT3") is not None else 0.0

        def t_max_newton(h_m: float) -> float:
            hp_ft = h_m * 3.28084
            return CT1 * (1.0 - hp_ft / CT2) + CT3 * (hp_ft ** 2)

        def t_idle_newton(h_m: float) -> float:
            hp_ft = h_m * 3.28084
            coeff = CTdesc_high if hp_ft >= hpdesc_ft else CTdesc_low
            return coeff * max(0.0, t_max_newton(h_m))

        # Integration setup
        hmax_m = 12192.0  # FL400
        x: List[float] = []
        h: List[float] = []
        current_x = 0.0
        current_h = Calculate.IAF_Altitude

        iterations = 0
        max_iterations = 1000000  # safety guard
        while current_h < hmax_m and iterations < max_iterations:
            rho = isa_density(current_h)
            W = m * g0
            T = max(0.0, t_idle_newton(current_h))

            # CL from lift balance
            # Protect against extremely low density
            q = 0.5 * max(1e-6, rho)  # dynamic pressure factor without V^2

            # V_min RoD formula given
            term_inside = T * T + 12.0 * CD2 * (W ** 2) * CD0
            # Ensure numerical safety
            term_inside = max(0.0, term_inside)
            V = ((1.0 / (3.0 * max(1e-9, rho) * max(1e-9, S) * max(1e-9, CD0))) * (T + term_inside ** 0.5)) ** 0.5

            # Recompute CL and D at chosen V
            CL = W / (max(1e-9, q) * max(1e-9, S) * max(1e-9, V * V))
            CD = CD0 + CD2 * (CL ** 2)
            D = 0.5 * rho * V * V * S * CD

            dh_dt = V * (T - D) / max(1e-9, W)  # forward-time vertical rate (negative in descent)
            dx_dt = V  # zero wind, small gamma

            x.append(current_x)
            h.append(current_h)

            # Backward integration (increase altitude, move upstream)
            current_x -= dx_dt * DELTA_T
            # Backward integration: increase altitude using the magnitude of forward descent rate
            climb_rate_backwards = max(0.0, -dh_dt)
            if climb_rate_backwards <= 1e-9:
                # No vertical progress possible; break to avoid infinite loop
                break
            current_h += climb_rate_backwards * DELTA_T
            iterations += 1

        return x, h