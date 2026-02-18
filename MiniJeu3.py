import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# ===============================
# DONNÉES ASTROLOGIQUES RÉELLES
# ===============================

signes = [
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

elements = {
    "Bélier": "Feu", "Lion": "Feu", "Sagittaire": "Feu",
    "Taureau": "Terre", "Vierge": "Terre", "Capricorne": "Terre",
    "Gémeaux": "Air", "Balance": "Air", "Verseau": "Air",
    "Cancer": "Eau", "Scorpion": "Eau", "Poissons": "Eau"
}

# ===============================
# LOGIQUE ASTROLOGIQUE PRO
# ===============================

def determiner_signe(jour, mois):
    for signe, (m1, j1), (m2, j2) in signes:
        if (mois == m1 and jour >= j1) or (mois == m2 and jour <= j2):
            return signe
    return "Capricorne"

def compatibilite(signe1, signe2):
    e1 = elements[signe1]
    e2 = elements[signe2]

    if e1 == e2:
        return random.randint(80, 95)
    if (e1 == "Feu" and e2 == "Air") or (e1 == "Air" and e2 == "Feu"):
        return random.randint(70, 85)
    if (e1 == "Terre" and e2 == "Eau") or (e1 == "Eau" and e2 == "Terre"):
        return random.randint(70, 85)
    return random.randint(30, 55)

# ===============================
# ANIMATION ADAPTATIVE
# ===============================

def afficher_animation(pourcentage):
    for widget in frame_anim.winfo_children():
        widget.destroy()

    fig = plt.Figure(figsize=(3, 3))
    ax = fig.add_subplot(111)

    x = np.linspace(-2, 2, 400)

    if pourcentage >= 75:
        y = np.sqrt(1 - (abs(x) - 1)**2)
        couleur = "green"
        titre = "💚 Amour Fort"
    elif pourcentage >= 50:
        y = np.sin(5 * x)
        couleur = "orange"
        titre = "💛 Relation Instable"
    else:
        y = -abs(x)
        couleur = "red"
        titre = "🚨 Danger Émotionnel"

    ax.plot(x, y, color=couleur, linewidth=3)
    ax.axis("off")
    ax.set_title(titre)

    canvas = FigureCanvasTkAgg(fig, master=frame_anim)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ===============================
# FONCTION PRINCIPALE
# ===============================

def analyser():
    try:
        nom1 = entry_nom1.get()
        nom2 = entry_nom2.get()
        d1 = datetime.strptime(entry_date1.get(), "%d/%m/%Y")
        d2 = datetime.strptime(entry_date2.get(), "%d/%m/%Y")
    except:
        messagebox.showerror("Erreur", "Format date : JJ/MM/AAAA")
        return

    signe1 = determiner_signe(d1.day, d1.month)
    signe2 = determiner_signe(d2.day, d2.month)

    score = compatibilite(signe1, signe2)

    if score >= 75:
        msg = "💍 Connexion très forte. Relation prometteuse."
    elif score >= 50:
        msg = "🙂 Relation possible avec des efforts."
    else:
        msg = "⚠️ Relation émotionnellement risquée."

    resultat.config(
        text=f"""
👤 {nom1} ({signe1})
👤 {nom2} ({signe2})

💖 Compatibilité : {score} %

🧠 Analyse :
{msg}
"""
    )

    afficher_animation(score)

# ===============================
# INTERFACE TKINTER
# ===============================

fenetre = tk.Tk()
fenetre.title("💫 AstroMatch Pro")
fenetre.geometry("520x650")
fenetre.resizable(False, False)

tk.Label(fenetre, text="💘 AstroMatch Pro 💘", font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(fenetre, text="Nom Personne A").pack()
entry_nom1 = tk.Entry(fenetre)
entry_nom1.pack()

tk.Label(fenetre, text="Date de naissance A (JJ/MM/AAAA)").pack()
entry_date1 = tk.Entry(fenetre)
entry_date1.pack(pady=5)

tk.Label(fenetre, text="Nom Personne B").pack()
entry_nom2 = tk.Entry(fenetre)
entry_nom2.pack()

tk.Label(fenetre, text="Date de naissance B (JJ/MM/AAAA)").pack()
entry_date2 = tk.Entry(fenetre)
entry_date2.pack(pady=5)

tk.Button(
    fenetre,
    text="🔮 Analyser la compatibilité",
    command=analyser,
    bg="pink",
    font=("Arial", 12, "bold")
).pack(pady=15)

resultat = tk.Label(fenetre, text="", justify="center", font=("Arial", 11))
resultat.pack(pady=10)

frame_anim = tk.Frame(fenetre)
frame_anim.pack(pady=10)

fenetre.mainloop()
