import tkinter as tk
from tkinter import ttk
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound

# -----------------------------
# Compatibilité des signes
# -----------------------------
compatibilite = {
    "Bélier": 80,
    "Taureau": 75,
    "Gémeaux": 70,
    "Cancer": 85,
    "Lion": 90,
    "Vierge": 65,
    "Balance": 88,
    "Scorpion": 92,
    "Sagittaire": 78,
    "Capricorne": 72,
    "Verseau": 83,
    "Poissons": 95
}

# -----------------------------
# Animation du cœur
# -----------------------------
def afficher_coeur():
    fig = plt.Figure(figsize=(3, 3))
    ax = fig.add_subplot(111)

    x = np.linspace(-2, 2, 4000)
    y = np.cbrt(x**2) + 0.9 * np.sin(50 * x) * np.sqrt(3 - x**2)

    ax.plot(x, y, color="red")
    ax.axis("off")
    ax.set_title("💖")

    canvas = FigureCanvasTkAgg(fig, master=frame_animation)
    canvas.draw()
    canvas.get_tk_widget().pack()

# -----------------------------
# Calcul amour
# -----------------------------
def calculer_amour():
    nom = entry_nom.get()
    signe = combo_signe.get()

    if nom == "" or signe == "":
        resultat.config(text="⚠️ Remplis tous les champs !", fg="red")
        return

    base = compatibilite[signe]
    alea = random.randint(-10, 10)
    pourcentage = max(10, min(100, base + alea))

    winsound.Beep(800, 300)

    if pourcentage < 40:
        message = "😂 L’amour te regarde mais hésite..."
    elif pourcentage < 70:
        message = "🙂 Belle connexion, continue !"
    elif pourcentage < 90:
        message = "😍 Coup de foudre probable !"
    else:
        message = "💍💘 ÂME SŒUR DÉTECTÉE 💘💍"

    resultat.config(
        text=f"👤 {nom}\n♈ {signe}\n\n💖 Probabilité d’amour : {pourcentage}%\n\n{message}",
        fg="darkred"
    )

    # Sauvegarde
    with open("resultats_amour.txt", "a", encoding="utf-8") as f:
        f.write(f"{nom} - {signe} - {pourcentage}%\n")

    afficher_coeur()

# -----------------------------
# Interface graphique
# -----------------------------
fenetre = tk.Tk()
fenetre.title("💘 Machine de l'Amour Ultime 💘")
fenetre.geometry("450x550")
fenetre.resizable(False, False)

tk.Label(fenetre, text="💖 LA MACHINE DE L’AMOUR 💖",
         font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(fenetre, text="Ton nom :").pack()
entry_nom = tk.Entry(fenetre)
entry_nom.pack(pady=5)

tk.Label(fenetre, text="Ton signe astrologique :").pack()

combo_signe = ttk.Combobox(
    fenetre,
    values=list(compatibilite.keys()),
    state="readonly"
)
combo_signe.pack(pady=5)

tk.Button(
    fenetre,
    text="Tester l’amour ❤️",
    command=calculer_amour,
    bg="pink",
    font=("Arial", 12, "bold")
).pack(pady=15)

resultat = tk.Label(fenetre, text="", font=("Arial", 11),
                    wraplength=380, justify="center")
resultat.pack(pady=10)

frame_animation = tk.Frame(fenetre)
frame_animation.pack(pady=10)

fenetre.mainloop()
