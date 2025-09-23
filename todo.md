En cours
===
Menu *(Voir retours)*

---
A faire
===
Sauvegarde des personnages
Refonte des classes de perso et monstres

**REFACTORING - Code Review (Priorité Haute)**

**1. Variables globales à refactoriser** ⚠️
- [ ] Créer une classe GameState pour centraliser les 34+ variables globales
- [ ] Regrouper les flags de sélection (selecPerso, selecNOM, selecPV, etc.) dans un dictionnaire
- [ ] Créer une classe GameManager pour orchestrer state, UI et combat

**2. Architecture des classes**
- [ ] Créer une classe abstraite Combattant comme classe de base
- [ ] Refactoriser la classe J (30k+ caractères) en :
  * Classe Joueur (données)
  * Classe CombatLogic (logique de combat)  
  * Classe PlayerUI (interface)
- [ ] Réduire la duplication de code entre J, Banshee, Night_walker

**3. Méthodes trop longues à découper**
- [ ] J.attack() : 10k caractères → découper en sous-méthodes
- [ ] J.defences() : 9k caractères → découper en sous-méthodes
- [ ] Bouton.affiche_bouton() : 4k caractères → séparer logique d'affichage

**4. Standards de code**
- [ ] Renommer classe J → Joueur
- [ ] Renommer classe Night_walker → NightWalker (PascalCase)
- [ ] Renommer fonction nbperso() → nombre_personnages()

**5. Gestion d'erreurs**
- [ ] Ajouter validation dans setpv(), setmana(), etc.
- [ ] Gérer les cas d'erreur dans les sliders (valeurs dépassant max)
- [ ] Ajouter try/catch pour le chargement des fichiers

**6. Organisation des fichiers**
- [ ] Créer constants.py pour COULEURS, TAILLES, etc.
- [ ] Séparer les classes d'interface dans ui_components.py
- [ ] Créer game_logic.py pour la logique de combat

---
Retours
===
- [ ] PV et Mana en un seul slider avec un texte clair et explicatif <br>
- [ ] Slider nb dépassé retour au max pré dépassage plus pop-up de validataion <br>
- [x] Règles au début <br>
- [x] Pour le gameplay le défilement du texte est chiant <br>
- [ ] Précision to chances de critique ou préciser que c'est un ajout à son taux de réussite de base. Ajouter une jauge de chance de crit pendant le choix de la précision. <br>
- [ ] Organiser le placement des textes et garder un historique des trois/quatres dernières actions ou ajouter un menu historique ouvrable avec h <br>
- [ ] Dégats et def entiers et non float <br>
- [ ] Ordre des opérations  :
* -[ ] But du jeu
* -[x] Régles du jeu
* -[ ] Conditions de victoire et de défaite

- [ ] Remplacer le menu quitter par un menu pour playtest. Son but est d'arriver à un gamestate precis pour tester différent éléments rapidement. <br>