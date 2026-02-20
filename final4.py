import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import random
import re
from datetime import date
from PIL import Image, ImageTk, ImageDraw, ImageOps

# =====================================================
# CONFIGURATION DU DESIGN
# =====================================================
C_BG = "#FFF9E3"
C_HEADER = "#FFD1DC"
C_CARD = "#FFFFFF"
C_TEXT = "#000000"  
C_ACCENT = "#FFB7CE"
C_BORDER = "#FFDAE5"

FONT_TITLE = ("Comic Sans MS", 16, "bold")
FONT_LABEL = ("Comic Sans MS", 8, "bold")
FONT_INPUT = ("Comic Sans MS", 8)
FONT_BUBBLE = ("Comic Sans MS", 8, "italic")

# =====================================================
# DONNÉES RÉELLES
# =====================================================
COULEURS = [
    "Rouge Passion", "Bleu Azur", "Vert Émeraude", "Rose Bonbon", "Jaune Citron", 
    "Violet Royal", "Orange Corail", "Noir Intense", "Blanc Pur", "Or Brillant", 
    "Argent Satin", "Lavande", "Turquoise", "Marron Chocolat", "Beige Sable", 
    "Bordeaux", "Vert Menthe", "Bleu Marine", "Rose Poudré", "Gris Perle",
    "Indigo", "Magenta", "Ocre", "Cyan", "Ambre", "Terracotta", "Vert Sapin"
]

LOISIRS = [
    "Cuisine Gourmande", "Jeux Vidéo", "Voyage", "Lecture", "Musculation", 
    "Dessin", "Piano", "Guitare", "Cinéma", "Jardinage", "Photographie", 
    "Danse", "Randonnée", "Yoga", "Échecs", "Écriture", "Pêche", "Shopping", 
    "Séries TV", "Théâtre", "Poterie", "Escalade", "Surf", "Natation",
    "Astronomie", "Skateboard", "Chant", "Couture", "Modélisme", "Bénévolat"
]

CARACTERES = [
    "Introverti", "Extraverti", "Calme", "Énergique", "Rêveur", "Pragmatique",
    "Optimiste", "Pessimiste", "Ambitieux", "Altruiste", "Timide", "Audacieux",
    "Organisé", "Désordonné", "Patient", "Impulsif", "Sérieux", "Farceur",
    "Mystérieux", "Sincère", "Sensible", "Protecteur", "Indépendant", "Loyal"
]

LANGAGES = ["Paroles valorisantes", "Moments de qualité", "Cadeaux", "Services rendus", "Toucher physique"]

VISIONS = [
    "Fonder une famille", "Voyager sans cesse", "Réussir sa carrière", 
    "Vivre de son art", "Vivre au jour le jour", "Engagement spirituel",
    "Vie tranquille à la campagne", "Vivre en ville (Luxe)"
]

# +50 PROVERBES ET CITATIONS
CITATIONS_DB = {
    "excellent": [
        "L'amour est une âme en deux corps.", "Le vrai bonheur est dans le partage.", 
        "Deux cœurs qui s'aiment n'ont pas besoin de paroles.", "Quand on aime, on ne compte pas.",
        "Aimer, c'est savoir dire je t'aime sans parler.", "L'amour est la poésie des sens.",
        "Le cœur a ses propres yeux pour voir l'invisible.", "Toi et moi, c'est écrit dans les étoiles.",
        "La vie est une fleur, l'amour en est le miel.", "Aimer, ce n'est pas se regarder, c'est regarder ensemble.",
        "Le plus grand bonheur est d'aimer et d'être aimé.", "Rien n'est petit dans l'amour.",
        "L'amour ne se voit pas avec les yeux, mais avec l'âme.", "Où il y a de l'amour, il y a de la vie."
    ],
    "moyen": [
        "L'amour est un jardin qui se cultive chaque jour.", "Il n'y a pas d'amour sans un peu de folie.",
        "Petit à petit, l'oiseau fait son nid.", "Le temps renforce ce que l'amour a créé.",
        "Un seul être vous manque et tout est dépeuplé.", "La patience est la clé d'un cœur heureux.",
        "L'amitié est souvent l'antichambre de l'amour.", "S'aimer, c'est apprendre à se découvrir.",
        "Le sourire est le chemin le plus court entre deux cœurs.", "L'amour demande du temps.",
        "Chaque rencontre est un nouveau chemin.", "Mieux vaut tard que jamais pour s'aimer.",
        "L'amour commence par une étincelle.", "Apprendre à s'écouter est le début de l'amour."
    ],
    "faible": [
        "Mieux vaut être seul que mal accompagné.", "Le cœur a ses raisons que la raison ne connaît point.",
        "Chaque pot a son couvercle, il faut juste chercher.", "L'amour ne se force jamais.",
        "Il faut apprendre à s'aimer soi-même d'abord.", "Le destin n'est pas toujours celui qu'on croit.",
        "Le temps guérit toutes les blessures.", "Une déception est un pas vers la vérité.",
        "Ne cours pas après l'amour, il viendra à toi.", "Le calme après la tempête.",
        "Parfois, l'amitié suffit amplement.", "La vie réserve toujours des surprises.",
        "Le plus grand voyage commence par un pas.", "Rien n'arrive par hasard."
    ],
    "opposés": [
        "Les opposés s'attirent et se complètent parfaitement.", "La diversité est le sel de l'amour.",
        "On se passionne par nos différences.", "L'harmonie naît de la différence.",
        "Deux mondes différents pour une seule histoire.", "Le feu et la glace font parfois bon ménage.",
        "Tes manques sont mes forces.", "La différence est une richesse.",
        "On s'aime par nos ressemblances, on se passionne par nos différences."
    ]
}

# =====================================================
# FONCTIONS LOGIQUES
# =====================================================
def get_zodiac_sign(birth_date):
    day = birth_date.day
    month = birth_date.month
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Bélier"
    if (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taureau"
    if (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gémeaux"
    if (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Lion"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Vierge"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Balance"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpion"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittaire"
    if (month == 12 and day >= 22) or (month == 1 and day <= 19): return "Capricorne"
    if (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Verseau"
    return "Poissons"

def make_circle(img_path, size=(85, 85)):
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
# APPLICATION
# =====================================================
class PocketLoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love Destiny")
        self.root.geometry("850x650") # Légèrement agrandi pour le confort
        self.root.configure(bg=C_BG)

        header = tk.Frame(root, bg=C_HEADER)
        header.pack(fill="x")
        tk.Label(header, text="❤ DESTINY MATCHMAKER ❤", font=FONT_TITLE, bg=C_HEADER, fg="white").pack(pady=5)

        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(fill="both", padx=10, pady=5)

        self.data_a = self.create_player_ui(self.main_frame, "LUI", "images.jfif", "left")
        self.data_b = self.create_player_ui(self.main_frame, "ELLE", "images (1).jfif", "right")

        self.res_card = tk.Frame(root, bg=C_CARD, highlightbackground=C_ACCENT, highlightthickness=2)
        self.res_card.pack(fill="x", padx=150, pady=5)
        
        self.score_lbl = tk.Label(self.res_card, text="Résultat", font=FONT_TITLE, bg=C_CARD, fg=C_TEXT)
        self.score_lbl.pack(pady=2)
        self.msg_lbl = tk.Label(self.res_card, text="Entrez vos prénoms...", font=FONT_BUBBLE, bg=C_CARD, fg=C_TEXT, wraplength=450)
        self.msg_lbl.pack(pady=5)

        self.btn = tk.Button(root, text="VÉRIFIER LE DESTIN", font=FONT_TITLE, bg=C_ACCENT, fg="white", relief="flat", command=self.analyser, cursor="hand2")
        self.btn.pack(pady=10, ipadx=20)

    def create_player_ui(self, parent, label, img_path, side):
        container = tk.Frame(parent, bg=C_BG)
        container.pack(side=side, expand=True, fill="both", padx=10)

        top_zone = tk.Frame(container, bg=C_BG)
        top_zone.pack(fill="x")

        photo = make_circle(img_path)
        img_lbl = tk.Label(top_zone, image=photo, bg=C_BG)
        img_lbl.image = photo
        img_lbl.pack(side="left")

        canvas = tk.Canvas(top_zone, width=120, height=60, bg=C_BG, highlightthickness=0)
        canvas.pack(side="left")
        canvas.create_oval(10, 5, 115, 45, fill="white", outline=C_ACCENT, width=2)
        canvas.create_polygon(0, 25, 12, 18, 12, 32, fill="white", outline=C_ACCENT, width=2)
        canvas.create_line(11, 19, 11, 31, fill="white", width=3)
        b_txt = canvas.create_text(65, 25, text="Dis-moi...", font=FONT_BUBBLE, width=80, fill=C_TEXT)

        form = tk.LabelFrame(container, text=f" Profil {label} ", bg=C_CARD, font=FONT_LABEL, fg=C_ACCENT)
        form.pack(fill="x", pady=2)

        inputs = {}
        fields = [("Nom", "entry"), ("Naissance", "date"), ("Couleur", COULEURS), ("Langage", LANGAGES), ("Loisirs", LOISIRS), ("Caractère", CARACTERES), ("Vision", VISIONS)]

        for name, dtype in fields:
            f_row = tk.Frame(form, bg=C_CARD)
            f_row.pack(fill="x", pady=1)
            tk.Label(f_row, text=name, bg=C_CARD, font=FONT_LABEL, width=9, anchor="w", fg=C_TEXT).pack(side="left", padx=5)
            if dtype == "entry":
                w = tk.Entry(f_row, font=FONT_INPUT, relief="flat", highlightbackground="#EEE", highlightthickness=1, fg=C_TEXT)
            elif dtype == "date":
                w = DateEntry(f_row, font=FONT_INPUT, date_pattern="dd/mm/yyyy")
            else:
                w = ttk.Combobox(f_row, values=dtype, state="readonly", font=FONT_INPUT)
                w.current(0)
            w.pack(side="right", padx=5, expand=True, fill="x")
            inputs[name] = w
            
        inputs["canvas"] = canvas
        inputs["b_txt"] = b_txt
        return inputs

    def analyser(self):
        today = date.today()
        try:
            # Correction automatique de la majuscule
            nom_a = self.data_a["Nom"].get().strip().capitalize()
            nom_b = self.data_b["Nom"].get().strip().capitalize()
            
            # Mise à jour visuelle des champs avec la majuscule
            self.data_a["Nom"].delete(0, tk.END)
            self.data_a["Nom"].insert(0, nom_a)
            self.data_b["Nom"].delete(0, tk.END)
            self.data_b["Nom"].insert(0, nom_b)

            if not nom_a or not nom_b:
                messagebox.showwarning("Prénoms !", "Veuillez entrer les prénoms.")
                return
            
            bday_a = self.data_a["Naissance"].get_date()
            bday_b = self.data_b["Naissance"].get_date()

            # Calcul âge et signes
            age_a = today.year - bday_a.year - ((today.month, today.day) < (bday_a.month, bday_a.day))
            age_b = today.year - bday_b.year - ((today.month, today.day) < (bday_b.month, bday_b.day))
            
            sign_a = get_zodiac_sign(bday_a)
            sign_b = get_zodiac_sign(bday_b)

            if age_a < 15 or age_b < 15:
                self.score_lbl.config(text="Refusé", fg="#E74C3C")
                self.msg_lbl.config(text="Désolé, revenez quand vous aurez 15 ans !")
                return

            # Calcul du score
            score = random.randint(45, 98)
            pool = CITATIONS_DB["excellent"] if score > 80 else CITATIONS_DB["moyen"] if score > 55 else CITATIONS_DB["faible"]
            
            citation = random.choice(pool)
            self.score_lbl.config(text=f"Score : {score}%", fg=C_ACCENT)
            
            # Affichage avec Signes Astrologiques entre parenthèses
            self.msg_lbl.config(text=f"Pour {nom_a} ({sign_a}) & {nom_b} ({sign_b}) :\n« {citation} »")
            
            self.data_a["canvas"].itemconfig(self.data_a["b_txt"], text=f"{sign_a} ✨")
            self.data_b["canvas"].itemconfig(self.data_b["b_txt"], text=f"{sign_b} 💖")

        except Exception as e:
            messagebox.showerror("Erreur", "Vérifiez vos données.")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="white", background=C_ACCENT, foreground="black")
    app = PocketLoveApp(root)
    root.mainloop()