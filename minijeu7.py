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

ELEMENT_SCORE = {
    ("Feu", "Feu"): 30,
    ("Eau", "Eau"): 30,
    ("Air", "Air"): 30,
    ("Terre", "Terre"): 30,
    ("Feu", "Air"): 25,
    ("Air", "Feu"): 25,
    ("Eau", "Terre"): 25,
    ("Terre", "Eau"): 25,
}

# =====================================================
# UTILITAIRES
# =====================================================

def calcul_age(d):
    today = date.today()
    return today.year - d.year - ((today.month, today.day) < (d.month, d.day))


def get_sign(d):
    for sign, start, end, element in SIGNS:
        if (d.month == start[0] and d.day >= start[1]) or \
           (d.month == end[0] and d.day <= end[1]):
            return sign, element
    return "Capricorne", "Terre"


# =====================================================
# CALCUL DE COMPATIBILITÉ
# =====================================================

def calcul_score(p1, p2):
    score = 0

    # Astrologie (30)
    score += ELEMENT_SCORE.get((p1["element"], p2["element"]), 15)

    # Loisirs communs (20)
    communs = len(set(p1["loisirs"]) & set(p2["loisirs"]))
    score += min(communs * 5, 20)

    # Couleur (10)
    if p1["couleur"] == p2["couleur"]:
        score += 10

    # Langage de l’amour (20)
    if p1["amour"] == p2["amour"]:
        score += 20

    # Vision relationnelle (15)
    if p1["vision"] == p2["vision"]:
        score += 15

    # Ajustement IA réaliste (5)
    score += random.randint(0, 5)

    return min(score, 100)


# =====================================================
# INTERFACE
# =====================================================

root = tk.Tk()
root.title("LOVE AI – Compatibility Analyzer (PRO)")
root.geometry("720x780")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 11))
style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)


def personne_frame(titre):
    f = ttk.LabelFrame(frame, text=titre, padding=15)
    f.pack(fill="x", pady=10)

    nom = ttk.Entry(f)
    naissance = DateEntry(f, date_pattern="dd/mm/yyyy")
    couleur = ttk.Combobox(f, values=["Rouge", "Bleu", "Vert", "Noir", "Blanc"])
    loisirs = ttk.Entry(f)
    amour = ttk.Combobox(f, values=["Attention", "Cadeaux", "Temps", "Paroles"])
    vision = ttk.Combobox(f, values=["Sérieux", "Libre", "Indécis"])

    champs = [
        ("Nom", nom),
        ("Date de naissance", naissance),
        ("Couleur préférée", couleur),
        ("Loisirs (séparés par ,)", loisirs),
        ("Langage de l'amour", amour),
        ("Vision relationnelle", vision),
    ]

    for i, (label, widget) in enumerate(champs):
        ttk.Label(f, text=label).grid(row=i, column=0, sticky="w", pady=5)
        widget.grid(row=i, column=1, sticky="ew", pady=5)

    f.columnconfigure(1, weight=1)

    return {
        "nom": nom,
        "date": naissance,
        "couleur": couleur,
        "loisirs": loisirs,
        "amour": amour,
        "vision": vision,
    }


p1 = personne_frame("Personne A")
p2 = personne_frame("Personne B")


def analyser():
    try:
        def extract(p):
            d = p["date"].get_date()
            age = calcul_age(d)

            if age < 15:
                raise ValueError("Analyse réservée aux personnes âgées de 15 ans ou plus.")

            sign, element = get_sign(d)

            return {
                "nom": p["nom"].get(),
                "age": age,
                "signe": sign,
                "element": element,
                "couleur": p["couleur"].get(),
                "loisirs": [x.strip().lower() for x in p["loisirs"].get().split(",") if x.strip()],
                "amour": p["amour"].get(),
                "vision": p["vision"].get(),
            }

        perso1 = extract(p1)
        perso2 = extract(p2)

        score = calcul_score(perso1, perso2)

        if score >= 80:
            msg = "Relation solide, mature et émotionnellement stable."
        elif score >= 60:
            msg = "Potentiel sérieux avec communication et compromis."
        elif score >= 40:
            msg = "Compatibilité fragile, nécessite des efforts réciproques."
        else:
            msg = "Risque émotionnel élevé, relation instable."

        messagebox.showinfo(
            "Résultat de l'analyse",
            f"""
{perso1['nom']} ({perso1['signe']}) ❤️ {perso2['nom']} ({perso2['signe']})

Compatibilité globale : {score} %

Analyse :
{msg}
            """
        )

    except Exception as e:
        messagebox.showerror("Erreur", str(e))


ttk.Button(
    frame,
    text="Analyser la compatibilité",
    command=analyser
).pack(pady=25)

root.mainloop()
