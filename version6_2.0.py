import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import random
import re
from PIL import Image, ImageTk, ImageDraw, ImageOps

# =====================================================
# CONFIGURATION DESIGN
# =====================================================
C_BG = "#FFF9E3"
C_HEADER = "#FFD1DC"
C_CARD = "#FFFFFF"
C_TEXT = "#5D4037"
C_ACCENT = "#FFB7CE"
FONT_TITLE = ("Comic Sans MS", 16, "bold")
FONT_SMALL = ("Comic Sans MS", 8)
FONT_BOLD_SM = ("Comic Sans MS", 9, "bold")
FONT_BUBBLE = ("Comic Sans MS", 9, "italic")

# Données (simplifiées pour la clarté, gardez vos listes massives ici)
COULEURS = ["Rouge", "Bleu", "Vert", "Rose", "Or"] + [f"Teinte {i}" for i in range(20)]
CARACTERES = ["Introverti", "Extraverti", "Calme", "Explosif"] + [f"Trait {i}" for i in range(100)]
VISIONS = ["Famille", "Aventure", "Carrière", "Zen"]

CITATIONS = {
    "excellent": ["L'amour est une âme en deux corps.", "Deux cœurs qui s'aiment..."],
    "opposés": ["Les opposés s'attirent et se complètent.", "La diversité est le sel de l'amour."]
}

# =====================================================
# OUTILS GRAPHIQUES
# =====================================================
def make_circle(img_path, size=(100, 100)):
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

# =====================================================
# INTERFACE
# =====================================================
class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love Destiny")
        self.root.geometry("850x800")
        self.root.configure(bg=C_BG)

        # Header réduit
        header = tk.Frame(root, bg=C_HEADER)
        header.pack(fill="x")
        tk.Label(header, text="💖 DESTINY MATCHMAKER 💖", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=5)

        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Création des colonnes
        self.data_a = self.create_player_ui(self.main_frame, "LUI", "images.jfif", "left")
        self.data_b = self.create_player_ui(self.main_frame, "ELLE", "images (1).jfif", "right")

        # Résultat
        self.res_card = tk.Frame(root, bg=C_CARD, highlightbackground=C_ACCENT, highlightthickness=2)
        self.res_card.pack(fill="x", padx=150, pady=10)
        
        self.score_lbl = tk.Label(self.res_card, text="Prêt pour le destin ?", font=FONT_BOLD_SM, bg=C_CARD)
        self.score_lbl.pack(pady=(5,0))
        self.msg_lbl = tk.Label(self.res_card, text="", font=FONT_BUBBLE, bg=C_CARD, fg=C_ACCENT, wraplength=400)
        self.msg_lbl.pack(pady=5)

        self.btn = tk.Button(root, text="VÉRIFIER LE DESTIN", font=FONT_BOLD_SM, bg=C_ACCENT, fg="white", 
                             relief="flat", padx=20, pady=8, command=self.analyser)
        self.btn.pack(pady=10)

    def create_player_ui(self, parent, label, img_path, side):
        container = tk.Frame(parent, bg=C_BG)
        container.pack(side=side, expand=True, fill="both", padx=10)

        # Zone Avatar + Bulle (Haut)
        top_zone = tk.Frame(container, bg=C_BG)
        top_zone.pack(fill="x")

        # Avatar rond
        photo = make_circle(img_path, (90, 90))
        img_lbl = tk.Label(top_zone, image=photo, bg=C_BG)
        img_lbl.image = photo
        img_lbl.pack(side="left")

        # Bulle en haut à droite de l'avatar
        bubble_canvas = tk.Canvas(top_zone, width=120, height=60, bg=C_BG, highlightthickness=0)
        bubble_canvas.pack(side="left", padx=5)
        
        # Dessin de la bulle (Rectangle arrondi simplifié + pointe)
        bubble_canvas.create_oval(5, 5, 115, 45, fill="white", outline=C_ACCENT, width=2)
        bubble_canvas.create_polygon(5, 25, 20, 20, 20, 30, fill="white", outline=C_ACCENT, width=2)
        bubble_canvas.create_line(19, 21, 19, 29, fill="white", width=3) # Cache la ligne de jonction
        
        bubble_txt = bubble_canvas.create_text(60, 25, text="Dis-moi tout...", font=FONT_BUBBLE, width=90, fill=C_TEXT)

        # Formulaire réduit
        form = tk.LabelFrame(container, text=f" Profil {label} ", bg=C_CARD, font=FONT_BOLD_SM, fg=C_ACCENT)
        form.pack(fill="x", pady=5)

        vcmd = (self.root.register(self.validate_name), '%P')
        inputs = {}
        fields = [("Nom", "entry"), ("Date", "date"), ("Couleur", COULEURS), 
                  ("Loisirs", ["Cuisine", "Voyage", "Musique"]), ("Caractère", CARACTERES), ("Vision", VISIONS)]

        for name, dtype in fields:
            f_row = tk.Frame(form, bg=C_CARD)
            f_row.pack(fill="x", pady=1)
            tk.Label(f_row, text=name, bg=C_CARD, font=FONT_SMALL, width=8, anchor="w").pack(side="left", padx=5)
            
            if dtype == "entry":
                w = tk.Entry(f_row, validate="key", validatecommand=vcmd, font=FONT_SMALL, width=15)
            elif dtype == "date":
                w = DateEntry(f_row, date_pattern="dd/mm/yyyy", width=12, font=FONT_SMALL)
            else:
                w = ttk.Combobox(f_row, values=dtype, state="readonly", font=FONT_SMALL, width=13)
                w.current(0)
            w.pack(side="right", padx=5, expand=True, fill="x")
            inputs[name] = w
            
        inputs["bubble_canvas"] = bubble_canvas
        inputs["bubble_txt"] = bubble_txt
        return inputs

    def validate_name(self, P):
        if P == "": return True
        return bool(re.match(r"^[A-Z][a-zA-Z]*$", P))

    def analyser(self):
        nom_a = self.data_a["Nom"].get()
        nom_b = self.data_b["Nom"].get()

        if not nom_a or not nom_b:
            self.score_lbl.config(text="⚠️ Noms manquants", fg="red")
            return

        score = random.randint(40, 99)
        prov = random.choice(CITATIONS["excellent"] if score > 75 else CITATIONS["opposés"])

        self.score_lbl.config(text=f"COMPATIBILITÉ : {score}%", fg="#FF6B6B")
        self.msg_lbl.config(text=f"« {prov} »")
        
        # On change le texte des bulles
        self.data_a["bubble_canvas"].itemconfig(self.data_a["bubble_txt"], text=f"Score: {score}%")
        self.data_b["bubble_canvas"].itemconfig(self.data_b["bubble_txt"], text="C'est le destin !")

if __name__ == "__main__":
    root = tk.Tk()
    app = PocketLoveApp(root)
    root.mainloop()