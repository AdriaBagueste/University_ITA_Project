"""
Simulador CDO (Python)
Genera trayectorias [x,h] desde IAF (x=0, h=5000 ft) hacia atrás hasta FL400 (40000 ft).
- Un paso por iteración = 1 s
- Todas las fórmulas según Annex A/B (BADA) tal y como se solicitó.
"""

import numpy as np
import matplotlib.pyplot as plt
from Aircraft_lib import *
from Calculator_lib import *




def main():
    modelos = ["B767-300ER", "B777-300", "B737", "A320-212", "A319-131"]
    pesos = [100, 80]  # % MLW

    # colores principales por avión
    base_colors = {
        "B767-300ER": "blue",
        "B777-300": "red",
        "B737": "green",
        "A320-212": "purple",
        "A319-131": "orange"
    }

    plt.figure(figsize=(11,6))

    for model in modelos:
        for p in pesos:
            x, h = getCDO(model, p)
            base_color = base_colors[model]
            # intensidad distinta según peso
            if p == 100:
                color = base_color        # fuerte
            else:
                color = base_color        # más claro
                # convertir a un color más transparente
                plt.plot(x, h, label=f"{model} [{p}% MLW]",
                         linewidth=1.8, color=color, alpha=0.5)
                continue
            plt.plot(x, h, label=f"{model} [{p}% MLW]",
                     linewidth=1.8, color=color, alpha=0.9)
    x, h = getCDO("B767-300ER", 80)
    distancia_star = 211870  # 166.31 km hasta el IAF
    h_wp, t_wp = obtener_altura_y_tiempo(x, h, distancia_star)

    print(f"Altura al inicio de la STAR (70 km antes del IAF): {h_wp / 0.3048:.0f} ft")
    print(f"Tiempo desde ese punto hasta el IAF: {t_wp / 60:.1f} min")
    print("\n=== Velocidades en el IAF (h=5000 ft) ===")
    for model in modelos:
        for p in pesos:
            V = velocidad_en_IAF(model, p)
            V_kt = V * 1.94384   # m/s → knots
            print(f"{model} [{p}% MLW]: {V_kt:.1f} kt")


    plt.title("Trayectorias CDO simuladas (IAF en x=0, h=5000 ft)")
    plt.xlabel("x [m] (0 a la derecha)")
    plt.ylabel("h [m]")
    plt.grid(True)
    plt.legend(loc="upper right", fontsize="small")



    plt.show()



if __name__ == "__main__":
    main()