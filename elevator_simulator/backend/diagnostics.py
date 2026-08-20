"""
Diagnostics Module - Module de diagnostic
Ce module fournit des outils pour diagnostiquer les pannes d'ascenseur.
"""

import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

from .elevator_system import (
    ElevatorSystem, Fault, FaultType, FaultSeverity,
    ElevatorComponent, ElevatorState
)


class DiagnosticLevel(Enum):
    """Niveaux de diagnostic"""
    QUICK = "quick"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class DiagnosticStatus(Enum):
    """États du diagnostic"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class DiagnosticTest:
    """Test de diagnostic"""
    name: str
    test_type: str
    description: str
    status: DiagnosticStatus = DiagnosticStatus.PENDING
    result: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def run(self, elevator: ElevatorSystem) -> bool:
        """Exécuter le test"""
        self.status = DiagnosticStatus.IN_PROGRESS
        self.timestamp = datetime.now()
        
        try:
            result = self._execute_test(elevator)
            self.result = "PASSED" if result else "FAILED"
            self.status = DiagnosticStatus.COMPLETED
            return result
        except Exception as e:
            self.result = f"ERROR: {str(e)}"
            self.status = DiagnosticStatus.ERROR
            return False
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Méthode à implémenter par les sous-classes"""
        raise NotImplementedError()


@dataclass
class ComponentStatusTest(DiagnosticTest):
    """Test de statut des composants"""
    
    def __post_init__(self):
        self.name = "Component Status Check"
        self.test_type = "component_status"
        self.description = "Vérifie le statut de tous les composants"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Vérifier le statut de tous les composants"""
        components = elevator.get_all_components()
        all_operational = True
        
        for comp in components:
            status = comp.status
            if status != "operational":
                all_operational = False
                self.details[comp.name] = {
                    'status': status,
                    'active_faults': len(comp.get_active_faults())
                }
            else:
                self.details[comp.name] = {'status': status}
        
        return all_operational


@dataclass
class FaultDetectionTest(DiagnosticTest):
    """Test de détection de pannes"""
    
    def __post_init__(self):
        self.name = "Fault Detection"
        self.test_type = "fault_detection"
        self.description = "Détecte les pannes actives dans le système"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Détecter les pannes actives"""
        active_faults = elevator.get_active_faults()
        
        if not active_faults:
            self.result = "No active faults detected"
            return True
        
        # Classer les pannes par sévérité
        critical_faults = [f for f in active_faults if f.severity == FaultSeverity.CRITICAL]
        major_faults = [f for f in active_faults if f.severity == FaultSeverity.MAJOR]
        moderate_faults = [f for f in active_faults if f.severity == FaultSeverity.MODERATE]
        minor_faults = [f for f in active_faults if f.severity == FaultSeverity.MINOR]
        
        self.details = {
            'total_active_faults': len(active_faults),
            'critical': len(critical_faults),
            'major': len(major_faults),
            'moderate': len(moderate_faults),
            'minor': len(minor_faults),
            'faults': [
                {
                    'type': f.fault_type.value,
                    'severity': f.severity.value,
                    'description': f.description,
                    'component': f.affected_component,
                    'timestamp': f.timestamp.isoformat()
                } for f in active_faults
            ]
        }
        
        # Si des pannes critiques ou majeures, le test échoue
        return len(critical_faults) == 0 and len(major_faults) == 0


@dataclass
class MotorTest(DiagnosticTest):
    """Test du moteur"""
    
    def __post_init__(self):
        self.name = "Motor System Test"
        self.test_type = "motor_test"
        self.description = "Test du système de moteur"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Tester le moteur"""
        motor = elevator.motor
        
        # Vérifier le statut
        if motor.status != "operational":
            self.details['status'] = motor.status
            self.details['active_faults'] = len(motor.get_active_faults())
            return False
        
        # Vérifier la température
        if motor.temperature > 80:  # Seuil critique
            self.details['temperature'] = motor.temperature
            self.details['issue'] = "Overheating"
            return False
        
        # Vérifier le courant
        if motor.current > motor.power * 1000 / motor.voltage * 1.5:  # 150% du courant nominal
            self.details['current'] = motor.current
            self.details['issue'] = "Overcurrent"
            return False
        
        self.details = {
            'temperature': motor.temperature,
            'current': motor.current,
            'voltage': motor.voltage,
            'power': motor.power
        }
        
        return True


@dataclass
class BrakeTest(DiagnosticTest):
    """Test du système de freinage"""
    
    def __post_init__(self):
        self.name = "Brake System Test"
        self.test_type = "brake_test"
        self.description = "Test du système de freinage"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Tester le frein"""
        brake = elevator.brake_system
        
        # Vérifier le statut
        if brake.status != "operational":
            self.details['status'] = brake.status
            return False
        
        # Vérifier l'engagement
        if elevator.state == ElevatorState.MOVING_UP or elevator.state == ElevatorState.MOVING_DOWN:
            if brake.is_engaged:
                self.details['issue'] = "Brake engaged while moving"
                return False
        
        self.details = {
            'is_engaged': brake.is_engaged,
            'brake_force': brake.brake_force
        }
        
        return True


@dataclass
class DoorTest(DiagnosticTest):
    """Test du système de portes"""
    
    def __post_init__(self):
        self.name = "Door System Test"
        self.test_type = "door_test"
        self.description = "Test du système de portes"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Tester les portes"""
        door = elevator.door_system
        
        # Vérifier le statut
        if door.status != "operational":
            self.details['status'] = door.status
            return False
        
        # Vérifier si obstacle détecté
        if door.obstacle_detected:
            self.details['issue'] = "Obstacle detected"
            return False
        
        # Vérifier la cohérence des états
        if door.is_open and (door.is_opening or door.is_closing):
            self.details['issue'] = "Inconsistent door state"
            return False
        
        self.details = {
            'is_open': door.is_open,
            'is_opening': door.is_opening,
            'is_closing': door.is_closing,
            'door_type': door.door_type,
            'obstacle_detected': door.obstacle_detected
        }
        
        return True


@dataclass
class SafetyTest(DiagnosticTest):
    """Test des systèmes de sécurité"""
    
    def __post_init__(self):
        self.name = "Safety Systems Test"
        self.test_type = "safety_test"
        self.description = "Test des systèmes de sécurité"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Tester les systèmes de sécurité"""
        all_passed = True
        
        # Vérifier le frein d'urgence
        if elevator.car.emergency_stop:
            if not elevator.brake_system.is_engaged:
                self.details['emergency_brake'] = "Not engaged during emergency stop"
                all_passed = False
        
        # Vérifier les pannes critiques
        critical_faults = [f for f in elevator.get_active_faults() 
                          if f.severity == FaultSeverity.CRITICAL]
        
        if critical_faults:
            if elevator.state != ElevatorState.EMERGENCY_STOP:
                self.details['critical_faults'] = "System not in emergency stop with critical faults"
                all_passed = False
        
        self.details['emergency_stop'] = elevator.car.emergency_stop
        self.details['brake_engaged'] = elevator.brake_system.is_engaged
        self.details['critical_faults_count'] = len(critical_faults)
        
        return all_passed


@dataclass
class CommunicationTest(DiagnosticTest):
    """Test de communication"""
    
    def __post_init__(self):
        self.name = "Communication Test"
        self.test_type = "communication_test"
        self.description = "Test de communication entre composants"
    
    def _execute_test(self, elevator: ElevatorSystem) -> bool:
        """Tester la communication"""
        control = elevator.control_system
        
        # Vérifier le statut
        if control.status != "operational":
            self.details['status'] = control.status
            return False
        
        # Vérifier les pannes de communication
        comm_faults = [f for f in elevator.get_active_faults() 
                      if f.fault_type == FaultType.COMMUNICATION_ERROR]
        
        if comm_faults:
            self.details['communication_faults'] = len(comm_faults)
            return False
        
        self.details['algorithm'] = control.algorithm
        self.details['active_faults'] = len(control.get_active_faults())
        
        return True


@dataclass
class DiagnosticEngine:
    """Moteur de diagnostic"""
    elevator: ElevatorSystem
    
    # Tests disponibles
    tests: Dict[str, DiagnosticTest] = field(default_factory=dict)
    
    # Historique des diagnostics
    diagnostic_history: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        self._init_tests()
    
    def _init_tests(self):
        """Initialiser les tests de diagnostic"""
        self.tests = {
            'component_status': ComponentStatusTest(),
            'fault_detection': FaultDetectionTest(),
            'motor': MotorTest(),
            'brake': BrakeTest(),
            'door': DoorTest(),
            'safety': SafetyTest(),
            'communication': CommunicationTest()
        }
    
    def run_test(self, test_name: str) -> Optional[DiagnosticTest]:
        """Exécuter un test spécifique"""
        if test_name not in self.tests:
            return None
        
        test = self.tests[test_name]
        result = test.run(self.elevator)
        
        # Enregistrer dans l'historique
        self._record_diagnostic(test_name, test)
        
        return test
    
    def run_all_tests(self) -> Dict[str, DiagnosticTest]:
        """Exécuter tous les tests"""
        results = {}
        for test_name, test in self.tests.items():
            test.run(self.elevator)
            results[test_name] = test
            self._record_diagnostic(test_name, test)
        
        return results
    
    def run_quick_diagnostic(self) -> Dict[str, Any]:
        """Exécuter un diagnostic rapide"""
        results = {}
        
        # Tests essentiels
        essential_tests = ['fault_detection', 'safety']
        for test_name in essential_tests:
            if test_name in self.tests:
                test = self.tests[test_name]
                test.run(self.elevator)
                results[test_name] = self._test_to_dict(test)
                self._record_diagnostic(test_name, test)
        
        return results
    
    def run_comprehensive_diagnostic(self) -> Dict[str, Any]:
        """Exécuter un diagnostic complet"""
        results = {}
        for test_name, test in self.tests.items():
            test.run(self.elevator)
            results[test_name] = self._test_to_dict(test)
            self._record_diagnostic(test_name, test)
        
        # Ajouter des informations système
        results['system_info'] = self._get_system_info()
        
        return results
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Obtenir les informations système"""
        return {
            'state': self.elevator.state.value,
            'current_floor': self.elevator.car.current_floor,
            'target_floor': self.elevator.car.target_floor,
            'direction': self.elevator.car.direction.value,
            'num_floors': self.elevator.num_floors,
            'active_faults': len(self.elevator.get_active_faults()),
            'total_faults': len(self.elevator.faults),
            'maintenance_mode': self.elevator.maintenance_mode
        }
    
    def _test_to_dict(self, test: DiagnosticTest) -> Dict[str, Any]:
        """Convertir un test en dictionnaire"""
        return {
            'name': test.name,
            'type': test.test_type,
            'status': test.status.value,
            'result': test.result,
            'details': test.details,
            'timestamp': test.timestamp.isoformat()
        }
    
    def _record_diagnostic(self, test_name: str, test: DiagnosticTest):
        """Enregistrer un diagnostic dans l'historique"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'test_name': test_name,
            'test_type': test.test_type,
            'status': test.status.value,
            'result': test.result,
            'details': test.details
        }
        self.diagnostic_history.append(record)
    
    def get_diagnostic_history(self, limit: int = 100) -> List[Dict]:
        """Obtenir l'historique des diagnostics"""
        return self.diagnostic_history[-limit:]
    
    def get_fault_diagnosis(self, fault: Fault) -> Dict[str, Any]:
        """Obtenir un diagnostic pour une panne spécifique"""
        diagnosis = {
            'fault_type': fault.fault_type.value,
            'severity': fault.severity.value,
            'description': fault.description,
            'affected_component': fault.affected_component,
            'timestamp': fault.timestamp.isoformat(),
            'is_resolved': fault.is_resolved,
            'recommended_actions': self._get_recommended_actions(fault),
            'possible_causes': self._get_possible_causes(fault),
            'estimated_repair_time': self._get_estimated_repair_time(fault)
        }
        
        if fault.resolution_time:
            diagnosis['resolution_time'] = fault.resolution_time.isoformat()
            diagnosis['duration'] = fault.get_duration()
        
        return diagnosis
    
    def _get_recommended_actions(self, fault: Fault) -> List[str]:
        """Obtenir les actions recommandées pour une panne"""
        actions = []
        
        # Actions générales
        if fault.severity in [FaultSeverity.CRITICAL, FaultSeverity.MAJOR]:
            actions.append("Arrêter immédiatement l'ascenseur")
            actions.append("Activer le mode maintenance")
            actions.append("Contacter le service technique")
        
        # Actions spécifiques par type de panne
        if fault.fault_type == FaultType.MOTOR_FAILURE:
            actions.append("Vérifier l'alimentation du moteur")
            actions.append("Tester le circuit de commande")
            actions.append("Inspecter les connexions électriques")
        
        elif fault.fault_type == FaultType.BRAKE_FAILURE:
            actions.append("Vérifier l'état des freins")
            actions.append("Tester le système de freinage d'urgence")
            actions.append("Inspecter les câbles de commande")
        
        elif fault.fault_type == FaultType.DOOR_SENSOR_FAILURE:
            actions.append("Nettoyer les capteurs de porte")
            actions.append("Vérifier les connexions des capteurs")
            actions.append("Tester le fonctionnement des capteurs")
        
        elif fault.fault_type == FaultType.POWER_SUPPLY_FAILURE:
            actions.append("Vérifier l'alimentation électrique")
            actions.append("Tester les fusibles et disjoncteurs")
            actions.append("Inspecter les câbles d'alimentation")
        
        elif fault.fault_type == FaultType.CABLE_ISSUE:
            actions.append("Inspecter visuellement les câbles")
            actions.append("Vérifier la tension des câbles")
            actions.append("Tester la résistance des câbles")
        
        elif fault.fault_type == FaultType.OVERHEATING:
            actions.append("Laisser refroidir le système")
            actions.append("Vérifier la ventilation")
            actions.append("Nettoyer les composants")
        
        return actions
    
    def _get_possible_causes(self, fault: Fault) -> List[str]:
        """Obtenir les causes possibles d'une panne"""
        causes = []
        
        if fault.fault_type == FaultType.MOTOR_FAILURE:
            causes = [
                "Court-circuit dans le moteur",
                "Surchauffe du moteur",
                "Défaillance du circuit de commande",
                "Problème d'alimentation",
                "Usure des balais (pour moteur à courant continu)"
            ]
        
        elif fault.fault_type == FaultType.BRAKE_FAILURE:
            causes = [
                "Usure des garnitures de frein",
                "Problème hydraulique (si frein hydraulique)",
                "Défaillance du système de commande",
                "Corrosion des composants",
                "Problème mécanique"
            ]
        
        elif fault.fault_type == FaultType.DOOR_SENSOR_FAILURE:
            causes = [
                "Saleté sur le capteur",
                "Alignement incorrect du capteur",
                "Défaillance électronique",
                "Problème de connexion",
                "Usure du capteur"
            ]
        
        elif fault.fault_type == FaultType.POWER_SUPPLY_FAILURE:
            causes = [
                "Coupure de courant",
                "Défaillance de l'onduleur",
                "Problème de batterie de secours",
                "Surcharge du circuit",
                "Défaillance du transformateur"
            ]
        
        elif fault.fault_type == FaultType.CABLE_ISSUE:
            causes = [
                "Usure des câbles",
                "Corrosion",
                "Surcharge mécanique",
                "Défaut de fabrication",
                "Mauvaise installation"
            ]
        
        elif fault.fault_type == FaultType.OVERHEATING:
            causes = [
                "Manque de ventilation",
                "Surcharge du système",
                "Fonctionnement prolongé",
                "Problème de refroidissement",
                "Environnement trop chaud"
            ]
        
        return causes
    
    def _get_estimated_repair_time(self, fault: Fault) -> str:
        """Obtenir le temps de réparation estimé"""
        if fault.severity == FaultSeverity.CRITICAL:
            return "4-8 heures"
        elif fault.severity == FaultSeverity.MAJOR:
            return "2-4 heures"
        elif fault.severity == FaultSeverity.MODERATE:
            return "1-2 heures"
        else:
            return "30-60 minutes"
    
    def generate_diagnostic_report(self) -> str:
        """Générer un rapport de diagnostic"""
        results = self.run_comprehensive_diagnostic()
        
        report = """
# Rapport de Diagnostic - Système d'Ascenseur

## Date: {date}

## État du Système
- **État**: {state}
- **Étage actuel**: {current_floor}
- **Direction**: {direction}
- **Mode maintenance**: {maintenance_mode}

## Pannes Actives
- **Total**: {total_faults}
- **Actives**: {active_faults}

{active_faults_details}

## Résultats des Tests

{fault_detection}

{component_status}

{motor_test}

{brake_test}

{door_test}

{safety_test}

{communication_test}

## Recommandations
{recommendations}

---
*Ce rapport a été généré automatiquement par le système de diagnostic*
"""
        
        # Remplir les placeholders
        system_info = results.get('system_info', {})
        
        report = report.format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            state=system_info.get('state', 'Unknown'),
            current_floor=system_info.get('current_floor', 'Unknown'),
            direction=system_info.get('direction', 'Unknown'),
            maintenance_mode="Oui" if system_info.get('maintenance_mode') else "Non",
            total_faults=system_info.get('total_faults', 0),
            active_faults=system_info.get('active_faults', 0),
            active_faults_details=self._format_active_faults(self.elevator.get_active_faults()),
            fault_detection=self._format_test_result(results.get('fault_detection', {})),
            component_status=self._format_test_result(results.get('component_status', {})),
            motor_test=self._format_test_result(results.get('motor', {})),
            brake_test=self._format_test_result(results.get('brake', {})),
            door_test=self._format_test_result(results.get('door', {})),
            safety_test=self._format_test_result(results.get('safety', {})),
            communication_test=self._format_test_result(results.get('communication', {})),
            recommendations=self._generate_recommendations(self.elevator)
        )
        
        return report
    
    def _format_active_faults(self, faults: List[Fault]) -> str:
        """Formater les pannes actives pour le rapport"""
        if not faults:
            return "Aucune panne active"
        
        lines = []
        for fault in faults:
            lines.append(f"  - **{fault.fault_type.value}** ({fault.severity.value}): {fault.description}")
            lines.append(f"    Composant: {fault.affected_component}")
            lines.append(f"    Date: {fault.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(lines)
    
    def _format_test_result(self, test: Dict) -> str:
        """Formater le résultat d'un test"""
        if not test:
            return ""
        
        status_emoji = "✓" if test.get('result') == "PASSED" else "✗"
        
        lines = [
            f"### {test.get('name', 'Unknown')}",
            f"- **Statut**: {status_emoji} {test.get('status', 'Unknown')}",
            f"- **Résultat**: {test.get('result', 'Unknown')}"
        ]
        
        if test.get('details'):
            lines.append("- **Détails**:")
            for key, value in test.get('details', {}).items():
                lines.append(f"  - {key}: {value}")
        
        return "\n".join(lines)
    
    def _generate_recommendations(self, elevator: ElevatorSystem) -> str:
        """Générer des recommandations"""
        recommendations = []
        
        active_faults = elevator.get_active_faults()
        if active_faults:
            recommendations.append("Résoudre les pannes actives avant de reprendre le service")
        
        if elevator.state == ElevatorState.EMERGENCY_STOP:
            recommendations.append("Investiguer la cause de l'arrêt d'urgence")
        
        if elevator.maintenance_mode:
            recommendations.append("Terminer les opérations de maintenance")
        
        if not recommendations:
            recommendations.append("Le système fonctionne normalement. Aucune action immédiate requise.")
        
        return "\n- ".join(recommendations)


if __name__ == "__main__":
    # Test du moteur de diagnostic
    from .elevator_system import create_default_elevator
    
    elevator = create_default_elevator(10)
    
    # Injecter quelques pannes
    from .fault_simulator import FaultType, FaultSeverity
    elevator.add_fault(Fault(
        FaultType.MOTOR_FAILURE,
        FaultSeverity.MAJOR,
        "Moteur principal défectueux",
        "Elevator Motor"
    ))
    
    # Créer le moteur de diagnostic
    diagnostic_engine = DiagnosticEngine(elevator)
    
    print("=== Diagnostic complet ===")
    results = diagnostic_engine.run_comprehensive_diagnostic()
    
    for test_name, test_data in results.items():
        if test_name != 'system_info':
            print(f"\n{test_name}:")
            print(f"  Résultat: {test_data['result']}")
            print(f"  Statut: {test_data['status']}")
    
    print("\n=== Rapport de diagnostic ===")
    report = diagnostic_engine.generate_diagnostic_report()
    print(report)
