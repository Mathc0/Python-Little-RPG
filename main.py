import random
from abc import ABC, abstractmethod

class Entite(ABC):
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
        degats_reels = max(0, degats - self._defense)
        self._pv -= degats_reels
        return degats_reels

    @abstractmethod
    def attaquer(self, cible):
        pass

class Heros(Entite):
    def __init__(self, nom, pv=100, attaque=20, defense=5):
        super().__init__(nom, pv, attaque, defense)
        self._niveau = 1
        self._xp = 0
        self._xp_prochain_niveau = 100
        self._capacite_speciale = "Coup Puissant"  # Exemple de capacité spéciale

    @property
    def niveau(self):
        return self._niveau

    @property
    def xp(self):
        return self._xp

    @property
    def capacite_speciale(self):
        return self._capacite_speciale

    def gagner_xp(self, xp):
        self._xp += xp
        while self._xp >= self._xp_prochain_niveau:
            self.monter_niveau()

    def monter_niveau(self):
        self._niveau += 1
        self._xp -= self._xp_prochain_niveau
        self._xp_prochain_niveau = int(self._xp_prochain_niveau * 1.5)
        self._pv_max += 10
        self._pv = self._pv_max
        self._attaque += 5
        self._defense += 2
        print(f"{self.nom} monte au niveau {self._niveau} !")

    def attaquer(self, cible):
        degats = self._attaque + random.randint(-2, 2)
        cible.recevoir_degats(degats)
        print(f"{self.nom} attaque {cible.nom} pour {degats} dégâts !")

    def capacite_speciale_action(self, cible):
        degats = self._attaque * 2 + random.randint(0, 5)
        cible.recevoir_degats(degats)
        print(f"{self.nom} utilise {self._capacite_speciale} sur {cible.nom} pour {degats} dégâts !")

    def soin(self):
        soin = 20
        self._pv = min(self._pv_max, self._pv + soin)
        print(f"{self.nom} se soigne pour {soin} PV. PV actuel : {self._pv}/{self._pv_max}")

class Ennemi(Entite):
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
        # Polymorphisme : chaque type d'ennemi a une attaque différente
        if self._type == "Gobelin":
            degats = self._attaque + random.randint(-1, 1)
            cible.recevoir_degats(degats)
            print(f"{self.nom} (Gobelin) attaque {cible.nom} pour {degats} dégâts !")
        elif self._type == "Orc":
            degats = self._attaque + random.randint(0, 3)
            cible.recevoir_degats(degats)
            print(f"{self.nom} (Orc) charge {cible.nom} pour {degats} dégâts !")
        elif self._type == "Sorcier":
            degats = self._attaque + random.randint(1, 4)
            cible.recevoir_degats(degats)
            print(f"{self.nom} (Sorcier) lance un sort sur {cible.nom} pour {degats} dégâts !")
        else:
            degats = self._attaque
            cible.recevoir_degats(degats)
            print(f"{self.nom} attaque {cible.nom} pour {degats} dégâts !")

class Boss(Ennemi):
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
        # Attaque spéciale pour le boss
        degats = int(self._attaque * 1.5) + random.randint(0, 5)
        cible.recevoir_degats(degats)
        print(f"{self.nom} (Boss) utilise {self._competence_unique} sur {cible.nom} pour {degats} dégâts !")

class Arene:
    def __init__(self):
        self._numero_vague = 1
        self._historique_scores = []
        self.heros = Heros("Héros")

    def creer_vague(self):
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
            butin_xp = 20 + self._numero_vague * 5
            ennemi = Ennemi(f"{type_ennemi} {i+1}", pv, attaque, defense, type_ennemi, butin_xp)
            ennemis.append(ennemi)

        # Boss toutes les 5 vagues
        if self._numero_vague % 5 == 0:
            boss = Boss("Boss Dragon", 200 + self._numero_vague * 20, 30 + self._numero_vague * 5, 10 + self._numero_vague * 2, "Boss", 100 + self._numero_vague * 10, "Souffle de Feu", 2.0)
            ennemis.append(boss)

        return ennemis

    def combat(self, ennemis):
        print(f"\n--- Vague {self._numero_vague} ---")
        while self.heros.est_vivant() and any(e.est_vivant() for e in ennemis):
            print(f"\n{self.heros.nom} : PV {self.heros.pv}/{self.heros.pv_max}")
            for ennemi in ennemis:
                if ennemi.est_vivant():
                    print(f"{ennemi.nom} ({ennemi.type}) : PV {ennemi.pv}")

            # Tour du héros
            action = input("Choisissez une action : 1. Attaque 2. Capacité Spéciale 3. Soin : ")
            if action == "1":
                cible = random.choice([e for e in ennemis if e.est_vivant()])
                self.heros.attaquer(cible)
            elif action == "2":
                cible = random.choice([e for e in ennemis if e.est_vivant()])
                self.heros.capacite_speciale_action(cible)
            elif action == "3":
                self.heros.soin()
            else:
                print("Action invalide, attaque par défaut.")
                cible = random.choice([e for e in ennemis if e.est_vivant()])
                self.heros.attaquer(cible)

            # Tours des ennemis
            for ennemi in ennemis:
                if ennemi.est_vivant():
                    ennemi.attaquer(self.heros)
                    if not self.heros.est_vivant():
                        break

        if self.heros.est_vivant():
            print(f"\nVictoire de la vague {self._numero_vague} !")
            xp_total = sum(e.butin_xp for e in ennemis)
            self.heros.gagner_xp(xp_total)
            print(f"XP gagné : {xp_total}")
            self.recompense()
            self._numero_vague += 1
        else:
            print(f"\nDéfaite à la vague {self._numero_vague}.")
            self._historique_scores.append(self._numero_vague - 1)
            return False
        return True

    def recompense(self):
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
            self.heros._pv_max += 20
            print("PV Max augmentés !")
        else:
            print("Choix invalide, +10 Attaque par défaut.")
            self.heros.attaque += 10

    def jouer(self):
        print("Bienvenue dans le RPG Python !")
        while True:
            ennemis = self.creer_vague()
            if not self.combat(ennemis):
                break
            if input("Continuer ? (o/n) : ").lower() != 'o':
                break
        print(f"Score final : Vague {self._numero_vague - 1}")
        self._historique_scores.append(self._numero_vague - 1)

if __name__ == "__main__":
    arene = Arene()
    arene.jouer()