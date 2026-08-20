"""
Console Interface - Interface en ligne de commande
Interface textuelle pour le simulateur d'ascenseur.
"""

import sys
import os
import time
import json
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.elevator_system import (
    ElevatorSystem, create_default_elevator, ElevatorState, 
    Fault, FaultType, FaultSeverity, Direction
)
from backend.fault_simulator import FaultSimulator, ScenarioType, SimulationMode
from backend.diagnostics import DiagnosticEngine


class ConsoleColors:
    """Couleurs pour l'interface console"""
    
    @staticmethod
    def red(text: str) -> str:
        return f"\033[91m{text}\033[0m"
    
    @staticmethod
    def green(text: str) -> str:
        return f"\033[92m{text}\033[0m"
    
    @staticmethod
    def yellow(text: str) -> str:
        return f"\033[93m{text}\033[0m"
    
    @staticmethod
    def blue(text: str) -> str:
        return f"\033[94m{text}\033[0m"
    
    @staticmethod
    def magenta(text: str) -> str:
        return f"\033[95m{text}\033[0m"
    
    @staticmethod
    def cyan(text: str) -> str:
        return f"\033[96m{text}\033[0m"
    
    @staticmethod
    def bold(text: str) -> str:
        return f"\033[1m{text}\033[0m"
    
    @staticmethod
    def header(text: str) -> str:
        return f"\033[1m\033[94m{text}\033[0m"
    
    @staticmethod
    def warning(text: str) -> str:
        return f"\033[1m\033[93m{text}\033[0m"
    
    @staticmethod
    def error(text: str) -> str:
        return f"\033[1m\033[91m{text}\033[0m"
    
    @staticmethod
    def success(text: str) -> str:
        return f"\033[1m\033[92m{text}\033[0m"


class ConsoleInterface:
    """Interface en ligne de commande pour le simulateur"""
    
    def __init__(self):
        self.elevator = create_default_elevator(10)
        self.simulator = FaultSimulator(self.elevator)
        self.diagnostic_engine = DiagnosticEngine(self.elevator)
        
        self.running = True
        self.simulation_mode = SimulationMode.MANUAL
    
    def display_header(self):
        """Afficher l'en-tête"""
        print("\n" + "=" * 60)
        print(ConsoleColors.header("SIMULATEUR DE PANNES D'ASCENSEUR"))
        print("=" * 60)
        print(f"Système: {self.elevator.name}")
        print(f"Nombre d'étages: {self.elevator.num_floors}")
        print("=" * 60)
    
    def display_status(self):
        """Afficher l'état actuel"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("ÉTAT DU SYSTÈME"))
        print("-" * 40)
        
        # État
        state_text = f"État: {self.elevator.state.value}"
        if self.elevator.state == ElevatorState.EMERGENCY_STOP:
            print(ConsoleColors.error(state_text))
        elif self.elevator.state in [ElevatorState.MOVING_UP, ElevatorState.MOVING_DOWN]:
            print(ConsoleColors.blue(state_text))
        elif self.elevator.state == ElevatorState.MAINTENANCE:
            print(ConsoleColors.yellow(state_text))
        else:
            print(state_text)
        
        # Position
        print(f"Position: Étage {self.elevator.car.current_floor} "
              f"(Cible: {self.elevator.car.target_floor})")
        print(f"Direction: {self.elevator.car.direction.value}")
        
        # Mode maintenance
        maintenance_text = f"Mode maintenance: {'Oui' if self.elevator.maintenance_mode else 'Non'}"
        if self.elevator.maintenance_mode:
            print(ConsoleColors.yellow(maintenance_text))
        else:
            print(maintenance_text)
        
        # Pannes
        active_faults = self.elevator.get_active_faults()
        total_faults = len(self.elevator.faults)
        
        if active_faults:
            print(ConsoleColors.error(f"Pannes actives: {len(active_faults)}/{total_faults}"))
        else:
            print(ConsoleColors.success(f"Pannes actives: {len(active_faults)}/{total_faults}"))
    
    def display_faults(self):
        """Afficher les pannes"""
        active_faults = self.elevator.get_active_faults()
        resolved_faults = [f for f in self.elevator.faults if f.is_resolved]
        
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("PANNES ACTIVES"))
        print("-" * 40)
        
        if not active_faults:
            print(ConsoleColors.success("Aucune panne active"))
        else:
            for i, fault in enumerate(active_faults):
                severity_color = {
                    FaultSeverity.CRITICAL: ConsoleColors.error,
                    FaultSeverity.MAJOR: ConsoleColors.red,
                    FaultSeverity.MODERATE: ConsoleColors.yellow,
                    FaultSeverity.MINOR: ConsoleColors.cyan
                }.get(fault.severity, lambda x: x)
                
                print(f"{i+1}. {severity_color(f'[{fault.severity.value}]')} {fault.fault_type.value}")
                print(f"   Composant: {fault.affected_component}")
                print(f"   Description: {fault.description}")
                print(f"   Date: {fault.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
        
        print("-" * 40)
        print(ConsoleColors.bold("PANNES RÉSOLUES"))
        print("-" * 40)
        
        if not resolved_faults:
            print("Aucune panne résolue")
        else:
            for i, fault in enumerate(resolved_faults):
                print(f"{i+1}. [{fault.severity.value}] {fault.fault_type.value}")
                print(f"   Composant: {fault.affected_component}")
                print(f"   Durée: {fault.get_duration():.2f} secondes")
                print()
    
    def display_menu(self):
        """Afficher le menu principal"""
        print("\n" + "=" * 60)
        print(ConsoleColors.header("MENU PRINCIPAL"))
        print("=" * 60)
        print("1.  Afficher l'état du système")
        print("2.  Contrôle manuel")
        print("3.  Gestion des pannes")
        print("4.  Diagnostic")
        print("5.  Scénarios")
        print("6.  Simulation automatique")
        print("7.  Visualisation 3D")
        print("8.  Quitter")
        print("=" * 60)
    
    def display_control_menu(self):
        """Afficher le menu de contrôle"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("CONTRÔLE MANUEL"))
        print("-" * 40)
        print("1.  Déplacer vers un étage")
        print("2.  Monter d'un étage")
        print("3.  Descendre d'un étage")
        print("4.  Ouvrir les portes")
        print("5.  Fermer les portes")
        print("6.  Arrêt d'urgence")
        print("7.  Réinitialiser l'arrêt d'urgence")
        print("8.  Basculer le mode maintenance")
        print("9.  Retour au menu principal")
        print("-" * 40)
    
    def display_faults_menu(self):
        """Afficher le menu des pannes"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("GESTION DES PANNES"))
        print("-" * 40)
        print("1.  Afficher les pannes")
        print("2.  Injecter une panne aléatoire")
        print("3.  Injecter une panne spécifique")
        print("4.  Résoudre une panne")
        print("5.  Résoudre toutes les pannes")
        print("6.  Effacer toutes les pannes")
        print("7.  Retour au menu principal")
        print("-" * 40)
    
    def display_diagnostic_menu(self):
        """Afficher le menu de diagnostic"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("DIAGNOSTIC"))
        print("-" * 40)
        print("1.  Exécuter un diagnostic complet")
        print("2.  Exécuter un test spécifique")
        print("3.  Afficher le diagnostic d'une panne")
        print("4.  Générer un rapport")
        print("5.  Retour au menu principal")
        print("-" * 40)
    
    def display_scenarios_menu(self):
        """Afficher le menu des scénarios"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("SCÉNARIOS"))
        print("-" * 40)
        
        scenarios = self.simulator.get_available_scenarios()
        for i, scenario in enumerate(scenarios):
            print(f"{i+1}.  {scenario['name']}")
            print(f"    Type: {scenario['type']}")
            print(f"    Durée: {scenario['duration']} secondes")
            print(f"    Pannes: {scenario['num_faults']}")
            print()
        
        print(f"{len(scenarios)+1}.  Retour au menu principal")
        print("-" * 40)
    
    def display_auto_sim_menu(self):
        """Afficher le menu de simulation automatique"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("SIMULATION AUTOMATIQUE"))
        print("-" * 40)
        print(f"Mode actuel: {self.simulation_mode.value}")
        print(f"Probabilité de panne: {self.simulator.fault_probability * 100:.1f}%")
        print("1.  Démarrer la simulation automatique")
        print("2.  Arrêter la simulation automatique")
        print("3.  Configurer la probabilité de panne")
        print("4.  Afficher les statistiques")
        print("5.  Retour au menu principal")
        print("-" * 40)
    
    def display_3d_menu(self):
        """Afficher le menu de visualisation 3D"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("VISUALISATION 3D"))
        print("-" * 40)
        print("1.  Visualiser le modèle 3D")
        print("2.  Visualiser les pannes en 3D")
        print("3.  Exporter le modèle 3D (STL)")
        print("4.  Exporter le modèle 3D (OBJ)")
        print("5.  Retour au menu principal")
        print("-" * 40)
    
    def get_input(self, prompt: str, input_type: type = str) -> any:
        """Obtenir une entrée utilisateur"""
        while True:
            try:
                value = input(prompt)
                if value.lower() == 'exit':
                    self.running = False
                    return None
                return input_type(value)
            except ValueError:
                print(ConsoleColors.error("Entrée invalide. Veuillez réessayer."))
    
    def handle_main_menu(self):
        """Gérer le menu principal"""
        while self.running:
            self.display_header()
            self.display_status()
            self.display_menu()
            
            choice = self.get_input("Choix: ", int)
            
            if choice == 1:
                self.display_status()
                self.display_faults()
            elif choice == 2:
                self.handle_control_menu()
            elif choice == 3:
                self.handle_faults_menu()
            elif choice == 4:
                self.handle_diagnostic_menu()
            elif choice == 5:
                self.handle_scenarios_menu()
            elif choice == 6:
                self.handle_auto_sim_menu()
            elif choice == 7:
                self.handle_3d_menu()
            elif choice == 8:
                self.running = False
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def handle_control_menu(self):
        """Gérer le menu de contrôle"""
        while self.running:
            self.display_control_menu()
            
            choice = self.get_input("Choix: ", int)
            
            if choice == 1:
                floor = self.get_input("Numéro d'étage (1-10): ", int)
                if 1 <= floor <= self.elevator.num_floors:
                    self.elevator.send_to_floor(floor)
                    self.elevator.car.current_floor = floor
                    print(ConsoleColors.success(f"Déplacement vers l'étage {floor}"))
                else:
                    print(ConsoleColors.error("Numéro d'étage invalide"))
            elif choice == 2:
                current = self.elevator.car.current_floor
                if current < self.elevator.num_floors:
                    self.elevator.send_to_floor(current + 1)
                    self.elevator.car.current_floor += 1
                    print(ConsoleColors.success(f"Montée à l'étage {current + 1}"))
                else:
                    print(ConsoleColors.error("Déjà au dernier étage"))
            elif choice == 3:
                current = self.elevator.car.current_floor
                if current > 1:
                    self.elevator.send_to_floor(current - 1)
                    self.elevator.car.current_floor -= 1
                    print(ConsoleColors.success(f"Descente à l'étage {current - 1}"))
                else:
                    print(ConsoleColors.error("Déjà au premier étage"))
            elif choice == 4:
                self.elevator.door_system.open()
                print(ConsoleColors.success("Ouverture des portes..."))
            elif choice == 5:
                self.elevator.door_system.close()
                print(ConsoleColors.success("Fermeture des portes..."))
            elif choice == 6:
                self.elevator.emergency_stop()
                print(ConsoleColors.error("ARRÊT D'URGENCE ACTIVÉ!"))
            elif choice == 7:
                self.elevator.reset_emergency()
                print(ConsoleColors.success("Arrêt d'urgence réinitialisé"))
            elif choice == 8:
                if self.elevator.maintenance_mode:
                    self.elevator.exit_maintenance_mode()
                    print(ConsoleColors.success("Mode maintenance désactivé"))
                else:
                    self.elevator.enter_maintenance_mode()
                    print(ConsoleColors.yellow("Mode maintenance activé"))
            elif choice == 9:
                break
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def handle_faults_menu(self):
        """Gérer le menu des pannes"""
        while self.running:
            self.display_faults_menu()
            
            choice = self.get_input("Choix: ", int)
            
            if choice == 1:
                self.display_faults()
            elif choice == 2:
                fault = self.simulator.inject_random_fault()
                print(ConsoleColors.warning(f"Panne injectée: {fault.fault_type.value} ({fault.severity.value})"))
                print(f"Composant: {fault.affected_component}")
            elif choice == 3:
                self.inject_specific_fault()
            elif choice == 4:
                self.resolve_fault()
            elif choice == 5:
                active_faults = self.elevator.get_active_faults()
                for i, fault in enumerate(active_faults):
                    self.elevator.resolve_fault(i)
                print(ConsoleColors.success(f"{len(active_faults)} panne(s) résolue(s)"))
            elif choice == 6:
                self.elevator.faults = []
                for comp in self.elevator.get_all_components():
                    comp.faults = []
                    comp.status = "operational"
                self.elevator.state = ElevatorState.IDLE
                print(ConsoleColors.success("Toutes les pannes ont été effacées"))
            elif choice == 7:
                break
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def inject_specific_fault(self):
        """Injecter une panne spécifique"""
        print("\nTypes de pannes disponibles:")
        for i, fault_type in enumerate(FaultType, 1):
            print(f"{i}. {fault_type.value}")
        
        fault_type_index = self.get_input("Type de panne: ", int)
        if fault_type_index is None:
            return
        
        fault_types = list(FaultType)
        if 1 <= fault_type_index <= len(fault_types):
            fault_type = fault_types[fault_type_index - 1]
        else:
            print(ConsoleColors.error("Type de panne invalide"))
            return
        
        print("\nSévérités disponibles:")
        for i, severity in enumerate(FaultSeverity, 1):
            print(f"{i}. {severity.value}")
        
        severity_index = self.get_input("Sévérité: ", int)
        if severity_index is None:
            return
        
        severities = list(FaultSeverity)
        if 1 <= severity_index <= len(severities):
            severity = severities[severity_index - 1]
        else:
            print(ConsoleColors.error("Sévérité invalide"))
            return
        
        description = self.get_input("Description: ")
        if description is None:
            return
        
        print("\nComposants disponibles:")
        components = self.elevator.get_all_components()
        for i, comp in enumerate(components, 1):
            print(f"{i}. {comp.name}")
        
        component_index = self.get_input("Composant: ", int)
        if component_index is None:
            return
        
        if 1 <= component_index <= len(components):
            component = components[component_index - 1]
            fault = self.simulator.inject_fault(
                fault_type, severity, description, component.name
            )
            print(ConsoleColors.warning(f"Panne injectée: {fault.fault_type.value}"))
        else:
            print(ConsoleColors.error("Composant invalide"))
    
    def resolve_fault(self):
        """Résoudre une panne"""
        active_faults = self.elevator.get_active_faults()
        
        if not active_faults:
            print(ConsoleColors.success("Aucune panne active à résoudre"))
            return
        
        print("\nPannes actives:")
        for i, fault in enumerate(active_faults):
            print(f"{i+1}. {fault.fault_type.value} ({fault.severity.value}) - {fault.affected_component}")
        
        fault_index = self.get_input("Numéro de la panne à résoudre: ", int)
        if fault_index is None:
            return
        
        if 1 <= fault_index <= len(active_faults):
            # Trouver l'index dans la liste complète des pannes
            for i, fault in enumerate(self.elevator.faults):
                if not fault.is_resolved and fault == active_faults[fault_index - 1]:
                    self.elevator.resolve_fault(i)
                    print(ConsoleColors.success("Panne résolue"))
                    break
        else:
            print(ConsoleColors.error("Numéro de panne invalide"))
    
    def handle_diagnostic_menu(self):
        """Gérer le menu de diagnostic"""
        while self.running:
            self.display_diagnostic_menu()
            
            choice = self.get_input("Choix: ", int)
            
            if choice == 1:
                self.run_full_diagnostic()
            elif choice == 2:
                self.run_specific_test()
            elif choice == 3:
                self.diagnose_fault()
            elif choice == 4:
                self.generate_report()
            elif choice == 5:
                break
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def run_full_diagnostic(self):
        """Exécuter un diagnostic complet"""
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("DIAGNOSTIC COMPLET"))
        print("-" * 40)
        
        results = self.diagnostic_engine.run_comprehensive_diagnostic()
        
        system_info = results.get('system_info', {})
        print(f"\nÉtat du système: {system_info.get('state', 'Unknown')}")
        print(f"Étage actuel: {system_info.get('current_floor', 'Unknown')}")
        print(f"Pannes actives: {system_info.get('active_faults', 0)}")
        
        print("\nRésultats des tests:")
        for test_name, test_data in results.items():
            if test_name != 'system_info':
                result = test_data.get('result', 'Unknown')
                if result == "PASSED":
                    print(f"  {ConsoleColors.success('✓')} {test_data.get('name', test_name)}: {result}")
                else:
                    print(f"  {ConsoleColors.error('✗')} {test_data.get('name', test_name)}: {result}")
    
    def run_specific_test(self):
        """Exécuter un test spécifique"""
        tests = [
            "component_status",
            "fault_detection",
            "motor",
            "brake",
            "door",
            "safety",
            "communication"
        ]
        
        print("\nTests disponibles:")
        for i, test_name in enumerate(tests, 1):
            test = self.diagnostic_engine.tests.get(test_name)
            if test:
                print(f"{i}. {test.name}")
        
        test_index = self.get_input("Numéro du test: ", int)
        if test_index is None:
            return
        
        if 1 <= test_index <= len(tests):
            test_name = tests[test_index - 1]
            test = self.diagnostic_engine.run_test(test_name)
            if test:
                print(f"\nRésultat: {test.result}")
                print(f"Statut: {test.status.value}")
                if test.details:
                    print("Détails:")
                    for key, value in test.details.items():
                        print(f"  {key}: {value}")
        else:
            print(ConsoleColors.error("Test invalide"))
    
    def diagnose_fault(self):
        """Diagnostiquer une panne"""
        active_faults = self.elevator.get_active_faults()
        
        if not active_faults:
            print(ConsoleColors.success("Aucune panne active à diagnostiquer"))
            return
        
        print("\nPannes actives:")
        for i, fault in enumerate(active_faults):
            print(f"{i+1}. {fault.fault_type.value} ({fault.severity.value})")
        
        fault_index = self.get_input("Numéro de la panne à diagnostiquer: ", int)
        if fault_index is None:
            return
        
        if 1 <= fault_index <= len(active_faults):
            diagnosis = self.diagnostic_engine.get_fault_diagnosis(active_faults[fault_index - 1])
            
            print("\n" + "-" * 40)
            print(ConsoleColors.bold("DIAGNOSTIC DE LA PANNE"))
            print("-" * 40)
            print(f"Type: {diagnosis['fault_type']}")
            print(f"Sévérité: {diagnosis['severity']}")
            print(f"Description: {diagnosis['description']}")
            print(f"Composant: {diagnosis['affected_component']}")
            print(f"Résolue: {'Oui' if diagnosis['is_resolved'] else 'Non'}")
            
            if not diagnosis['is_resolved']:
                print(f"\nTemps de réparation estimé: {diagnosis['estimated_repair_time']}")
                
                print("\nCauses possibles:")
                for i, cause in enumerate(diagnosis['possible_causes'], 1):
                    print(f"  {i}. {cause}")
                
                print("\nActions recommandées:")
                for i, action in enumerate(diagnosis['recommended_actions'], 1):
                    print(f"  {i}. {action}")
    
    def generate_report(self):
        """Générer un rapport"""
        report = self.diagnostic_engine.generate_diagnostic_report()
        print("\n" + "=" * 60)
        print(ConsoleColors.header("RAPPORT DE DIAGNOSTIC"))
        print("=" * 60)
        print(report)
        
        # Sauvegarder dans un fichier
        filename = f"elevator_diagnostic_{self.elevator.num_floors}floors_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nRapport sauvegardé dans {filename}")
    
    def handle_scenarios_menu(self):
        """Gérer le menu des scénarios"""
        while self.running:
            self.display_scenarios_menu()
            
            scenarios = self.simulator.get_available_scenarios()
            choice = self.get_input("Choix: ", int)
            
            if 1 <= choice <= len(scenarios):
                scenario = scenarios[choice - 1]
                scenario_type = ScenarioType(scenario['type'])
                
                print(f"\nExécution du scénario: {scenario['name']}")
                faults = self.simulator.run_scenario(scenario_type)
                print(f"Scénario terminé. {len(faults)} panne(s) injectée(s)")
            elif choice == len(scenarios) + 1:
                break
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def handle_auto_sim_menu(self):
        """Gérer le menu de simulation automatique"""
        while self.running:
            self.display_auto_sim_menu()
            
            choice = self.get_input("Choix: ", int)
            
            if choice == 1:
                self.simulation_mode = SimulationMode.AUTOMATIC
                self.simulator.start_automatic_simulation()
                print(ConsoleColors.success("Simulation automatique démarrée"))
                self.run_auto_simulation()
            elif choice == 2:
                self.simulation_mode = SimulationMode.MANUAL
                self.simulator.stop_automatic_simulation()
                print(ConsoleColors.success("Simulation automatique arrêtée"))
            elif choice == 3:
                probability = self.get_input("Probabilité de panne (1-100): ", int)
                if probability is not None:
                    self.simulator.fault_probability = probability / 100.0
                    print(f"Probabilité définie à {probability}%")
            elif choice == 4:
                self.display_stats()
            elif choice == 5:
                break
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def run_auto_simulation(self):
        """Exécuter la simulation automatique"""
        print("\nSimulation automatique en cours...")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        try:
            while self.simulation_mode == SimulationMode.AUTOMATIC and self.running:
                self.simulator.update(1.0)  # 1 seconde
                time.sleep(1.0)
                
                # Afficher l'état périodiquement
                if len(self.elevator.faults) % 5 == 0:
                    self.display_status()
        except KeyboardInterrupt:
            self.simulation_mode = SimulationMode.MANUAL
            self.simulator.stop_automatic_simulation()
            print("\nSimulation arrêtée")
    
    def display_stats(self):
        """Afficher les statistiques"""
        stats = self.simulator.get_simulation_stats()
        
        print("\n" + "-" * 40)
        print(ConsoleColors.bold("STATISTIQUES DE SIMULATION"))
        print("-" * 40)
        print(f"Mode: {stats['mode']}")
        print(f"Durée: {stats['simulation_duration']:.2f} secondes")
        print(f"Pannes totales: {stats['total_faults']}")
        print(f"Pannes actives: {stats['active_faults']}")
        print(f"Pannes résolues: {stats['resolved_faults']}")
        
        print("\nPar type:")
        for fault_type, count in stats['fault_type_counts'].items():
            print(f"  {fault_type}: {count}")
        
        print("\nPar sévérité:")
        for severity, count in stats['severity_counts'].items():
            print(f"  {severity}: {count}")
    
    def handle_3d_menu(self):
        """Gérer le menu de visualisation 3D"""
        while self.running:
            self.display_3d_menu()
            
            choice = self.get_input("Choix: ", int)
            
            if choice == 1:
                self.show_3d_model()
            elif choice == 2:
                self.show_3d_faults()
            elif choice == 3:
                self.export_3d_model("stl")
            elif choice == 4:
                self.export_3d_model("obj")
            elif choice == 5:
                break
            else:
                print(ConsoleColors.error("Choix invalide"))
    
    def show_3d_model(self):
        """Afficher le modèle 3D"""
        try:
            from models.elevator_3d_model import Elevator3DModel
            model = Elevator3DModel(self.elevator)
            model.visualize()
        except ImportError as e:
            print(ConsoleColors.error(f"Impossible de charger PyVista: {e}"))
            print("Installez PyVista avec: pip install pyvista")
    
    def show_3d_faults(self):
        """Afficher les pannes en 3D"""
        try:
            from models.elevator_3d_model import Elevator3DModel
            model = Elevator3DModel(self.elevator)
            model.visualize_faults()
        except ImportError as e:
            print(ConsoleColors.error(f"Impossible de charger PyVista: {e}"))
    
    def export_3d_model(self, format: str):
        """Exporter le modèle 3D"""
        try:
            from models.elevator_3d_model import Elevator3DModel
            model = Elevator3DModel(self.elevator)
            
            filename = f"elevator_model_{int(time.time())}.{format}"
            
            if format == "stl":
                model.export_to_stl(filename)
            else:
                model.export_to_obj(filename)
            
            print(ConsoleColors.success(f"Modèle exporté vers {filename}"))
        except ImportError as e:
            print(ConsoleColors.error(f"Impossible d'exporter le modèle: {e}"))
    
    def run(self):
        """Exécuter l'interface console"""
        print("\n" + "=" * 60)
        print(ConsoleColors.header("BIENVENUE DANS LE SIMULATEUR DE PANNES D'ASCENSEUR"))
        print("=" * 60)
        print("Tapez 'exit' à tout moment pour quitter")
        
        self.handle_main_menu()
        
        print("\n" + "=" * 60)
        print(ConsoleColors.success("MERCI D'AVOIR UTILISÉ LE SIMULATEUR"))
        print("=" * 60)


def main():
    """Point d'entrée de l'application console"""
    interface = ConsoleInterface()
    interface.run()


if __name__ == "__main__":
    main()
