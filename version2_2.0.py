import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import random
import re

# --- CONFIGURATION DESIGN ---
C_BG = "#FFF5F7"        # Rose très pâle
C_ACCENT = "#FF8FAB"    # Rose bouton
C_TEXT = "#4A4A4A"
FONT_MAIN = ("Verdana", 9)
FONT_BOLD = ("Verdana", 9, "bold")
FONT_TITLE = ("Courier New", 16, "bold")

# --- DONNÉES ÉTENDUES ---
COULEURS = ["Rouge", "Bleu", "Vert", "Jaune", "Violet", "Orange", "Rose", "Cyan", "Marron", "Gris", "Noir", "Blanc", "Doré", "Argent", "Indigo", "Turquoise", "Lavande", "Bordeaux", "Beige", "Kaki", "Corail"]

LOISIRS = [f"Loisir {i}" for i in range(1, 101)] # Simulé pour l'exemple, peut être remplacé par une liste réelle
CARACTERES = ["Calme", "Énergique", "Rêveur", "Pragmatique", "Aventurier", "Pantouflard", "Optimiste", "Pessimiste", "Sérieux", "Drôle"] + [f"Trait {i}" for i in range(11, 101)]
VISIONS = ["Famille d'abord", "Carrière pro", "Voyages", "Vie simple", "Grand luxe", "Artiste", "Engagement social"] + [f"Vision {i}" for i in range(8, 101)]
LANGAGES = ["Mots d'encouragement", "Actes de service", "Cadeaux", "Moments de qualité", "Toucher physique"]

PROVERBES = {
    "high": ["L'amour est une âme en deux corps.", "Qui se ressemble s'assemble !"],
    "opposes": ["Les opposés s'attirent, la preuve en est !", "La diversité fait la force du couple."],
    "low": ["Il reste encore du chemin à parcourir.", "L'amitié est parfois le plus beau des amours."]
}

# --- LOGIQUE ASTRO ---
SIGNS = [
    ("Capricorne", (12, 22), (1, 19), "Terre"), ("Verseau", (1, 20), (2, 18), "Air"),
    ("Poissons", (2, 19), (3, 20), "Eau"), ("Bélier", (3, 21), (4, 19), "Feu"),
    ("Taureau", (4, 20), (5, 20), "Terre"), ("Gémeaux", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Eau"), ("Lion", (7, 23), (8, 22), "Feu"),
    ("Vierge", (8, 23), (9, 22), "Terre"), ("Balance", (9, 23), (10, 22), "Air"),
    ("Scorpion", (10, 23), (11, 21), "Eau"), ("Sagittaire", (11, 22), (12, 21), "Feu")
]

class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love AI v2")
        self.root.geometry("700x800")
        self.root.configure(bg=C_BG)

        # Titre
        tk.Label(root, text="♡ LOVE COMPATIBILITY ♡", font=FONT_TITLE, bg=C_BG, fg=C_ACCENT).pack(pady=10)

        # Zone Formulaires
        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(fill="both", expand=True, padx=20)

        self.form_a = self.create_compact_form(self.main_frame, "PERSONNE A", "left")
        self.form_b = self.create_compact_form(self.main_frame, "PERSONNE B", "right")

        # Zone Résultat (Remplace la Message Box)
        self.res_frame = tk.Frame(root, bg="white", highlightbackground=C_ACCENT, highlightthickness=2)
        self.res_frame.pack(fill="x", padx=40, pady=10)
        
        self.res_label = tk.Label(self.res_frame, text="Entrez les noms pour tester l'alchimie...", 
                                 font=FONT_BOLD, bg="white", fg=C_TEXT, wraplength=500)
        self.res_label.pack(pady=10)

        # Bouton
        self.btn_calc = tk.Button(root, text="CALCULER L'AMOUR", font=FONT_BOLD, bg=C_ACCENT, 
                                 fg="white", relief="flat", command=self.calculer, pady=10, cursor="hand2")
        self.btn_calc.pack(fill="x", padx=100, pady=20)

    def create_compact_form(self, parent, title, side):
        frame = tk.LabelFrame(parent, text=title, bg="white", font=FONT_BOLD, fg=C_ACCENT, padx=10, pady=5)
        frame.pack(side=side, fill="both", expand=True, padx=5)

        fields = {}
        
        # Validation du nom (Majuscule, pas de chiffres, pas d'espaces)
        vcmd = (self.root.register(self.validate_name), '%P')
        
        tk.Label(frame, text="Nom:", bg="white", font=FONT_MAIN).pack(anchor="w")
        fields["Nom"] = tk.Entry(frame, validate="key", validatecommand=vcmd)
        fields["Nom"].pack(fill="x", pady=(0,5))

        tk.Label(frame, text="Date de Naissance:", bg="white", font=FONT_MAIN).pack(anchor="w")
        fields["Date"] = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        fields["Date"].pack(fill="x", pady=(0,5))

        # Listes déroulantes (readonly pour empêcher la saisie)
        options = [
            ("Couleur", COULEURS),
            ("Langage", LANGAGES),
            ("Loisirs", LOISIRS),
            ("Vision", VISIONS),
            ("Caractère", CARACTERES)
        ]

        for label, values in options:
            tk.Label(frame, text=label+":", bg="white", font=FONT_MAIN).pack(anchor="w")
            cb = ttk.Combobox(frame, values=values, state="readonly")
            cb.pack(fill="x", pady=(0,5))
            fields[label] = cb

        return fields

    def validate_name(self, text):
        # Autorise vide (pour effacer), sinon vérifie majuscule et alphabet uniquement sans espace
        if text == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", text))

    def get_sign_info(self, d):
        for s, start, end, e in SIGNS:
            if (d.month == start[0] and d.day >= start[1]) or (d.month == end[0] and d.day <= end[1]):
                return s, e
        return "Capricorne", "Terre"

    def calculer(self):
        try:
            data = []
            for f in [self.form_a, self.form_b]:
                res = {k: v.get() for k, v in f.items()}
                if not res["Nom"]: raise ValueError("Nom manquant")
                # Calcul astro
                sign, elem = self.get_sign_info(f["Date"].get_date())
                res["elem"] = elem
                data.append(res)

            # --- ALGORITHME DE PROBABILITÉ ---
            score = 50
            p1, p2 = data[0], data[1]

            # 1. Éléments
            if p1["elem"] == p2["elem"]: score += 15
            
            # 2. Caractère (Opposés qui s'attirent ou similitude ?)
            if p1["Caractère"] == p2["Caractère"]:
                score += 10
                prov = random.choice(PROVERBES["high"])
            else:
                score += 12 # Bonus pour la complémentarité
                prov = random.choice(PROVERBES["opposes"])

            # 3. Vision & Loisirs
            if p1["Vision"] == p2["Vision"]: score += 15
            if p1["Loisirs"] == p2["Loisirs"]: score += 5
            
            score += random.randint(-5, 5) # Facteur chance
            score = max(5, min(99, score))

            # Affichage
            final_text = f"COMPATIBILITÉ : {score}%\n\n"
            if score > 75: final_text += f"✨ {prov} ✨"
            elif score > 40: final_text += f"⚖️ {prov}"
            else: final_text += f"🧊 {random.choice(PROVERBES['low'])}"

            self.res_label.config(text=final_text, fg="#D81B60")

        except Exception:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs correctement.\n(Le nom doit commencer par une Majuscule)")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="white", background=C_ACCENT)
    app = PocketLoveApp(root)
    root.mainloop()
