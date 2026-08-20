"""
Elevator System Core - Système principal de l'ascenseur
Ce module contient les classes principales pour modéliser un ascenseur
avec plusieurs étages et ses composants.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
import random
import time
from datetime import datetime


class ElevatorState(Enum):
    """États possibles de l'ascenseur"""
    IDLE = "idle"
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    DOOR_OPENING = "door_opening"
    DOOR_CLOSING = "door_closing"
    DOOR_OPEN = "door_open"
    EMERGENCY_STOP = "emergency_stop"
    MAINTENANCE = "maintenance"


class Direction(Enum):
    """Direction de déplacement"""
    UP = "up"
    DOWN = "down"
    NONE = "none"


class FaultType(Enum):
    """Types de pannes possibles"""
    # Pannes mécaniques
    MOTOR_FAILURE = "motor_failure"
    BRAKE_FAILURE = "brake_failure"
    CABLE_ISSUE = "cable_issue"
    DOOR_SENSOR_FAILURE = "door_sensor_failure"
    DOOR_MOTOR_FAILURE = "door_motor_failure"
    
    # Pannes électriques
    POWER_SUPPLY_FAILURE = "power_supply_failure"
    CONTROL_CIRCUIT_FAILURE = "control_circuit_failure"
    SENSOR_FAILURE = "sensor_failure"
    OVERLOAD = "overload"
    SHORT_CIRCUIT = "short_circuit"
    
    # Pannes de sécurité
    EMERGENCY_BRAKE_ACTIVATED = "emergency_brake_activated"
    SAFETY_GEAR_FAILURE = "safety_gear_failure"
    FIRE_ALARM = "fire_alarm"
    OVERHEATING = "overheating"
    
    # Pannes logicielles
    SOFTWARE_BUG = "software_bug"
    COMMUNICATION_ERROR = "communication_error"
    CONTROLLER_FAILURE = "controller_failure"


class FaultSeverity(Enum):
    """Niveaux de gravité des pannes"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


@dataclass
class Fault:
    """Classe représentant une panne"""
    fault_type: FaultType
    severity: FaultSeverity
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    is_resolved: bool = False
    affected_component: str = ""
    resolution_time: Optional[datetime] = None
    
    def resolve(self):
        """Marquer la panne comme résolue"""
        self.is_resolved = True
        self.resolution_time = datetime.now()
    
    def get_duration(self) -> Optional[float]:
        """Durée de la panne en secondes"""
        if self.resolution_time:
            return (self.resolution_time - self.timestamp).total_seconds()
        return None


@dataclass
class ElevatorComponent:
    """Composant générique de l'ascenseur"""
    name: str
    component_type: str
    status: str = "operational"
    faults: List[Fault] = field(default_factory=list)
    
    def add_fault(self, fault: Fault):
        """Ajouter une panne au composant"""
        self.faults.append(fault)
        self.status = "faulty"
    
    def resolve_all_faults(self):
        """Résoudre toutes les pannes du composant"""
        for fault in self.faults:
            fault.resolve()
        if not self.faults:
            self.status = "operational"
    
    def get_active_faults(self) -> List[Fault]:
        """Obtenir les pannes actives (non résolues)"""
        return [f for f in self.faults if not f.is_resolved]


@dataclass
class ElevatorCar(ElevatorComponent):
    """Cabine d'ascenseur"""
    current_floor: int = 1
    target_floor: int = 1
    direction: Direction = Direction.NONE
    speed: float = 0.0  # m/s
    max_speed: float = 2.0  # m/s
    capacity: int = 10  # Nombre de personnes
    current_load: int = 0  # Charge actuelle
    door_open: bool = False
    emergency_stop: bool = False
    
    def __post_init__(self):
        super().__init__(
            name="Elevator Car",
            component_type="car",
            status="operational"
        )
    
    def move_to_floor(self, target: int, floors: List['Floor']):
        """Déplacer la cabine vers un étage"""
        if self.emergency_stop:
            return False
        
        if target < 1 or target > len(floors):
            return False
        
        self.target_floor = target
        if target > self.current_floor:
            self.direction = Direction.UP
        elif target < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.NONE
        
        return True
    
    def update_position(self, delta_time: float):
        """Mettre à jour la position en fonction du temps écoulé"""
        if self.direction == Direction.NONE or self.emergency_stop:
            self.speed = 0
            return
        
        # Accélération/décélération
        acceleration = 0.5  # m/s²
        if self.speed < self.max_speed:
            self.speed = min(self.speed + acceleration * delta_time, self.max_speed)
        
        # Calcul de la distance parcourue
        distance = self.speed * delta_time
        
        # Mise à jour de l'étage (simplifié)
        if self.direction == Direction.UP:
            self.current_floor = min(self.current_floor + int(distance), self.target_floor)
        else:
            self.current_floor = max(self.current_floor - int(distance), self.target_floor)
        
        # Si on atteint l'étage cible
        if self.current_floor == self.target_floor:
            self.speed = 0
            self.direction = Direction.NONE


@dataclass
class Floor:
    """Étage de l'immeuble"""
    number: int
    height: float  # Hauteur par rapport au sol (m)
    has_call_button_up: bool = True
    has_call_button_down: bool = True
    call_button_up_pressed: bool = False
    call_button_down_pressed: bool = False
    door_status: str = "closed"
    
    def press_call_button(self, direction: Direction):
        """Appuyer sur le bouton d'appel"""
        if direction == Direction.UP:
            self.call_button_up_pressed = True
        elif direction == Direction.DOWN:
            self.call_button_down_pressed = True
    
    def reset_call_buttons(self):
        """Réinitialiser les boutons d'appel"""
        self.call_button_up_pressed = False
        self.call_button_down_pressed = False


@dataclass
class ElevatorShaft:
    """Gaine d'ascenseur"""
    width: float = 2.0  # m
    depth: float = 2.0  # m
    height: float = 30.0  # m (hauteur totale)
    material: str = "steel"
    
    def get_height_per_floor(self, num_floors: int) -> float:
        """Calculer la hauteur par étage"""
        return self.height / num_floors


@dataclass
class Counterweight(ElevatorComponent):
    """Contrepoids"""
    weight: float = 1000.0  # kg
    
    def __post_init__(self):
        super().__init__(
            name="Counterweight",
            component_type="counterweight",
            status="operational"
        )


@dataclass
class Motor(ElevatorComponent):
    """Moteur de l'ascenseur"""
    power: float = 15.0  # kW
    voltage: float = 380.0  # V
    current: float = 0.0  # A
    temperature: float = 25.0  # °C
    
    def __post_init__(self):
        super().__init__(
            name="Elevator Motor",
            component_type="motor",
            status="operational"
        )
    
    def start(self):
        """Démarrer le moteur"""
        self.current = self.power * 1000 / self.voltage  # Estimation
        self.status = "running"
    
    def stop(self):
        """Arrêter le moteur"""
        self.current = 0
        self.status = "operational"


@dataclass
class BrakeSystem(ElevatorComponent):
    """Système de freinage"""
    brake_force: float = 5000.0  # N
    is_engaged: bool = True
    
    def __post_init__(self):
        super().__init__(
            name="Brake System",
            component_type="brake",
            status="operational"
        )
    
    def engage(self):
        """Engager le frein"""
        self.is_engaged = True
    
    def release(self):
        """Relâcher le frein"""
        self.is_engaged = False


@dataclass
class DoorSystem(ElevatorComponent):
    """Système de portes"""
    door_type: str = "sliding"  # sliding, swing
    open_time: float = 2.0  # s
    close_time: float = 2.0  # s
    is_open: bool = False
    is_opening: bool = False
    is_closing: bool = False
    obstacle_detected: bool = False
    
    def __post_init__(self):
        super().__init__(
            name="Door System",
            component_type="door",
            status="operational"
        )
    
    def open(self):
        """Ouvrir les portes"""
        if not self.obstacle_detected:
            self.is_opening = True
            self.is_closing = False
    
    def close(self):
        """Fermer les portes"""
        if not self.obstacle_detected:
            self.is_closing = True
            self.is_opening = False
    
    def update(self, delta_time: float):
        """Mettre à jour l'état des portes"""
        if self.is_opening:
            # Simulation de l'ouverture
            time.sleep(self.open_time)
            self.is_open = True
            self.is_opening = False
        elif self.is_closing:
            # Simulation de la fermeture
            time.sleep(self.close_time)
            self.is_open = False
            self.is_closing = False


@dataclass
class ControlSystem(ElevatorComponent):
    """Système de contrôle"""
    algorithm: str = "collective"  # collective, selective, etc.
    
    def __post_init__(self):
        super().__init__(
            name="Control System",
            component_type="control",
            status="operational"
        )


@dataclass
class ElevatorSystem:
    """Système complet d'ascenseur"""
    num_floors: int = 10
    name: str = "Main Elevator"
    
    # Composants
    car: ElevatorCar = field(default_factory=ElevatorCar)
    shaft: ElevatorShaft = field(default_factory=ElevatorShaft)
    counterweight: Counterweight = field(default_factory=Counterweight)
    motor: Motor = field(default_factory=Motor)
    brake_system: BrakeSystem = field(default_factory=BrakeSystem)
    door_system: DoorSystem = field(default_factory=DoorSystem)
    control_system: ControlSystem = field(default_factory=ControlSystem)
    
    # État global
    state: ElevatorState = ElevatorState.IDLE
    faults: List[Fault] = field(default_factory=list)
    maintenance_mode: bool = False
    
    # Étages
    floors: List[Floor] = field(default_factory=list)
    
    def __post_init__(self):
        # Initialiser les étages
        if not self.floors:
            height_per_floor = self.shaft.get_height_per_floor(self.num_floors)
            for i in range(1, self.num_floors + 1):
                self.floors.append(Floor(
                    number=i,
                    height=height_per_floor * i
                ))
    
    def get_component_by_name(self, name: str) -> Optional[ElevatorComponent]:
        """Obtenir un composant par son nom"""
        components = [
            self.car, self.shaft, self.counterweight, 
            self.motor, self.brake_system, self.door_system, 
            self.control_system
        ]
        for comp in components:
            if comp.name == name:
                return comp
        return None
    
    def get_all_components(self) -> List[ElevatorComponent]:
        """Obtenir tous les composants"""
        return [
            self.car, self.shaft, self.counterweight, 
            self.motor, self.brake_system, self.door_system, 
            self.control_system
        ]
    
    def add_fault(self, fault: Fault):
        """Ajouter une panne au système"""
        self.faults.append(fault)
        
        # Mettre à jour le statut du composant affecté
        for comp in self.get_all_components():
            if comp.name == fault.affected_component:
                comp.add_fault(fault)
        
        # Mettre à jour l'état global
        if fault.severity in [FaultSeverity.CRITICAL, FaultSeverity.MAJOR]:
            self.state = ElevatorState.EMERGENCY_STOP
    
    def inject_random_fault(self) -> Fault:
        """Injecter une panne aléatoire"""
        fault_types = list(FaultType)
        fault_type = random.choice(fault_types)
        
        # Déterminer la sévérité aléatoirement
        severities = list(FaultSeverity)
        severity = random.choice(severities)
        
        # Sélectionner un composant aléatoire
        components = self.get_all_components()
        component = random.choice(components)
        
        fault = Fault(
            fault_type=fault_type,
            severity=severity,
            description=f"Random {fault_type.value} detected in {component.name}",
            affected_component=component.name
        )
        
        self.add_fault(fault)
        return fault
    
    def resolve_fault(self, fault_index: int) -> bool:
        """Résoudre une panne par index"""
        if 0 <= fault_index < len(self.faults):
            fault = self.faults[fault_index]
            fault.resolve()
            
            # Mettre à jour le statut du composant
            for comp in self.get_all_components():
                if comp.name == fault.affected_component:
                    comp.resolve_all_faults()
            
            # Vérifier si on peut reprendre le fonctionnement normal
            active_faults = [f for f in self.faults if not f.is_resolved]
            if not active_faults:
                self.state = ElevatorState.IDLE
            
            return True
        return False
    
    def get_active_faults(self) -> List[Fault]:
        """Obtenir toutes les pannes actives"""
        return [f for f in self.faults if not f.is_resolved]
    
    def call_elevator(self, floor_number: int, direction: Direction) -> bool:
        """Appeler l'ascenseur depuis un étage"""
        if floor_number < 1 or floor_number > self.num_floors:
            return False
        
        floor = self.floors[floor_number - 1]
        floor.press_call_button(direction)
        return True
    
    def send_to_floor(self, floor_number: int) -> bool:
        """Envoyer l'ascenseur à un étage"""
        return self.car.move_to_floor(floor_number, self.floors)
    
    def emergency_stop(self):
        """Arrêt d'urgence"""
        self.state = ElevatorState.EMERGENCY_STOP
        self.car.emergency_stop = True
        self.motor.stop()
        self.brake_system.engage()
    
    def reset_emergency(self):
        """Réinitialiser l'arrêt d'urgence"""
        self.state = ElevatorState.IDLE
        self.car.emergency_stop = False
    
    def enter_maintenance_mode(self):
        """Entrer en mode maintenance"""
        self.maintenance_mode = True
        self.state = ElevatorState.MAINTENANCE
    
    def exit_maintenance_mode(self):
        """Quitter le mode maintenance"""
        self.maintenance_mode = False
        self.state = ElevatorState.IDLE
    
    def update(self, delta_time: float):
        """Mettre à jour le système"""
        # Mettre à jour la position de la cabine
        self.car.update_position(delta_time)
        
        # Mettre à jour les portes
        self.door_system.update(delta_time)
        
        # Mettre à jour l'état global
        if self.car.direction != Direction.NONE:
            if self.car.direction == Direction.UP:
                self.state = ElevatorState.MOVING_UP
            else:
                self.state = ElevatorState.MOVING_DOWN
        elif self.door_system.is_opening:
            self.state = ElevatorState.DOOR_OPENING
        elif self.door_system.is_closing:
            self.state = ElevatorState.DOOR_CLOSING
        elif self.door_system.is_open:
            self.state = ElevatorState.DOOR_OPEN
        elif self.car.emergency_stop:
            self.state = ElevatorState.EMERGENCY_STOP
        elif self.maintenance_mode:
            self.state = ElevatorState.MAINTENANCE
        else:
            self.state = ElevatorState.IDLE


# Fonction pour créer un système d'ascenseur par défaut
def create_default_elevator(num_floors: int = 10) -> ElevatorSystem:
    """Créer un système d'ascenseur avec des paramètres par défaut"""
    return ElevatorSystem(num_floors=num_floors)


if __name__ == "__main__":
    # Test du système
    elevator = create_default_elevator(10)
    print(f"Système d'ascenseur créé avec {elevator.num_floors} étages")
    print(f"État initial: {elevator.state.value}")
    
    # Injecter une panne
    fault = elevator.inject_random_fault()
    print(f"Panne injectée: {fault.fault_type.value} - {fault.severity.value}")
    print(f"État après panne: {elevator.state.value}")
    
    # Résoudre la panne
    elevator.resolve_fault(0)
    print(f"État après résolution: {elevator.state.value}")
