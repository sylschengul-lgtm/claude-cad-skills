# Elevator Simulator Package
# Package principal du simulateur d'ascenseur

__version__ = "1.0.0"
__author__ = "Vibe Code Agent"
__description__ = "Simulateur de pannes d'ascenseur avec modélisation 3D et diagnostic"

# Importer les modules principaux
from .backend.elevator_system import (
    ElevatorSystem, create_default_elevator, 
    ElevatorState, Fault, FaultType, FaultSeverity, Direction
)
from .backend.fault_simulator import FaultSimulator, ScenarioType, SimulationMode
from .backend.diagnostics import DiagnosticEngine

# Version du package
VERSION = __version__

# Informations sur le package
PACKAGE_INFO = {
    'name': 'Elevator Simulator',
    'version': VERSION,
    'description': __description__,
    'author': __author__,
    'license': 'MIT'
}

def get_version():
    """Obtenir la version du package"""
    return VERSION

def get_info():
    """Obtenir les informations sur le package"""
    return PACKAGE_INFO
