import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import random

# --- CONFIGURATION DESIGN (PASTEL) ---
C_BG = "#FFF9E3"      # Crème fond
C_FRAME = "#FFFFFF"   # Blanc pur
C_ACCENT = "#FFB7CE"  # Rose pastel
C_TEXT = "#5D4037"    # Brun doux (pas de noir pur)
FONT_MAIN = ("Comic Sans MS", 10)
FONT_BOLD = ("Comic Sans MS", 12, "bold")

# --- DONNÉES ÉTENDUES ---
TRAITS_SIGNES = {
    "Bélier": "Énergique", "Taureau": "Fidèle", "Gémeaux": "Curieux",
    "Cancer": "Protecteur", "Lion": "Fier", "Vierge": "Analytique",
    "Balance": "Harmonieux", "Scorpion": "Passionné", "Sagittaire": "Aventurier",
    "Capricorne": "Ambitieux", "Verseau": "Original", "Poissons": "Empathique"
}

SIGNS = [
    ("Capricorne", (12, 22), (1, 19), "Terre"), ("Verseau", (1, 20), (2, 18), "Air"),
    ("Poissons", (2, 19), (3, 20), "Eau"), ("Bélier", (3, 21), (4, 19), "Feu"),
    ("Taureau", (4, 20), (5, 20), "Terre"), ("Gémeaux", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Eau"), ("Lion", (7, 23), (8, 22), "Feu"),
    ("Vierge", (8, 23), (9, 22), "Terre"), ("Balance", (9, 23), (10, 22), "Air"),
    ("Scorpion", (10, 23), (11, 21), "Eau"), ("Sagittaire", (11, 22), (12, 21), "Feu")
]

# --- LOGIQUE AMÉLIORÉE ---
def calcul_score_ia(p1, p2):
    score = 40 # Base neutre
    
    # 1. Écart d'âge (Supposition : trop d'écart = vision différente)
    diff_age = abs(p1['age'] - p2['age'])
    if diff_age <= 3: score += 15
    elif diff_age <= 7: score += 8
    
    # 2. Synergie des éléments
    synergies = [("Feu", "Air"), ("Terre", "Eau")]
    if p1['element'] == p2['element']: score += 12
    elif (p1['element'], p2['element']) in synergies or (p2['element'], p1['element']) in synergies:
        score += 10
        
    # 3. Supposition de tempérament (via le signe)
    trait1 = TRAITS_SIGNES.get(p1['signe'])
    trait2 = TRAITS_SIGNES.get(p2['signe'])
    # Si les deux sont "stables" (Terre/Eau)
    if p1['element'] in ["Terre", "Eau"] and p2['element'] in ["Terre", "Eau"]:
        score += 10 
        
    # 4. Loisirs et Vision
    if p1['vision'] == p2['vision']: score += 15
    communs = len(set(p1["loisirs"]) & set(p2["loisirs"]))
    score += min(communs * 6, 18)

    return min(max(score, 5), 100)

# --- INTERFACE ---
class LoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Love AI")
        self.root.geometry("600x800")
        self.root.configure(bg=C_BG)
        
        # Header stylé
        header = tk.Frame(root, bg=C_ACCENT, height=80)
        header.pack(fill="x")
        tk.Label(header, text="CHOOSE YOUR DESTINY", font=FONT_BOLD, bg=C_ACCENT, fg="white").pack(pady=20)

        self.main_frame = tk.Frame(root, bg=C_BG)
        self.main_frame.pack(pady=10, padx=20, fill="both")

        # Layout : Personne A (Homme) | Personne B
        self.p1_data = self.create_profile(self.main_frame, "L'AVATAR (Homme)", "blue")
        self.p2_data = self.create_profile(self.main_frame, "PARTENAIRE", "pink")

        # Bouton "Play" style bouton rose
        btn = tk.Button(root, text="ANALYSER LE LOOK", command=self.analyser, 
                        bg=C_ACCENT, fg="white", font=FONT_BOLD, relief="flat", 
                        padx=20, pady=10, cursor="hand2")
        btn.pack(pady=20)

    def create_profile(self, parent, titre, accent):
        frame = tk.LabelFrame(parent, text=titre, bg=C_FRAME, fg=C_TEXT, font=FONT_BOLD, padx=10, pady=10)
        frame.pack(side="left", expand=True, fill="both", padx=5)

        inputs = {}
        fields = [
            ("Nom", "entry"),
            ("Naissance", "date"),
            ("Style", ["Chic", "Street", "Kawaii", "Goth"]),
            ("Vision", ["Sérieux", "Libre", "Indécis"])
        ]

        for label, t in fields:
            tk.Label(frame, text=label, bg=C_FRAME, fg=C_TEXT, font=FONT_MAIN).pack(anchor="w")
            if t == "entry":
                w = tk.Entry(frame, relief="solid", bd=1)
            elif t == "date":
                w = DateEntry(frame, background=C_ACCENT, borderwidth=1)
            else:
                w = ttk.Combobox(frame, values=t)
            w.pack(fill="x", pady=2)
            inputs[label] = w
        
        # Mention Homme pour Personne A
        if titre == "L'AVATAR (Homme)":
            tk.Label(frame, text="♂ Masculin", fg="#4A90E2", bg=C_FRAME, font=("Arial", 8, "italic")).pack()

        return inputs

    def analyser(self):
        try:
            def get_info(d, inputs):
                birth = inputs["Naissance"].get_date()
                sign, elem = self.get_sign(birth)
                return {
                    "nom": inputs["Nom"].get(),
                    "age": (date.today() - birth).days // 365,
                    "signe": sign,
                    "element": elem,
                    "vision": inputs["Vision"].get(),
                    "loisirs": [] # Simplifié ici
                }

            a = get_info("A", self.p1_data)
            b = get_info("B", self.p2_data)
            
            res = calcul_score_ia(a, b)
            
            # Popup personnalisé
            msg = f"RÉSULTAT POUR {a['nom'].upper()}\n"
            msg += f"Signe: {a['signe']} ({TRAITS_SIGNES[a['signe']]})\n"
            msg += "--------------------------\n"
            msg += f"Compatibilité: {res}%\n\n"
            msg += "L'IA suppose que votre futur sera radieux !" if res > 70 else "Prenez votre temps..."
            
            messagebox.showinfo("Pocket Love Result", msg)
            
        except Exception as e:
            messagebox.showerror("Oups", "Vérifie les informations !")

    def get_sign(self, d):
        for s, start, end, e in SIGNS:
            if (d.month == start[0] and d.day >= start[1]) or (d.month == end[0] and d.day <= end[1]):
                return s, e
        return "Capricorne", "Terre"

if __name__ == "__main__":
    root = tk.Tk()
    app = LoveApp(root)
    root.mainloop()
