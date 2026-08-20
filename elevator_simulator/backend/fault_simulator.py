"""
Fault Simulator - Simulateur de pannes
Ce module permet de simuler différents types de pannes sur un système d'ascenseur.
"""

import random
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from .elevator_system import (
    ElevatorSystem, ElevatorState, Fault, FaultType, FaultSeverity,
    ElevatorComponent, Direction
)


class SimulationMode(Enum):
    """Modes de simulation"""
    MANUAL = "manual"  # Injection manuelle de pannes
    AUTOMATIC = "automatic"  # Injection automatique aléatoire
    SCENARIO = "scenario"  # Scénarios prédéfinis
    STRESS_TEST = "stress_test"  # Test de résistance


class ScenarioType(Enum):
    """Types de scénarios prédéfinis"""
    POWER_OUTAGE = "power_outage"
    MOTOR_OVERHEAT = "motor_overheat"
    DOOR_JAM = "door_jam"
    CABLE_SNAP = "cable_snap"
    CONTROL_FAILURE = "control_failure"
    FIRE_EMERGENCY = "fire_emergency"
    OVERLOAD = "overload"
    SENSOR_FAILURE = "sensor_failure"
    BRAKE_FAILURE = "brake_failure"
    COMMUNICATION_ERROR = "communication_error"


@dataclass
class SimulationScenario:
    """Scénario de simulation prédéfini"""
    name: str
    scenario_type: ScenarioType
    description: str
    faults: List[Dict] = field(default_factory=list)
    duration: float = 60.0  # Durée en secondes
    
    def apply_to_elevator(self, elevator: ElevatorSystem) -> List[Fault]:
        """Appliquer le scénario à un système d'ascenseur"""
        applied_faults = []
        for fault_data in self.faults:
            fault = Fault(
                fault_type=FaultType(fault_data['type']),
                severity=FaultSeverity(fault_data['severity']),
                description=fault_data['description'],
                affected_component=fault_data.get('component', '')
            )
            elevator.add_fault(fault)
            applied_faults.append(fault)
        return applied_faults


@dataclass
class FaultSimulator:
    """Simulateur de pannes"""
    elevator: ElevatorSystem
    mode: SimulationMode = SimulationMode.MANUAL
    simulation_speed: float = 1.0  # Multiplicateur de vitesse
    
    # Paramètres de simulation automatique
    fault_probability: float = 0.01  # Probabilité par seconde
    min_fault_interval: float = 30.0  # Intervalle minimum entre pannes (s)
    max_fault_interval: float = 300.0  # Intervalle maximum entre pannes (s)
    
    # Historique
    simulation_history: List[Dict] = field(default_factory=list)
    
    # Scénarios prédéfinis
    scenarios: Dict[ScenarioType, SimulationScenario] = field(default_factory=dict)
    
    # Callbacks
    on_fault_injected: Optional[Callable[[Fault], None]] = None
    on_fault_resolved: Optional[Callable[[Fault], None]] = None
    on_state_changed: Optional[Callable[[ElevatorState], None]] = None
    
    def __post_init__(self):
        self._last_fault_time = 0.0
        self._simulation_start_time = datetime.now()
        self._init_scenarios()
    
    def _init_scenarios(self):
        """Initialiser les scénarios prédéfinis"""
        self.scenarios = {
            ScenarioType.POWER_OUTAGE: SimulationScenario(
                name="Coupure de courant",
                scenario_type=ScenarioType.POWER_OUTAGE,
                description="Coupure complète de l'alimentation électrique",
                faults=[
                    {
                        'type': FaultType.POWER_SUPPLY_FAILURE.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Perte complète de l\'alimentation électrique',
                        'component': 'Elevator System'
                    },
                    {
                        'type': FaultType.CONTROLLER_FAILURE.value,
                        'severity': FaultSeverity.MAJOR.value,
                        'description': 'Contrôleur hors tension',
                        'component': 'Control System'
                    }
                ],
                duration=120.0
            ),
            ScenarioType.MOTOR_OVERHEAT: SimulationScenario(
                name="Surchauffe du moteur",
                scenario_type=ScenarioType.MOTOR_OVERHEAT,
                description="Surchauffe du moteur principal",
                faults=[
                    {
                        'type': FaultType.OVERHEATING.value,
                        'severity': FaultSeverity.MAJOR.value,
                        'description': 'Température du moteur dépassant le seuil critique',
                        'component': 'Elevator Motor'
                    },
                    {
                        'type': FaultType.SENSOR_FAILURE.value,
                        'severity': FaultSeverity.MODERATE.value,
                        'description': 'Capteur de température défectueux',
                        'component': 'Elevator Motor'
                    }
                ],
                duration=90.0
            ),
            ScenarioType.DOOR_JAM: SimulationScenario(
                name="Porte bloquée",
                scenario_type=ScenarioType.DOOR_JAM,
                description="Obstacle bloquant la fermeture des portes",
                faults=[
                    {
                        'type': FaultType.DOOR_SENSOR_FAILURE.value,
                        'severity': FaultSeverity.MODERATE.value,
                        'description': 'Capteur de porte bloqué',
                        'component': 'Door System'
                    },
                    {
                        'type': FaultType.OBSTACLE_DETECTED.value,
                        'severity': FaultSeverity.MINOR.value,
                        'description': 'Obstacle détecté dans l\'ouverture de la porte',
                        'component': 'Door System'
                    }
                ],
                duration=60.0
            ),
            ScenarioType.CABLE_SNAP: SimulationScenario(
                name="Câble rompu",
                scenario_type=ScenarioType.CABLE_SNAP,
                description="Rupture d'un câble de traction",
                faults=[
                    {
                        'type': FaultType.CABLE_ISSUE.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Câble de traction principal rompu',
                        'component': 'Elevator Car'
                    },
                    {
                        'type': FaultType.SAFETY_GEAR_FAILURE.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Système de sécurité activé',
                        'component': 'Brake System'
                    }
                ],
                duration=30.0
            ),
            ScenarioType.CONTROL_FAILURE: SimulationScenario(
                name="Défaillance du contrôleur",
                scenario_type=ScenarioType.CONTROL_FAILURE,
                description="Défaillance du système de contrôle principal",
                faults=[
                    {
                        'type': FaultType.CONTROLLER_FAILURE.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Contrôleur principal hors service',
                        'component': 'Control System'
                    },
                    {
                        'type': FaultType.COMMUNICATION_ERROR.value,
                        'severity': FaultSeverity.MAJOR.value,
                        'description': 'Perte de communication entre composants',
                        'component': 'Control System'
                    }
                ],
                duration=180.0
            ),
            ScenarioType.FIRE_EMERGENCY: SimulationScenario(
                name="Urgence incendie",
                scenario_type=ScenarioType.FIRE_EMERGENCY,
                description="Détection d'incendie dans la gaine",
                faults=[
                    {
                        'type': FaultType.FIRE_ALARM.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Alarme incendie déclenchée',
                        'component': 'Elevator System'
                    },
                    {
                        'type': FaultType.EMERGENCY_BRAKE_ACTIVATED.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Frein d\'urgence activé',
                        'component': 'Brake System'
                    }
                ],
                duration=300.0
            ),
            ScenarioType.OVERLOAD: SimulationScenario(
                name="Surcharge",
                scenario_type=ScenarioType.OVERLOAD,
                description="Dépassement de la charge maximale",
                faults=[
                    {
                        'type': FaultType.OVERLOAD.value,
                        'severity': FaultSeverity.MAJOR.value,
                        'description': 'Charge dépassant la capacité maximale',
                        'component': 'Elevator Car'
                    },
                    {
                        'type': FaultType.MOTOR_FAILURE.value,
                        'severity': FaultSeverity.MODERATE.value,
                        'description': 'Moteur surchargé',
                        'component': 'Elevator Motor'
                    }
                ],
                duration=120.0
            ),
            ScenarioType.SENSOR_FAILURE: SimulationScenario(
                name="Défaillance des capteurs",
                scenario_type=ScenarioType.SENSOR_FAILURE,
                description="Défaillance multiple des capteurs",
                faults=[
                    {
                        'type': FaultType.SENSOR_FAILURE.value,
                        'severity': FaultSeverity.MODERATE.value,
                        'description': 'Capteur de position défectueux',
                        'component': 'Elevator Car'
                    },
                    {
                        'type': FaultType.SENSOR_FAILURE.value,
                        'severity': FaultSeverity.MODERATE.value,
                        'description': 'Capteur de vitesse défectueux',
                        'component': 'Elevator Car'
                    }
                ],
                duration=60.0
            ),
            ScenarioType.BRAKE_FAILURE: SimulationScenario(
                name="Défaillance du frein",
                scenario_type=ScenarioType.BRAKE_FAILURE,
                description="Défaillance du système de freinage",
                faults=[
                    {
                        'type': FaultType.BRAKE_FAILURE.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Frein principal défectueux',
                        'component': 'Brake System'
                    },
                    {
                        'type': FaultType.SAFETY_GEAR_FAILURE.value,
                        'severity': FaultSeverity.CRITICAL.value,
                        'description': 'Système de sécurité de secours activé',
                        'component': 'Brake System'
                    }
                ],
                duration=90.0
            ),
            ScenarioType.COMMUNICATION_ERROR: SimulationScenario(
                name="Erreur de communication",
                scenario_type=ScenarioType.COMMUNICATION_ERROR,
                description="Problèmes de communication entre systèmes",
                faults=[
                    {
                        'type': FaultType.COMMUNICATION_ERROR.value,
                        'severity': FaultSeverity.MODERATE.value,
                        'description': 'Perte de communication avec le contrôleur',
                        'component': 'Control System'
                    },
                    {
                        'type': FaultType.SOFTWARE_BUG.value,
                        'severity': FaultSeverity.MINOR.value,
                        'description': 'Bug logiciel dans le protocole de communication',
                        'component': 'Control System'
                    }
                ],
                duration=45.0
            )
        }
    
    def inject_fault(self, fault_type: FaultType, severity: FaultSeverity, 
                     description: str, component_name: str = "") -> Fault:
        """Injecter une panne spécifique"""
        fault = Fault(
            fault_type=fault_type,
            severity=severity,
            description=description,
            affected_component=component_name
        )
        
        self.elevator.add_fault(fault)
        
        # Appeler le callback
        if self.on_fault_injected:
            self.on_fault_injected(fault)
        
        # Enregistrer dans l'historique
        self._record_event("fault_injected", {
            'fault_type': fault_type.value,
            'severity': severity.value,
            'description': description,
            'component': component_name,
            'timestamp': fault.timestamp.isoformat()
        })
        
        return fault
    
    def inject_random_fault(self) -> Fault:
        """Injecter une panne aléatoire"""
        return self.elevator.inject_random_fault()
    
    def run_scenario(self, scenario_type: ScenarioType) -> List[Fault]:
        """Exécuter un scénario prédéfini"""
        if scenario_type not in self.scenarios:
            raise ValueError(f"Scénario inconnu: {scenario_type}")
        
        scenario = self.scenarios[scenario_type]
        faults = scenario.apply_to_elevator(self.elevator)
        
        # Enregistrer dans l'historique
        self._record_event("scenario_executed", {
            'scenario': scenario_type.value,
            'name': scenario.name,
            'faults': [f.fault_type.value for f in faults],
            'timestamp': datetime.now().isoformat()
        })
        
        return faults
    
    def start_automatic_simulation(self):
        """Démarrer la simulation automatique"""
        self.mode = SimulationMode.AUTOMATIC
        self._last_fault_time = time.time()
        self._simulation_start_time = datetime.now()
        
        self._record_event("simulation_started", {
            'mode': 'automatic',
            'timestamp': datetime.now().isoformat()
        })
    
    def stop_automatic_simulation(self):
        """Arrêter la simulation automatique"""
        self.mode = SimulationMode.MANUAL
        
        self._record_event("simulation_stopped", {
            'mode': 'automatic',
            'timestamp': datetime.now().isoformat()
        })
    
    def update(self, delta_time: float):
        """Mettre à jour le simulateur"""
        # Mettre à jour le système d'ascenseur
        self.elevator.update(delta_time * self.simulation_speed)
        
        # Simulation automatique
        if self.mode == SimulationMode.AUTOMATIC:
            current_time = time.time()
            
            # Vérifier si on doit injecter une nouvelle panne
            if current_time - self._last_fault_time > self._get_random_interval():
                if random.random() < self.fault_probability:
                    fault = self.inject_random_fault()
                    self._last_fault_time = current_time
        
        # Vérifier les changements d'état
        if self.on_state_changed:
            previous_state = self.elevator.state
            # Le state est déjà mis à jour par elevator.update()
            if previous_state != self.elevator.state:
                self.on_state_changed(self.elevator.state)
    
    def _get_random_interval(self) -> float:
        """Obtenir un intervalle aléatoire entre pannes"""
        return random.uniform(self.min_fault_interval, self.max_fault_interval)
    
    def _record_event(self, event_type: str, data: Dict):
        """Enregistrer un événement dans l'historique"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': data,
            'simulation_time': (datetime.now() - self._simulation_start_time).total_seconds()
        }
        self.simulation_history.append(event)
    
    def get_simulation_stats(self) -> Dict:
        """Obtenir les statistiques de simulation"""
        total_faults = len(self.elevator.faults)
        active_faults = len(self.elevator.get_active_faults())
        resolved_faults = total_faults - active_faults
        
        # Compter par type de panne
        fault_type_counts = {}
        for fault in self.elevator.faults:
            fault_type = fault.fault_type.value
            fault_type_counts[fault_type] = fault_type_counts.get(fault_type, 0) + 1
        
        # Compter par sévérité
        severity_counts = {}
        for fault in self.elevator.faults:
            severity = fault.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Temps de simulation
        simulation_duration = (datetime.now() - self._simulation_start_time).total_seconds()
        
        return {
            'total_faults': total_faults,
            'active_faults': active_faults,
            'resolved_faults': resolved_faults,
            'fault_type_counts': fault_type_counts,
            'severity_counts': severity_counts,
            'simulation_duration': simulation_duration,
            'current_state': self.elevator.state.value,
            'mode': self.mode.value
        }
    
    def get_available_scenarios(self) -> List[Dict]:
        """Obtenir la liste des scénarios disponibles"""
        scenarios = []
        for scenario_type, scenario in self.scenarios.items():
            scenarios.append({
                'type': scenario_type.value,
                'name': scenario.name,
                'description': scenario.description,
                'duration': scenario.duration,
                'num_faults': len(scenario.faults)
            })
        return scenarios
    
    def reset(self):
        """Réinitialiser le simulateur"""
        self.elevator = ElevatorSystem(num_floors=self.elevator.num_floors)
        self.simulation_history = []
        self._last_fault_time = 0.0
        self._simulation_start_time = datetime.now()
        
        self._record_event("simulator_reset", {
            'timestamp': datetime.now().isoformat()
        })


class StressTestSimulator:
    """Simulateur de test de résistance"""
    
    def __init__(self, elevator: ElevatorSystem):
        self.elevator = elevator
        self.test_results: List[Dict] = []
    
    def run_stress_test(self, num_faults: int = 100, duration: float = 3600.0) -> Dict:
        """Exécuter un test de résistance"""
        start_time = datetime.now()
        
        # Injecter plusieurs pannes
        for i in range(num_faults):
            fault = self.elevator.inject_random_fault()
            
            # Attendre un peu entre chaque panne
            time.sleep(0.1)
        
        # Simuler le fonctionnement
        current_time = time.time()
        end_time = current_time + duration
        
        while time.time() < end_time:
            delta_time = min(0.1, end_time - time.time())
            self.elevator.update(delta_time)
            time.sleep(delta_time * 0.1)  # Accélérer la simulation
        
        # Collecter les résultats
        results = {
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration': duration,
            'num_faults_injected': num_faults,
            'active_faults': len(self.elevator.get_active_faults()),
            'final_state': self.elevator.state.value,
            'car_position': self.elevator.car.current_floor
        }
        
        self.test_results.append(results)
        return results


if __name__ == "__main__":
    # Test du simulateur de pannes
    from .elevator_system import create_default_elevator
    
    elevator = create_default_elevator(10)
    simulator = FaultSimulator(elevator)
    
    print("=== Test du simulateur de pannes ===")
    print(f"État initial: {elevator.state.value}")
    
    # Injecter une panne manuellement
    fault = simulator.inject_fault(
        FaultType.MOTOR_FAILURE,
        FaultSeverity.CRITICAL,
        "Moteur principal en panne",
        "Elevator Motor"
    )
    print(f"Panne injectée: {fault.fault_type.value} - {fault.severity.value}")
    print(f"État après panne: {elevator.state.value}")
    
    # Exécuter un scénario
    print("\n=== Exécution d'un scénario ===")
    faults = simulator.run_scenario(ScenarioType.FIRE_EMERGENCY)
    print(f"Scénario exécuté avec {len(faults)} pannes")
    print(f"État après scénario: {elevator.state.value}")
    
    # Statistiques
    print("\n=== Statistiques ===")
    stats = simulator.get_simulation_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Scénarios disponibles
    print("\n=== Scénarios disponibles ===")
    scenarios = simulator.get_available_scenarios()
    for scenario in scenarios:
        print(f"{scenario['type']}: {scenario['name']}")
