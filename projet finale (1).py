import tkinter as tk
from tkinter import messagebox
import random
import math
import winsound
import threading

class Jeton:
    '''
    Classe représentant un jeton du jeu
    '''
    def __init__(self, joueur, face_claire=True):
        '''
        Initialise un jeton
        Préconditions:
            joueur: "joueur1" ou "joueur2"
            face_claire: booléen indiquant si la face claire est visible
        Postconditions:
            Crée un objet Jeton avec les attributs joueur et face_claire
        '''
        self.joueur = joueur
        self.face_claire = face_claire

    def retourner(self):
        '''
        Retourne le jeton (change la face visible)
        Préconditions: aucune
        Postconditions: inverse la valeur de face_claire
        '''
        self.face_claire = not self.face_claire


class Plateau:
    '''
    Classe représentant le plateau de jeu 4x4
    '''
    def __init__(self):
        '''
        Initialise un plateau vide
        Préconditions: aucune
        Postconditions: crée une grille 4x4 vide
        '''
        self.grille = [[None for _ in range(4)] for _ in range(4)]

    def placer_jeton(self, ligne, colonne, jeton):
        '''
        Place un jeton sur le plateau
        Préconditions:
            ligne: entier entre 0 et 3
            colonne: entier entre 0 et 3
            jeton: objet Jeton
        Postconditions: place le jeton à la position donnée
        '''
        self.grille[ligne][colonne] = jeton

    def retirer_jeton(self, ligne, colonne):
        '''
        Retire un jeton du plateau
        Préconditions:
            ligne: entier entre 0 et 3
            colonne: entier entre 0 et 3
        Postconditions: met None à la position donnée et renvoie le jeton retiré
        '''
        jeton = self.grille[ligne][colonne]
        self.grille[ligne][colonne] = None
        return jeton

    def est_vide(self, ligne, colonne):
        '''
        Vérifie si une case est vide
        Préconditions:
            ligne: entier entre 0 et 3
            colonne: entier entre 0 et 3
        Postconditions: renvoie True si la case est vide, False sinon
        '''
        return self.grille[ligne][colonne] is None

    def est_contigu(self, ligne1, col1, ligne2, col2):
        '''
        Vérifie si deux cases sont contiguës
        Préconditions:
            ligne1, col1, ligne2, col2: entiers entre 0 et 3
        Postconditions: renvoie True si les cases sont adjacentes, False sinon
        '''
        diff_ligne = abs(ligne1 - ligne2)
        diff_col = abs(col1 - col2)
        return (diff_ligne == 1 and diff_col == 0) or (diff_ligne == 0 and diff_col == 1)

    def verifier_alignement(self, joueur):
        '''
        Vérifie si un joueur a trois jetons alignés avec la même face
        Préconditions:
            joueur: "joueur1" ou "joueur2"
        Postconditions: renvoie True si le joueur a gagné, False sinon
        '''
        # Vérification horizontale
        for ligne in range(4):
            for col in range(2):
                if (self.grille[ligne][col] and
                    self.grille[ligne][col+1] and
                    self.grille[ligne][col+2]):
                    if (self.grille[ligne][col].joueur == joueur and
                        self.grille[ligne][col+1].joueur == joueur and
                        self.grille[ligne][col+2].joueur == joueur and
                        self.grille[ligne][col].face_claire == self.grille[ligne][col+1].face_claire and
                        self.grille[ligne][col+1].face_claire == self.grille[ligne][col+2].face_claire):
                        return True

        # Vérification verticale
        for col in range(4):
            for ligne in range(2):
                if (self.grille[ligne][col] and
                    self.grille[ligne+1][col] and
                    self.grille[ligne+2][col]):
                    if (self.grille[ligne][col].joueur == joueur and
                        self.grille[ligne+1][col].joueur == joueur and
                        self.grille[ligne+2][col].joueur == joueur and
                        self.grille[ligne][col].face_claire == self.grille[ligne+1][col].face_claire and
                        self.grille[ligne+1][col].face_claire == self.grille[ligne+2][col].face_claire):
                        return True

        # Vérification diagonale
        for ligne in range(2):
            for col in range(2):
                if (self.grille[ligne][col] and
                    self.grille[ligne+1][col+1] and
                    self.grille[ligne+2][col+2]):
                    if (self.grille[ligne][col].joueur == joueur and
                        self.grille[ligne+1][col+1].joueur == joueur and
                        self.grille[ligne+2][col+2].joueur == joueur and
                        self.grille[ligne][col].face_claire == self.grille[ligne+1][col+1].face_claire and
                        self.grille[ligne+1][col+1].face_claire == self.grille[ligne+2][col+2].face_claire):
                        return True

        for ligne in range(2, 4):
            for col in range(2):
                if (self.grille[ligne][col] and
                    self.grille[ligne-1][col+1] and
                    self.grille[ligne-2][col+2]):
                    if (self.grille[ligne][col].joueur == joueur and
                        self.grille[ligne-1][col+1].joueur == joueur and
                        self.grille[ligne-2][col+2].joueur == joueur and
                        self.grille[ligne][col].face_claire == self.grille[ligne-1][col+1].face_claire and
                        self.grille[ligne-1][col+1].face_claire == self.grille[ligne-2][col+2].face_claire):
                        return True

        return False

    def copier(self):
        '''
        Crée une copie du plateau
        Préconditions: aucune
        Postconditions: renvoie une copie du plateau
        '''
        nouveau = Plateau()
        for i in range(4):
            for j in range(4):
                if self.grille[i][j]:
                    nouveau.grille[i][j] = Jeton(
                        self.grille[i][j].joueur,
                        self.grille[i][j].face_claire
                    )
        return nouveau


class IA:
    '''
    Classe pour l'intelligence artificielle
    '''
    @staticmethod
    def jouer_facile(plateau, joueur):
        '''
        IA facile - joue aléatoirement
        Préconditions:
            plateau: objet Plateau
            joueur: "joueur1" ou "joueur2"
        Postconditions: renvoie (action, params) pour un coup valide
        '''
        adversaire = "joueur1" if joueur == "joueur2" else "joueur2"

        # Trouver les jetons adverses
        jetons_adv = []
        for i in range(4):
            for j in range(4):
                if plateau.grille[i][j] and plateau.grille[i][j].joueur == adversaire:
                    jetons_adv.append((i, j))

        # Choisir un jeton à retourner
        if jetons_adv:
            ligne_src, col_src = random.choice(jetons_adv)

            # Trouver cases contiguës vides
            cases_contigues = []
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = ligne_src + di, col_src + dj
                if 0 <= ni < 4 and 0 <= nj < 4 and plateau.est_vide(ni, nj):
                    cases_contigues.append((ni, nj))

            if cases_contigues:
                ligne_dest, col_dest = random.choice(cases_contigues)
            else:
                ligne_dest, col_dest = ligne_src, col_src
        else:
            ligne_src = col_src = ligne_dest = col_dest = 0

        # Trouver une case vide pour placer
        cases_vides = []
        for i in range(4):
            for j in range(4):
                if plateau.est_vide(i, j) and (i, j) != (ligne_dest, col_dest):
                    cases_vides.append((i, j))

        if cases_vides:
            ligne_place, col_place = random.choice(cases_vides)
        else:
            ligne_place, col_place = 0, 0

        face = random.choice([True, False])

        return {
            'retourner': (ligne_src, col_src, ligne_dest, col_dest),
            'placer': (ligne_place, col_place, face)
        }

    @staticmethod
    def jouer_difficile(plateau, joueur, jetons_restants):
        '''
        IA difficile - stratégie avancée
        Préconditions:
            plateau: objet Plateau
            joueur: "joueur1" ou "joueur2"
            jetons_restants: nombre de jetons restants
        Postconditions: renvoie (action, params) pour un coup optimal
        '''
        adversaire = "joueur1" if joueur == "joueur2" else "joueur2"

        # Trouver jetons adverses
        jetons_adv = []
        for i in range(4):
            for j in range(4):
                if plateau.grille[i][j] and plateau.grille[i][j].joueur == adversaire:
                    jetons_adv.append((i, j))

        meilleur_coup = None
        meilleur_score = -999999

        # Évaluer tous les coups possibles
        for ligne_src, col_src in jetons_adv:
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = ligne_src + di, col_src + dj
                if 0 <= ni < 4 and 0 <= nj < 4 and plateau.est_vide(ni, nj):
                    for ligne_place in range(4):
                        for col_place in range(4):
                            if plateau.est_vide(ligne_place, col_place) and (ligne_place, col_place) != (ni, nj):
                                for face in [True, False]:
                                    # Simuler le coup
                                    test_plateau = plateau.copier()
                                    jeton = test_plateau.retirer_jeton(ligne_src, col_src)
                                    if jeton:
                                        jeton.retourner()
                                        test_plateau.placer_jeton(ni, nj, jeton)
                                        test_plateau.placer_jeton(ligne_place, col_place, Jeton(joueur, face))

                                        # Évaluer la position
                                        score = IA.evaluer_plateau(test_plateau, joueur)

                                        if score > meilleur_score:
                                            meilleur_score = score
                                            meilleur_coup = {
                                                'retourner': (ligne_src, col_src, ni, nj),
                                                'placer': (ligne_place, col_place, face)
                                            }

        if meilleur_coup:
            return meilleur_coup
        else:
            return IA.jouer_facile(plateau, joueur)

    @staticmethod
    def evaluer_plateau(plateau, joueur):
        '''
        Évalue la qualité d'une position
        Préconditions:
            plateau: objet Plateau
            joueur: "joueur1" ou "joueur2"
        Postconditions: renvoie un score (plus élevé = meilleur)
        '''
        score = 0
        adversaire = "joueur1" if joueur == "joueur2" else "joueur2"

        # Vérifier si victoire
        if plateau.verifier_alignement(joueur):
            return 10000
        if plateau.verifier_alignement(adversaire):
            return -10000

        # Compter les alignements partiels
        for i in range(4):
            for j in range(2):
                # Horizontal
                seq_joueur = 0
                seq_adv = 0
                meme_face_j = True
                meme_face_a = True
                face_ref_j = None
                face_ref_a = None

                for k in range(3):
                    if plateau.grille[i][j+k]:
                        if plateau.grille[i][j+k].joueur == joueur:
                            seq_joueur += 1
                            if face_ref_j is None:
                                face_ref_j = plateau.grille[i][j+k].face_claire
                            elif face_ref_j != plateau.grille[i][j+k].face_claire:
                                meme_face_j = False
                        elif plateau.grille[i][j+k].joueur == adversaire:
                            seq_adv += 1
                            if face_ref_a is None:
                                face_ref_a = plateau.grille[i][j+k].face_claire
                            elif face_ref_a != plateau.grille[i][j+k].face_claire:
                                meme_face_a = False

                if seq_joueur == 2 and meme_face_j:
                    score += 50
                if seq_adv == 2 and meme_face_a:
                    score -= 50

        return score


class JeuMorpionReversi:
    '''
    Classe principale du jeu
    '''
    def __init__(self, fenetre):
        '''
        Initialise le jeu
        Préconditions:
            fenetre: objet Tk
        Postconditions: crée l'interface graphique
        '''
        self.fenetre = fenetre
        self.fenetre.title("🌌 MORPION DOUBLE REVERSI 🌌")
        self.fenetre.geometry("600x650")
        self.fenetre.configure(bg="#0a0520")

        # Énigmes disponibles
        self.enigmes = [
            {"question": "x = 5\nx = x + 3\nValeur de x ?", "reponse": "8"},
            {"question": "a = 10\na = a - 4\nValeur de a ?", "reponse": "6"},
            {"question": "b = 7\nb = b * 2\nValeur de b ?", "reponse": "14"},
            {"question": "c = 20\nc = c // 3\nValeur de c ?", "reponse": "6"},
            {"question": "d = 15\nd = d % 4\nValeur de d ?", "reponse": "3"},
            {"question": "e = 3\ne = e ** 2\nValeur de e ?", "reponse": "9"},
        ]
        self.enigme_actuelle = random.choice(self.enigmes)

        # Variables
        self.plateau = None
        self.joueur1_nom = ""
        self.joueur2_nom = ""
        self.joueur_actuel = "joueur1"
        self.jetons_restants = {"joueur1": 8, "joueur2": 8}
        self.premier_coup = True
        self.phase_action = "placer"
        self.jeton_selectionne = None
        self.face_choisie = True
        self.mode_ia = None
        self.niveau_ia = None
        self.partie_en_cours = False

        # Message d'erreur intégré
        self.message_erreur = ""
        self.message_timer = None

        # Étoiles pour le fond
        self.etoiles = []
        for _ in range(100):
            self.etoiles.append({
                'x': random.randint(0, 600),
                'y': random.randint(0, 650),
                'taille': random.randint(1, 3),
            })

        self.creer_ecran_connexion()

    def jouer_son(self):
        '''
        Joue un son lors du placement d'un jeton
        Préconditions: aucune
        Postconditions: joue un bip sonore
        '''
        def beep():
            try:
                # Fréquence aléatoire pour varier les sons
                freq = random.choice([800, 1000, 1200])
                winsound.Beep(freq, 100)
            except:
                pass

        # Lancer dans un thread pour ne pas bloquer
        threading.Thread(target=beep, daemon=True).start()

    def afficher_message(self, texte, couleur="#ff6b6b"):
        '''
        Affiche un message d'erreur temporaire
        Préconditions:
            texte: message à afficher
            couleur: couleur du message
        Postconditions: affiche le message pendant 3 secondes
        '''
        self.message_erreur = texte
        self.message_couleur = couleur

        if hasattr(self, 'label_message'):
            self.label_message.config(text=texte, fg=couleur)

        # Effacer après 3 secondes
        if self.message_timer:
            self.fenetre.after_cancel(self.message_timer)

        self.message_timer = self.fenetre.after(3000, self.effacer_message)

    def effacer_message(self):
        '''
        Efface le message d'erreur
        Préconditions: aucune
        Postconditions: efface le message
        '''
        self.message_erreur = ""
        if hasattr(self, 'label_message'):
            self.label_message.config(text="")

    def creer_ecran_connexion(self):
        '''
        Crée l'écran de connexion avec énigme
        Préconditions: aucune
        Postconditions: affiche l'écran de connexion
        '''
        self.frame_connexion = tk.Frame(self.fenetre, bg="#0a0520")
        self.frame_connexion.pack(expand=True, fill=tk.BOTH)

        # Canvas pour le fond spatial
        self.canvas_fond = tk.Canvas(
            self.frame_connexion,
            width=600,
            height=650,
            bg="#0a0520",
            highlightthickness=0
        )
        self.canvas_fond.place(x=0, y=0)

        # Dessiner les étoiles
        for etoile in self.etoiles:
            self.canvas_fond.create_oval(
                etoile['x'], etoile['y'],
                etoile['x'] + etoile['taille'], etoile['y'] + etoile['taille'],
                fill="white", outline=""
            )

        # Titre
        titre = tk.Label(
            self.frame_connexion,
            text="🌌 MORPION GALACTIQUE 🌌",
            font=("Courier", 26, "bold"),
            fg="#00ffff",
            bg="#0a0520"
        )
        titre.place(x=300, y=40, anchor="center")

        # Règles du jeu
        regles_frame = tk.Frame(self.frame_connexion, bg="#1a1f3a", bd=3, relief=tk.RIDGE)
        regles_frame.place(x=300, y=120, anchor="center")

        tk.Label(
            regles_frame,
            text="📜 RÈGLES DU JEU 📜",
            font=("Courier", 12, "bold"),
            fg="#ffff00",
            bg="#1a1f3a"
        ).pack(pady=5)

        regles_texte = """🎯 BUT: Aligner 3 jetons de MÊME FACE
(horizontalement, verticalement ou diagonalement)

🎮 DÉROULEMENT:
1️⃣ Premier coup: Placez 1 jeton
2️⃣ Tours suivants (2 actions):
   • Retournez un jeton adverse vers case vide adjacente
   • Placez un de vos jetons (face claire ☀️ ou sombre 🌙)

⚠️ ATTENTION: En retournant un jeton adverse,
vous pouvez créer son alignement gagnant!"""

        tk.Label(
            regles_frame,
            text=regles_texte,
            font=("Courier", 9),
            fg="#ffffff",
            bg="#1a1f3a",
            justify=tk.LEFT
        ).pack(pady=5, padx=10)

        # Énigme
        enigme_frame = tk.Frame(self.frame_connexion, bg="#1a1f3a", bd=3, relief=tk.RIDGE)
        enigme_frame.place(x=300, y=330, anchor="center")

        tk.Label(
            enigme_frame,
            text="🔐 ÉNIGME PYTHON 🔐",
            font=("Courier", 14, "bold"),
            fg="#ffff00",
            bg="#1a1f3a"
        ).pack(pady=5)

        tk.Label(
            enigme_frame,
            text=self.enigme_actuelle["question"],
            font=("Courier", 11),
            fg="#ffffff",
            bg="#1a1f3a",
            justify=tk.LEFT
        ).pack(pady=10, padx=20)

        self.entry_enigme = tk.Entry(
            enigme_frame,
            font=("Courier", 14),
            bg="#0a0520",
            fg="#00ff00",
            insertbackground="#00ff00",
            width=15,
            justify="center"
        )
        self.entry_enigme.pack(pady=10)
        self.entry_enigme.bind("<Return>", lambda e: self.verifier_enigme())

        tk.Button(
            enigme_frame,
            text="🚀 VALIDER",
            font=("Courier", 12, "bold"),
            bg="#00ffff",
            fg="#0a0520",
            activebackground="#00cccc",
            command=self.verifier_enigme,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=5
        ).pack(pady=10)

        # Message d'erreur
        self.label_msg_enigme = tk.Label(
            self.frame_connexion,
            text="",
            font=("Courier", 10, "bold"),
            fg="#ff6b6b",
            bg="#0a0520"
        )
        self.label_msg_enigme.place(x=300, y=430, anchor="center")

        # Noms des joueurs
        noms_frame = tk.Frame(self.frame_connexion, bg="#0a0520")
        noms_frame.place(x=300, y=500, anchor="center")

        tk.Label(
            noms_frame,
            text="👤 Joueur 1:",
            font=("Courier", 12, "bold"),
            fg="#ffcc00",
            bg="#0a0520"
        ).grid(row=0, column=0, pady=5, padx=5)

        self.entry_j1 = tk.Entry(
            noms_frame,
            font=("Courier", 12),
            bg="#1a1f3a",
            fg="#ffffff",
            insertbackground="#00ff00",
            width=15,
            state=tk.DISABLED
        )
        self.entry_j1.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(
            noms_frame,
            text="🤖 Mode:",
            font=("Courier", 12, "bold"),
            fg="#ff6b6b",
            bg="#0a0520"
        ).grid(row=1, column=0, pady=5, padx=5)

        self.mode_var = tk.StringVar(value="2joueurs")

        mode_frame = tk.Frame(noms_frame, bg="#0a0520")
        mode_frame.grid(row=1, column=1, pady=5, padx=5)

        self.radio_2j = tk.Radiobutton(
            mode_frame,
            text="2 Joueurs",
            variable=self.mode_var,
            value="2joueurs",
            font=("Courier", 10),
            fg="#ffffff",
            bg="#0a0520",
            selectcolor="#1a1f3a",
            activebackground="#0a0520",
            activeforeground="#00ffff",
            command=self.changer_mode,
            state=tk.DISABLED
        )
        self.radio_2j.pack(side=tk.LEFT)

        self.radio_ia = tk.Radiobutton(
            mode_frame,
            text="vs IA",
            variable=self.mode_var,
            value="ia",
            font=("Courier", 10),
            fg="#ffffff",
            bg="#0a0520",
            selectcolor="#1a1f3a",
            activebackground="#0a0520",
            activeforeground="#00ffff",
            command=self.changer_mode,
            state=tk.DISABLED
        )
        self.radio_ia.pack(side=tk.LEFT)

        self.label_j2 = tk.Label(
            noms_frame,
            text="👤 Joueur 2:",
            font=("Courier", 12, "bold"),
            fg="#ff6b6b",
            bg="#0a0520"
        )
        self.label_j2.grid(row=2, column=0, pady=5, padx=5)

        self.entry_j2 = tk.Entry(
            noms_frame,
            font=("Courier", 12),
            bg="#1a1f3a",
            fg="#ffffff",
            insertbackground="#00ff00",
            width=15,
            state=tk.DISABLED
        )
        self.entry_j2.grid(row=2, column=1, pady=5, padx=5)

        self.niveau_frame = tk.Frame(noms_frame, bg="#0a0520")

        self.btn_commencer_partie = tk.Button(
            self.frame_connexion,
            text="🎮 COMMENCER LA PARTIE",
            font=("Courier", 14, "bold"),
            bg="#00ff00",
            fg="#0a0520",
            activebackground="#00cc00",
            state=tk.DISABLED,
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.lancer_jeu
        )
        self.btn_commencer_partie.place(x=300, y=600, anchor="center")

        self.entry_enigme.focus()

    def changer_mode(self):
        '''
        Change le mode de jeu (2 joueurs ou vs IA)
        Préconditions: aucune
        Postconditions: affiche/cache les options appropriées
        '''
        if self.mode_var.get() == "ia":
            self.label_j2.grid_forget()
            self.entry_j2.grid_forget()

            self.niveau_frame.grid(row=2, column=0, columnspan=2, pady=10)

            for widget in self.niveau_frame.winfo_children():
                widget.destroy()

            tk.Label(
                self.niveau_frame,
                text="Niveau IA:",
                font=("Courier", 11, "bold"),
                fg="#ffffff",
                bg="#0a0520"
            ).pack()

            self.niveau_var = tk.StringVar(value="facile")

            tk.Radiobutton(
                self.niveau_frame,
                text="😊 Facile",
                variable=self.niveau_var,
                value="facile",
                font=("Courier", 10),
                fg="#00ff00",
                bg="#0a0520",
                selectcolor="#1a1f3a",
                activebackground="#0a0520"
            ).pack()

            tk.Radiobutton(
                self.niveau_frame,
                text="💀 Extrêmement Dur",
                variable=self.niveau_var,
                value="difficile",
                font=("Courier", 10),
                fg="#ff0000",
                bg="#0a0520",
                selectcolor="#1a1f3a",
                activebackground="#0a0520"
            ).pack()
        else:
            self.niveau_frame.grid_forget()
            self.label_j2.grid(row=2, column=0, pady=5, padx=5)
            self.entry_j2.grid(row=2, column=1, pady=5, padx=5)

    def verifier_enigme(self):
        '''
        Vérifie la réponse à l'énigme
        Préconditions: aucune
        Postconditions: active le bouton si la réponse est correcte
        '''
        reponse = self.entry_enigme.get().strip()

        if reponse == self.enigme_actuelle["reponse"]:
            self.entry_enigme.configure(bg="#004400", fg="#00ff00", state=tk.DISABLED)
            self.btn_commencer_partie.config(state=tk.NORMAL)
            self.entry_j1.config(state=tk.NORMAL)
            self.entry_j2.config(state=tk.NORMAL)
            self.radio_2j.config(state=tk.NORMAL)
            self.radio_ia.config(state=tk.NORMAL)
            self.label_msg_enigme.config(text="✅ Bravo! Entrez les noms des joueurs", fg="#00ff00")
        else:
            self.entry_enigme.delete(0, tk.END)
            self.entry_enigme.configure(bg="#440000")
            self.label_msg_enigme.config(text="❌ Mauvaise réponse! Réessayez", fg="#ff6b6b")
            self.fenetre.after(300, lambda: self.entry_enigme.configure(bg="#0a0520"))

    def lancer_jeu(self):
        '''
        Lance le jeu après validation
        Préconditions: énigme résolue
        Postconditions: démarre la partie
        '''
        j1 = self.entry_j1.get().strip()

        if not j1:
            self.label_msg_enigme.config(text="⚠️ Entrez au moins le nom du Joueur 1!", fg="#ff6b6b")
            return

        self.joueur1_nom = j1

        if self.mode_var.get() == "ia":
            self.joueur2_nom = "🤖 IA"
            self.mode_ia = True
            self.niveau_ia = self.niveau_var.get()
        else:
            j2 = self.entry_j2.get().strip()
            if not j2:
                self.label_msg_enigme.config(text="⚠️ Entrez le nom du Joueur 2!", fg="#ff6b6b")
                return
            self.joueur2_nom = j2
            self.mode_ia = False

        self.frame_connexion.destroy()
        self.creer_interface_jeu()
        self.commencer_partie()

    def creer_interface_jeu(self):
        '''
        Crée l'interface de jeu
        Préconditions: aucune
        Postconditions: affiche l'interface de jeu
        '''
        main_frame = tk.Frame(self.fenetre, bg="#0a0520")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Info
        self.label_info = tk.Label(
            main_frame,
            text="",
            font=("Courier", 13, "bold"),
            fg="#00ffff",
            bg="#0a0520"
        )
        self.label_info.pack(pady=5)

        # Message d'erreur intégré
        self.label_message = tk.Label(
            main_frame,
            text="",
            font=("Courier", 11, "bold"),
            fg="#ff6b6b",
            bg="#0a0520",
            height=2
        )
        self.label_message.pack()

        # Frame jeu
        game_frame = tk.Frame(main_frame, bg="#0a0520")
        game_frame.pack(expand=True)

        # Joueur 1
        left_frame = tk.Frame(game_frame, bg="#0a0520", width=150)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.label_joueur1 = tk.Label(
            left_frame,
            text="",
            font=("Courier", 11, "bold"),
            fg="#ffcc00",
            bg="#0a0520"
        )
        self.label_joueur1.pack(pady=5)

        self.canvas_j1 = tk.Canvas(left_frame, width=120, height=350, bg="#0a0520", highlightthickness=0)
        self.canvas_j1.pack()

        # Plateau
        center_frame = tk.Frame(game_frame, bg="#0a0520")
        center_frame.pack(side=tk.LEFT, padx=20)

        self.canvas_plateau = tk.Canvas(center_frame, width=400, height=400, bg="#0a0520", highlightthickness=0)
        self.canvas_plateau.pack()
        self.canvas_plateau.bind("<Button-1>", self.clic_plateau)

        # Boutons face
        face_frame = tk.Frame(center_frame, bg="#0a0520")
        face_frame.pack(pady=10)

        tk.Label(face_frame, text="✨ Face:", fg="#ffffff", bg="#0a0520", font=("Courier", 10)).pack()

        btn_f = tk.Frame(face_frame, bg="#0a0520")
        btn_f.pack()

        self.btn_claire = tk.Button(
            btn_f,
            text="☀️ Claire",
            font=("Courier", 9),
            bg="#ffff00",
            fg="#000000",
            activebackground="#cccc00",
            relief=tk.SUNKEN,
            padx=10,
            pady=3,
            cursor="hand2",
            command=lambda: self.choisir_face(True)
        )
        self.btn_claire.pack(side=tk.LEFT, padx=3)

        self.btn_sombre = tk.Button(
            btn_f,
            text="🌙 Sombre",
            font=("Courier", 9),
            bg="#1a1f3a",
            fg="#ffffff",
            activebackground="#0f1428",
            relief=tk.RAISED,
            padx=10,
            pady=3,
            cursor="hand2",
            command=lambda: self.choisir_face(False)
        )
        self.btn_sombre.pack(side=tk.LEFT, padx=3)

        # Joueur 2
        right_frame = tk.Frame(game_frame, bg="#0a0520", width=150)
        right_frame.pack(side=tk.LEFT, padx=10)

        self.label_joueur2 = tk.Label(
            right_frame,
            text="",
            font=("Courier", 11, "bold"),
            fg="#ff6b6b",
            bg="#0a0520"
        )
        self.label_joueur2.pack(pady=5)

        self.canvas_j2 = tk.Canvas(right_frame, width=120, height=350, bg="#0a0520", highlightthickness=0)
        self.canvas_j2.pack()

        # Boutons contrôle
        ctrl_frame = tk.Frame(main_frame, bg="#0a0520")
        ctrl_frame.pack(pady=10)

        self.btn_abandonner = tk.Button(
            ctrl_frame,
            text="🏳️ Abandonner",
            font=("Courier", 10),
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#cc5555",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.abandonner
        )
        self.btn_abandonner.pack(side=tk.LEFT, padx=5)

        self.btn_rejouer = tk.Button(
            ctrl_frame,
            text="🔄 Rejouer",
            font=("Courier", 10),
            bg="#51cf66",
            fg="#ffffff",
            activebackground="#3db54a",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.rejouer
        )
        self.btn_rejouer.pack(side=tk.LEFT, padx=5)

        tk.Button(
            ctrl_frame,
            text="❌ Quitter",
            font=("Courier", 10),
            bg="#868e96",
            fg="#ffffff",
            activebackground="#666e76",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.fenetre.quit
        ).pack(side=tk.LEFT, padx=5)

    def commencer_partie(self):
        '''
        Commence une nouvelle partie
        Préconditions: aucune
        Postconditions: initialise la partie
        '''
        self.plateau = Plateau()
        self.joueur_actuel = "joueur1"
        self.jetons_restants = {"joueur1": 8, "joueur2": 8}
        self.premier_coup = True
        self.phase_action = "placer"
        self.jeton_selectionne = None
        self.face_choisie = True
        self.partie_en_cours = True

        self.btn_abandonner.config(state=tk.NORMAL)
        self.btn_rejouer.config(state=tk.DISABLED)

        self.label_joueur1.config(text=f"⭐ {self.joueur1_nom}\n🔵 Jetons: 8")
        self.label_joueur2.config(text=f"⭐ {self.joueur2_nom}\n🔴 Jetons: 8")

        self.dessiner_plateau()
        self.dessiner_jetons()
        self.mettre_a_jour_info()
        self.effacer_message()

    def dessiner_plateau(self):
        '''
        Dessine le plateau de jeu
        Préconditions: aucune
        Postconditions: affiche le plateau avec jetons
        '''
        self.canvas_plateau.delete("all")

        # Fond spatial
        for i in range(20):
            x = random.randint(0, 400)
            y = random.randint(0, 400)
            self.canvas_plateau.create_oval(x, y, x+2, y+2, fill="white", outline="")

        taille = 100
        for i in range(4):
            for j in range(4):
                x1 = j * taille
                y1 = i * taille
                x2 = x1 + taille
                y2 = y1 + taille

                # Case avec effet néon
                self.canvas_plateau.create_rectangle(
                    x1+2, y1+2, x2-2, y2-2,
                    fill="#0f1535",
                    outline="#00ffff",
                    width=2
                )

                # Jeton si présent
                if self.plateau and self.plateau.grille[i][j]:
                    jeton = self.plateau.grille[i][j]
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2

                    if jeton.joueur == "joueur1":
                        couleur = "#4dabf7" if jeton.face_claire else "#1971c2"
                        symbole = "🔵"
                    else:
                        couleur = "#ff6b6b" if jeton.face_claire else "#c92a2a"
                        symbole = "🔴"

                    # Cercle avec effet de lumière
                    self.canvas_plateau.create_oval(
                        cx-35, cy-35, cx+35, cy+35,
                        fill=couleur,
                        outline="#ffffff",
                        width=3
                    )

                    # Symbole
                    self.canvas_plateau.create_text(
                        cx, cy,
                        text=symbole,
                        font=("Arial", 40),
                        fill="white"
                    )

                    # Indicateur de face
                    face_txt = "☀️" if jeton.face_claire else "🌙"
                    self.canvas_plateau.create_text(
                        cx, cy+25,
                        text=face_txt,
                        font=("Arial", 16)
                    )

    def dessiner_jetons(self):
        '''
        Dessine les jetons restants
        Préconditions: aucune
        Postconditions: affiche les jetons disponibles
        '''
        self.canvas_j1.delete("all")
        self.canvas_j2.delete("all")

        # Jetons joueur 1
        for i in range(self.jetons_restants["joueur1"]):
            y = 20 + i * 40
            self.canvas_j1.create_oval(10, y, 50, y+35, fill="#4dabf7", outline="#ffffff", width=2)
            self.canvas_j1.create_text(30, y+17, text="🔵", font=("Arial", 20))

        # Jetons joueur 2
        for i in range(self.jetons_restants["joueur2"]):
            y = 20 + i * 40
            self.canvas_j2.create_oval(10, y, 50, y+35, fill="#ff6b6b", outline="#ffffff", width=2)
            self.canvas_j2.create_text(30, y+17, text="🔴", font=("Arial", 20))

    def mettre_a_jour_info(self):
        '''
        Met à jour le label d'information
        Préconditions: aucune
        Postconditions: affiche les instructions
        '''
        nom = self.joueur1_nom if self.joueur_actuel == "joueur1" else self.joueur2_nom

        if self.premier_coup:
            texte = f"🎯 {nom}: Placez votre premier jeton"
        elif self.phase_action == "retourner":
            texte = f"🔄 {nom}: Sélectionnez un jeton adverse à retourner"
        elif self.phase_action == "choisir_dest":
            texte = f"📍 {nom}: Choisissez une case vide adjacente"
        else:
            texte = f"✨ {nom}: Placez votre jeton (choisissez la face)"

        self.label_info.config(text=texte)

    def choisir_face(self, claire):
        '''
        Choisit la face du jeton
        Préconditions:
            claire: booléen
        Postconditions: enregistre le choix
        '''
        self.face_choisie = claire
        if claire:
            self.btn_claire.config(relief=tk.SUNKEN, bg="#ffff00")
            self.btn_sombre.config(relief=tk.RAISED, bg="#1a1f3a")
        else:
            self.btn_claire.config(relief=tk.RAISED, bg="#cccc00")
            self.btn_sombre.config(relief=tk.SUNKEN, bg="#0f1428")

    def clic_plateau(self, event):
        '''
        Gère les clics sur le plateau
        Préconditions:
            event: événement tkinter
        Postconditions: traite l'action du joueur
        '''
        if not self.partie_en_cours:
            return

        if self.mode_ia and self.joueur_actuel == "joueur2":
            return

        taille = 100
        col = event.x // taille
        ligne = event.y // taille

        if not (0 <= ligne < 4 and 0 <= col < 4):
            return

        if self.premier_coup:
            self.placer_premier(ligne, col)
        elif self.phase_action == "retourner":
            self.selectionner_retourner(ligne, col)
        elif self.phase_action == "choisir_dest":
            self.choisir_destination(ligne, col)
        elif self.phase_action == "placer":
            self.placer_jeton(ligne, col)

    def placer_premier(self, ligne, col):
        '''
        Place le premier jeton
        Préconditions:
            ligne, col: entiers 0-3
        Postconditions: place le jeton et change de joueur
        '''
        if not self.plateau.est_vide(ligne, col):
            self.afficher_message("⚠️ Cette case est déjà occupée!")
            return

        self.jouer_son()
        jeton = Jeton(self.joueur_actuel, self.face_choisie)
        self.plateau.placer_jeton(ligne, col, jeton)
        self.jetons_restants[self.joueur_actuel] -= 1

        self.premier_coup = False
        self.phase_action = "retourner"
        self.changer_joueur()

        self.dessiner_plateau()
        self.dessiner_jetons()
        self.mettre_a_jour_info()

        if self.mode_ia and self.joueur_actuel == "joueur2":
            self.fenetre.after(1000, self.jouer_ia)

    def selectionner_retourner(self, ligne, col):
        '''
        Sélectionne un jeton à retourner
        Préconditions:
            ligne, col: entiers 0-3
        Postconditions: enregistre le jeton sélectionné
        '''
        if self.plateau.est_vide(ligne, col):
            self.afficher_message("⚠️ Sélectionnez une case avec un jeton!")
            return

        jeton = self.plateau.grille[ligne][col]
        adversaire = "joueur2" if self.joueur_actuel == "joueur1" else "joueur1"

        if jeton.joueur != adversaire:
            self.afficher_message("⚠️ Vous devez sélectionner un jeton ADVERSE!")
            return

        self.jeton_selectionne = (ligne, col)
        self.phase_action = "choisir_dest"
        self.mettre_a_jour_info()
        self.afficher_message("✓ Jeton sélectionné! Choisissez où le déplacer", "#00ff00")

    def choisir_destination(self, ligne, col):
        '''
        Choisit où déplacer le jeton retourné
        Préconditions:
            ligne, col: entiers 0-3
        Postconditions: déplace et retourne le jeton
        '''
        if not self.plateau.est_vide(ligne, col):
            self.afficher_message("⚠️ Choisissez une case VIDE!")
            return

        l_src, c_src = self.jeton_selectionne

        if not self.plateau.est_contigu(l_src, c_src, ligne, col):
            self.afficher_message("⚠️ Choisissez une case ADJACENTE (haut/bas/gauche/droite)!")
            return

        self.jouer_son()
        jeton = self.plateau.retirer_jeton(l_src, c_src)
        jeton.retourner()
        self.plateau.placer_jeton(ligne, col, jeton)

        adversaire = "joueur2" if self.joueur_actuel == "joueur1" else "joueur1"
        if self.plateau.verifier_alignement(adversaire):
            self.dessiner_plateau()
            nom = self.joueur2_nom if adversaire == "joueur2" else self.joueur1_nom
            self.afficher_message(f"🎉 {nom} a gagné en alignant 3 jetons!", "#00ff00")
            self.fin_partie()
            return

        self.phase_action = "placer"
        self.dessiner_plateau()
        self.mettre_a_jour_info()
        self.effacer_message()

    def placer_jeton(self, ligne, col):
        '''
        Place un nouveau jeton
        Préconditions:
            ligne, col: entiers 0-3
        Postconditions: place le jeton et vérifie victoire
        '''
        if not self.plateau.est_vide(ligne, col):
            self.afficher_message("⚠️ Cette case est déjà occupée!")
            return

        if self.jetons_restants[self.joueur_actuel] <= 0:
            self.afficher_message("⚠️ Vous n'avez plus de jetons!")
            return

        self.jouer_son()
        jeton = Jeton(self.joueur_actuel, self.face_choisie)
        self.plateau.placer_jeton(ligne, col, jeton)
        self.jetons_restants[self.joueur_actuel] -= 1

        self.dessiner_plateau()
        self.dessiner_jetons()

        if self.plateau.verifier_alignement(self.joueur_actuel):
            nom = self.joueur1_nom if self.joueur_actuel == "joueur1" else self.joueur2_nom
            self.afficher_message(f"🎉 Félicitations {nom}! Vous avez gagné!", "#00ff00")
            self.fin_partie()
            return

        self.phase_action = "retourner"
        self.changer_joueur()
        self.mettre_a_jour_info()
        self.effacer_message()

        self.label_joueur1.config(text=f"⭐ {self.joueur1_nom}\n🔵 Jetons: {self.jetons_restants['joueur1']}")
        self.label_joueur2.config(text=f"⭐ {self.joueur2_nom}\n🔴 Jetons: {self.jetons_restants['joueur2']}")

        if self.mode_ia and self.joueur_actuel == "joueur2":
            self.fenetre.after(1000, self.jouer_ia)

    def jouer_ia(self):
        '''
        Fait jouer l'IA
        Préconditions: mode IA activé
        Postconditions: l'IA effectue son tour
        '''
        if not self.partie_en_cours:
            return

        if self.niveau_ia == "facile":
            coup = IA.jouer_facile(self.plateau, "joueur2")
        else:
            coup = IA.jouer_difficile(self.plateau, "joueur2", self.jetons_restants["joueur2"])

        # Retourner
        l_src, c_src, l_dest, c_dest = coup['retourner']
        if not self.plateau.est_vide(l_src, c_src):
            jeton = self.plateau.retirer_jeton(l_src, c_src)
            if jeton:
                jeton.retourner()
                self.plateau.placer_jeton(l_dest, c_dest, jeton)

        self.jouer_son()
        self.dessiner_plateau()

        adversaire = "joueur1"
        if self.plateau.verifier_alignement(adversaire):
            nom = self.joueur1_nom
            self.afficher_message(f"🎉 {nom} a gagné!", "#00ff00")
            self.fin_partie()
            return

        # Placer
        self.fenetre.after(500, lambda: self.ia_placer(coup))

    def ia_placer(self, coup):
        '''
        L'IA place son jeton
        Préconditions:
            coup: dictionnaire avec les actions
        Postconditions: place le jeton de l'IA
        '''
        if not self.partie_en_cours:
            return

        l_place, c_place, face = coup['placer']

        if self.plateau.est_vide(l_place, c_place) and self.jetons_restants["joueur2"] > 0:
            jeton = Jeton("joueur2", face)
            self.plateau.placer_jeton(l_place, c_place, jeton)
            self.jetons_restants["joueur2"] -= 1

            self.jouer_son()
            self.dessiner_plateau()
            self.dessiner_jetons()

            if self.plateau.verifier_alignement("joueur2"):
                self.afficher_message(f"🎉 {self.joueur2_nom} a gagné!", "#00ff00")
                self.fin_partie()
                return

            self.phase_action = "retourner"
            self.changer_joueur()
            self.mettre_a_jour_info()

            self.label_joueur1.config(text=f"⭐ {self.joueur1_nom}\n🔵 Jetons: {self.jetons_restants['joueur1']}")
            self.label_joueur2.config(text=f"⭐ {self.joueur2_nom}\n🔴 Jetons: {self.jetons_restants['joueur2']}")

    def changer_joueur(self):
        '''
        Change le joueur actuel
        Préconditions: aucune
        Postconditions: alterne entre joueur1 et joueur2
        '''
        self.joueur_actuel = "joueur2" if self.joueur_actuel == "joueur1" else "joueur1"

    def abandonner(self):
        '''
        Abandonne la partie
        Préconditions: aucune
        Postconditions: déclare l'autre joueur vainqueur
        '''
        nom_perdant = self.joueur1_nom if self.joueur_actuel == "joueur1" else self.joueur2_nom
        nom_gagnant = self.joueur2_nom if self.joueur_actuel == "joueur1" else self.joueur1_nom

        self.afficher_message(f"🏳️ {nom_perdant} a abandonné. {nom_gagnant} gagne!", "#ffff00")
        self.fin_partie()

    def fin_partie(self):
        '''
        Termine la partie
        Préconditions: aucune
        Postconditions: désactive les contrôles
        '''
        self.partie_en_cours = False
        self.btn_abandonner.config(state=tk.DISABLED)
        self.btn_rejouer.config(state=tk.NORMAL)

    def rejouer(self):
        '''
        Relance une nouvelle partie
        Préconditions: aucune
        Postconditions: réinitialise le jeu
        '''
        self.commencer_partie()


# Programme principal
if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = JeuMorpionReversi(fenetre)
    fenetre.mainloop()