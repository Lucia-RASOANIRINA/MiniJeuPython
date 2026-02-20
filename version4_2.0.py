import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import random
import re
from PIL import Image, ImageTk

# =====================================================
# CONFIGURATION DESIGN & DONNÉES
# =====================================================
C_BG = "#FFF9E3"
C_HEADER = "#FFD1DC"
C_CARD = "#FFFFFF"
C_TEXT = "#5D4037"
C_ACCENT = "#FFB7CE"
FONT_TITLE = ("Comic Sans MS", 18, "bold")
FONT_LABEL = ("Comic Sans MS", 10)
FONT_BOLD = ("Comic Sans MS", 10, "bold")
FONT_BUBBLE = ("Comic Sans MS", 9, "italic")

# Données massives
COULEURS = ["Rouge Passion", "Bleu Azur", "Vert Émeraude", "Rose Bonbon", "Or", "Argent", "Lavande"] + [f"Teinte {i}" for i in range(1, 20)]
LANGAGES = ["Paroles valorisantes", "Moments de qualité", "Cadeaux", "Services rendus", "Toucher physique"]
LOISIRS = ["Jeux Vidéo", "Cuisine", "Voyage", "Sport", "Dessin", "Musique"] + [f"Activité {i}" for i in range(1, 100)]
CARACTERES = ["Introverti", "Extraverti", "Calme", "Explosif", "Rêveur", "Pragmatique"] + [f"Trait {i}" for i in range(1, 100)]
VISIONS = ["Sérieux/Famille", "Libre/Aventure", "Carrière d'abord", "Vie d'artiste", "Vivre au jour le jour"]

# Système de proverbes par paliers
CITATIONS = {
    "excellent": [
        "L'amour est une âme en deux corps.",
        "Deux cœurs qui s'aiment n'ont pas besoin de paroles.",
        "Le vrai bonheur est dans le partage.",
        "Quand on aime, on ne compte pas."
    ],
    "moyen": [
        "L'amour est un jardin qui se cultive chaque jour.",
        "Il n'y a pas d'amour sans un peu de folie.",
        "La patience est la clé d'un cœur heureux.",
        "On ne voit bien qu'avec le cœur."
    ],
    "faible": [
        "Le cœur a ses raisons que la raison ne connaît point.",
        "Mieux vaut être seul que mal accompagné.",
        "L'amour demande du temps et de la réflexion.",
        "Chaque pot a son couvercle, il faut juste encore chercher."
    ],
    "opposés": [
        "Les opposés s'attirent et se complètent.",
        "La diversité est le sel de l'amour.",
        "On s'aime par nos ressemblances, on se passionne par nos différences."
    ]
}

SIGNS = [
    ("Capricorne", (12, 22), (1, 19), "Terre"), ("Verseau", (1, 20), (2, 18), "Air"),
    ("Poissons", (2, 19), (3, 20), "Eau"), ("Bélier", (3, 21), (4, 19), "Feu"),
    ("Taureau", (4, 20), (5, 20), "Terre"), ("Gémeaux", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Eau"), ("Lion", (7, 23), (8, 22), "Feu"),
    ("Vierge", (8, 23), (9, 22), "Terre"), ("Balance", (9, 23), (10, 22), "Air"),
    ("Scorpion", (10, 23), (11, 21), "Eau"), ("Sagittaire", (11, 22), (12, 21), "Feu"),
]

class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love AI")
        self.root.geometry("900x850")
        self.root.configure(bg=C_BG)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background=C_ACCENT)

        # Header
        header = tk.Frame(root, bg=C_HEADER)
        header.pack(fill="x")
        tk.Label(header, text="💖 DESTINY MATCHMAKER 💖", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=10)

        # Zone centrale
        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(expand=True, fill="both", padx=10)

        # Création des UI
        self.data_a = self.create_player_ui(self.main_frame, "LUI", "images.jfif", "left")
        self.data_b = self.create_player_ui(self.main_frame, "ELLE", "images (1).jfif", "right")

        # Zone Résultat
        self.res_card = tk.Frame(root, bg=C_CARD, highlightbackground=C_ACCENT, highlightthickness=2, pady=10)
        self.res_card.pack(fill="x", padx=100, pady=15)
        
        self.score_lbl = tk.Label(self.res_card, text="Prêt pour l'analyse ?", font=("Comic Sans MS", 16, "bold"), bg=C_CARD, fg=C_TEXT)
        self.score_lbl.pack()
        self.msg_lbl = tk.Label(self.res_card, text="", font=FONT_BUBBLE, bg=C_CARD, fg=C_ACCENT, wraplength=600)
        self.msg_lbl.pack()

        # Bouton
        self.btn = tk.Button(root, text="VÉRIFIER LA COMPATIBILITÉ", font=FONT_BOLD, bg=C_ACCENT, fg="white", 
                             relief="flat", padx=20, pady=10, command=self.analyser, cursor="hand2")
        self.btn.pack(pady=(0, 20))

    def validate_name(self, P):
        if P == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", P))

    def create_player_ui(self, parent, label, img_path, side):
        container = tk.Frame(parent, bg=C_BG)
        container.pack(side=side, expand=True, fill="both", padx=15)

        bubble = tk.Label(container, text="Dis-moi tout...", font=FONT_BUBBLE, bg="white", 
                          highlightbackground=C_ACCENT, highlightthickness=1, padx=5)
        bubble.pack(pady=5)

        # IMAGE PLUS PETITE (120x160 au lieu de 180x240)
        try:
            img = Image.open(img_path).resize((80, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_lbl = tk.Label(container, image=photo, bg=C_BG)
            img_lbl.image = photo
            img_lbl.pack()
        except:
            img_lbl = tk.Label(container, text="[Photo]", bg="#DDD", width=15, height=7)
            img_lbl.pack()

        form = tk.LabelFrame(container, text=f" Profil {label} ", bg=C_CARD, font=FONT_BOLD)
        form.pack(fill="x", pady=5)

        inputs = {}
        vcmd = (self.root.register(self.validate_name), '%P')

        fields = [
            ("Nom", "entry"),
            ("Naissance", "date"),
            ("Couleur", COULEURS),
            ("Langage d'Amour", LANGAGES),
            ("Loisirs", LOISIRS),
            ("Caractère", CARACTERES),
            ("Vision", VISIONS)
        ]

        for name, dtype in fields:
            tk.Label(form, text=name, bg=C_CARD, font=FONT_LABEL).pack(anchor="w", padx=5)
            if dtype == "entry":
                w = tk.Entry(form, validate="key", validatecommand=vcmd)
            elif dtype == "date":
                w = DateEntry(form, date_pattern="dd/mm/yyyy", width=12)
            else:
                w = ttk.Combobox(form, values=dtype, state="readonly")
                w.current(0)
            w.pack(fill="x", padx=5, pady=1)
            inputs[name] = w
            
        inputs["bubble"] = bubble
        return inputs

    def analyser(self):
        nom_a = self.data_a["Nom"].get()
        nom_b = self.data_b["Nom"].get()

        if not nom_a or not nom_b:
            self.score_lbl.config(text="⚠️ Noms requis !", fg="#E74C3C")
            return

        # Calcul
        score = 30
        
        # Bonus opposés
        opposes = self.data_a["Caractère"].get() != self.data_b["Caractère"].get()
        if opposes: score += 25
        
        if self.data_a["Vision"].get() == self.data_b["Vision"].get(): score += 20
        if self.data_a["Langage d'Amour"].get() == self.data_b["Langage d'Amour"].get(): score += 15
        
        score = min(99, score + random.randint(0, 10))

        # Sélection du proverbe
        if score >= 80:
            prov = random.choice(CITATIONS["excellent"])
        elif score >= 50:
            prov = random.choice(CITATIONS["moyen"])
        else:
            prov = random.choice(CITATIONS["faible"])
            
        if opposes and score > 60: # Si score correct malgré les différences
            prov = random.choice(CITATIONS["opposés"])

        # Affichage
        self.score_lbl.config(text=f"COMPATIBILITÉ : {score}%", fg=C_ACCENT)
        self.msg_lbl.config(text=f"Pour {nom_a} & {nom_b} :\n« {prov} »")
        
        self.data_a["bubble"].config(text=f"{score}% !")
        self.data_b["bubble"].config(text="Wow !")

if __name__ == "__main__":
    root = tk.Tk()
    app = PocketLoveApp(root)
    root.mainloop()