import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import random
import re

# --- CONFIGURATION ESTHÉTIQUE ---
C_BG = "#FFF0F5"        # Rose très pâle (Lavender Blush)
C_CARD = "#FFFFFF"      # Blanc pur
C_TEXT = "#4A4A4A"      # Gris foncé doux
C_ACCENT = "#FF6B6B"    # Corail pour les boutons
C_GOLD = "#FFD700"      # Or pour le score
FONT_MAIN = ("Comic Sans MS", 10)
FONT_BOLD = ("Comic Sans MS", 11, "bold")

# --- DONNÉES MASSIVES ---
COULEURS = ["Rouge Passion", "Bleu Indigo", "Vert Émeraude", "Jaune Citron", "Rose Bonbon", "Violet Royal", "Orange Corail", "Noir Jais", "Blanc Pur", "Gris Anthracite", "Marron Chocolat", "Turquoise", "Beige Sable", "Bordeaux", "Kaki", "Or", "Argent", "Lavande", "Menthe", "Saumon", "Cyan", "Marine"]
LANGAGES = ["Paroles valorisantes", "Moments de qualité", "Cadeaux", "Services rendus", "Toucher physique"]
LOISIRS = [f"Activité {i}" for i in range(1, 101)] # Simulé pour l'exemple, peut être rempli
CARACTERES = ["Calme", "Explosif", "Rêveur", "Pragmatique", "Aventurier", "Pantouflard", "Timide", "Extraverti", "Sérieux", "Farceur", "Altruiste", "Ambitieux"] + [f"Trait {i}" for i in range(1, 90)]
VISIONS = ["Fonder une famille", "Voyager autour du monde", "Carrière d'abord", "Vivre au jour le jour", "Construire une maison", "Vie d'artiste"]

PROVERBES = {
    "high": ["L'amour est une âme en deux corps.", "Qui se ressemble s'assemble !"],
    "opposed": ["Les opposés s'attirent.", "La différence est le sel de la vie."],
    "low": ["Mieux vaut être seul que mal accompagné.", "Chaque pot a son couvercle, mais pas celui-ci."]
}

class LoveGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Matchmaker AI")
        self.root.geometry("1000x900")
        self.root.configure(bg=C_BG)

        # Style pour empêcher la saisie dans les Combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", postoffset=(0,0,0,0))
        self.root.option_add("*TCombobox*Listbox.ReadOnly", 1)

        # Titre
        tk.Label(root, text="💖 TEST DE COMPATIBILITÉ 💖", font=("Comic Sans MS", 22, "bold"), bg=C_BG, fg=C_ACCENT).pack(pady=10)

        # Container Principal
        self.main_container = tk.Frame(root, bg=C_BG)
        self.main_container.pack(fill="both", expand=True, padx=20)

        # Formulaires GAUCHE et DROITE
        self.data_a = self.draw_player_form(self.main_container, "PROFIL A", "left")
        self.data_b = self.draw_player_form(self.main_container, "PROFIL B", "right")

        # Zone de résultat (cachée au début)
        self.res_frame = tk.Frame(root, bg=C_CARD, highlightbackground=C_ACCENT, highlightthickness=3, padx=20, pady=20)
        self.res_label = tk.Label(self.res_frame, text="", font=FONT_BOLD, bg=C_CARD, wraplength=400)
        self.res_label.pack()

        # Bouton Action
        self.btn_calc = tk.Button(root, text="VÉRIFIER LE DESTIN", font=("Comic Sans MS", 14, "bold"), 
                                 bg=C_ACCENT, fg="white", bd=0, padx=30, pady=10, command=self.calculer)
        self.btn_calc.pack(pady=20)
        self.res_frame.pack(pady=10)

    def validate_name(self, text):
        # Autorise vide (pour l'effacement) ou uniquement Lettres, commence par Maj
        if text == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", text))

    def draw_player_form(self, parent, title, side):
        frame = tk.LabelFrame(parent, text=title, bg=C_CARD, font=FONT_BOLD, fg=C_ACCENT, padx=15, pady=15)
        frame.pack(side=side, expand=True, fill="both", padx=10)

        inputs = {}
        
        # Validation Nom
        vcmd = (self.root.register(self.validate_name), '%P')
        
        fields = [
            ("Nom (Majuscule, sans espace)", "entry"),
            ("Date de Naissance", "date"),
            ("Couleur Préférée", COULEURS),
            ("Langage de l'Amour", LANGAGES),
            ("Loisir Principal", LOISIRS),
            ("Caractère", CARACTERES),
            ("Vision de vie", VISIONS)
        ]

        for label, data in fields:
            tk.Label(frame, text=label, bg=C_CARD, font=FONT_MAIN).pack(anchor="w", pady=(5,0))
            if data == "entry":
                w = tk.Entry(frame, validate="key", validatecommand=vcmd, font=FONT_MAIN)
            elif data == "date":
                w = DateEntry(frame, date_pattern="dd/mm/yyyy")
            else:
                # state="readonly" empêche la saisie manuelle
                w = ttk.Combobox(frame, values=data, state="readonly", font=FONT_MAIN)
                w.current(0)
            w.pack(fill="x", pady=2)
            inputs[label] = w

        return inputs

    def calculer(self):
        # 1. Vérification Nom vide
        nom_a = self.data_a["Nom (Majuscule, sans espace)"].get()
        nom_b = self.data_b["Nom (Majuscule, sans espace)"].get()
        
        if not nom_a or not nom_b:
            self.res_label.config(text="⚠️ Veuillez entrer les noms !", fg="red")
            return

        # 2. Logique de Probabilité complexe
        score = 50
        logs = []

        # Bonus Opposés (Caractère différent = +15%)
        if self.data_a["Caractère"].get() != self.data_b["Caractère"].get():
            score += 15
            logs.append("Les opposés s'attirent vraiment !")
            proverbe = random.choice(PROVERBES["opposed"])
        else:
            score += 5
            proverbe = random.choice(PROVERBES["high"])

        # Bonus Vision commune
        if self.data_a["Vision de vie"].get() == self.data_b["Vision de vie"].get():
            score += 20
        
        # Aléatoire "Destin"
        score += random.randint(-10, 15)
        score = max(0, min(100, score))

        # 3. Affichage
        color = "#2ecc71" if score > 70 else "#f1c40f" if score > 40 else "#e74c3c"
        result_text = f"COMPATIBILITÉ : {score}%\n\n{proverbe}\n\n"
        
        if score > 75:
            result_text += "✨ Un match parfait écrit dans les étoiles ! ✨"
        elif score > 50:
            result_text += "🤝 Une belle amitié qui pourrait fleurir."
        else:
            result_text += "🥀 Le courant a du mal à passer..."

        self.res_label.config(text=result_text, fg=color)

if __name__ == "__main__":
    root = tk.Tk()
    game = LoveGame(root)
    root.mainloop()