# 🏢 Simulateur de Pannes d'Ascenseur

Un simulateur complet pour modéliser, diagnostiquer et visualiser les pannes d'ascenseur avec des modèles 3D interactifs.

## 📋 Table des Matières

- [📖 Introduction](#-introduction)
- [🛠️ Installation](#-installation)
- [🚀 Utilisation](#-utilisation)
- [🏗️ Architecture](#-architecture)
- [🎯 Fonctionnalités](#-fonctionnalités)
- [📦 Structure du Projet](#-structure-du-projet)
- [🔧 Configuration](#-configuration)
- [📊 Exemples](#-exemples)
- [📚 Documentation Technique](#-documentation-technique)
- [🤝 Contribution](#-contribution)
- [📜 Licence](#-licence)

---

## 📖 Introduction

Ce simulateur permet de :
- **Modéliser** un système d'ascenseur complet avec plusieurs étages
- **Simuler** différents types de pannes (mécaniques, électriques, de sécurité, logicielles)
- **Diagnostiquer** les problèmes avec des tests automatisés
- **Visualiser** en 3D la structure de l'ascenseur et les pannes
- **Exporter** les modèles 3D pour une analyse externe

Parfait pour la formation, le débogage, la maintenance prédictive et l'analyse de sécurité.

---

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

#### Installation de base (tout le simulateur)
```bash
pip install -r requirements.txt
```

#### Installation pour le backend uniquement
```bash
cd elevator_simulator/backend
pip install -r requirements.txt
```

#### Installation pour la visualisation 3D
```bash
cd elevator_simulator/models
pip install -r requirements.txt
```

#### Installation pour l'interface graphique
```bash
cd elevator_simulator/frontend
pip install -r requirements.txt
```

### Installation complète
```bash
# Depuis la racine du projet
pip install -r elevator_simulator/requirements.txt
```

---

## 🚀 Utilisation

### Interface en ligne de commande

```bash
# Démarrer l'interface console
python elevator_simulator/frontend/console_interface.py
```

### Interface graphique (PyQt5)

```bash
# Démarrer l'application graphique
python elevator_simulator/frontend/main_window.py
```

### Utilisation en tant que bibliothèque

```python
from elevator_simulator.backend.elevator_system import create_default_elevator
from elevator_simulator.backend.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from elevator_simulator.backend.diagnostics import DiagnosticEngine

# Créer un système d'ascenseur
elevator = create_default_elevator(num_floors=10)

# Créer un simulateur de pannes
simulator = FaultSimulator(elevator)

# Injecter une panne
simulator.inject_fault(
    FaultType.MOTOR_FAILURE,
    FaultSeverity.CRITICAL,
    "Moteur principal en panne",
    "Elevator Motor"
)

# Exécuter un diagnostic
diagnostic_engine = DiagnosticEngine(elevator)
results = diagnostic_engine.run_comprehensive_diagnostic()

# Afficher les résultats
for test_name, test_data in results.items():
    print(f"{test_name}: {test_data['result']}")
```

### Visualisation 3D

```python
from elevator_simulator.models.elevator_3d_model import Elevator3DModel

# Créer le modèle 3D
model = Elevator3DModel(elevator)

# Visualiser
model.visualize()

# Visualiser avec les pannes
model.visualize_faults()

# Exporter vers STL
model.export_to_stl("elevator_model.stl")
```

---

## 🏗️ Architecture

```
elevator_simulator/
├── backend/                  # Logique métier
│   ├── __init__.py
│   ├── elevator_system.py   # Système d'ascenseur principal
│   ├── fault_simulator.py   # Simulateur de pannes
│   └── diagnostics.py       # Moteur de diagnostic
│
├── models/                   # Modèles 3D
│   ├── __init__.py
│   ├── elevator_3d_model.py # Modèle 3D complet
│   └── requirements.txt
│
├── frontend/                 # Interfaces utilisateur
│   ├── __init__.py
│   ├── main_window.py       # Interface graphique (PyQt5)
│   ├── console_interface.py # Interface console
│   └── requirements.txt
│
├── docs/                     # Documentation
│   └── __init__.py
│
└── README.md                 # Documentation principale
```

---

## 🎯 Fonctionnalités

### 1. Simulation du Système d'Ascenseur

- **Modélisation complète** : Cabine, gaine, contrepoids, moteur, frein, portes, système de contrôle
- **Déplacement entre étages** : Simulation réaliste du mouvement
- **Gestion des portes** : Ouverture, fermeture, détection d'obstacles
- **Sécurité** : Arrêt d'urgence, freinage, détection de surcharge

### 2. Simulation de Pannes

#### Types de pannes supportés

**Pannes mécaniques :**
- Défaillance du moteur
- Défaillance du frein
- Problème de câble
- Défaillance du capteur de porte
- Défaillance du moteur de porte

**Pannes électriques :**
- Coupure d'alimentation
- Défaillance du circuit de contrôle
- Défaillance des capteurs
- Surcharge
- Court-circuit

**Pannes de sécurité :**
- Frein d'urgence activé
- Défaillance du système de sécurité
- Alarme incendie
- Surchauffe

**Pannes logicielles :**
- Bug logiciel
- Erreur de communication
- Défaillance du contrôleur

#### Scénarios prédéfinis

- Coupure de courant
- Surchauffe du moteur
- Porte bloquée
- Câble rompu
- Défaillance du contrôleur
- Urgence incendie
- Surcharge
- Défaillance des capteurs
- Défaillance du frein
- Erreur de communication

### 3. Diagnostic Automatique

- **Tests de composants** : Vérification du statut de tous les composants
- **Détection de pannes** : Identification et classification des pannes actives
- **Tests spécialisés** : Moteur, frein, portes, sécurité, communication
- **Diagnostic des pannes** : Causes possibles, actions recommandées, temps de réparation estimé
- **Rapport complet** : Génération de rapports de diagnostic détaillés

### 4. Visualisation 3D

- **Modèle 3D complet** : Représentation réaliste de l'ascenseur
- **Coloration par état** : Composants opérationnels vs défectueux
- **Visualisation des pannes** : Mise en évidence des composants en panne
- **Export** : STL, OBJ pour impression 3D ou analyse externe
- **Interactivité** : Rotation, zoom, sélection des composants

### 5. Interfaces Utilisateur

- **Interface graphique** : PyQt5 avec visualisation intégrée
- **Interface console** : Navigation par menu, contrôle complet
- **API Python** : Intégration dans d'autres applications

---

## 📦 Structure du Projet

### Backend

#### `elevator_system.py`

Classe principale du système d'ascenseur avec :

- **ElevatorSystem** : Système complet avec tous les composants
- **ElevatorCar** : Cabine d'ascenseur
- **ElevatorShaft** : Gaine d'ascenseur
- **Counterweight** : Contrepoids
- **Motor** : Moteur principal
- **BrakeSystem** : Système de freinage
- **DoorSystem** : Système de portes
- **ControlSystem** : Système de contrôle
- **Floor** : Étage de l'immeuble
- **Fault** : Représentation d'une panne

États possibles :
- IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPENING, DOOR_CLOSING, DOOR_OPEN, EMERGENCY_STOP, MAINTENANCE

#### `fault_simulator.py`

Simulateur de pannes avec :

- **FaultSimulator** : Classe principale pour injecter et gérer les pannes
- **SimulationMode** : MANUAL, AUTOMATIC, SCENARIO, STRESS_TEST
- **ScenarioType** : Types de scénarios prédéfinis
- **SimulationScenario** : Définition d'un scénario de simulation
- **StressTestSimulator** : Tests de résistance

#### `diagnostics.py`

Moteur de diagnostic avec :

- **DiagnosticEngine** : Moteur principal
- **DiagnosticTest** : Classe de base pour les tests
- **ComponentStatusTest** : Test de statut des composants
- **FaultDetectionTest** : Détection des pannes
- **MotorTest, BrakeTest, DoorTest, SafetyTest, CommunicationTest** : Tests spécialisés

### Models

#### `elevator_3d_model.py`

Modélisation 3D avec :

- **Elevator3DModel** : Modèle 3D complet
- **ColorScheme** : Schéma de couleurs pour la visualisation
- **MeshComponent** : Composant avec mesh 3D
- **InteractiveElevatorVisualizer** : Visualiseur interactif

Fonctionnalités :
- Création de tous les composants 3D
- Mise à jour des positions (cabine, contrepoids)
- Mise à jour des couleurs en fonction des pannes
- Visualisation avec PyVista
- Export vers STL/OBJ

### Frontend

#### `main_window.py`

Interface graphique PyQt5 avec :

- **ElevatorApp** : Application principale
- Panneaux : Contrôle, Visualisation 3D, Diagnostic
- Onglets : Pannes, Tests, Scénarios, Rapport
- Barre d'outils et barre de statut

#### `console_interface.py`

Interface console avec :

- **ConsoleInterface** : Interface principale
- Menus interactifs pour toutes les fonctionnalités
- Affichage coloré des informations
- Navigation intuitive

---

## 🔧 Configuration

### Configuration du système

```python
# Créer un ascenseur personnalisé
elevator = ElevatorSystem(
    num_floors=15,  # Nombre d'étages
    name="Main Elevator"
)

# Personnaliser les dimensions
elevator.shaft.width = 2.5  # Largeur de la gaine (m)
elevator.shaft.depth = 2.5  # Profondeur de la gaine (m)
elevator.shaft.height = 45  # Hauteur totale (m)

# Personnaliser la cabine
elevator.car.capacity = 12  # Nombre de personnes
elevator.car.max_speed = 2.5  # Vitesse maximale (m/s)
```

### Configuration du simulateur

```python
# Configurer le simulateur de pannes
simulator = FaultSimulator(elevator)
simulator.fault_probability = 0.05  # 5% de probabilité par seconde
simulator.min_fault_interval = 60.0  # 60 secondes minimum entre pannes
simulator.max_fault_interval = 300.0  # 5 minutes maximum entre pannes
```

### Configuration de la visualisation 3D

```python
# Configurer le modèle 3D
model = Elevator3DModel(elevator)
model.show_faults = True  # Montrer les pannes
model.show_labels = True  # Montrer les étiquettes
model.show_axes = True  # Montrer les axes
model.show_grid = True  # Montrer la grille
```

---

## 📊 Exemples

### Exemple 1 : Simulation simple

```python
from elevator_simulator.backend.elevator_system import create_default_elevator
from elevator_simulator.backend.fault_simulator import FaultType, FaultSeverity

# Créer un ascenseur
elevator = create_default_elevator(10)

# Déplacer vers un étage
elevator.send_to_floor(5)

# Injecter une panne
elevator.add_fault(Fault(
    FaultType.MOTOR_FAILURE,
    FaultSeverity.CRITICAL,
    "Moteur en panne",
    "Elevator Motor"
))

print(f"État: {elevator.state.value}")
print(f"Pannes actives: {len(elevator.get_active_faults())}")
```

### Exemple 2 : Diagnostic complet

```python
from elevator_simulator.backend.elevator_system import create_default_elevator
from elevator_simulator.backend.diagnostics import DiagnosticEngine

# Créer un ascenseur et un moteur de diagnostic
elevator = create_default_elevator(10)
diagnostic_engine = DiagnosticEngine(elevator)

# Exécuter un diagnostic complet
results = diagnostic_engine.run_comprehensive_diagnostic()

# Afficher les résultats
for test_name, test_data in results.items():
    if test_name != 'system_info':
        print(f"{test_data['name']}: {test_data['result']}")

# Générer un rapport
report = diagnostic_engine.generate_diagnostic_report()
print(report)
```

### Exemple 3 : Visualisation 3D

```python
from elevator_simulator.backend.elevator_system import create_default_elevator
from elevator_simulator.backend.fault_simulator import FaultType, FaultSeverity, Fault
from elevator_simulator.models.elevator_3d_model import Elevator3DModel

# Créer un ascenseur avec une panne
elevator = create_default_elevator(5)
elevator.add_fault(Fault(
    FaultType.MOTOR_FAILURE,
    FaultSeverity.MAJOR,
    "Moteur défectueux",
    "Elevator Motor"
))

# Créer et visualiser le modèle 3D
model = Elevator3DModel(elevator)
model.visualize()

# Visualiser avec les pannes en évidence
model.visualize_faults()
```

### Exemple 4 : Scénario de panne

```python
from elevator_simulator.backend.elevator_system import create_default_elevator
from elevator_simulator.backend.fault_simulator import FaultSimulator, ScenarioType

# Créer un ascenseur et un simulateur
elevator = create_default_elevator(10)
simulator = FaultSimulator(elevator)

# Exécuter un scénario d'urgence incendie
faults = simulator.run_scenario(ScenarioType.FIRE_EMERGENCY)

print(f"Scénario exécuté: {len(faults)} pannes injectées")
print(f"État du système: {elevator.state.value}")

# Afficher les pannes
for fault in faults:
    print(f"- {fault.fault_type.value}: {fault.description}")
```

### Exemple 5 : Simulation automatique

```python
from elevator_simulator.backend.elevator_system import create_default_elevator
from elevator_simulator.backend.fault_simulator import FaultSimulator, SimulationMode
import time

# Créer un ascenseur et un simulateur
elevator = create_default_elevator(10)
simulator = FaultSimulator(elevator)

# Configurer la simulation automatique
simulator.fault_probability = 0.02  # 2% de probabilité
simulator.min_fault_interval = 30.0
simulator.max_fault_interval = 180.0

# Démarrer la simulation
simulator.start_automatic_simulation()

# Exécuter pendant 60 secondes
for _ in range(60):
    simulator.update(1.0)
    print(f"Temps: {_+1}s | Pannes: {len(elevator.faults)} | État: {elevator.state.value}")
    time.sleep(1)

# Arrêter la simulation
simulator.stop_automatic_simulation()

# Afficher les statistiques
stats = simulator.get_simulation_stats()
print(f"\nStatistiques: {stats}")
```

---

## 📚 Documentation Technique

### Diagramme de classes

```
+------------------+       +---------------------+       +------------------+
|  ElevatorSystem  |       |   FaultSimulator   |       | DiagnosticEngine |
+------------------+       +---------------------+       +------------------+
| - num_floors     |       | - elevator          |       | - elevator       |
| - name           |       | - mode              |       | - tests          |
| - car            |       | - fault_probability|       | - history         |
| - shaft          |       | - simulation_speed |       +------------------+
| - counterweight  |       +---------------------+         | + run_test()     |
| - motor          |               |                         | + run_all_tests()|
| - brake_system   |               |                         | + generate_report()|
| - door_system    |               |                         +------------------+
| - control_system |       +---------------------+
| - state          |       | SimulationScenario |
| - faults         |       +---------------------+
+------------------+       | - name             |
| + get_component()|       | - scenario_type     |
| + add_fault()    |       | - description      |
| + inject_fault() |       | - faults           |
| + get_active_faults()|   | - duration        |
+------------------+       +---------------------+
        |
        v
+------------------+
| ElevatorCar      |
+------------------+
| - current_floor  |
| - target_floor   |
| - direction      |
| - speed          |
+------------------+
| + move_to_floor()|
| + update_position()|
+------------------+
```

### Types de données

#### FaultType (Énumération)

Pannes mécaniques :
- MOTOR_FAILURE
- BRAKE_FAILURE
- CABLE_ISSUE
- DOOR_SENSOR_FAILURE
- DOOR_MOTOR_FAILURE

Pannes électriques :
- POWER_SUPPLY_FAILURE
- CONTROL_CIRCUIT_FAILURE
- SENSOR_FAILURE
- OVERLOAD
- SHORT_CIRCUIT

Pannes de sécurité :
- EMERGENCY_BRAKE_ACTIVATED
- SAFETY_GEAR_FAILURE
- FIRE_ALARM
- OVERHEATING

Pannes logicielles :
- SOFTWARE_BUG
- COMMUNICATION_ERROR
- CONTROLLER_FAILURE

#### FaultSeverity (Énumération)

- MINOR
- MODERATE
- MAJOR
- CRITICAL

#### ElevatorState (Énumération)

- IDLE
- MOVING_UP
- MOVING_DOWN
- DOOR_OPENING
- DOOR_CLOSING
- DOOR_OPEN
- EMERGENCY_STOP
- MAINTENANCE

### Flux de travail

1. **Initialisation**
   - Créer un ElevatorSystem
   - Configurer les paramètres (nombre d'étages, dimensions, etc.)

2. **Simulation**
   - Déplacer la cabine entre les étages
   - Contrôler les portes
   - Injecter des pannes manuellement ou automatiquement

3. **Diagnostic**
   - Exécuter des tests de diagnostic
   - Analyser les pannes détectées
   - Générer des rapports

4. **Visualisation**
   - Visualiser le modèle 3D
   - Identifier visuellement les pannes
   - Exporter pour analyse externe

5. **Résolution**
   - Résoudre les pannes
   - Réinitialiser le système
   - Reprendre le fonctionnement normal

---

## 🤝 Contribution

Les contributions sont les bienvenues !

### Comment contribuer

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalité`)
3. Commiter vos changements (`git commit -m 'Ajout de la nouvelle fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/nouvelle-fonctionnalité`)
5. Ouvrir une Pull Request

### Idées de contribution

- Ajouter de nouveaux types de pannes
- Implémenter de nouveaux scénarios
- Améliorer la visualisation 3D
- Ajouter des tests unitaires
- Améliorer l'interface utilisateur
- Ajouter des fonctionnalités de monitoring en temps réel
- Intégrer avec des systèmes IoT

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- À tous ceux qui contribuent à l'open source
- Aux développeurs de PyVista pour la visualisation 3D
- À la communauté Python pour ses excellentes bibliothèques

---

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à contribuer au projet.

**Bon simulation !** 🚀
