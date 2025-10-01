from Aircraft_dict import *
import math

class calculate:
    def isa_atmosphere(h_m: float):
        """
        Devuelve (rho, T, p) en SI para altitud geometric h_m (metros),
        usando el modelo ISA hasta ~20 km suficiente para nuestro caso.
        """

        Temperature_0 = 288.15  
        Pressure_0 = 101325.0
        R = 287.05    
        GRAVITY_CONSTANT = g
        L = 0.0065

        if h_m <= 11000.0:
            T = Temperature_0 - L * h_m
            Pressure = Pressure_0 * (1 - (L * h_m) / Temperature_0) ** (GRAVITY_CONSTANT / (R * L))
        else:
            # region 11-20 km (isothermal at 216.65 K)
            T = 216.65
            Pressure_Isothermal = Pressure_0 * (1 - (L * 11000) / Temperature_0) ** (GRAVITY_CONSTANT / (R * L))
            Pressure = Pressure_Isothermal * math.exp(-GRAVITY_CONSTANT * (h_m - 11000) / (R * T))
        Air_density = Pressure / (R * T)

        return Air_density, T, Pressure

    # ---------- Thrust functions ----------
    def thrust_max(Aircraft_parameters: dict, hp_ft: float):
        # Tmax = CT1 * (1 - hp / CT2 + CT3 * hp^2)
        thrust = Aircraft_parameters["CT1"] * (1.0 - (hp_ft / Aircraft_parameters["CT2"]) + Aircraft_parameters["CT3"] * (hp_ft ** 2))

        return thrust

    def thrust_idle(Aircraft_parameters, hp_ft, config="clean"):
        Thrust_max = calculate.thrust_max(Aircraft_parameters, hp_ft)
        if hp_ft > Aircraft_parameters["hp_desc"]:
            return Aircraft_parameters["CT_desc_high"] * Thrust_max
        else:
            if config == "clean":
                return Aircraft_parameters["CT_desc_low"] * Thrust_max
            else:
                return Aircraft_parameters["CT_desc_app"] * Thrust_max

    # ---------- Velocidad mínima de descenso ----------
    def v_minimum_descent(Aircraft_parameters, Air_density, T_N, Mass, config="clean"):
        # Vmin = sqrt( (1/(3 rho S CD0)) * ( T + sqrt(T^2 + 12 CD2 (m g)^2 CD0 ) ) )

        if config == "clean":
            CD0 = Aircraft_parameters["CD0_clean"]
            CD2 = Aircraft_parameters["CD2_clean"]
        else:
            CD0 = Aircraft_parameters["CD0_app"]
            CD2 = Aircraft_parameters["CD2_app"]

        S = Aircraft_parameters["S"]
        term = T_N + math.sqrt(T_N**2 + 12.0 * CD2 * (Mass * g)**2 * CD0)
        inside = (1.0 / (3.0 * Air_density * S * CD0)) * term
        # numerical safety
        inside = max(inside, 1e-6)
        V = math.sqrt(inside)
        return V  # m/s

    # ---------- Drag ----------
    def compute_drag(Aircraft_parameters, Air_density, Velocity, Mass, config="clean"):
        # CL = W / (0.5 rho V^2 S)   (W ~= m*g)

        Aircraft_surface = Aircraft_parameters["S"]
        CL = (Mass * g) / (0.5 * Air_density * Velocity**2 * Aircraft_surface)

        if config == "clean":
            CD = Aircraft_parameters["CD0_clean"] + Aircraft_parameters["CD2_clean"] * (CL**2)
        else:
            CD = Aircraft_parameters["CD0_app"] + Aircraft_parameters["CD2_app"] * (CL**2)
        Drag = 0.5 * Air_density * Velocity**2 * Aircraft_surface * CD
        return Drag, CD, CL

    # ---------- Función que simula la trayectoria (backwards) ----------
    def getCDO(aircraft_model, MLW_percent):
        """
        Entrada:
        - aircraft_model: clave en aircraft_params
        - MLW_percent: 100 o 80, etc.
        Salida:
        x (m, negativo hacia atrás), h (m)
        """
        Aircraft_parameters = aircraft_params[aircraft_model]
        # masa final (kg) al IAF
        m = Aircraft_parameters["MLW"] * (MLW_percent / 100.0)

        # condiciones iniciales en SI
        h0_m = 5000.0 * ft2m    # IAF = 5000 ft -> metros
        Max_altitude = 25000 * ft2m # FL400 -> metros
        delta_t = 1.0  # s

        x = [0.0]      # m (IAF)
        h = [h0_m]     # m

        max_iteration = 500000  # seguridad
        iteration = 0

        while h[-1] < Max_altitude and iteration < max_iteration:
            iteration += 1
            h_last = h[-1]
            # presión/altitud para thrust usa ft
            hp_ft = h_last * m2ft

            # densidad con ISA
            rho, Tisa, pisa = calculate.isa_atmosphere(h_last)

            # configuración: approach si <= 6000 ft
            config = "clean" if (h_last > 6000.0 * ft2m) else "app"

            # empuje idle (N)
            T_idle = calculate.thrust_idle(Aircraft_parameters, hp_ft, config)

            # velocidad mínima para minimizar ROD (m/s)
            Vmin = calculate.v_minimum_descent(Aircraft_parameters, rho, T_idle, m, config)

            # arrastre a esa velocidad
            D, CD, CL = calculate.compute_drag(Aircraft_parameters, rho, Vmin, m, config)

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
                print(f"[{aircraft_model}] parada por V≈0 en it {iteration}")
                break

            h.append(h_new)
            x.append(x_new)

        if iteration >= max_iteration:
            print(f"[{aircraft_model}] alcanzado max_iter = {max_iteration}, h={h[-1]:.1f} m")

        return x, h
