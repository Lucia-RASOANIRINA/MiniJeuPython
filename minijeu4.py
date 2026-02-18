import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================
# ASTROLOGIE RÉELLE
# =========================

elements = {
    "Bélier": "Feu", "Lion": "Feu", "Sagittaire": "Feu",
    "Taureau": "Terre", "Vierge": "Terre", "Capricorne": "Terre",
    "Gémeaux": "Air", "Balance": "Air", "Verseau": "Air",
    "Cancer": "Eau", "Scorpion": "Eau", "Poissons": "Eau"
}

signes_dates = [
    ("Capricorne", (12, 22), (1, 19)),
    ("Verseau", (1, 20), (2, 18)),
    ("Poissons", (2, 19), (3, 20)),
    ("Bélier", (3, 21), (4, 19)),
    ("Taureau", (4, 20), (5, 20)),
    ("Gémeaux", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Lion", (7, 23), (8, 22)),
    ("Vierge", (8, 23), (9, 22)),
    ("Balance", (9, 23), (10, 22)),
    ("Scorpion", (10, 23), (11, 21)),
    ("Sagittaire", (11, 22), (12, 21)),
]

def get_signe(jour, mois):
    for signe, (m1, j1), (m2, j2) in signes_dates:
        if (mois == m1 and jour >= j1) or (mois == m2 and jour <= j2):
            return signe
    return "Capricorne"

def compatibilite(s1, s2):
    e1, e2 = elements[s1], elements[s2]
    if e1 == e2:
        return 90
    if (e1 == "Feu" and e2 == "Air") or (e1 == "Air" and e2 == "Feu"):
        return 75
    if (e1 == "Terre" and e2 == "Eau") or (e1 == "Eau" and e2 == "Terre"):
        return 75
    return 40

# =========================
# ANIMATION CŒUR (IMAGE)
# =========================

def afficher_coeur(pourcentage):
    for w in frame_anim.winfo_children():
        w.destroy()

    fig = plt.Figure(figsize=(3.5, 3.5))
    ax = fig.add_subplot(111)

    t = np.linspace(0, 2*np.pi, 2000)
    x = 16 * np.sin(t)**3
    y = (13*np.cos(t) - 5*np.cos(2*t)
         - 2*np.cos(3*t) - np.cos(4*t))

    couleurs = ["#ff4d6d"] if pourcentage >= 75 else \
               ["#ffa94d"] if pourcentage >= 50 else \
               ["#ff0000"]

    for i, col in enumerate(couleurs):
        ax.fill(x*(1-i*0.08), y*(1-i*0.08), col)

    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_title("💖 Compatibilité", fontsize=12)

    canvas = FigureCanvasTkAgg(fig, master=frame_anim)
    canvas.draw()
    canvas.get_tk_widget().pack()

# =========================
# ANALYSE
# =========================

def analyser():
    nom1 = entry_nom1.get()
    nom2 = entry_nom2.get()

    d1 = cal1.get_date()
    d2 = cal2.get_date()

    s1 = get_signe(d1.day, d1.month)
    s2 = get_signe(d2.day, d2.month)

    score = compatibilite(s1, s2)

    if score == 90:
        msg = "💍 Affinité naturelle exceptionnelle"
    elif score == 75:
        msg = "💞 Relation harmonieuse et équilibrée"
    else:
        msg = "⚠️ Relation émotionnellement instable"

    resultat.config(text=f"""
👤 {nom1} ({s1})
👤 {nom2} ({s2})

💖 Compatibilité : {score} %

{msg}
""")

    afficher_coeur(score)

# =========================
# INTERFACE MODERNE
# =========================

fen = tk.Tk()
fen.title("💘 AstroMatch – Mini Game")
fen.geometry("520x680")
fen.configure(bg="#1e1e1e")

def label(txt):
    return tk.Label(fen, text=txt, fg="white", bg="#1e1e1e", font=("Arial", 11))

tk.Label(fen, text="💫 AstroMatch 💫",
         fg="#ff4d6d", bg="#1e1e1e",
         font=("Arial", 20, "bold")).pack(pady=10)

label("Nom personne A").pack()
entry_nom1 = tk.Entry(fen)
entry_nom1.pack()

label("Date de naissance A").pack()
cal1 = DateEntry(fen, date_pattern="dd/mm/yyyy")
cal1.pack(pady=5)

label("Nom personne B").pack()
entry_nom2 = tk.Entry(fen)
entry_nom2.pack()

label("Date de naissance B").pack()
cal2 = DateEntry(fen, date_pattern="dd/mm/yyyy")
cal2.pack(pady=5)

tk.Button(
    fen,
    text="🔮 Analyser la compatibilité",
    command=analyser,
    bg="#ff4d6d",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat"
).pack(pady=15)

resultat = tk.Label(
    fen, text="", fg="white", bg="#1e1e1e",
    font=("Arial", 11), justify="center"
)
resultat.pack(pady=10)

frame_anim = tk.Frame(fen, bg="#1e1e1e")
frame_anim.pack(pady=10)

fen.mainloop()
