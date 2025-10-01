"""
Simulador CDO (Python)
Genera trayectorias [x,h] desde IAF (x=0, h=5000 ft) hacia atrás hasta FL400 (40000 ft).
- Un paso por iteración = 1 s
- Todas las fórmulas según Annex A/B (BADA) tal y como se solicitó.
"""

import matplotlib.pyplot as plt
from Calculator_lib import *


def main():
    Aircrafts = ["B767-300ER", "B777-300", "B737", "A320-212", "A319-131"]
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

    for Aircraft_model in Aircrafts:
        for p in pesos:

            x, h = calculate.getCDO(Aircraft_model, p)

            base_color = base_colors[Aircraft_model]
            
            # intensidad distinta según peso
            if p == 100:
                color = base_color        # fuerte
            else:
                color = base_color        # más claro
                # convertir a un color más transparente
                plt.plot(x, h, label=f"{Aircraft_model} [{p}% MLW]",
                         linewidth=1.8, color=color, alpha=0.5)
                continue
            plt.plot(x, h, label=f"{Aircraft_model} [{p}% MLW]",
                     linewidth=1.8, color=color, alpha=0.9)

    plt.title("Trayectorias CDO simuladas (IAF en x=0, h=5000 ft)")
    plt.xlabel("x [m] (0 a la derecha)")
    plt.ylabel("h [m]")
    plt.grid(True)
    plt.legend(loc="upper right", fontsize="small")


    plt.savefig("figure.png")
    plt.show()
    

if __name__ == "__main__":
    main()
