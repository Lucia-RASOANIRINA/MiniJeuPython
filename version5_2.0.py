import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import random
import re
from PIL import Image, ImageTk, ImageDraw, ImageOps

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
FONT_BUBBLE = ("Comic Sans MS", 10, "italic")

# Données massives
COULEURS = ["Rouge Passion", "Bleu Azur", "Vert Émeraude", "Rose Bonbon", "Or", "Argent", "Lavande"] + [f"Teinte {i}" for i in range(1, 20)]
LANGAGES = ["Paroles valorisantes", "Moments de qualité", "Cadeaux", "Services rendus", "Toucher physique"]
LOISIRS = ["Jeux Vidéo", "Cuisine", "Voyage", "Sport", "Dessin", "Musique"] + [f"Activité {i}" for i in range(1, 100)]
CARACTERES = ["Introverti", "Extraverti", "Calme", "Explosif", "Rêveur", "Pragmatique"] + [f"Trait {i}" for i in range(1, 100)]
VISIONS = ["Sérieux/Famille", "Libre/Aventure", "Carrière d'abord", "Vie d'artiste", "Vivre au jour le jour"]

CITATIONS = {
    "excellent": ["L'amour est une âme en deux corps.", "Deux cœurs qui s'aiment n'ont pas besoin de paroles.", "Quand on aime, on ne compte pas."],
    "moyen": ["L'amour est un jardin qui se cultive chaque jour.", "Il n'y a pas d'amour sans un peu de folie.", "On ne voit bien qu'avec le cœur."],
    "faible": ["Le cœur a ses raisons que la raison ne connaît point.", "Mieux vaut être seul que mal accompagné.", "Chaque pot a son couvercle."],
    "opposés": ["Les opposés s'attirent et se complètent.", "La diversité est le sel de l'amour.", "On se passionne par nos différences."]
}

# =====================================================
# OUTILS GRAPHIQUES
# =====================================================
def make_circle(img_path, size=(120, 120)):
    """Découpe une image en cercle parfait"""
    try:
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        
        img = Image.open(img_path).convert("RGBA")
        img = ImageOps.fit(img, size, centering=(0.5, 0.5))
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)
    except:
        return None

class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love AI")
        self.root.geometry("950x900")
        self.root.configure(bg=C_BG)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background=C_ACCENT)

        # Header
        header = tk.Frame(root, bg=C_HEADER)
        header.pack(fill="x")
        tk.Label(header, text="💖 DESTINY MATCHMAKER 💖", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=5)

        # Zone centrale
        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Création des UI
        self.data_a = self.create_player_ui(self.main_frame, "LUI", "images.jfif", "left")
        self.data_b = self.create_player_ui(self.main_frame, "ELLE", "images (1).jfif", "right")

        # Zone Résultat
        self.res_card = tk.Frame(root, bg=C_CARD, highlightbackground=C_ACCENT, highlightthickness=2, pady=7)
        self.res_card.pack(fill="x", padx=80, pady=7)
        
        self.score_lbl = tk.Label(self.res_card, text="Prêt pour l'analyse ?", font=("Comic Sans MS", 18, "bold"), bg=C_CARD, fg=C_TEXT)
        self.score_lbl.pack()
        self.msg_lbl = tk.Label(self.res_card, text="", font=FONT_BUBBLE, bg=C_CARD, fg=C_ACCENT, wraplength=600)
        self.msg_lbl.pack()

        # Bouton
        self.btn = tk.Button(root, text="VÉRIFIER LE DESTIN", font=FONT_BOLD, bg=C_ACCENT, fg="white", 
                             relief="flat", padx=30, pady=12, command=self.analyser, cursor="hand2")
        self.btn.pack(pady=(0, 20))

    def validate_name(self, P):
        if P == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", P))

    def create_player_ui(self, parent, label, img_path, side):
        container = tk.Frame(parent, bg=C_BG)
        container.pack(side=side, expand=True, fill="both", padx=20)

        # Bulle de parole stylisée
        bubble_frame = tk.Frame(container, bg=C_BG)
        bubble_frame.pack(pady=(0, 0))
        
        bubble_text = tk.Label(bubble_frame, text="Dis-moi tout...", font=FONT_BUBBLE, 
                               bg="white", fg=C_TEXT, padx=10, pady=5, 
                               highlightbackground=C_ACCENT, highlightthickness=2)
        bubble_text.pack()
        
        # Le petit triangle de la bulle (caractère unicode)
        tk.Label(bubble_frame, text="▼", font=("Arial", 12), bg=C_BG, fg=C_ACCENT).pack(pady=(0, 2))

        # IMAGE EN RONDE
        photo = make_circle(img_path, (130, 130))
        if photo:
            img_lbl = tk.Label(container, image=photo, bg=C_BG)
            img_lbl.image = photo
        else:
            img_lbl = tk.Label(container, text="[Photo]", bg=C_ACCENT, fg="white", 
                               width=12, height=6, font=FONT_BOLD)
        img_lbl.pack(pady=5)

        # Formulaire
        form = tk.LabelFrame(container, text=f" Profil {label} ", bg=C_CARD, font=FONT_BOLD, fg=C_TEXT)
        form.pack(fill="x", pady=10)

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
            tk.Label(form, text=name, bg=C_CARD, font=FONT_LABEL).pack(anchor="w", padx=10)
            if dtype == "entry":
                w = tk.Entry(form, validate="key", validatecommand=vcmd, relief="flat", highlightbackground="#DDD", highlightthickness=1)
            elif dtype == "date":
                w = DateEntry(form, date_pattern="dd/mm/yyyy", width=12)
            else:
                w = ttk.Combobox(form, values=dtype, state="readonly")
                w.current(0)
            w.pack(fill="x", padx=10, pady=2)
            inputs[name] = w
            
        inputs["bubble"] = bubble_text
        return inputs

    def analyser(self):
        nom_a = self.data_a["Nom"].get()
        nom_b = self.data_b["Nom"].get()

        if not nom_a or not nom_b:
            self.score_lbl.config(text="⚠️ Noms requis !", fg="#E74C3C")
            return

        score = 35
        opposes = self.data_a["Caractère"].get() != self.data_b["Caractère"].get()
        if opposes: score += 25
        if self.data_a["Vision"].get() == self.data_b["Vision"].get(): score += 20
        
        score = min(99, score + random.randint(0, 10))

        if score >= 85: prov = random.choice(CITATIONS["excellent"])
        elif score >= 55: prov = random.choice(CITATIONS["moyen"])
        else: prov = random.choice(CITATIONS["faible"])
            
        if opposes and score > 65: prov = random.choice(CITATIONS["opposés"])

        # Update UI
        self.score_lbl.config(text=f"COMPATIBILITÉ : {score}%", fg="#FF6B6B")
        self.msg_lbl.config(text=f"Pour {nom_a} & {nom_b} :\n« {prov} »")
        
        # Changement du texte dans les bulles
        self.data_a["bubble"].config(text=f"Score : {score}% !")
        self.data_b["bubble"].config(text="C'est magique !")

if __name__ == "__main__":
    root = tk.Tk()
    app = PocketLoveApp(root)
    root.mainloop()