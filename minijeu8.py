import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import random

# =====================================================
# ASTROLOGIE
# =====================================================

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

ELEMENT_COMPAT = {
    ("Feu", "Feu"): 30,
    ("Air", "Air"): 30,
    ("Eau", "Eau"): 30,
    ("Terre", "Terre"): 30,
    ("Feu", "Air"): 25,
    ("Air", "Feu"): 25,
    ("Eau", "Terre"): 25,
    ("Terre", "Eau"): 25,
}

# =====================================================
# PSYCHOLOGIE DES COULEURS
# =====================================================

COLOR_COMPAT = {
    ("Rouge", "Rouge"): 10,
    ("Bleu", "Bleu"): 10,
    ("Vert", "Vert"): 10,
    ("Noir", "Noir"): 10,
    ("Blanc", "Blanc"): 10,
    ("Rouge", "Noir"): 6,
    ("Bleu", "Blanc"): 6,
    ("Vert", "Bleu"): 6,
}

# =====================================================
# UTILITAIRES
# =====================================================

def age(d):
    today = date.today()
    return today.year - d.year - ((today.month, today.day) < (d.month, d.day))


def get_sign(d):
    for s, start, end, e in SIGNS:
        if (d.month == start[0] and d.day >= start[1]) or \
           (d.month == end[0] and d.day <= end[1]):
            return s, e
    return "Capricorne", "Terre"

# =====================================================
# CALCUL IA
# =====================================================

def calcul_score(p1, p2):
    score = 0

    # Astrologie (30)
    score += ELEMENT_COMPAT.get((p1["element"], p2["element"]), 15)

    # Loisirs (20)
    communs = len(set(p1["loisirs"]) & set(p2["loisirs"]))
    score += min(communs * 5, 20)

    # Couleurs (10)
    score += COLOR_COMPAT.get(
        (p1["couleur"], p2["couleur"]),
        COLOR_COMPAT.get((p2["couleur"], p1["couleur"]), 3)
    )

    # Intro / Extraverti (15)
    if p1["caractere"] == p2["caractere"]:
        score += 15
    else:
        score += 10

    # Langage de l’amour (15)
    if p1["amour"] == p2["amour"]:
        score += 15

    # Vision relationnelle (10)
    if p1["vision"] == p2["vision"]:
        score += 10

    # Ajustement IA réaliste
    score += random.randint(0, 5)

    return min(score, 100)

# =====================================================
# INTERFACE
# =====================================================

root = tk.Tk()
root.title("LOVE AI – Compatibility Analyzer (PRO)")
root.geometry("750x820")
root.configure(bg="#f4f4f4")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

style = ttk.Style()
style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

def personne_frame(titre):
    f = ttk.LabelFrame(frame, text=titre, padding=15)
    f.pack(fill="x", pady=10)

    champs = {
        "Nom": ttk.Entry(f),
        "Date de naissance": DateEntry(f, date_pattern="dd/mm/yyyy"),
        "Couleur préférée": ttk.Combobox(f, values=["Rouge", "Bleu", "Vert", "Noir", "Blanc"]),
        "Caractère": ttk.Combobox(f, values=["Introverti", "Extraverti"]),
        "Loisirs (séparés par ,)": ttk.Entry(f),
        "Langage de l'amour": ttk.Combobox(f, values=["Attention", "Cadeaux", "Temps", "Paroles"]),
        "Vision relationnelle": ttk.Combobox(f, values=["Sérieux", "Libre", "Indécis"]),
    }

    for i, (label, widget) in enumerate(champs.items()):
        ttk.Label(f, text=label).grid(row=i, column=0, sticky="w", pady=5)
        widget.grid(row=i, column=1, sticky="ew", pady=5)

    f.columnconfigure(1, weight=1)
    return champs

p1 = personne_frame("Personne A")
p2 = personne_frame("Personne B")

def analyser():
    try:
        def extract(p):
            d = p["Date de naissance"].get_date()
            if age(d) < 15:
                raise ValueError("Application réservée aux personnes de 15 ans et plus.")

            sign, elem = get_sign(d)

            return {
                "nom": p["Nom"].get(),
                "signe": sign,
                "element": elem,
                "couleur": p["Couleur préférée"].get(),
                "caractere": p["Caractère"].get(),
                "loisirs": [x.strip().lower() for x in p["Loisirs (séparés par ,)"].get().split(",") if x.strip()],
                "amour": p["Langage de l'amour"].get(),
                "vision": p["Vision relationnelle"].get(),
            }

        A = extract(p1)
        B = extract(p2)

        score = calcul_score(A, B)

        interpretation = (
            "Relation stable et mature." if score >= 80 else
            "Bon potentiel avec communication." if score >= 60 else
            "Compatibilité fragile." if score >= 40 else
            "Risque émotionnel élevé."
        )

        messagebox.showinfo(
            "Résultat IA",
            f"{A['nom']} ({A['signe']}) ❤️ {B['nom']} ({B['signe']})\n\n"
            f"Compatibilité : {score}%\n\n{interpretation}"
        )

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(frame, text="Analyser la compatibilité", command=analyser).pack(pady=25)

root.mainloop()
