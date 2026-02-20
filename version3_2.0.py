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

# Listes massives (+ de 100 options générées pour les loisirs et caractères)
COULEURS = ["Rouge Passion", "Bleu Azur", "Vert Émeraude", "Jaune Pastel", "Rose Bonbon", "Violet", "Orange", "Noir", "Blanc", "Or", "Argent"] + [f"Couleur Rare {i}" for i in range(1, 15)]
LANGAGES = ["Paroles valorisantes", "Moments de qualité", "Cadeaux", "Services rendus", "Toucher physique"]
LOISIRS = ["Jeux Vidéo", "Cuisine", "Voyage", "Lecture", "Sport", "Dessin", "Musique", "Cinéma", "Photographie", "Jardinage"] + [f"Activité {i}" for i in range(1, 95)]
CARACTERES = ["Introverti", "Extraverti", "Calme", "Explosif", "Rêveur", "Pragmatique", "Timide", "Ambitieux", "Généreux", "Mystérieux"] + [f"Trait {i}" for i in range(1, 95)]
VISIONS = ["Sérieux/Famille", "Libre/Aventure", "Carrière d'abord", "Vie d'artiste", "Vivre au jour le jour"]

SIGNS = [
    ("Capricorne", (12, 22), (1, 19), "Terre"), ("Verseau", (1, 20), (2, 18), "Air"),
    ("Poissons", (2, 19), (3, 20), "Eau"), ("Bélier", (3, 21), (4, 19), "Feu"),
    ("Taureau", (4, 20), (5, 20), "Terre"), ("Gémeaux", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Eau"), ("Lion", (7, 23), (8, 22), "Feu"),
    ("Vierge", (8, 23), (9, 22), "Terre"), ("Balance", (9, 23), (10, 22), "Air"),
    ("Scorpion", (10, 23), (11, 21), "Eau"), ("Sagittaire", (11, 22), (12, 21), "Feu"),
]

# =====================================================
# APPLICATION PRINCIPALE
# =====================================================
class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love AI - Mini Jeu")
        self.root.geometry("1000x920")
        self.root.configure(bg=C_BG)

        # Style pour empêcher la saisie dans les listes
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background=C_ACCENT)

        # Header
        header = tk.Frame(root, bg=C_HEADER, height=60)
        header.pack(fill="x")
        tk.Label(header, text="✨ TESTEUR DE DESTIN ✨", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=10)

        # Zone de jeu principale
        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Création des interfaces (Correction de l'erreur := ici)
        self.data_a = self.create_player_ui(self.main_frame, "LUI", "images.jfif", "left")
        self.data_b = self.create_player_ui(self.main_frame, "ELLE", "images (1).jfif", "right")

        # Zone Résultat stylisée
        self.res_card = tk.Frame(root, bg=C_CARD, highlightbackground=C_ACCENT, highlightthickness=3, pady=10)
        self.res_card.pack(fill="x", padx=100, pady=10)
        
        self.score_lbl = tk.Label(self.res_card, text="En attente des profils...", font=("Comic Sans MS", 16, "bold"), bg=C_CARD, fg=C_TEXT)
        self.score_lbl.pack()
        self.msg_lbl = tk.Label(self.res_card, text="", font=FONT_BUBBLE, bg=C_CARD, fg=C_ACCENT, wraplength=700)
        self.msg_lbl.pack()

        # Bouton d'analyse
        self.btn = tk.Button(root, text="ANALYSER LE DESTIN", font=FONT_TITLE, bg=C_ACCENT, fg="white", 
                             relief="flat", padx=30, command=self.analyser, cursor="hand2")
        self.btn.pack(pady=(0, 20))

    def validate_name(self, P):
        """Validation stricte du nom : Majuscule, pas de chiffres, pas de caractères spéciaux."""
        if P == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", P))

    def create_player_ui(self, parent, label, img_path, side):
        container = tk.Frame(parent, bg=C_BG)
        container.pack(side=side, expand=True, fill="both", padx=20)

        # Bulle de texte au-dessus de l'avatar
        bubble = tk.Label(container, text="Parle-moi de toi !", font=FONT_BUBBLE, bg="white", 
                          highlightbackground=C_ACCENT, highlightthickness=1, padx=8, pady=4)
        bubble.pack(pady=5)

        # Chargement de l'avatar
        try:
            img = Image.open(img_path).resize((160, 220), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_lbl = tk.Label(container, image=photo, bg=C_BG)
            img_lbl.image = photo
            img_lbl.pack()
        except Exception:
            # Fallback si l'image n'existe pas
            img_lbl = tk.Label(container, text="[Photo]", bg="#DDD", width=20, height=10, font=FONT_BOLD)
            img_lbl.pack()

        # Formulaire dans une carte blanche
        form = tk.LabelFrame(container, text=f" Profil {label} ", bg=C_CARD, font=FONT_BOLD, fg=C_TEXT)
        form.pack(fill="x", pady=10, padx=5)

        inputs = {}
        vcmd = (self.root.register(self.validate_name), '%P')

        # Configuration des champs
        fields = [
            ("Nom", "entry"),
            ("Naissance", "date"),
            ("Couleur Préférée", COULEURS),
            ("Langage d'Amour", LANGAGES),
            ("Loisirs (+100)", LOISIRS),
            ("Caractère (+100)", CARACTERES),
            ("Vision de vie", VISIONS)
        ]

        for name, dtype in fields:
            tk.Label(form, text=name, bg=C_CARD, font=FONT_LABEL, fg=C_TEXT).pack(anchor="w", padx=10, pady=(5,0))
            if dtype == "entry":
                w = tk.Entry(form, validate="key", validatecommand=vcmd, font=FONT_LABEL)
            elif dtype == "date":
                w = DateEntry(form, date_pattern="dd/mm/yyyy", background=C_ACCENT, font=FONT_LABEL)
            else:
                # state="readonly" empêche l'utilisateur d'écrire dans la liste
                w = ttk.Combobox(form, values=dtype, state="readonly", font=FONT_LABEL)
                w.current(0)
            w.pack(fill="x", padx=10, pady=2)
            inputs[name] = w
            
        inputs["bubble"] = bubble
        return inputs

    def get_astro_element(self, d):
        for s, start, end, e in SIGNS:
            if (d.month == start[0] and d.day >= start[1]) or (d.month == end[0] and d.day <= end[1]):
                return e
        return "Terre"

    def analyser(self):
        nom_a = self.data_a["Nom"].get()
        nom_b = self.data_b["Nom"].get()

        # Vérification si les noms sont remplis
        if not nom_a or not nom_b:
            self.score_lbl.config(text="⚠️ Noms manquants !", fg="#E74C3C")
            return

        # --- LOGIQUE DE CALCUL DES PROBABILITÉS ---
        score = 40
        
        # 1. Élément Astrologique
        elem_a = self.get_astro_element(self.data_a["Naissance"].get_date())
        elem_b = self.get_astro_element(self.data_b["Naissance"].get_date())
        if elem_a == elem_b: score += 15
        
        # 2. Bonus "Les opposés s'attirent" (si caractères différents)
        char_a = self.data_a["Caractère (+100)"].get()
        char_b = self.data_b["Caractère (+100)"].get()
        
        proverbe = ""
        if char_a != char_b:
            score += 25
            proverbe = "On dit que 'Les opposés s'attirent'... Vos différences sont votre plus grande force !"
        else:
            score += 10
            proverbe = "Comme le dit le proverbe : 'Qui se ressemble s'assemble'. Vous êtes faits du même bois !"

        # 3. Vision de vie identique
        if self.data_a["Vision de vie"].get() == self.data_b["Vision de vie"].get():
            score += 15

        # Randomisation finale pour le côté "Destin"
        score = min(100, score + random.randint(0, 10))
        
        # --- MISE À JOUR DE L'INTERFACE ---
        self.score_lbl.config(text=f"COMPATIBILITÉ : {score}%", fg=C_ACCENT)
        
        # Messages et proverbes personnalisés
        if score > 80:
            final_msg = f"Fusion Totale entre {nom_a} et {nom_b} ! {proverbe} L'amour est une âme en deux corps."
        elif score > 50:
            final_msg = f"Une belle étincelle entre {nom_a} et {nom_b}. {proverbe} Il y a un vrai potentiel !"
        else:
            final_msg = f"Le courant passe difficilement... Mais n'oubliez pas : 'Le cœur a ses raisons que la raison ne connaît point'."
            
        self.msg_lbl.config(text=final_msg)
        
        # Mise à jour des bulles des avatars
        self.data_a["bubble"].config(text=f"Score : {score}% !")
        self.data_b["bubble"].config(text="Incroyable !")

if __name__ == "__main__":
    root = tk.Tk()
    app = PocketLoveApp(root)
    root.mainloop()