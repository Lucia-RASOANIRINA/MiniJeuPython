import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

# ----------------- ASTROLOGIE -----------------

def signe_astrologique(jour, mois):
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
        ("Sagittaire", (11, 22), (12, 21))
    ]

    for signe, debut, fin in signes:
        if (mois == debut[0] and jour >= debut[1]) or \
           (mois == fin[0] and jour <= fin[1]):
            return signe
    return "Capricorne"


compatibilite_signes = {
    ("Bélier", "Lion"): 90,
    ("Taureau", "Vierge"): 85,
    ("Gémeaux", "Balance"): 88,
    ("Cancer", "Poissons"): 92,
    ("Lion", "Sagittaire"): 90,
}

def score_signes(s1, s2):
    if s1 == s2:
        return 80
    return compatibilite_signes.get((s1, s2)) or compatibilite_signes.get((s2, s1), 60)

# ----------------- CALCUL -----------------

def calcul_score(p1, p2):
    score = 0

    score += score_signes(p1["signe"], p2["signe"]) * 0.3

    loisirs_communs = len(set(p1["loisirs"]) & set(p2["loisirs"]))
    score += min(loisirs_communs * 10, 20)

    if p1["couleur"] == p2["couleur"]:
        score += 10

    if p1["amour"] == p2["amour"]:
        score += 25

    if p1["vision"] == p2["vision"]:
        score += 15

    return int(score)

# ----------------- INTERFACE -----------------

root = tk.Tk()
root.title("Love Compatibility Pro")
root.geometry("650x700")
root.configure(bg="#f5f5f5")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 11))

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

def personne_frame(titre):
    f = ttk.LabelFrame(frame, text=titre, padding=10)
    f.pack(fill="x", pady=10)

    nom = ttk.Entry(f)
    date_naissance = DateEntry(f, date_pattern="dd/mm/yyyy")
    couleur = ttk.Combobox(f, values=["Rouge", "Bleu", "Vert", "Noir", "Blanc"])
    loisirs = ttk.Entry(f)
    amour = ttk.Combobox(f, values=["Attention", "Cadeaux", "Temps", "Paroles"])
    vision = ttk.Combobox(f, values=["Sérieux", "Libre", "Indécis"])

    widgets = [nom, date_naissance, couleur, loisirs, amour, vision]
    labels = ["Nom", "Date de naissance", "Couleur préférée",
              "Loisirs (séparés par ,)", "Langage de l'amour", "Vision relationnelle"]

    for i, (lab, w) in enumerate(zip(labels, widgets)):
        ttk.Label(f, text=lab).grid(row=i, column=0, sticky="w", pady=4)
        w.grid(row=i, column=1, pady=4, sticky="ew")

    return {
        "nom": nom,
        "date": date_naissance,
        "couleur": couleur,
        "loisirs": loisirs,
        "amour": amour,
        "vision": vision
    }

p1 = personne_frame("Personne 1")
p2 = personne_frame("Personne 2")

def analyser():
    try:
        def extract(p):
            d = p["date"].get_date()
            return {
                "nom": p["nom"].get(),
                "signe": signe_astrologique(d.day, d.month),
                "couleur": p["couleur"].get(),
                "loisirs": [x.strip().lower() for x in p["loisirs"].get().split(",")],
                "amour": p["amour"].get(),
                "vision": p["vision"].get()
            }

        perso1 = extract(p1)
        perso2 = extract(p2)

        score = calcul_score(perso1, perso2)

        if score >= 80:
            msg = "❤️ Amour puissant et stable"
        elif score >= 60:
            msg = "💛 Potentiel sérieux"
        elif score >= 40:
            msg = "⚠️ Relation fragile"
        else:
            msg = "❌ Risque émotionnel élevé"

        messagebox.showinfo("Résultat", f"Compatibilité : {score}%\n\n{msg}")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(frame, text="Analyser la compatibilité", command=analyser).pack(pady=20)

root.mainloop()
