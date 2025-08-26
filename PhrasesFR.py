phrasesClass = {
    "banshee": {
        "Name": "Banshee",
        "Hist": [
            "Vous arrivez dans une clairière illuminée par la lumière de la nuit et vous réjouissez d'être enfin dans un endroit traquille",
            "Après avoir mangé vous vous mettez au coin du feu, puis allez vous coucher",
            "Au beau millieu de la nuit vous vous reveillez sans savoir pourquoi vous avez cru enttendre un cri, mais plus aucun signe donc vous vous rendormez",
            "A peine rendormie que vous entendez à nouveau ce cri...",
            "Vous sortez de votre abri de fortune et vous retrouvez dans un épais brouillard",
            "Vous entendez des cries venant de toutes les directions",
            "Le brouillard semble se mettre à se concentrer en un point et commence à former une silouhette",
            "Vous vous retrouvez en face à face avec une banshee",
        ],
        "attack": {
            "noTarget": "Il n'y a aucun joueur à attaquer.",
            "prepare": "La banshee prépare son attaque",
            "norm": {
                "bas": [
                    "La banshee attaque le joueur ",
                    " en consommant peu de mana et lui inflige ",
                    " dégâts",
                ],
                "moy": [
                    "La banshee attaque le joueur ",
                    " en consommant une grande quantitée de mana et lui inflige ",
                    " dégâts",
                ],
                "haut": [
                    "La banshee sacrifie ses points de vie restant pour infliger ",
                    " dégâts à tous les joueurs",
                ],
                "noHaut": [
                    "La banshee a essayé de lancer son attaque la plus puissante en sacrifiant ces points de vie restant mais elle n'était pas assez affaiblie pour cette attaque et inflige donc ",
                    " dégâts à tous les joueurs",
                ],
            },
        },
        "defense": {
            "fail": [
                "Vous avez frappé dans la faille du bouclier de la banshee, elle subit donc les dégats de plein fouet équivalent à ",
                " dégâts",
            ],
            "succes": [
                "La banshee diminue les dégats reçus de 50 points avec son bouclier magique et subit ",
                " dégâts",
            ],
        },
        "infoBox": {
            "pv": " PV",
            "stats": "Stats :",
            "strength": "Force :",
            "defense": "Défense :",
            "mana": "Mana :",
            "precision": "Précision :",
        },
        "Fight": {
            "Lose": [
                "Les cries de la banshee ont réduit en charpie tous les aventuriers",
                "Fin de la partie",
            ],
            "HalfWin": "Vous avez gagnez au prix de la vie de vos camarades",
            "Win": "Félicitations, vous avez vaincu la banshee",
        },
    },
    "NW": {
        "Name": "Marcheur de la nuit",
        "Hist": [
            "Vous arrivez dans une salle obscure, plus obscure que la nuit la plus noir de toute votre vie",
            "Sortant de cette obscurité vous pouvez appercevoir celui que vous allez combattre",
            "L'ancien chevalier à l'armure noir, mort il y a de cela bien des années",
            "Le marcheur de la nuit",
        ],
        "attack": {
            "crit": {
                "phy": [
                    "Le marcheur de la nuit attaque ",
                    " rapidement et lui inflige un coup critique de ",
                    " dégâts",
                ],
                "reinf": [
                    "Le marcheur de la nuit attaque ",
                    " avec un objet lourd trouvé à coté faisant preuve d'une force surprenante et lui inflige ",
                    " dégâts",
                ],
                "mag": [
                    "Le marcheur de la nuit attaque ",
                    " rapidement et lui inflige un coup critique de ",
                    " dégâts avant de disparaitre dans l'obsurité",
                ],
            },
            "norm": {
                "phy": [
                    "Le marcheur de la nuit attaque ",
                    " rapidement et lui inflige ",
                    " dégâts",
                ],
                "reinf": [
                    "Le marcheur de la nuit attaque ",
                    " avec un objet lourd trouvé à coté et lui inflige ",
                    " dégâts",
                ],
                "mag": [
                    "Le marcheur de la nuit attaque ",
                    " rapidement et lui inflige ",
                    " dégâts avant de disparaitre dans l'obsurité",
                ],
            },
            "noTarget": "Il n'y a aucun joueur à attaquer.",
            "prepare": "Le marcheur de la nuit prépare son attaque",
            "fail": "Le marcheur de la nuit rate son attaque",
        },
        "defense": {
            "crit": {
                "phy": [
                    "Le marcheur de la nuit parvient à faire la meilleure défence possible et défend ",
                    " points de dégâts",
                ],
                "reinf": [
                    "Le marcheur de la nuit se défend et utilise de la mana afin de transformer de nombreuses parties de son corps en obscuritée et défend ",
                    " points de dégâts",
                ],
                "mag": "Le marcheur de la nuit transorme l'entièreté de son corps en ombre évite tout les dégâts",
            },
            "norm": {
                "phy": [
                    "Le marcheur de la nuit parvient à effectuer une très bonne défense et pare ",
                    " dégâts",
                ],
                "reinf": [
                    "Le marcheur de la nuit se défend et utilise de la mana afin de transformer certaines parties de son corps en obscuritée et défend ",
                    " points de dégâts",
                ],
                "mag": [
                    "Le marcheur de la nuit transorme de nombreuses parties de son corps en ombre évite ",
                    " dégâts",
                ],
            },
            "prepare": "Le marcheur de la nuit prépare sa défense",
            "shadowEscape": "Le marcheur de la nuit se déplace trop vite dans l'obscuritée et parvient à éviter vos attaques",
            "fail": "Le marcheur de la nuit rate sa défense",
        },
        "infoBox": {
            "pv": " PV",
            "stats": "Stats :",
            "strength": "Force :",
            "defense": "Défense :",
            "mana": "Mana :",
            "precision": "Précision :",
            "ombre": "Ombre :",
        },
        "Fight": {
            "Lose": ["Les ténèbres ont engloutie tous les joueurs", "Fin de la partie"],
            "HalfWin": "Vous avez gagnez au prix de la vie de vos camarades",
            "Win": "Félicitations, vous avez vaincu le marcheur de la nuit",
        },
    },
    "J": {
        "attack": {
            "crit": {
                "phy": ["Vous infligez ", " de dégats physique sur un coup critique"],
                "reinf": [
                    "Vous infligez ",
                    " de dégats physique sur un coup critique grâce à votre attaque renforcée au mana",
                ],
                "mag": [
                    "Vous infligez ",
                    " de dégats sur un coup critique avec votre attaque magique",
                ],
            },
            "norm": {
                "phy": ["Vous infligez ", " de dégats physique"],
                "reinf": [
                    "Vous infligez ",
                    " de dégats grâce à votre attaque renforcée au mana",
                ],
                "mag": ["Vous infligez ", " de dégats avec votre attaque magique"],
            },
            "fail": "Vous avez raté votre attaque",
            "attackType": ["Physique", "Renforcée", "Magique"],
        },
        "defense": {
            "crit": {
                "phy": [
                    "Vous défendez ",
                    " de dégats physique sur une défense parfaitement réussi",
                ],
                "reinf": [
                    "Vous défendez ",
                    " de dégats sur une défense enchanté des plus magnifiques",
                ],
                "mag": [
                    "Vous défendez ",
                    " de dégats sur une défense magique digne des plus grands mages",
                ],
            },
            "norm": {
                "phy": ["Vous défendez ", " de dégats physique"],
                "reinf": [
                    "Vous défendez ",
                    " de dégats grâce à votre défense enchantée",
                ],
                "mag": ["Vous défendez ", " de dégats avec votre défense magique"],
            },
            "fail": "Votre défense à raté et vous prenez l'attaque de plein fouet",
            "defenseType": ["Physique", "Enchantée", "Magique"],
        },
        "selection": {
            "atk": [
                "Veuillez séléctionner votre attaque ? ",
                "Vous allez utiliser une attaque ",
                "",
            ],
            "def": [
                "Veuillez séléctionner votre défense ? ",
                "Vous allez utiliser une défense ",
                "",
            ],
            "mana": [
                "Quelle quantité de mana souhaitez-vous utiliser ? ",
                ["Vous allez utiliser ", " points de mana"],
            ],
        },
        "infoBox": {
            "pv": " PV",
            "stats": "Stats :",
            "strength": "Force :",
            "defense": "Défense :",
            "mana": "Mana :",
            "precision": "Précision :",
        },
        "info": {
            "attack": [
                "Une attaque physique n'utilise pas de mana, une attaque renforcée utilise entre 1 et 50 de mana et une attaque magique entre 51 et 500 de mana (:"
            ],
            "defense": [
                "Une défense physique n'utilise pas de mana, une défense enchantée utilise entre 1 et 50 de mana et une défense magique entre 51 et 500 de mana (:"
            ],
        },
    },
    "Bouton": {
        "Play": "Jouer",
        "Quit": "Quitter",
        "Rules": "Compris",
        "Validate": "Valider",
        "BTN1": "1 Joueur",
        "BTN2": "2 Joueurs",
        "BTN3": "3 Joueurs",
        "BTN4": "4 Joueurs",
    },
    "Creation": {
        "NbPerso": [
            "Combien de joueurs voulez-vous créer ? (4 max)",
            "Vous avez choisi de jouer à : ",
        ],
        "Name": ["Quel est votre nom, aventurier ? ", "Votre nom est : "],
        "PV": ["Combien de points de vie avez vous ? ", ["Vous avez ", " PV"]],
        "Mana": [
            "Quelle est la taille de votre réserve de mana ?",
            ["Vous avez ", " mana"],
        ],
        "Stats": {
            "Question": "Quelles sont vos statistiques ? (Force / Défense / Précision)",
            "Response": {
                "Str": ["Vous avez ", " points de force"],
                "Def": ["Vous avez ", " points de défense"],
                "Prec": ["Vous avez ", " % de précision"],
            },
        },
    },
    "Boucle": {
        "Question": "Voullez-vous lancer une nouvelle partie ?",
        "Possibility": ["Oui", "Non"],
    },
}
