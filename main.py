# Importation des modules nécessaires pour le jeu
import random
from abc import ABC, abstractmethod
import pygame
import os

# Initialisation du moteur audio Pygame
SOUND_ENABLED = True
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Attention : Le mixeur Pygame n'a pas pu être initialisé : {e}. Le son sera désactivé.")
    SOUND_ENABLED = False

def play_music(file_path):
    """Charge et joue une musique de fond en boucle."""
    if SOUND_ENABLED and os.path.exists(file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Impossible de jouer la musique {file_path}: {e}")

def stop_music():
    """Arrête toute musique de fond actuellement diffusée."""
    if SOUND_ENABLED:
        pygame.mixer.music.stop()

def play_sound_effect(file_path):
    """Joue un effet sonore court (bruitage) une seule fois."""
    if SOUND_ENABLED and os.path.exists(file_path):
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.play()
        except pygame.error as e:
            print(f"Impossible de jouer l'effet sonore {file_path}: {e}")

# Définition des constantes pour les chemins des fichiers audio
MUSIC_MENU = "assets/musiques/menu_theme.mp3"
MUSIC_TUTORIAL = "assets/musiques/tutorial_theme.mp3"
MUSIC_BATTLE = "assets/musiques/battle_theme.mp3"
MUSIC_DEFEAT = "assets/musiques/defeat_theme.mp3"
MUSIC_BOSS_BATTLE = "assets/musiques/boss_battle_theme.mp3"
MUSIC_EXPLORATION = "assets/musiques/exploration_theme.mp3"
MUSIC_SHOP = "assets/musiques/shop_theme.mp3"
SFX_ATTACK = "assets/sfx/attack.wav"
SFX_HEAL = "assets/sfx/heal.wav"
SFX_LEVEL_UP = "assets/sfx/level_up.wav"
SFX_VICTORY = "assets/sfx/victory.wav"
SFX_DEFEAT = "assets/sfx/defeat.wav"
SFX_ITEM_USE = "assets/sfx/item_use.wav"
SFX_SHOP_ENTER = "assets/sfx/shop_enter.mp3"


class Menu:
    """Gère l'interface utilisateur textuelle et la navigation dans les menus."""

    def __init__(self):
        # Stockage local de l'historique des scores (vagues atteintes)
        self.scores = []
        self.arene = None

    def afficher_titre(self):
        """Affiche le titre du jeu."""
        print("\n" + "="*40)
        print("     === RPG PYTHON ===")
        print("="*40 + "\n")

    def afficher_menu_principal(self):
        """Affiche le menu principal."""
        self.afficher_titre()
        print("1. Jouer")
        print("2. Tutoriel")
        print("3. Historique des scores")
        print("4. Quitter")
        print("-"*40)
        return input("Votre choix : ").strip()

    def jouer(self):
        """Lance une partie du jeu."""
        self.arene = Arene()
        self.arene.jouer()
        self.scores = self.arene._historique_scores

    def afficher_tutoriel(self):
        """Affiche les règles du jeu avec une musique d'ambiance spécifique."""
        stop_music()
        play_music(MUSIC_TUTORIAL)
        print("\n" + "="*40)
        print("       TUTORIEL INTERACTIF")
        print("="*40)

        etapes = [
            ("\n--- BIENVENUE ---",
             "Dans ce RPG, vous affrontez des vagues d'ennemis de plus en plus forts."),
            ("\n--- LE COMBAT ---",
             "À chaque tour, vous pouvez attaquer, utiliser une capacité spéciale (2x dégâts),\n"
             "vous soigner ou utiliser un objet de votre inventaire."),
            ("\n--- PROGRESSION ---",
             "Vaincre des ennemis rapporte de l'XP et de l'Or.\n"
             "L'XP vous fait monter de niveau automatiquement, augmentant vos stats."),
            ("\n--- LA BOUTIQUE ---",
             "Entre chaque vague, vous pouvez dépenser votre Or pour acheter des potions\n"
             "ou des boosts de statistiques."),
            ("\n--- CONSEIL ---",
             "Économisez vos capacités spéciales pour les Boss qui apparaissent toutes les 5 vagues !")
        ]

        # Ajout d'une étape de combat interactif
        etapes.insert(2, ("\n--- COMBAT INTERACTIF ---", "Nous allons simuler un petit combat pour vous montrer les bases."))
        for titre, texte in etapes:
            print(titre)
            print(texte)
            input("\n[Appuyez sur Entrée pour continuer...]")
            
            # Appel de la simulation de combat si c'est l'étape du combat interactif
            if "COMBAT INTERACTIF" in titre:
                self._simuler_combat_tutoriel()

        print("\nFin du tutoriel. Vous êtes prêt pour l'aventure !")
        print("="*40 + "\n")
        # Assurez-vous que la musique du tutoriel est toujours active après le combat interactif
        stop_music() 
        play_music(MUSIC_MENU)

    def _simuler_combat_tutoriel(self):
        """Simule un petit combat interactif pour le tutoriel."""
        print("\n--- DÉBUT DU COMBAT DE TUTORIEL ---")
        stop_music()
        play_music(MUSIC_BATTLE)

        hero_tuto = Heros("Apprenti", pv=50, attaque=10, defense=2)
        ennemi_tuto = Ennemi("Gobelin d'entraînement", pv=30, attaque=5, defense=1, type_ennemi="Gobelin", butin_xp=0)

        print(f"\nVous affrontez un {ennemi_tuto.nom} !")

        tour = 1
        # Limite le combat à quelques tours pour le tutoriel ou jusqu'à ce que l'ennemi soit vaincu
        while hero_tuto.est_vivant() and ennemi_tuto.est_vivant() and tour <= 3: 
            print(f"\n--- Tour {tour} ---")
            print(f"{hero_tuto.nom} : PV {hero_tuto.pv}/{hero_tuto.pv_max}")
            print(f"{ennemi_tuto.nom} : PV {ennemi_tuto.pv}/{ennemi_tuto.pv_max}")

            action = input("Choisissez une action : 1. Attaque 2. Capacité Spéciale 3. Soin : ")

            if action == "1":
                hero_tuto.attaquer(ennemi_tuto)
            elif action == "2":
                hero_tuto.capacite_speciale_action(ennemi_tuto)
            elif action == "3":
                hero_tuto.soin()
            else:
                print("Action invalide. Attaque par défaut.")
                hero_tuto.attaquer(ennemi_tuto)

            if not ennemi_tuto.est_vivant():
                print(f"\nVous avez vaincu le {ennemi_tuto.nom} d'entraînement !")
                break

            # Tour de l'ennemi
            if ennemi_tuto.est_vivant():
                ennemi_tuto.attaquer(hero_tuto)
            tour += 1

        print("\n--- FIN DU COMBAT DE TUTORIEL ---")
        stop_music()
        play_music(MUSIC_MENU)

    def afficher_scores(self):
        """Affiche l'historique des scores."""
        print("\n" + "="*40)
        print("       HISTORIQUE DES SCORES")
        print("="*40)
        if not self.scores:
            print("Aucun score enregistré pour le moment.")
        else:
            for i, score in enumerate(self.scores, 1):
                print(f"{i}. Vague {score}")
        print("-"*40 + "\n")

    def lancer(self):
        """Lance la boucle du menu principal."""
        play_music(MUSIC_MENU)
        while True:
            choix = self.afficher_menu_principal()

            if choix == "1":
                stop_music()
                self.jouer()
                play_music(MUSIC_MENU)
            elif choix == "2":
                self.afficher_tutoriel()
            elif choix == "3":
                self.afficher_scores()
            elif choix == "4":
                stop_music()
                print("Merci d'avoir joué ! À bientôt !\n")
                break
            else:
                print("Choix invalide. Veuillez réessayer.\n")


class Item:
    """Représente un objet consommable avec différents types d'effets (soin, boost, débuff)."""

    def __init__(self, nom, type_, effet, cout):
        self.nom = nom
        self.type = type_
        self.effet = effet
        self.cout = cout

    def utiliser(self, joueur, ennemi=None):
        """Applique l'effet de l'objet sur le joueur ou un ennemi."""
        if self.type == 'soin':
            if self.effet == 'max':
                soin = joueur.pv_max - joueur.pv
            else:
                soin = self.effet
            joueur.pv = min(joueur.pv_max, joueur.pv + soin)
            play_sound_effect(SFX_HEAL)
            print(f"{joueur.nom} utilise {self.nom} et récupère {soin} PV. PV actuel : {joueur.pv}/{joueur.pv_max}")
        elif self.type == 'boost_joueur':
            if 'attaque' in self.effet:
                joueur.attaque += self.effet['attaque']
                print(f"{joueur.nom} utilise {self.nom} et gagne +{self.effet['attaque']} attaque temporaire.")
            if 'defense' in self.effet:
                joueur.defense += self.effet['defense']
                print(f"{joueur.nom} utilise {self.nom} et gagne +{self.effet['defense']} défense temporaire.")
            play_sound_effect(SFX_ITEM_USE)
        elif self.type == 'debuff_ennemi':
            if ennemi:
                if 'attaque' in self.effet:
                    ennemi.attaque -= self.effet['attaque']
                    print(f"{joueur.nom} utilise {self.nom} et réduit l'attaque de {ennemi.nom} de {self.effet['attaque']}.")
                if 'defense' in self.effet:
                    ennemi.defense -= self.effet['defense']
                    print(f"{joueur.nom} utilise {self.nom} et réduit la défense de {ennemi.nom} de {self.effet['defense']}.")
            play_sound_effect(SFX_ITEM_USE)


# Liste des objets que le joueur peut acheter au magasin
items_disponibles = [
    Item("Potion Petite", 'soin', 5, 10),
    Item("Potion Moyenne", 'soin', 10, 15),
    Item("Potion Grande", 'soin', 15, 20),
    Item("Potion Complète", 'soin', 'max', 30),
    Item("Boost Attaque", 'boost_joueur', {'attaque': 5}, 25),
    Item("Boost Défense", 'boost_joueur', {'defense': 5}, 25),
    Item("Débuff Attaque Ennemi", 'debuff_ennemi', {'attaque': 5}, 30),
    Item("Débuff Défense Ennemi", 'debuff_ennemi', {'defense': 5}, 30),
]


class Entite(ABC):
    """Classe de base abstraite pour toutes les entités du jeu (Héros et Ennemis)."""

    def __init__(self, nom, pv, attaque, defense):
        self._nom = nom
        self._pv = pv
        self._pv_max = pv
        self._attaque = attaque
        self._defense = defense

    @property
    def nom(self):
        return self._nom

    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, value):
        self._pv = max(0, value)

    @property
    def pv_max(self):
        return self._pv_max

    @property
    def attaque(self):
        return self._attaque

    @attaque.setter
    def attaque(self, value):
        self._attaque = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    def est_vivant(self):
        return self._pv > 0

    def recevoir_degats(self, degats):
        """Calcule et applique les dégâts subis après réduction par la défense."""
        degats_reels = max(0, degats - self._defense)
        self.pv -= degats_reels
        return degats_reels

    @abstractmethod
    def attaquer(self, cible):
        """Méthode abstraite devant être implémentée par les sous-classes."""
        pass


class Heros(Entite):
    """Représente le personnage contrôlé par le joueur."""
    def __init__(self, nom, pv=100, attaque=20, defense=5):
        super().__init__(nom, pv, attaque, defense)
        self._niveau = 1
        self._xp = 0
        self._xp_prochain_niveau = 100
        self._capacite_speciale = "Coup Puissant"
        self._inventaire = []
        self._or = 0

    @property
    def niveau(self):
        return self._niveau

    @property
    def xp(self):
        return self._xp

    @property
    def capacite_speciale(self):
        return self._capacite_speciale

    @property
    def inventaire(self):
        return self._inventaire

    @property
    def or_(self):
        return self._or

    @or_.setter
    def or_(self, value):
        self._or = max(0, value)

    def gagner_xp(self, xp):
        """Ajoute de l'XP et gère la montée de niveau si le seuil est atteint."""
        self._xp += xp
        while self._xp >= self._xp_prochain_niveau:
            self.monter_niveau()

    def monter_niveau(self):
        """Augmente les statistiques du héros lors d'un gain de niveau."""
        self._niveau += 1
        play_sound_effect(SFX_LEVEL_UP)
        self._xp -= self._xp_prochain_niveau
        self._xp_prochain_niveau = int(self._xp_prochain_niveau * 1.5)
        self._pv_max += 10
        self._pv = self._pv_max
        self._attaque += 5
        self._defense += 2
        print(f"{self.nom} monte au niveau {self._niveau} ! Ses statistiques augmentent.")

    def attaquer(self, cible):
        """Effectue une attaque standard sur une cible."""
        degats = self._attaque + random.randint(-2, 2)
        degats_reels = cible.recevoir_degats(degats)
        play_sound_effect(SFX_ATTACK)
        print(f"{self.nom} attaque {cible.nom} pour {degats_reels} dégâts !")

    def capacite_speciale_action(self, cible):
        """Utilise la capacité spéciale infligeant de lourds dégâts."""
        degats = self._attaque * 2 + random.randint(0, 5)
        degats_reels = cible.recevoir_degats(degats)
        print(f"{self.nom} utilise {self._capacite_speciale} sur {cible.nom} pour {degats_reels} dégâts !")

    def soin(self):
        soin = 20
        play_sound_effect(SFX_HEAL)
        self._pv = min(self._pv_max, self._pv + soin)
        print(f"{self.nom} se soigne pour {soin} PV. PV actuel : {self._pv}/{self._pv_max}")

    def augmenter_pv_max(self, valeur):
        self._pv_max += valeur


class Ennemi(Entite):
    """Classe représentant les adversaires de base."""

    def __init__(self, nom, pv, attaque, defense, type_ennemi, butin_xp):
        super().__init__(nom, pv, attaque, defense)
        self._type = type_ennemi
        self._butin_xp = butin_xp

    @property
    def type(self):
        return self._type

    @property
    def butin_xp(self):
        return self._butin_xp

    def attaquer(self, cible):
        """Logique d'attaque spécifique selon le type d'ennemi (Polymorphisme)."""
        if self._type == "Gobelin":
            degats = self._attaque + random.randint(-1, 1)
            play_sound_effect(SFX_ATTACK)
            degats_reels = cible.recevoir_degats(degats)
            print(f"{self.nom} (Gobelin) attaque {cible.nom} pour {degats_reels} dégâts !")
        elif self._type == "Orc":
            degats = self._attaque + random.randint(0, 3)
            play_sound_effect(SFX_ATTACK)
            degats_reels = cible.recevoir_degats(degats)
            print(f"{self.nom} (Orc) charge {cible.nom} pour {degats_reels} dégâts !")
        elif self._type == "Sorcier":
            degats = self._attaque + random.randint(1, 4)
            play_sound_effect(SFX_ATTACK)
            degats_reels = cible.recevoir_degats(degats)
            print(f"{self.nom} (Sorcier) lance un sort sur {cible.nom} pour {degats_reels} dégâts !")
        else:
            degats = self._attaque
            play_sound_effect(SFX_ATTACK)
            degats_reels = cible.recevoir_degats(degats)
            print(f"{self.nom} attaque {cible.nom} pour {degats_reels} dégâts !")


class Boss(Ennemi):
    """Version puissante d'un ennemi apparaissant à des intervalles réguliers."""

    def __init__(self, nom, pv, attaque, defense, type_ennemi, butin_xp, competence_unique, multiplicateur_stats):
        super().__init__(nom, pv, attaque, defense, type_ennemi, butin_xp)
        self._competence_unique = competence_unique
        self._multiplicateur_stats = multiplicateur_stats

    @property
    def competence_unique(self):
        return self._competence_unique

    @property
    def multiplicateur_stats(self):
        return self._multiplicateur_stats

    def attaquer(self, cible):
        """Attaque spéciale de Boss."""
        degats = int(self._attaque * 1.5) + random.randint(0, 5)
        play_sound_effect(SFX_ATTACK)
        degats_reels = cible.recevoir_degats(degats)
        print(f"{self.nom} (Boss) utilise {self._competence_unique} sur {cible.nom} pour {degats_reels} dégâts !")


class Arene:
    """Moteur principal de la logique de jeu, gérant les vagues, le combat et le magasin."""

    def __init__(self):
        self._numero_vague = 1
        self._historique_scores = []
        self.heros = Heros("Héros")

    def creer_vague(self):
        """Génère dynamiquement une liste d'ennemis en fonction du numéro de la vague."""
        ennemis = []
        nombre_ennemis = 2 + self._numero_vague // 2
        types = ["Gobelin", "Orc", "Sorcier"]
        for i in range(nombre_ennemis):
            type_ennemi = random.choice(types)
            if type_ennemi == "Gobelin":
                pv = 30 + self._numero_vague * 5
                attaque = 10 + self._numero_vague * 2
                defense = 2 + self._numero_vague
            elif type_ennemi == "Orc":
                pv = 50 + self._numero_vague * 7
                attaque = 15 + self._numero_vague * 3
                defense = 5 + self._numero_vague
            elif type_ennemi == "Sorcier":
                pv = 25 + self._numero_vague * 4
                attaque = 20 + self._numero_vague * 4
                defense = 1 + self._numero_vague
            else:
                raise ValueError(f"Type d'ennemi inattendu: {type_ennemi}")
            butin_xp = 20 + self._numero_vague * 5
            ennemi = Ennemi(f"{type_ennemi} {i+1}", pv, attaque, defense, type_ennemi, butin_xp)
            ennemis.append(ennemi)

        if self._numero_vague % 5 == 0:
            boss = Boss(
                "Boss Dragon",
                200 + self._numero_vague * 20,
                30 + self._numero_vague * 5,
                10 + self._numero_vague * 2,
                "Boss",
                100 + self._numero_vague * 10,
                "Souffle de Feu",
                2.0
            )
            ennemis.append(boss)

        return ennemis

    def combat(self, ennemis):
        """Gère la boucle de combat au tour par tour entre le héros et la vague d'ennemis."""
        play_music(MUSIC_BATTLE)
        print(f"\n--- Vague {self._numero_vague} ---")
        while self.heros.est_vivant() and any(e.est_vivant() for e in ennemis):
            print(f"\n{self.heros.nom} : PV {self.heros.pv}/{self.heros.pv_max}")
            for ennemi in ennemis:
                if ennemi.est_vivant():
                    print(f"{ennemi.nom} ({ennemi.type}) : PV {ennemi.pv}")

            # Menu d'actions du joueur
            action = input("Choisissez une action : 1. Attaque 2. Capacité Spéciale 3. Soin 4. Utiliser Item : ")
            if action == "1":
                cible = random.choice([e for e in ennemis if e.est_vivant()])
                self.heros.attaquer(cible)
            elif action == "2":
                cible = random.choice([e for e in ennemis if e.est_vivant()])
                self.heros.capacite_speciale_action(cible)
            elif action == "3":
                self.heros.soin()
            elif action == "4":
                if self.heros.inventaire:
                    print("Inventaire :")
                    for i, item in enumerate(self.heros.inventaire):
                        print(f"{i+1}. {item.nom}")
                    choix_item = input("Choisissez un item (numéro) : ")
                    try:
                        idx = int(choix_item) - 1
                        item = self.heros.inventaire[idx]
                        if item.type == 'debuff_ennemi':
                            ennemis_vivants = [e for e in ennemis if e.est_vivant()]
                            if ennemis_vivants:
                                print("Choisissez un ennemi :")
                                for j, enn in enumerate(ennemis_vivants):
                                    print(f"{j+1}. {enn.nom}")
                                choix_enn = input("Numéro de l'ennemi : ")
                                try:
                                    idx_enn = int(choix_enn) - 1
                                    ennemi_cible = ennemis_vivants[idx_enn]
                                    item.utiliser(self.heros, ennemi_cible)
                                except (ValueError, IndexError):
                                    print("Choix invalide.")
                            else:
                                print("Aucun ennemi vivant.")
                        else:
                            item.utiliser(self.heros)
                        self.heros.inventaire.pop(idx)
                    except (ValueError, IndexError):
                        print("Choix invalide.")
                else:
                    print("Inventaire vide.")
            else:
                print("Action invalide, attaque par défaut.")
                cible = random.choice([e for e in ennemis if e.est_vivant()])
                self.heros.attaquer(cible)

            # Tour des ennemis
            for ennemi in ennemis:
                if ennemi.est_vivant():
                    ennemi.attaquer(self.heros)
                    if not self.heros.est_vivant():
                        break

        if self.heros.est_vivant():
            play_sound_effect(SFX_VICTORY)
            stop_music()
            print(f"\nVictoire de la vague {self._numero_vague} !")
            xp_total = sum(e.butin_xp for e in ennemis)
            self.heros.gagner_xp(xp_total)
            print(f"XP gagné : {xp_total}")
            or_gagne = 50 + self._numero_vague * 10
            self.heros.or_ += or_gagne
            print(f"Or gagné : {or_gagne}. Or total : {self.heros.or_}")
            play_music(MUSIC_EXPLORATION)
            self.recompense()
            self.magasin()
            self._numero_vague += 1
        else:
            play_sound_effect(SFX_DEFEAT)
            stop_music()
            play_music(MUSIC_DEFEAT)
            print(f"\nDéfaite à la vague {self._numero_vague}.")
            print(f"Appuyez sur une touche pour revenir au menu.")
            input()
            stop_music()
            self._historique_scores.append(self._numero_vague - 1)
            return False
        return True

    def recompense(self):
        """Permet au joueur de choisir un bonus statistique permanent après une victoire."""
        print("\nRécompense : Choisissez un bonus :")
        print("1. +10 Attaque")
        print("2. +5 Défense")
        print("3. +20 PV Max")
        choix = input("Votre choix : ")
        if choix == "1":
            self.heros.attaque += 10
            print("Attaque augmentée !")
        elif choix == "2":
            self.heros.defense += 5
            print("Défense augmentée !")
        elif choix == "3":
            self.heros.augmenter_pv_max(20)
            print("PV Max augmentés !")
        else:
            print("Choix invalide, +10 Attaque par défaut.")
            self.heros.attaque += 10

    def magasin(self):
        """Interface d'achat d'objets avec de l'or."""
        play_music(MUSIC_SHOP)  # On utilise bien la constante MUSIC_SHOP définie en haut du fichier
        play_sound_effect(SFX_SHOP_ENTER)
        print(f"\nBienvenue au magasin ! Vous avez {self.heros.or_} or.")
        print("Items disponibles :")
        for i, item in enumerate(items_disponibles):
            print(f"{i+1}. {item.nom} - Coût : {item.cout} or")
        print("0. Quitter le magasin")
        while True:
            choix = input("Choisissez un item à acheter (numéro) : ")
            if choix == "0":
                play_music(MUSIC_EXPLORATION) # Retour à la musique d'exploration
                break
            try:
                idx = int(choix) - 1
                item = items_disponibles[idx]
                if self.heros.or_ >= item.cout:
                    self.heros.or_ -= item.cout
                    self.heros.inventaire.append(item)
                    print(f"Acheté {item.nom}. Or restant : {self.heros.or_}")
                else:
                    print("Pas assez d'or.")
            except (ValueError, IndexError):
                print("Choix invalide.")

    def jouer(self):
        """Boucle principale d'une partie de jeu."""
        play_music(MUSIC_EXPLORATION)
        print("Bienvenue dans le RPG Python !")
        while True:
            ennemis = self.creer_vague()
            if not self.combat(ennemis):
                break
            if input("Continuer ? (o/n) : ").lower() != 'o':
                break
        stop_music()
        score = self._numero_vague - 1
        print(f"Score final : Vague {score}")
        if self.heros.est_vivant() and (not self._historique_scores or self._historique_scores[-1] != score):
            self._historique_scores.append(score)


# Point d'entrée principal
if __name__ == "__main__":
    menu = Menu()
    menu.lancer()