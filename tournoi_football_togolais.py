import random
import os
import json
import logging
from datetime import datetime

class ConfigurationTournoi:
    """Gère la configuration et la persistance des données du tournoi."""
    def __init__(self, fichier_config='config_tournoi.json'):
        self.fichier_config = fichier_config
        self.configurations = self.charger_configuration()

    def charger_configuration(self):
        """Charge la configuration existante ou crée une nouvelle."""
        try:
            with open(self.fichier_config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'historique_matchs': [],
                'villes_utilisees': [],
                'regions_utilisees': []
            }

    def sauvegarder_configuration(self, donnees):
        """Sauvegarde la configuration du tournoi."""
        with open(self.fichier_config, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, ensure_ascii=False, indent=4)

class JournalTournoi:
    """Système de journalisation pour le tournoi."""
    def __init__(self, fichier_journal='journal_tournoi.log'):
        self.logger = logging.getLogger('TournoiFootball')
        self.logger.setLevel(logging.INFO)
        
        # Créer un gestionnaire de fichiers
        gestionnaire_fichier = logging.FileHandler(fichier_journal, encoding='utf-8')
        gestionnaire_fichier.setLevel(logging.INFO)
        
        # Créer un formateur
        formateur = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', 
                                      datefmt='%Y-%m-%d %H:%M:%S')
        gestionnaire_fichier.setFormatter(formateur)
        
        # Ajouter le gestionnaire au logger
        self.logger.addHandler(gestionnaire_fichier)

    def journal_match(self, type_match, ville1, region1, ville2, region2):
        """Enregistre les détails d'un match dans le journal."""
        message = (f"Match {type_match} : "
                   f"{ville1} ({region1}) vs {ville2} ({region2})")
        self.logger.info(message)

class TournoiFootballTogolais:
    """Classe principale de gestion du tournoi."""
    REGIONS = {
        "Maritime": ["Lomé", "Aného", "Tabligbo", "Vogan", "Tsévié"],
        "Plateaux": ["Atakpamé", "Kpalimé", "Badou", "Notsé"],
        "Centrale": ["Sokodé", "Tchamba", "Sotouboua"],
        "Kara": ["Kara", "Lama-Kara", "Kandé"],
        "Savanes": ["Dapaong", "Mango", "Tandjoaré"]
    }

    def __init__(self):
        self.configuration = ConfigurationTournoi()
        self.journal = JournalTournoi()
        self.villes_utilisees = set(self.configuration.configurations.get('villes_utilisees', []))
        self.regions_utilisees = set(self.configuration.configurations.get('regions_utilisees', []))

    def obtenir_ville_aleatoire(self, region_exclue=None, villes_exclues=None):
        """Sélectionne une ville aléatoire avec des contraintes sophistiquées."""
        if villes_exclues is None:
            villes_exclues = set()
        
        villes_possibles = []
        for region, villes in self.REGIONS.items():
            if region != region_exclue:
                villes_possibles.extend([
                    (ville, region) for ville in villes 
                    if ville not in self.villes_utilisees 
                    and ville not in villes_exclues
                ])
        
        # Réinitialisation intelligente si toutes les villes sont utilisées
        if not villes_possibles:
            self.villes_utilisees.clear()
            villes_possibles = [
                (ville, region) for region, villes in self.REGIONS.items()
                if region != region_exclue
                for ville in villes
            ]
        
        if not villes_possibles:
            raise ValueError("Aucune ville disponible pour la sélection.")
        
        return random.choice(villes_possibles)

    def jouer_kpessekou(self):
        """Génère un match Kpessekou avec des règles avancées."""
        print("\n--- 🏆 Sélection de Match Kpessekou 🏆 ---")
        
        # Sélection de la première ville
        ville1, region1 = self.obtenir_ville_aleatoire()
        self.villes_utilisees.add(ville1)
        self.regions_utilisees.add(region1)
        
        # Sélection de la deuxième ville dans une région différente
        ville2, region2 = self.obtenir_ville_aleatoire(region_exclue=region1)
        self.villes_utilisees.add(ville2)
        self.regions_utilisees.add(region2)
        
        # Journal du match
        self.journal.journal_match('Kpessekou', ville1, region1, ville2, region2)
        
        # Mise à jour de la configuration
        config = self.configuration.configurations
        config['historique_matchs'].append({
            'type': 'Kpessekou',
            'date': datetime.now().isoformat(),
            'ville1': ville1,
            'region1': region1,
            'ville2': ville2,
            'region2': region2
        })
        config['villes_utilisees'] = list(self.villes_utilisees)
        config['regions_utilisees'] = list(self.regions_utilisees)
        self.configuration.sauvegarder_configuration(config)
        
        print(f"🏟️ Ville de Playoff 1 : {ville1} (Région {region1})")
        print(f"🏟️ Ville de Playoff 2 : {ville2} (Région {region2})")
        
        return (ville1, region1), (ville2, region2)

    def jouer_zobibi(self):
        """Génère un match Zobibi avec des règles de validation avancées."""
        print("\n--- 🏆 Sélection de Match Zobibi 🏆 ---")
        
        # Validation et sélection des régions
        regions_disponibles = list(self.REGIONS.keys())
        
        while True:
            print("\nRégions disponibles :")
            for i, region in enumerate(regions_disponibles, 1):
                print(f"{i}. {region}")
            
            try:
                choix1 = int(input("\nSélectionnez la région 1 (numéro) : ")) - 1
                choix2 = int(input("Sélectionnez la région 2 (numéro) : ")) - 1
                
                if 0 <= choix1 < len(regions_disponibles) and 0 <= choix2 < len(regions_disponibles) and choix1 != choix2:
                    region1 = regions_disponibles[choix1]
                    region2 = regions_disponibles[choix2]
                    break
                else:
                    print("⚠️ Sélection invalide. Réessayez.")
            except (ValueError, IndexError):
                print("⚠️ Entrée invalide. Utilisez les numéros des régions.")
        
        # Sélection des villes
        ville1, _ = self.obtenir_ville_aleatoire(region_exclue=region2)
        ville2, _ = self.obtenir_ville_aleatoire(region_exclue=region1, villes_exclues={ville1})
        
        self.villes_utilisees.update([ville1, ville2])
        self.regions_utilisees.update([region1, region2])
        
        # Journal du match
        self.journal.journal_match('Zobibi', ville1, region1, ville2, region2)
        
        # Mise à jour de la configuration
        config = self.configuration.configurations
        config['historique_matchs'].append({
            'type': 'Zobibi',
            'date': datetime.now().isoformat(),
            'ville1': ville1,
            'region1': region1,
            'ville2': ville2,
            'region2': region2
        })
        config['villes_utilisees'] = list(self.villes_utilisees)
        config['regions_utilisees'] = list(self.regions_utilisees)
        self.configuration.sauvegarder_configuration(config)
        
        print(f"🏟️ Ville de Playoff 1 : {ville1} (Région {region1})")
        print(f"🏟️ Ville de Playoff 2 : {ville2} (Région {region2})")
        
        return (ville1, region1), (ville2, region2)

    def afficher_statistiques(self):
        """Affiche les statistiques détaillées du tournoi."""
        config = self.configuration.configurations
        historique = config.get('historique_matchs', [])
        
        print("\n--- 📊 Statistiques du Tournoi 📊 ---")
        print(f"Nombre total de matchs joués : {len(historique)}")
        
        # Répartition par type de match
        types_matchs = {}
        for match in historique:
            types_matchs[match['type']] = types_matchs.get(match['type'], 0) + 1
        
        print("\nRépartition des matchs :")
        for type_match, nombre in types_matchs.items():
            print(f"- {type_match}: {nombre} matchs")
        
        # Régions et villes utilisées
        print(f"\nNombre de régions utilisées : {len(self.regions_utilisees)}")
        print(f"Nombre de villes utilisées : {len(self.villes_utilisees)}")

    def menu_principal(self):
        """Menu principal interactif avec gestion des erreurs."""
        while True:
            print("\n--- Menu Principal ---")
            print("1. Jouer un match Kpessekou")
            print("2. Jouer un match Zobibi")
            print("3. Afficher statistiques du tournoi")
            print("4. Quitter")
            
            try:
                choix = int(input("Choisissez une option (1-4) : "))
                if choix == 1:
                    self.jouer_kpessekou()
                elif choix == 2:
                    self.jouer_zobibi()
                elif choix == 3:
                    self.afficher_statistiques()
                elif choix == 4:
                    print("Merci d'avoir utilisé le tournoi ! À bientôt !")
                    break
                else:
                    print("⚠️ Option invalide. Réessayez.")
            except ValueError:
                print("⚠️ Entrée invalide. Utilisez les chiffres 1 à 4.")

if __name__ == '__main__':
    tournoi = TournoiFootballTogolais()
    tournoi.menu_principal()
