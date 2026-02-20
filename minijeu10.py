import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import random
from PIL import Image, ImageTk  # Nécessite: pip install Pillow

# =====================================================
# CONFIGURATION DESIGN "POCKET LOVE"
# =====================================================
C_BG = "#FFF9E3"        # Crème/Jaune très clair
C_HEADER = "#FFD1DC"    # Rose pastel
C_CARD = "#FFFFFF"      # Blanc pour les formulaires
C_TEXT = "#5D4037"      # Brun doux
C_ACCENT = "#FFB7CE"    # Rose bouton
FONT_TITLE = ("Comic Sans MS", 18, "bold")
FONT_LABEL = ("Comic Sans MS", 10)
FONT_BUBBLE = ("Comic Sans MS", 9, "italic")

# =====================================================
# LOGIQUE ASTROLOGIE & IA
# =====================================================
SIGNS = [
    ("Capricorne", (12, 22), (1, 19), "Terre"), ("Verseau", (1, 20), (2, 18), "Air"),
    ("Poissons", (2, 19), (3, 20), "Eau"), ("Bélier", (3, 21), (4, 19), "Feu"),
    ("Taureau", (4, 20), (5, 20), "Terre"), ("Gémeaux", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Eau"), ("Lion", (7, 23), (8, 22), "Feu"),
    ("Vierge", (8, 23), (9, 22), "Terre"), ("Balance", (9, 23), (10, 22), "Air"),
    ("Scorpion", (10, 23), (11, 21), "Eau"), ("Sagittaire", (11, 22), (12, 21), "Feu"),
]

ELEMENT_COMPAT = {
    ("Feu", "Feu"): 30, ("Air", "Air"): 30, ("Eau", "Eau"): 30, ("Terre", "Terre"): 30,
    ("Feu", "Air"): 25, ("Air", "Feu"): 25, ("Eau", "Terre"): 25, ("Terre", "Eau"): 25,
}

def get_sign(d):
    for s, start, end, e in SIGNS:
        if (d.month == start[0] and d.day >= start[1]) or (d.month == end[0] and d.day <= end[1]):
            return s, e
    return "Capricorne", "Terre"

# =====================================================
# INTERFACE PRINCIPALE
# =====================================================
class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love AI - Compatibility")
        self.root.geometry("950x850")
        self.root.configure(bg=C_BG)

        # Header
        header = tk.Frame(root, bg=C_HEADER, height=70)
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="CHOOSE your look!", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=15)

        # Zone de jeu (Grille 3 colonnes)
        self.game_frame = tk.Frame(root, bg=C_BG)
        self.game_frame.pack(expand=True, fill="both", padx=20)

        # --- COLONNE GAUCHE (HOMME) ---
        self.col_left = tk.Frame(self.game_frame, bg=C_BG)
        self.col_left.pack(side="left", expand=True, fill="both")
        
        self.bubble_a = self.create_bubble(self.col_left, "Prêt pour le test ?")
        self.img_a = self.load_avatar(self.col_left, "images.jfif")
        self.inputs_a = self.create_form(self.col_left, "HOMME")

        # --- COLONNE DROITE (FEMME) ---
        self.col_right = tk.Frame(self.game_frame, bg=C_BG)
        self.col_right.pack(side="right", expand=True, fill="both")
        
        self.bubble_b = self.create_bubble(self.col_right, "On y va !")
        self.img_b = self.load_avatar(self.col_right, "images (1).jfif")
        self.inputs_b = self.create_form(self.col_right, "FEMME")

        # Bouton Play
        self.btn_play = tk.Button(root, text="ANALYSER", font=("Comic Sans MS", 16, "bold"),
                                  bg=C_ACCENT, fg="white", relief="flat", padx=40, pady=10,
                                  command=self.analyser, cursor="hand2")
        self.btn_play.pack(pady=30)

    def create_bubble(self, parent, text):
        """Crée une bulle de dialogue au-dessus de l'avatar"""
        b_frame = tk.Frame(parent, bg="white", highlightbackground=C_ACCENT, highlightthickness=2)
        b_frame.pack(pady=5)
        lbl = tk.Label(b_frame, text=text, font=FONT_BUBBLE, bg="white", fg=C_TEXT, padx=10, pady=5)
        lbl.pack()
        return lbl

    def load_avatar(self, parent, filename):
        """Charge l'image de l'avatar"""
        try:
            img = Image.open(filename).resize((200, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(parent, image=photo, bg=C_BG)
            lbl.image = photo
            lbl.pack(pady=5)
            return lbl
        except:
            lbl = tk.Label(parent, text="", bg=C_BG, font=FONT_LABEL)
            lbl.pack(pady=5)
            return lbl

    def create_form(self, parent, genre):
        """Crée le formulaire de saisie identique au vôtre"""
        f = tk.LabelFrame(parent, text=f"Données {genre}", bg=C_CARD, font=FONT_LABEL, fg=C_TEXT, padx=10, pady=10)
        f.pack(padx=10, pady=10, fill="x")

        champs = {
            "Nom": ttk.Entry(f),
            "Naissance": DateEntry(f, date_pattern="dd/mm/yyyy"),
            "Couleur": ttk.Combobox(f, values=["Rouge", "Bleu", "Vert", "Noir", "Blanc"]),
            "Caractère": ttk.Combobox(f, values=["Introverti", "Extraverti"]),
            "Vision": ttk.Combobox(f, values=["Sérieux", "Libre", "Indécis"])
        }

        for label, widget in champs.items():
            tk.Label(f, text=label, bg=C_CARD, font=FONT_LABEL, fg=C_TEXT).pack(anchor="w")
            widget.pack(fill="x", pady=2)
        
        return champs

    def analyser(self):
        try:
            # Extraction des données
            def extract(inputs):
                d = inputs["Naissance"].get_date()
                sign, elem = get_sign(d)
                return {
                    "nom": inputs["Nom"].get(),
                    "signe": sign,
                    "element": elem,
                    "vision": inputs["Vision"].get()
                }

            pA = extract(self.inputs_a)
            pB = extract(self.inputs_b)

            # Calcul simplifié (votre logique)
            score = 50 
            if pA["element"] == pB["element"]: score += 20
            if pA["vision"] == pB["vision"]: score += 20
            score += random.randint(0, 10)
            score = min(score, 100)

            # Mise à jour des bulles de dialogue
            self.bubble_a.config(text=f"Score : {score}% !")
            if score >= 80:
                self.bubble_b.config(text="C'est le grand amour !")
            elif score >= 50:
                self.bubble_b.config(text="Pas mal du tout !")
            else:
                self.bubble_b.config(text="Juste amis ?")

            messagebox.showinfo("Résultat IA", f"Compatibilité entre {pA['nom']} et {pB['nom']} : {score}%")

        except Exception as e:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

if __name__ == "__main__":
    root = tk.Tk()
    # Configuration du style des Combobox pour qu'elles soient plus jolies
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="white", background=C_ACCENT)
    
    app = PocketLoveApp(root)
    root.mainloop()
