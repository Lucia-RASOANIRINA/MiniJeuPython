import tkinter as tk
import random
import time

# -----------------------------
# Fonction principale du jeu
# -----------------------------
def calculer_amour():
    nom = entry_nom.get()
    signe = entry_signe.get()

    if nom == "" or signe == "":
        resultat.config(text="⚠️ Entre ton nom et ton signe !", fg="red")
        return

    resultat.config(text="💓 Analyse de ton cœur en cours...", fg="purple")
    fenetre.update()
    time.sleep(1)

    # Animation simple
    for i in range(3):
        resultat.config(text="❤️ 💔 ❤️ 💔 ❤️")
        fenetre.update()
        time.sleep(0.4)
        resultat.config(text="")
        fenetre.update()
        time.sleep(0.4)

    # Probabilité d'amour
    pourcentage = random.randint(10, 100)

    # Messages drôles
    if pourcentage < 30:
        message = "😅 L’amour te fuit… mais le rire t’aime !"
    elif pourcentage < 60:
        message = "🙂 Ça sent l’amitié améliorée 😏"
    elif pourcentage < 80:
        message = "😍 Attention ! Coup de foudre imminent !"
    else:
        message = "💘💍 MARIAGE EN VUE !!! 💍💘"

    resultat.config(
        text=f"👤 {nom}\n♈ Signe : {signe}\n\n💖 Chance de tomber amoureux : {pourcentage}%\n\n{message}",
        fg="darkred"
    )

# -----------------------------
# Interface graphique
# -----------------------------
fenetre = tk.Tk()
fenetre.title("💘 Jeu de l'amour 💘")
fenetre.geometry("400x450")
fenetre.resizable(False, False)

tk.Label(fenetre, text="💖 LA MACHINE DE L'AMOUR 💖", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(fenetre, text="Entre ton nom :").pack()
entry_nom = tk.Entry(fenetre)
entry_nom.pack(pady=5)

tk.Label(fenetre, text="Entre ton signe astrologique :").pack()
entry_signe = tk.Entry(fenetre)
entry_signe.pack(pady=5)

tk.Button(
    fenetre,
    text="Tester l'amour ❤️",
    command=calculer_amour,
    bg="pink",
    font=("Arial", 12, "bold")
).pack(pady=15)

resultat = tk.Label(fenetre, text="", font=("Arial", 11), wraplength=350, justify="center")
resultat.pack(pady=20)

fenetre.mainloop()
