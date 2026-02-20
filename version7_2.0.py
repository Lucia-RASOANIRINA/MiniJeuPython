import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import random
import re
from datetime import date
from PIL import Image, ImageTk, ImageDraw, ImageOps

# =====================================================
# CONFIGURATION DU DESIGN "POCKET LOVE"
# =====================================================
C_BG = "#FFF9E3"      # Fond crème
C_HEADER = "#FFD1DC"  # Rose pastel header
C_CARD = "#FFFFFF"    # Blanc pur pour les cartes
C_TEXT = "#5D4037"    # Brun texte
C_ACCENT = "#FFB7CE"  # Rose accent
C_BORDER = "#FFDAE5"  # Bordure douce

FONT_TITLE = ("Comic Sans MS", 18, "bold")
FONT_LABEL = ("Comic Sans MS", 9, "bold")
FONT_INPUT = ("Comic Sans MS", 9)
FONT_BUBBLE = ("Comic Sans MS", 8, "italic")

# =====================================================
# LOGIQUE & CITATIONS
# =====================================================
CITATIONS = {
    "excellent": ["L'amour est une âme en deux corps.", "Un match écrit dans les étoiles !"],
    "moyen": ["Une belle étincelle à cultiver.", "Le début d'une jolie histoire ?"],
    "faible": ["Le cœur a ses raisons...", "L'amitié est parfois le plus beau des trésors."],
    "jeune": ["Patience ! L'amour est une fleur qui prend son temps pour éclore."]
}

def make_circle(img_path, size=(90, 90)):
    try:
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img = Image.open(img_path).convert("RGBA")
        img = ImageOps.fit(img, size, centering=(0.5, 0.5))
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)
    except: return None

# =====================================================
# APPLICATION PRINCIPALE
# =====================================================
class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love Destiny")
        self.root.geometry("800x850")
        self.root.configure(bg=C_BG)

        # Header stylisé
        header = tk.Frame(root, bg=C_HEADER, height=60)
        header.pack(fill="x")
        tk.Label(header, text="❤ DESTINY MATCHMAKER ❤", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=10)

        # Conteneur principal avec marges
        self.container = tk.Frame(root, bg=C_BG)
        self.container.pack(expand=True, fill="both", padx=20, pady=10)

        # Grille de profils
        self.data_a = self.create_profile_card(self.container, "LUI", "images.jfif", 0)
        self.data_b = self.create_profile_card(self.container, "ELLE", "images (1).jfif", 1)

        # Zone Résultat (Carte en bas)
        self.res_frame = tk.Frame(root, bg=C_CARD, bd=2, relief="flat", highlightbackground=C_ACCENT, highlightthickness=2)
        self.res_frame.pack(fill="x", padx=100, pady=20)
        
        self.res_title = tk.Label(self.res_frame, text="Prêt pour le destin ?", font=FONT_TITLE, bg=C_CARD, fg=C_TEXT)
        self.res_title.pack(pady=(10, 0))
        
        self.res_text = tk.Label(self.res_frame, text="Entrez vos infos pour voir si c'est le grand amour !", 
                                 font=FONT_BUBBLE, bg=C_CARD, fg=C_ACCENT, wraplength=500)
        self.res_text.pack(pady=10)

        # Bouton Action
        self.btn = tk.Button(root, text="VÉRIFIER LE DESTIN", font=FONT_TITLE, bg=C_ACCENT, fg="white", 
                             relief="flat", cursor="hand2", command=self.analyser, borderwidth=0)
        self.btn.pack(pady=(0, 30), ipadx=20, ipady=5)

    def create_profile_card(self, parent, label, img_path, col):
        # Frame de la colonne
        col_frame = tk.Frame(parent, bg=C_BG)
        col_frame.grid(row=0, column=col, sticky="nsew", padx=15)
        parent.grid_columnconfigure(col, weight=1)

        # Section Bulle + Avatar
        top_frame = tk.Frame(col_frame, bg=C_BG)
        top_frame.pack(fill="x", pady=5)

        # Avatar Rond
        photo = make_circle(img_path)
        img_lbl = tk.Label(top_frame, image=photo, bg=C_BG)
        img_lbl.image = photo
        img_lbl.pack(side="left")

        # Bulle de texte (Haut Droite de l'avatar)
        bubble_canvas = tk.Canvas(top_frame, width=120, height=60, bg=C_BG, highlightthickness=0)
        bubble_canvas.pack(side="left", padx=(5, 0))
        
        # Forme de la bulle
        bubble_canvas.create_oval(10, 5, 115, 45, fill="white", outline=C_ACCENT, width=2)
        bubble_canvas.create_polygon(0, 25, 12, 18, 12, 32, fill="white", outline=C_ACCENT, width=2)
        bubble_canvas.create_line(11, 19, 11, 31, fill="white", width=3) # Efface la bordure interne
        
        b_txt = bubble_canvas.create_text(65, 25, text="Dis-moi tout...", font=FONT_BUBBLE, width=80, fill=C_TEXT)

        # Formulaire (Carte blanche arrondie)
        card = tk.Frame(col_frame, bg=C_CARD, bd=0, highlightbackground=C_BORDER, highlightthickness=2)
        card.pack(fill="both", expand=True)
        
        tk.Label(card, text=f"Profil {label}", font=FONT_LABEL, bg=C_CARD, fg=C_ACCENT).pack(pady=5)

        inputs = {}
        vcmd = (self.root.register(self.validate_name), '%P')
        
        fields = [
            ("Nom", "entry"),
            ("Naissance", "date"),
            ("Couleur", ["Rouge", "Rose", "Bleu", "Jaune"]),
            ("Loisirs", ["Cuisine", "Jeux", "Sport", "Musique"]),
            ("Caractère", ["Calme", "Énergique", "Rêveur"]),
            ("Vision", ["Sérieux", "Libre", "Zen"])
        ]

        for name, dtype in fields:
            f_row = tk.Frame(card, bg=C_CARD)
            f_row.pack(fill="x", padx=10, pady=2)
            
            tk.Label(f_row, text=name, font=FONT_LABEL, bg=C_CARD, fg=C_TEXT, width=8, anchor="w").pack(side="left")
            
            if dtype == "entry":
                w = tk.Entry(f_row, font=FONT_INPUT, bg="#F9F9F9", relief="flat", validate="key", validatecommand=vcmd)
            elif dtype == "date":
                w = DateEntry(f_row, font=FONT_INPUT, date_pattern="dd/mm/yyyy", background=C_ACCENT)
            else:
                w = ttk.Combobox(f_row, values=dtype, state="readonly", font=FONT_INPUT)
                w.current(0)
            
            w.pack(side="right", fill="x", expand=True, padx=(5, 0))
            inputs[name] = w

        inputs["bubble_canvas"] = bubble_canvas
        inputs["bubble_txt"] = b_txt
        return inputs

    def validate_name(self, P):
        if P == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", P))

    def analyser(self):
        # 1. Vérification de l'âge (+15 ans)
        today = date.today()
        
        def check_age(inputs):
            bday = inputs["Naissance"].get_date()
            age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
            return age

        try:
            age_a = check_age(self.data_a)
            age_b = check_age(self.data_b)
            nom_a = self.data_a["Nom"].get()
            nom_b = self.data_b["Nom"].get()

            if not nom_a or not nom_b:
                messagebox.showwarning("Attention", "Veuillez entrer les deux prénoms !")
                return

            if age_a < 15 or age_b < 15:
                self.res_title.config(text="Désolé !", fg="#E74C3C")
                self.res_text.config(text=f"Le test n'est pas autorisé pour les moins de 15 ans.\n« {CITATIONS['jeune'][0]} »")
                return

            # 2. Calcul du score
            score = random.randint(45, 99)
            
            # Mise à jour graphique
            self.res_title.config(text=f"Compatibilité : {score}%", fg=C_ACCENT)
            
            if score > 80: prov = random.choice(CITATIONS["excellent"])
            elif score > 55: prov = random.choice(CITATIONS["moyen"])
            else: prov = random.choice(CITATIONS["faible"])
            
            self.res_text.config(text=f"« {prov} »")
            
            # Bulles animées
            self.data_a["bubble_canvas"].itemconfig(self.data_a["bubble_txt"], text=f"Incroyable !")
            self.data_b["bubble_canvas"].itemconfig(self.data_b["bubble_txt"], text=f"Love: {score}%")

        except Exception as e:
            messagebox.showerror("Erreur", "Veuillez vérifier les dates saisies.")

if __name__ == "__main__":
    root = tk.Tk()
    # Configuration du style global pour les combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="white", background=C_ACCENT)
    
    app = PocketLoveApp(root)
    root.mainloop()