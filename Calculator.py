import numpy as np
import matplotlib.pyplot as plt
from Aircraft_lib import *


def isa_atmosphere(h_m):
    """
    Devuelve (rho, T, p) en SI para altitud geometric h_m (metros),
    usando el modelo ISA hasta ~20 km suficiente para nuestro caso.
    """
    T0 = 288.15
    p0 = 101325.0
    R = 287.05
    g0 = 9.80665
    L = 0.0065
    if h_m <= 11000.0:
        T = T0 - L * h_m
        p = p0 * (1 - (L * h_m) / T0) ** (g0 / (R * L))
    else:
        # region 11-20 km (isothermal at 216.65 K)
        T = 216.65
        p11 = p0 * (1 - (L * 11000) / T0) ** (g0 / (R * L))
        p = p11 * np.exp(-g0 * (h_m - 11000) / (R * T))
    rho = p / (R * T)
    return rho, T, p

# ---------- Thrust functions ----------
def thrust_max(params, hp_ft):
    # Tmax = CT1 * (1 - hp / CT2 + CT3 * hp^2)
    return params["CT1"] * (1.0 - (hp_ft / params["CT2"]) + params["CT3"] * (hp_ft ** 2))

def thrust_idle(params, hp_ft, config="clean"):
    Tmax = thrust_max(params, hp_ft)
    if hp_ft > params["hp_desc"]:
        return params["CT_desc_high"] * Tmax
    else:
        if config == "clean":
            return params["CT_desc_low"] * Tmax
        else:
            return params["CT_desc_app"] * Tmax

# ---------- Velocidad mínima de descenso ----------
def v_minimum_descent(params, rho, T_N, m_kg, config="clean"):
    # Vmin = sqrt( (1/(3 rho S CD0)) * ( T + sqrt(T^2 + 12 CD2 (m g)^2 CD0 ) ) )
    if config == "clean":
        CD0 = params["CD0_clean"]
        CD2 = params["CD2_clean"]
    else:
        CD0 = params["CD0_app"]
        CD2 = params["CD2_app"]
    S = params["S"]
    term = T_N + np.sqrt(T_N**2 + 12.0 * CD2 * (m_kg * g)**2 * CD0)
    inside = (1.0 / (3.0 * rho * S * CD0)) * term
    # numerical safety
    inside = max(inside, 1e-6)
    V = np.sqrt(inside)
    return V  # m/s

# ---------- Drag ----------
def compute_drag(params, rho, V, m_kg, config="clean"):
    # CL = W / (0.5 rho V^2 S)   (W ~= m*g)
    S = params["S"]
    CL = (m_kg * g) / (0.5 * rho * V**2 * S)
    if config == "clean":
        CD = params["CD0_clean"] + params["CD2_clean"] * (CL**2)
    else:
        CD = params["CD0_app"] + params["CD2_app"] * (CL**2)
    D = 0.5 * rho * V**2 * S * CD
    return D, CD, CL

# ---------- Función que simula la trayectoria (backwards) ----------
def getCDO(aircraft_model, MLW_percent):
    """
    Entrada:
      - aircraft_model: clave en aircraft_params
      - MLW_percent: 100 o 80, etc.
    Salida:
      x (m, negativo hacia atrás), h (m)
    """
    params = aircraft_params[aircraft_model]
    # masa final (kg) al IAF
    m = params["MLW"] * (MLW_percent / 100.0)

    # condiciones iniciales en SI
    h0_m = 5000.0 * ft2m    # IAF = 5000 ft -> metros
    hmax_m = 40000.0 * ft2m # FL400 -> metros
    delta_t = 1.0  # s

    x = [0.0]      # m (IAF)
    h = [h0_m]     # m

    max_iter = 500000  # seguridad
    it = 0

    while h[-1] < hmax_m and it < max_iter:
        it += 1
        h_last = h[-1]
        # presión/altitud para thrust usa ft
        hp_ft = h_last * m2ft

        # densidad con ISA
        rho, Tisa, pisa = isa_atmosphere(h_last)

        # configuración: approach si <= 6000 ft
        config = "clean" if (h_last > 6000.0 * ft2m) else "app"

        # empuje idle (N)
        T_idle = thrust_idle(params, hp_ft, config)

        # velocidad mínima para minimizar ROD (m/s)
        Vmin = v_minimum_descent(params, rho, T_idle, m, config)

        # arrastre a esa velocidad
        D, CD, CL = compute_drag(params, rho, Vmin, m, config)

        # ROD (m/s) -> magnitude positiva (subimos en h al simular hacia atrás)
        ROD_m_s = Vmin * (D - T_idle) / (m * g)
        # en algunas situaciones numéricas D-T puede ser negativo (no queremos ascenso)
        if ROD_m_s < 0:
            ROD_m_s = 0.0

        # paso temporal: como simulamos hacia atrás, la altitud aumenta
        h_new = h_last + ROD_m_s * delta_t
        # posición horizontal hacia atrás (x negativo)
        x_new = x[-1] - Vmin * delta_t

        # seguridad: si Vmin es demasiado pequeño o ROD nulo, evitar bucle infinito
        if Vmin < 1e-3 and ROD_m_s < 1e-6:
            print(f"[{aircraft_model}] parada por V≈0 en it {it}")
            break

        h.append(h_new)
        x.append(x_new)

    if it >= max_iter:
        print(f"[{aircraft_model}] alcanzado max_iter = {max_iter}, h={h[-1]:.1f} m")

    return np.array(x), np.array(h)
def obtener_altura_y_tiempo(x, h, distancia_objetivo_m, delta_t=1.0):
    """
    Devuelve la altitud y el tiempo asociado al punto situado
    a una distancia dada (hacia atrás) desde el IAF (x=0).

    Parámetros:
      x, h : arrays de trayectoria simulada (m)
      distancia_objetivo_m : distancia horizontal hacia atrás desde el IAF (m)
      delta_t : paso temporal entre iteraciones (s)
    Retorna:
      h_interp : altitud interpolada (m)
      tiempo   : tiempo estimado desde ese punto hasta el IAF (s)
    """

    # Convertimos a valores absolutos positivos para comparar
    distancia_objetivo_m = abs(distancia_objetivo_m)

    # Buscamos el índice donde x ≈ -distancia_objetivo_m
    # (recuerda que x es negativo)
    objetivo = -distancia_objetivo_m
    idx = np.argmin(np.abs(x - objetivo))

    # Si queremos mayor precisión, interpolamos entre puntos
    if idx < len(x) - 1:
        x1, x2 = x[idx], x[idx+1]
        h1, h2 = h[idx], h[idx+1]
        h_interp = np.interp(objetivo, [x1, x2], [h1, h2])
    else:
        h_interp = h[idx]

    # Tiempo desde ese punto hasta el IAF
    tiempo = idx * delta_t  # como Δt = 1 s por iteración

    return h_interp, tiempo


def velocidad_en_IAF(aircraft_model, MLW_percent):
    """
    Calcula la velocidad (m/s) en el punto IAF (x=0, h=5000 ft)
    para un avión y peso dados.
    """
    params = aircraft_params[aircraft_model]
    m = params["MLW"] * (MLW_percent / 100.0)
    hp_ft = 5000.0  # altitud del IAF
    rho, _, _ = isa_atmosphere(hp_ft * ft2m)  # densidad local (ISA)

    # configuración: approach por debajo de 6000 ft
    config = "app"

    # empuje idle
    T_idle = thrust_idle(params, hp_ft, config)

    # velocidad mínima de descenso
    Vmin = v_minimum_descent(params, rho, T_idle, m, config)

    return Vmin  # m/s