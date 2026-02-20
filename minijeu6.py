import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import random
import math

# ===================== ASTROLOGIE =====================

SIGNS = [
    ("Capricorne", (12, 22), (1, 19), "Terre"),
    ("Verseau", (1, 20), (2, 18), "Air"),
    ("Poissons", (2, 19), (3, 20), "Eau"),
    ("Bélier", (3, 21), (4, 19), "Feu"),
    ("Taureau", (4, 20), (5, 20), "Terre"),
    ("Gémeaux", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Eau"),
    ("Lion", (7, 23), (8, 22), "Feu"),
    ("Vierge", (8, 23), (9, 22), "Terre"),
    ("Balance", (9, 23), (10, 22), "Air"),
    ("Scorpion", (10, 23), (11, 21), "Eau"),
    ("Sagittaire", (11, 22), (12, 21), "Feu"),
]

ELEMENT_SCORE = {
    ("Feu", "Feu"): 90,
    ("Eau", "Eau"): 90,
    ("Air", "Air"): 90,
    ("Terre", "Terre"): 90,
    ("Feu", "Air"): 75,
    ("Air", "Feu"): 75,
    ("Eau", "Terre"): 75,
    ("Terre", "Eau"): 75,
}

# ===================== IA MESSAGES =====================

MESSAGES = [
    "Connexion émotionnelle intense mais exigeante.",
    "Relation basée sur la communication et la confiance.",
    "Attraction forte, attention aux non-dits.",
    "Lien durable si les objectifs sont alignés.",
    "Compatibilité mature et stable dans le temps.",
    "Relation passionnée avec défis émotionnels.",
    "Potentiel élevé si chacun respecte l’espace de l’autre.",
]

# ===================== FONCTIONS IA =====================

def get_sign(date):
    d = date.day
    m = date.month
    for sign, start, end, element in SIGNS:
        if (m == start[0] and d >= start[1]) or \
           (m == end[0] and d <= end[1]):
            return sign, element
    return "Capricorne", "Terre"


def compatibility(sign1, elem1, sign2, elem2, hobbies, personality):
    score = 0

    # Astrologie
    score += ELEMENT_SCORE.get((elem1, elem2), 40)

    # Loisirs
    common = len(set(hobbies[0]) & set(hobbies[1]))
    score += min(common * 5, 15)

    # Personnalité
    if personality[0] == personality[1]:
        score += 20
    else:
        score += 12

    # Âge
    age_diff = abs(hobbies[2] - hobbies[3])
    score += max(0, 10 - age_diff)

    # Humanisation IA
    score += random.randint(-5, 10)

    return min(int(score), 100)


# ===================== INTERFACE =====================

root = tk.Tk()
root.title("LOVE AI – Compatibility Analyzer")
root.geometry("720x600")
root.configure(bg="#111")

style = ttk.Style()
style.theme_use("clam")

def analyze():
    try:
        d1 = date1.get_date()
        d2 = date2.get_date()

        sign1, elem1 = get_sign(d1)
        sign2, elem2 = get_sign(d2)

        hobbies1 = hobby1.get().split(",")
        hobbies2 = hobby2.get().split(",")

        score = compatibility(
            sign1, elem1, sign2, elem2,
            (hobbies1, hobbies2, age1.get(), age2.get()),
            (pers1.get(), pers2.get())
        )

        msg = random.choice(MESSAGES)

        messagebox.showinfo(
            "Résultat IA",
            f"""
{sign1} ({elem1}) ❤️ {sign2} ({elem2})

Compatibilité globale : {score}%

Analyse IA :
{msg}
            """
        )
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="LOVE AI – Analyse de compatibilité", font=("Segoe UI", 18)).pack(pady=10)

date1 = DateEntry(frame)
date2 = DateEntry(frame)
age1 = tk.IntVar(value=22)
age2 = tk.IntVar(value=22)
pers1 = ttk.Combobox(frame, values=["Introverti", "Extraverti"])
pers2 = ttk.Combobox(frame, values=["Introverti", "Extraverti"])
hobby1 = ttk.Entry(frame)
hobby2 = ttk.Entry(frame)

for label, widget in [
    ("Date naissance A", date1),
    ("Date naissance B", date2),
    ("Personnalité A", pers1),
    ("Personnalité B", pers2),
    ("Loisirs A (virgule)", hobby1),
    ("Loisirs B (virgule)", hobby2),
]:
    ttk.Label(frame, text=label).pack()
    widget.pack(fill="x", pady=4)

ttk.Button(frame, text="Analyser la compatibilité", command=analyze).pack(pady=20)

root.mainloop()
