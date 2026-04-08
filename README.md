# Python-Little-RPG

Un petit projet de RPG en Python basé sur des principes de programmation orientée objet.

## Objectif
Créer un jeu de type arène avec :
- une classe abstraite `Entite` pour gérer les points de vie, l'attaque et la défense
- du **polymorphisme** avec des méthodes `attaquer()` propres à chaque ennemi
- de l'**héritage** entre `Entite`, `Heros` et `Ennemi`
- de l'**encapsulation** des attributs sensibles (`pv`, `attaque`, `defense`)
- une boucle de jeu dynamique gérée par la classe `Arene`

## Fonctionnalités
- Combat tour par tour : le héros choisit entre attaquer, utiliser une capacité spéciale ou se soigner
- Vagues d'ennemis avec montée en difficulté à chaque niveau
- Boss toutes les 5 vagues
- Récompenses entre les vagues : XP ou bonus de statistiques
- Progression du héros avec gain d'expérience et montée en niveau

## Classes principales
- `Entite` : classe de base abstraite pour toute créature vivante
- `Heros` : personnage contrôlé par le joueur, avec XP, niveaux et capacité spéciale
- `Ennemi` : classe mère des adversaires
- `Gobelin`, `Squelette`, `Mage`, `Loup` : types d'ennemis avec attaques spécifiques
- `Boss` : ennemi puissant avec compétence unique
- `Arene` : moteur du jeu, gestion des vagues, scaling et récompenses

## Exécution
1. Ouvrir un terminal dans le dossier du projet
2. Lancer le jeu avec :

```bash
python3 main.py
```

3. Suivre les instructions à l'écran pour entrer le nom du héros et choisir les actions pendant les combats.

## Organisation du projet
- `main.py` : code du jeu et classes principales
- `README.md` : documentation du projet

## Notes
Le jeu est conçu pour illustrer les concepts clés de la POO en Python dans un petit RPG textuel.
 
