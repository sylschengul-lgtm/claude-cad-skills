"""
Elevator 3D Model - Modèle 3D de l'ascenseur
Ce module permet de créer une représentation 3D de l'ascenseur et de ses composants.
Utilise PyVista pour la visualisation 3D.
"""

import numpy as np
import pyvista as pv
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Importer les classes du système d'ascenseur
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.elevator_system import ElevatorSystem, ElevatorState, Fault, FaultType, FaultSeverity


class ColorScheme:
    """Schéma de couleurs pour la visualisation"""
    
    # Couleurs de base
    PRIMARY = (0.2, 0.4, 0.8)  # Bleu
    SECONDARY = (0.8, 0.2, 0.2)  # Rouge
    SUCCESS = (0.2, 0.8, 0.2)  # Vert
    WARNING = (0.8, 0.8, 0.2)  # Jaune
    DANGER = (0.8, 0.2, 0.2)  # Rouge
    INFO = (0.2, 0.6, 0.8)  # Bleu clair
    
    # Couleurs des composants
    CAR_COLOR = (0.5, 0.7, 0.9)  # Bleu clair
    SHAFT_COLOR = (0.7, 0.7, 0.7)  # Gris
    COUNTERWEIGHT_COLOR = (0.9, 0.5, 0.3)  # Orange
    MOTOR_COLOR = (0.8, 0.1, 0.1)  # Rouge
    BRAKE_COLOR = (0.9, 0.2, 0.2)  # Rouge clair
    DOOR_COLOR = (0.6, 0.6, 0.8)  # Bleu gris
    CONTROL_COLOR = (0.3, 0.8, 0.3)  # Vert
    
    # Couleurs par état
    OPERATIONAL_COLOR = (0.2, 0.8, 0.2)  # Vert
    FAULTY_COLOR = (0.8, 0.2, 0.2)  # Rouge
    WARNING_COLOR = (0.8, 0.8, 0.2)  # Jaune
    MAINTENANCE_COLOR = (0.5, 0.5, 0.5)  # Gris
    
    # Couleurs par sévérité de panne
    FAULT_SEVERITY_COLORS = {
        FaultSeverity.MINOR: (0.9, 0.7, 0.2),  # Orange clair
        FaultSeverity.MODERATE: (0.9, 0.5, 0.2),  # Orange
        FaultSeverity.MAJOR: (0.9, 0.2, 0.2),  # Rouge
        FaultSeverity.CRITICAL: (0.8, 0.1, 0.1)  # Rouge foncé
    }
    
    @classmethod
    def get_fault_color(cls, severity: FaultSeverity) -> Tuple[float, float, float]:
        """Obtenir la couleur en fonction de la sévérité de la panne"""
        return cls.FAULT_SEVERITY_COLORS.get(severity, cls.DANGER)
    
    @classmethod
    def get_component_color(cls, component_type: str, status: str = "operational") -> Tuple[float, float, float]:
        """Obtenir la couleur d'un composant en fonction de son type et statut"""
        if status == "faulty":
            return cls.FAULTY_COLOR
        elif status == "maintenance":
            return cls.MAINTENANCE_COLOR
        
        component_colors = {
            'car': cls.CAR_COLOR,
            'shaft': cls.SHAFT_COLOR,
            'counterweight': cls.COUNTERWEIGHT_COLOR,
            'motor': cls.MOTOR_COLOR,
            'brake': cls.BRAKE_COLOR,
            'door': cls.DOOR_COLOR,
            'control': cls.CONTROL_COLOR
        }
        
        return component_colors.get(component_type, cls.PRIMARY)


@dataclass
class MeshComponent:
    """Composant 3D avec mesh"""
    name: str
    mesh: pv.PolyData
    component_type: str
    status: str = "operational"
    faults: List[Fault] = field(default_factory=list)
    
    def get_color(self) -> Tuple[float, float, float]:
        """Obtenir la couleur du composant"""
        if self.faults:
            # Si plusieurs pannes, prendre la plus sévère
            severities = [f.severity for f in self.faults]
            max_severity = max(severities, key=lambda x: list(FaultSeverity).index(x))
            return ColorScheme.get_fault_color(max_severity)
        return ColorScheme.get_component_color(self.component_type, self.status)
    
    def update_appearance(self):
        """Mettre à jour l'apparence du mesh"""
        color = self.get_color()
        self.mesh.color = color


class Elevator3DModel:
    """Modèle 3D complet de l'ascenseur"""
    
    def __init__(self, elevator_system: ElevatorSystem):
        self.elevator = elevator_system
        self.plotter: Optional[pv.Plotter] = None
        self.components: Dict[str, MeshComponent] = {}
        self.meshes: Dict[str, pv.PolyData] = {}
        
        # Paramètres de visualisation
        self.show_faults = True
        self.show_labels = True
        self.show_axes = True
        self.show_grid = True
        self.show_bounding_box = False
        
        # Créer les composants 3D
        self._create_components()
    
    def _create_components(self):
        """Créer tous les composants 3D"""
        # Gaine d'ascenseur
        self._create_shaft()
        
        # Cabine
        self._create_car()
        
        # Contrepoids
        self._create_counterweight()
        
        # Moteur
        self._create_motor()
        
        # Frein
        self._create_brake()
        
        # Porte
        self._create_door()
        
        # Système de contrôle
        self._create_control_system()
        
        # Étages
        self._create_floors()
        
        # Câbles
        self._create_cables()
    
    def _create_shaft(self):
        """Créer la gaine d'ascenseur"""
        width = self.elevator.shaft.width
        depth = self.elevator.shaft.depth
        height = self.elevator.shaft.height
        
        # Créer un prisme rectangulaire pour la gaine
        shaft_mesh = pv.Box(
            x=(0, width),
            y=(0, depth),
            z=(0, height)
        )
        
        # Ajouter des détails (ouvertures pour les portes)
        # Pour chaque étage, ajouter une ouverture
        height_per_floor = height / self.elevator.num_floors
        
        for i in range(self.elevator.num_floors):
            z_min = i * height_per_floor
            z_max = (i + 1) * height_per_floor
            
            # Ouverture de porte (simplifiée)
            door_width = 1.0
            door_height = 2.0
            door_depth = depth
            
            door_opening = pv.Box(
                x=(width/2 - door_width/2, width/2 + door_width/2),
                y=(0, door_depth),
                z=(z_min + (height_per_floor - door_height)/2, 
                   z_min + (height_per_floor + door_height)/2)
            )
            
            # Soustraire l'ouverture de la gaine
            shaft_mesh = shaft_mesh.boolean_difference(door_opening)
        
        component = MeshComponent(
            name="Elevator Shaft",
            mesh=shaft_mesh,
            component_type="shaft",
            status=self.elevator.shaft.status
        )
        
        self.components["shaft"] = component
        self.meshes["shaft"] = shaft_mesh
    
    def _create_car(self):
        """Créer la cabine d'ascenseur"""
        # Dimensions de la cabine
        car_width = 1.5
        car_depth = 1.5
        car_height = 2.2
        
        # Créer la cabine
        car_mesh = pv.Box(
            x=(-car_width/2, car_width/2),
            y=(-car_depth/2, car_depth/2),
            z=(0, car_height)
        )
        
        component = MeshComponent(
            name="Elevator Car",
            mesh=car_mesh,
            component_type="car",
            status=self.elevator.car.status,
            faults=self.elevator.car.faults
        )
        
        self.components["car"] = component
        self.meshes["car"] = car_mesh
    
    def _create_counterweight(self):
        """Créer le contrepoids"""
        # Dimensions du contrepoids
        cw_width = 0.8
        cw_depth = 0.8
        cw_height = 2.2
        
        # Positionner à côté de la cabine
        cw_mesh = pv.Box(
            x=(self.elevator.shaft.width/2 + 0.1, 
               self.elevator.shaft.width/2 + 0.1 + cw_width),
            y=(-cw_depth/2, cw_depth/2),
            z=(0, cw_height)
        )
        
        component = MeshComponent(
            name="Counterweight",
            mesh=cw_mesh,
            component_type="counterweight",
            status=self.elevator.counterweight.status,
            faults=self.elevator.counterweight.faults
        )
        
        self.components["counterweight"] = component
        self.meshes["counterweight"] = cw_mesh
    
    def _create_motor(self):
        """Créer le moteur"""
        # Positionner le moteur en haut de la gaine
        motor_radius = 0.4
        motor_height = 0.5
        
        # Créer un cylindre pour le moteur
        motor_mesh = pv.Cylinder(
            center=(self.elevator.shaft.width/2, self.elevator.shaft.depth/2, 
                   self.elevator.shaft.height),
            direction=(0, 0, -1),
            radius=motor_radius,
            height=motor_height
        )
        
        component = MeshComponent(
            name="Elevator Motor",
            mesh=motor_mesh,
            component_type="motor",
            status=self.elevator.motor.status,
            faults=self.elevator.motor.faults
        )
        
        self.components["motor"] = component
        self.meshes["motor"] = motor_mesh
    
    def _create_brake(self):
        """Créer le système de freinage"""
        # Créer un disque de frein
        brake_radius = 0.3
        brake_thickness = 0.1
        
        brake_mesh = pv.Disc(
            center=(self.elevator.shaft.width/2, self.elevator.shaft.depth/2,
                   self.elevator.shaft.height + 0.1),
            inner=0,
            outer=brake_radius,
            r_res=20,
            theta_res=20
        )
        
        # Extruder pour donner de l'épaisseur
        brake_mesh = brake_mesh.extrude((0, 0, brake_thickness))
        
        component = MeshComponent(
            name="Brake System",
            mesh=brake_mesh,
            component_type="brake",
            status=self.elevator.brake_system.status,
            faults=self.elevator.brake_system.faults
        )
        
        self.components["brake"] = component
        self.meshes["brake"] = brake_mesh
    
    def _create_door(self):
        """Créer le système de portes"""
        # Créer les portes de la cabine
        door_width = 1.4
        door_height = 2.1
        door_thickness = 0.1
        
        # Porte gauche
        door_left = pv.Box(
            x=(-door_width/2, -door_width/2 - door_thickness),
            y=(-door_height/2, door_height/2),
            z=(0, door_thickness)
        )
        
        # Porte droite
        door_right = pv.Box(
            x=(door_width/2, door_width/2 + door_thickness),
            y=(-door_height/2, door_height/2),
            z=(0, door_thickness)
        )
        
        # Combiner les deux portes
        door_mesh = door_left + door_right
        
        component = MeshComponent(
            name="Door System",
            mesh=door_mesh,
            component_type="door",
            status=self.elevator.door_system.status,
            faults=self.elevator.door_system.faults
        )
        
        self.components["door"] = component
        self.meshes["door"] = door_mesh
    
    def _create_control_system(self):
        """Créer le système de contrôle"""
        # Créer un boîtier de contrôle
        control_width = 0.5
        control_depth = 0.5
        control_height = 0.3
        
        control_mesh = pv.Box(
            x=(0, control_width),
            y=(self.elevator.shaft.depth + 0.1, self.elevator.shaft.depth + 0.1 + control_depth),
            z=(self.elevator.shaft.height - control_height, self.elevator.shaft.height)
        )
        
        component = MeshComponent(
            name="Control System",
            mesh=control_mesh,
            component_type="control",
            status=self.elevator.control_system.status,
            faults=self.elevator.control_system.faults
        )
        
        self.components["control"] = component
        self.meshes["control"] = control_mesh
    
    def _create_floors(self):
        """Créer les étages"""
        height_per_floor = self.elevator.shaft.height / self.elevator.num_floors
        
        for i, floor in enumerate(self.elevator.floors):
            z_position = (i + 1) * height_per_floor
            
            # Créer un plancher pour chaque étage
            floor_width = self.elevator.shaft.width + 2
            floor_depth = self.elevator.shaft.depth + 2
            floor_thickness = 0.2
            
            floor_mesh = pv.Box(
                x=(-floor_width/2, floor_width/2),
                y=(-floor_depth/2, floor_depth/2),
                z=(z_position - floor_thickness, z_position)
            )
            
            component = MeshComponent(
                name=f"Floor {floor.number}",
                mesh=floor_mesh,
                component_type="floor",
                status="operational"
            )
            
            self.components[f"floor_{floor.number}"] = component
            self.meshes[f"floor_{floor.number}"] = floor_mesh
            
            # Ajouter les boutons d'appel
            self._create_call_buttons(i + 1, z_position)
    
    def _create_call_buttons(self, floor_number: int, z_position: float):
        """Créer les boutons d'appel pour un étage"""
        button_size = 0.1
        
        # Bouton pour monter
        up_button = pv.Box(
            x=(self.elevator.shaft.width/2 + 0.2, 
               self.elevator.shaft.width/2 + 0.2 + button_size),
            y=(0, button_size),
            z=(z_position - 1.5, z_position - 1.5 + button_size)
        )
        
        # Bouton pour descendre
        down_button = pv.Box(
            x=(self.elevator.shaft.width/2 + 0.2, 
               self.elevator.shaft.width/2 + 0.2 + button_size),
            y=(-button_size, 0),
            z=(z_position - 1.5, z_position - 1.5 + button_size)
        )
        
        # Combiner les boutons
        buttons_mesh = up_button + down_button
        
        component = MeshComponent(
            name=f"Call Buttons Floor {floor_number}",
            mesh=buttons_mesh,
            component_type="call_buttons",
            status="operational"
        )
        
        self.components[f"call_buttons_{floor_number}"] = component
        self.meshes[f"call_buttons_{floor_number}"] = buttons_mesh
    
    def _create_cables(self):
        """Créer les câbles"""
        # Câble principal
        cable_radius = 0.05
        
        # Points pour le câble (de la cabine au contrepoids en passant par la poulie)
        car_position = self.elevator.car.current_floor * (
            self.elevator.shaft.height / self.elevator.num_floors
        )
        
        # Position de la poulie (en haut de la gaine)
        pulley_z = self.elevator.shaft.height
        
        # Créer une ligne pour le câble
        points = np.array([
            [self.elevator.shaft.width/2, self.elevator.shaft.depth/2, car_position],
            [self.elevator.shaft.width/2, self.elevator.shaft.depth/2, pulley_z],
            [self.elevator.shaft.width/2 + 0.1 + self.elevator.counterweight.mesh.length/2, 
             0, pulley_z]
        ])
        
        # Créer un tube le long de la ligne
        cable_mesh = pv.Tube(polygon=points, radius=cable_radius)
        
        component = MeshComponent(
            name="Main Cable",
            mesh=cable_mesh,
            component_type="cable",
            status="operational"
        )
        
        self.components["cable"] = component
        self.meshes["cable"] = cable_mesh
    
    def update_positions(self):
        """Mettre à jour les positions des composants mobiles"""
        # Mettre à jour la position de la cabine
        height_per_floor = self.elevator.shaft.height / self.elevator.num_floors
        car_z = (self.elevator.car.current_floor - 1) * height_per_floor
        
        # Déplacer la cabine
        if "car" in self.meshes:
            self.meshes["car"].points[:, 2] += car_z - self.meshes["car"].center[2]
        
        # Mettre à jour la position du contrepoids (opposé à la cabine)
        counterweight_z = self.elevator.shaft.height - car_z
        if "counterweight" in self.meshes:
            self.meshes["counterweight"].points[:, 2] += counterweight_z - self.meshes["counterweight"].center[2]
        
        # Mettre à jour les câbles
        self._update_cables()
    
    def _update_cables(self):
        """Mettre à jour les câbles"""
        if "cable" not in self.meshes:
            return
        
        # Recalculer les points du câble
        height_per_floor = self.elevator.shaft.height / self.elevator.num_floors
        car_z = (self.elevator.car.current_floor - 1) * height_per_floor
        
        points = np.array([
            [self.elevator.shaft.width/2, self.elevator.shaft.depth/2, car_z],
            [self.elevator.shaft.width/2, self.elevator.shaft.depth/2, self.elevator.shaft.height],
            [self.elevator.shaft.width/2 + 0.1 + 0.4, 0, self.elevator.shaft.height]
        ])
        
        # Recréer le câble
        self.meshes["cable"] = pv.Tube(polygon=points, radius=0.05)
        self.components["cable"].mesh = self.meshes["cable"]
    
    def update_colors(self):
        """Mettre à jour les couleurs en fonction des pannes"""
        for comp_name, comp in self.components.items():
            # Mettre à jour les pannes du composant
            if comp_name == "car":
                comp.faults = self.elevator.car.faults
                comp.status = self.elevator.car.status
            elif comp_name == "shaft":
                comp.faults = self.elevator.shaft.faults if hasattr(self.elevator.shaft, 'faults') else []
                comp.status = self.elevator.shaft.status
            elif comp_name == "counterweight":
                comp.faults = self.elevator.counterweight.faults
                comp.status = self.elevator.counterweight.status
            elif comp_name == "motor":
                comp.faults = self.elevator.motor.faults
                comp.status = self.elevator.motor.status
            elif comp_name == "brake":
                comp.faults = self.elevator.brake_system.faults
                comp.status = self.elevator.brake_system.status
            elif comp_name == "door":
                comp.faults = self.elevator.door_system.faults
                comp.status = self.elevator.door_system.status
            elif comp_name == "control":
                comp.faults = self.elevator.control_system.faults
                comp.status = self.elevator.control_system.status
            
            comp.update_appearance()
    
    def visualize(self, screenshot_path: Optional[str] = None):
        """Visualiser le modèle 3D"""
        self.update_positions()
        self.update_colors()
        
        # Créer un plotter
        self.plotter = pv.Plotter()
        
        # Ajouter tous les composants
        for comp_name, comp in self.components.items():
            self.plotter.add_mesh(
                comp.mesh,
                color=comp.get_color(),
                name=comp.name,
                show_edges=True,
                edge_color='black',
                opacity=0.8
            )
        
        # Ajouter des labels si activé
        if self.show_labels:
            for comp_name, comp in self.components.items():
                # Position du label (au centre du composant)
                center = comp.mesh.center
                self.plotter.add_point_labels(
                    [center],
                    [comp.name],
                    point_color='white',
                    point_size=0,
                    font_size=12,
                    shape_color='white',
                    show_points=False
                )
        
        # Ajouter les axes
        if self.show_axes:
            self.plotter.show_axes()
        
        # Ajouter la grille
        if self.show_grid:
            self.plotter.show_grid()
        
        # Ajouter la bounding box
        if self.show_bounding_box:
            self.plotter.show_bounds(
                grid='front',
                location='outer',
                all_edges=True
            )
        
        # Ajouter une légende
        self.plotter.add_legend(
            bcolor=(1, 1, 1),
            border=True,
            size=(0.2, 0.2),
            position=(0.05, 0.05)
        )
        
        # Afficher
        if screenshot_path:
            self.plotter.screenshot(screenshot_path)
        
        self.plotter.show()
        
        return self.plotter
    
    def visualize_faults(self):
        """Visualiser spécifiquement les pannes"""
        active_faults = self.elevator.get_active_faults()
        
        if not active_faults:
            print("Aucune panne active à visualiser")
            return self.visualize()
        
        self.update_positions()
        self.update_colors()
        
        self.plotter = pv.Plotter()
        
        # Ajouter tous les composants
        for comp_name, comp in self.components.items():
            color = comp.get_color()
            
            # Si le composant a des pannes, le mettre en évidence
            if comp.faults:
                self.plotter.add_mesh(
                    comp.mesh,
                    color=color,
                    name=comp.name,
                    show_edges=True,
                    edge_color='red',
                    line_width=5,
                    opacity=0.9
                )
            else:
                self.plotter.add_mesh(
                    comp.mesh,
                    color=color,
                    name=comp.name,
                    show_edges=True,
                    edge_color='black',
                    opacity=0.6
                )
        
        # Ajouter des annotations pour les pannes
        for fault in active_faults:
            # Trouver le composant affecté
            for comp_name, comp in self.components.items():
                if comp.name == fault.affected_component:
                    center = comp.mesh.center
                    
                    # Ajouter une annotation
                    self.plotter.add_point_labels(
                        [center],
                        [f"{fault.fault_type.value}\n{fault.severity.value}"],
                        point_color=ColorScheme.get_fault_color(fault.severity),
                        point_size=20,
                        font_size=14,
                        shape_color='white',
                        show_points=True
                    )
                    break
        
        # Ajouter une légende pour les sévérités
        legend_items = []
        for severity in FaultSeverity:
            color = ColorScheme.get_fault_color(severity)
            legend_items.append(f"{severity.value}")
        
        self.plotter.add_legend(
            labels=legend_items,
            colors=[ColorScheme.get_fault_color(sev) for sev in FaultSeverity],
            bcolor=(1, 1, 1),
            border=True
        )
        
        self.plotter.show_axes()
        self.plotter.show_grid()
        
        self.plotter.show()
        
        return self.plotter
    
    def export_to_stl(self, filename: str):
        """Exporter le modèle vers un fichier STL"""
        # Combiner tous les meshes
        combined = pv.MultiBlock()
        for mesh in self.meshes.values():
            combined.append(mesh)
        
        # Convertir en un seul mesh
        combined_mesh = combined.combine()
        
        # Exporter
        combined_mesh.save(filename)
        print(f"Modèle exporté vers {filename}")
    
    def export_to_obj(self, filename: str):
        """Exporter le modèle vers un fichier OBJ"""
        combined = pv.MultiBlock()
        for mesh in self.meshes.values():
            combined.append(mesh)
        
        combined_mesh = combined.combine()
        combined_mesh.save(filename)
        print(f"Modèle exporté vers {filename}")
    
    def get_component_mesh(self, component_name: str) -> Optional[pv.PolyData]:
        """Obtenir le mesh d'un composant spécifique"""
        return self.meshes.get(component_name)
    
    def highlight_component(self, component_name: str, color: Tuple[float, float, float] = (1, 0, 0)):
        """Mettre en évidence un composant"""
        if component_name in self.meshes:
            self.meshes[component_name].color = color


class InteractiveElevatorVisualizer:
    """Visualiseur interactif pour l'ascenseur"""
    
    def __init__(self, elevator_system: ElevatorSystem):
        self.elevator = elevator_system
        self.model = Elevator3DModel(elevator_system)
        self.plotter: Optional[pv.Plotter] = None
    
    def start_interactive_session(self):
        """Démarrer une session interactive"""
        print("Démarrage de la session interactive...")
        print("Commandes disponibles:")
        print("  - visualize: Visualiser l'ascenseur")
        print("  - move <floor>: Déplacer vers un étage")
        print("  - fault: Visualiser les pannes")
        print("  - inject: Injecter une panne aléatoire")
        print("  - resolve: Résoudre toutes les pannes")
        print("  - quit: Quitter")
        
        while True:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("Fin de la session interactive")
                break
            
            elif command == "visualize":
                self.model.visualize()
            
            elif command == "fault":
                self.model.visualize_faults()
            
            elif command.startswith("move "):
                try:
                    floor = int(command.split()[1])
                    if 1 <= floor <= self.elevator.num_floors:
                        self.elevator.send_to_floor(floor)
                        self.elevator.car.current_floor = floor
                        self.elevator.car.target_floor = floor
                        print(f"Déplacement vers l'étage {floor}")
                    else:
                        print(f"Étage invalide. Doit être entre 1 et {self.elevator.num_floors}")
                except ValueError:
                    print("Commande invalide. Utilisation: move <numéro_étage>")
            
            elif command == "inject":
                fault = self.elevator.inject_random_fault()
                print(f"Panne injectée: {fault.fault_type.value} - {fault.severity.value}")
                print(f"Composant affecté: {fault.affected_component}")
            
            elif command == "resolve":
                active_faults = self.elevator.get_active_faults()
                for i, fault in enumerate(active_faults):
                    self.elevator.resolve_fault(i)
                print(f"{len(active_faults)} pannes résolues")
            
            elif command == "status":
                print(f"\nÉtat du système:")
                print(f"  État: {self.elevator.state.value}")
                print(f"  Étage actuel: {self.elevator.car.current_floor}")
                print(f"  Pannes actives: {len(self.elevator.get_active_faults())}")
            
            else:
                print("Commande inconnue")


if __name__ == "__main__":
    # Test de visualisation
    from backend.elevator_system import create_default_elevator
    from backend.fault_simulator import FaultType, FaultSeverity, Fault
    
    print("Création du système d'ascenseur...")
    elevator = create_default_elevator(5)
    
    # Injecter quelques pannes
    elevator.add_fault(Fault(
        FaultType.MOTOR_FAILURE,
        FaultSeverity.MAJOR,
        "Moteur principal défectueux",
        "Elevator Motor"
    ))
    
    elevator.add_fault(Fault(
        FaultType.DOOR_SENSOR_FAILURE,
        FaultSeverity.MINOR,
        "Capteur de porte défectueux",
        "Door System"
    ))
    
    print("Création du modèle 3D...")
    model = Elevator3DModel(elevator)
    
    print("Visualisation du modèle...")
    model.visualize()
    
    print("\nVisualisation des pannes...")
    model.visualize_faults()
    
    print("\nExport vers STL...")
    model.export_to_stl("/tmp/elevator_model.stl")
