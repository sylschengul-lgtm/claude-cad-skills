"""
Main Window - Fenêtre principale de l'application
Interface graphique pour le simulateur d'ascenseur avec visualisation 3D et diagnostic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTextEdit, QGroupBox,
    QSplitter, QTabWidget, QFormLayout, QLineEdit, QSpinBox,
    QMessageBox, QStatusBar, QToolBar, QAction, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette

from backend.elevator_system import (
    ElevatorSystem, create_default_elevator, ElevatorState, 
    Fault, FaultType, FaultSeverity, Direction
)
from backend.fault_simulator import FaultSimulator, ScenarioType, SimulationMode
from backend.diagnostics import DiagnosticEngine


class ElevatorApp(QMainWindow):
    """Application principale du simulateur d'ascenseur"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Simulateur de Pannes d'Ascenseur")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialiser le système d'ascenseur
        self.elevator = create_default_elevator(10)
        self.simulator = FaultSimulator(self.elevator)
        self.diagnostic_engine = DiagnosticEngine(self.elevator)
        
        # Configuration de l'interface
        self._setup_ui()
        self._setup_connections()
        self._setup_timers()
        
        # État de l'application
        self.simulation_running = False
        self.auto_refresh_enabled = True
        
        # Mettre à jour l'interface
        self.update_ui()
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Créer le widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Splitter pour diviser l'espace
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panneau de contrôle (gauche)
        self.control_panel = self._create_control_panel()
        splitter.addWidget(self.control_panel)
        
        # Panneau de visualisation (centre)
        self.visualization_panel = self._create_visualization_panel()
        splitter.addWidget(self.visualization_panel)
        
        # Panneau de diagnostic (droite)
        self.diagnostic_panel = self._create_diagnostic_panel()
        splitter.addWidget(self.diagnostic_panel)
        
        # Définir les tailles initiales
        splitter.setSizes([200, 600, 300])
        
        # Barre d'outils
        self._create_toolbar()
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
    
    def _create_control_panel(self):
        """Créer le panneau de contrôle"""
        panel = QGroupBox("Contrôle de l'Ascenseur")
        layout = QVBoxLayout()
        
        # État du système
        self.state_label = QLabel("État: IDLE")
        self.state_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.state_label)
        
        # Position actuelle
        self.position_label = QLabel("Position: Étage 1")
        layout.addWidget(self.position_label)
        
        # Contrôle de déplacement
        control_group = QGroupBox("Contrôle Manuel")
        control_layout = QVBoxLayout()
        
        # Sélection de l'étage
        self.floor_combo = QComboBox()
        for i in range(1, self.elevator.num_floors + 1):
            self.floor_combo.addItem(f"Étage {i}")
        control_layout.addWidget(QLabel("Destination:"))
        control_layout.addWidget(self.floor_combo)
        
        # Bouton de déplacement
        self.move_button = QPushButton("Déplacer")
        self.move_button.setIcon(QIcon.fromTheme("media-playback-start"))
        control_layout.addWidget(self.move_button)
        
        # Boutons de direction
        button_layout = QHBoxLayout()
        
        self.up_button = QPushButton("↑")
        self.up_button.setFixedSize(50, 50)
        button_layout.addWidget(self.up_button)
        
        self.down_button = QPushButton("↓")
        self.down_button.setFixedSize(50, 50)
        button_layout.addWidget(self.down_button)
        
        control_layout.addLayout(button_layout)
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Contrôle des portes
        door_group = QGroupBox("Contrôle des Portes")
        door_layout = QVBoxLayout()
        
        self.open_door_button = QPushButton("Ouvrir Portes")
        door_layout.addWidget(self.open_door_button)
        
        self.close_door_button = QPushButton("Fermer Portes")
        door_layout.addWidget(self.close_door_button)
        
        door_group.setLayout(door_layout)
        layout.addWidget(door_group)
        
        # Contrôle d'urgence
        emergency_group = QGroupBox("Contrôle d'Urgence")
        emergency_layout = QVBoxLayout()
        
        self.emergency_stop_button = QPushButton("ARRÊT D'URGENCE")
        self.emergency_stop_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        emergency_layout.addWidget(self.emergency_stop_button)
        
        self.reset_emergency_button = QPushButton("Réinitialiser")
        emergency_layout.addWidget(self.reset_emergency_button)
        
        self.maintenance_button = QPushButton("Mode Maintenance")
        emergency_layout.addWidget(self.maintenance_button)
        
        emergency_group.setLayout(emergency_layout)
        layout.addWidget(emergency_group)
        
        # Mode maintenance
        self.maintenance_mode_label = QLabel("Mode maintenance: Non")
        layout.addWidget(self.maintenance_mode_label)
        
        panel.setLayout(layout)
        return panel
    
    def _create_visualization_panel(self):
        """Créer le panneau de visualisation"""
        panel = QGroupBox("Visualisation 3D")
        layout = QVBoxLayout()
        
        # Espace pour la visualisation 3D
        self.visualization_widget = QWidget()
        self.visualization_widget.setMinimumSize(400, 400)
        self.visualization_widget.setStyleSheet("background-color: #f0f0f0;")
        
        # Label temporaire
        self.visualization_label = QLabel("Visualisation 3D\n(Requiert PyVista)")
        self.visualization_label.setAlignment(Qt.AlignCenter)
        self.visualization_label.setStyleSheet("font-size: 16px; color: #666;")
        
        visualization_container = QVBoxLayout(self.visualization_widget)
        visualization_container.addWidget(self.visualization_label)
        
        layout.addWidget(self.visualization_widget)
        
        # Boutons de visualisation
        self.refresh_3d_button = QPushButton("Rafraîchir la vue 3D")
        layout.addWidget(self.refresh_3d_button)
        
        self.show_faults_button = QPushButton("Montrer les pannes")
        layout.addWidget(self.show_faults_button)
        
        self.export_model_button = QPushButton("Exporter le modèle 3D")
        layout.addWidget(self.export_model_button)
        
        panel.setLayout(layout)
        return panel
    
    def _create_diagnostic_panel(self):
        """Créer le panneau de diagnostic"""
        panel = QGroupBox("Diagnostic")
        layout = QVBoxLayout()
        
        # Onglets pour le diagnostic
        self.diagnostic_tabs = QTabWidget()
        
        # Onglet des pannes
        self.faults_tab = self._create_faults_tab()
        self.diagnostic_tabs.addTab(self.faults_tab, "Pannes")
        
        # Onglet des tests
        self.tests_tab = self._create_tests_tab()
        self.diagnostic_tabs.addTab(self.tests_tab, "Tests")
        
        # Onglet des scénarios
        self.scenarios_tab = self._create_scenarios_tab()
        self.diagnostic_tabs.addTab(self.scenarios_tab, "Scénarios")
        
        # Onglet du rapport
        self.report_tab = self._create_report_tab()
        self.diagnostic_tabs.addTab(self.report_tab, "Rapport")
        
        layout.addWidget(self.diagnostic_tabs)
        
        # Boutons de diagnostic
        button_layout = QHBoxLayout()
        
        self.run_diagnostic_button = QPushButton("Exécuter Diagnostic")
        button_layout.addWidget(self.run_diagnostic_button)
        
        self.clear_faults_button = QPushButton("Effacer les pannes")
        button_layout.addWidget(self.clear_faults_button)
        
        layout.addLayout(button_layout)
        
        panel.setLayout(layout)
        return panel
    
    def _create_faults_tab(self):
        """Créer l'onglet des pannes"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Tableau des pannes
        self.faults_table = QTableWidget()
        self.faults_table.setColumnCount(5)
        self.faults_table.setHorizontalHeaderLabels([
            "Type", "Sévérité", "Composant", "Description", "Résolue"
        ])
        self.faults_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.faults_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.faults_table)
        
        # Boutons pour les pannes
        button_layout = QHBoxLayout()
        
        self.inject_fault_button = QPushButton("Injecter Panne Aléatoire")
        button_layout.addWidget(self.inject_fault_button)
        
        self.resolve_selected_button = QPushButton("Résoudre Sélection")
        button_layout.addWidget(self.resolve_selected_button)
        
        layout.addLayout(button_layout)
        
        # Statistiques
        self.faults_stats_label = QLabel("Pannes actives: 0 | Pannes totales: 0")
        layout.addWidget(self.faults_stats_label)
        
        tab.setLayout(layout)
        return tab
    
    def _create_tests_tab(self):
        """Créer l'onglet des tests"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Sélection du test
        self.test_combo = QComboBox()
        test_names = [
            "Tous les tests",
            "Statut des composants",
            "Détection de pannes",
            "Test du moteur",
            "Test du frein",
            "Test des portes",
            "Test de sécurité",
            "Test de communication"
        ]
        self.test_combo.addItems(test_names)
        layout.addWidget(QLabel("Sélectionner le test:"))
        layout.addWidget(self.test_combo)
        
        # Bouton d'exécution
        self.run_test_button = QPushButton("Exécuter le test")
        layout.addWidget(self.run_test_button)
        
        # Résultats des tests
        self.test_results_table = QTableWidget()
        self.test_results_table.setColumnCount(4)
        self.test_results_table.setHorizontalHeaderLabels([
            "Test", "Statut", "Résultat", "Détails"
        ])
        self.test_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.test_results_table)
        
        tab.setLayout(layout)
        return tab
    
    def _create_scenarios_tab(self):
        """Créer l'onglet des scénarios"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Liste des scénarios
        self.scenario_combo = QComboBox()
        scenarios = self.simulator.get_available_scenarios()
        for scenario in scenarios:
            self.scenario_combo.addItem(f"{scenario['name']} ({scenario['type']})", 
                                       scenario['type'])
        
        layout.addWidget(QLabel("Sélectionner le scénario:"))
        layout.addWidget(self.scenario_combo)
        
        # Description du scénario
        self.scenario_description_label = QLabel("")
        self.scenario_description_label.setWordWrap(True)
        layout.addWidget(self.scenario_description_label)
        
        # Bouton d'exécution
        self.run_scenario_button = QPushButton("Exécuter le scénario")
        layout.addWidget(self.run_scenario_button)
        
        # Mode de simulation
        self.simulation_mode_combo = QComboBox()
        self.simulation_mode_combo.addItems([
            "Manuel", "Automatique", "Scénario"
        ])
        layout.addWidget(QLabel("Mode de simulation:"))
        layout.addWidget(self.simulation_mode_combo)
        
        # Contrôles de simulation automatique
        self.auto_sim_group = QGroupBox("Simulation Automatique")
        auto_layout = QFormLayout()
        
        self.fault_probability_spin = QSpinBox()
        self.fault_probability_spin.setRange(1, 100)
        self.fault_probability_spin.setValue(1)
        self.fault_probability_spin.setSuffix("%")
        auto_layout.addRow("Probabilité de panne:", self.fault_probability_spin)
        
        self.start_auto_button = QPushButton("Démarrer")
        self.stop_auto_button = QPushButton("Arrêter")
        auto_layout.addRow(self.start_auto_button, self.stop_auto_button)
        
        self.auto_sim_group.setLayout(auto_layout)
        layout.addWidget(self.auto_sim_group)
        
        tab.setLayout(layout)
        return tab
    
    def _create_report_tab(self):
        """Créer l'onglet du rapport"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Zone de texte pour le rapport
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Courier", 10))
        
        layout.addWidget(self.report_text)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        self.generate_report_button = QPushButton("Générer Rapport")
        button_layout.addWidget(self.generate_report_button)
        
        self.save_report_button = QPushButton("Enregistrer Rapport")
        button_layout.addWidget(self.save_report_button)
        
        layout.addLayout(button_layout)
        
        tab.setLayout(layout)
        return tab
    
    def _create_toolbar(self):
        """Créer la barre d'outils"""
        toolbar = QToolBar("Outils")
        self.addToolBar(toolbar)
        
        # Actions
        new_action = QAction("Nouveau", self)
        new_action.setShortcut("Ctrl+N")
        toolbar.addAction(new_action)
        
        open_action = QAction("Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        toolbar.addAction(open_action)
        
        save_action = QAction("Enregistrer", self)
        save_action.setShortcut("Ctrl+S")
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Actions de simulation
        self.simulation_action = QAction("Démarrer Simulation", self)
        toolbar.addAction(self.simulation_action)
        
        self.stop_simulation_action = QAction("Arrêter Simulation", self)
        toolbar.addAction(self.stop_simulation_action)
        
        toolbar.addSeparator()
        
        # Actions de visualisation
        self.refresh_action = QAction("Rafraîchir", self)
        self.refresh_action.setShortcut("F5")
        toolbar.addAction(self.refresh_action)
        
        # Action de diagnostic
        self.diagnostic_action = QAction("Diagnostic", self)
        self.diagnostic_action.setShortcut("Ctrl+D")
        toolbar.addAction(self.diagnostic_action)
    
    def _setup_connections(self):
        """Configurer les connexions des signaux"""
        # Boutons de contrôle
        self.move_button.clicked.connect(self.move_to_floor)
        self.up_button.clicked.connect(lambda: self.move_direction(Direction.UP))
        self.down_button.clicked.connect(lambda: self.move_direction(Direction.DOWN))
        self.open_door_button.clicked.connect(self.open_door)
        self.close_door_button.clicked.connect(self.close_door)
        self.emergency_stop_button.clicked.connect(self.emergency_stop)
        self.reset_emergency_button.clicked.connect(self.reset_emergency)
        self.maintenance_button.clicked.connect(self.toggle_maintenance)
        
        # Boutons de diagnostic
        self.inject_fault_button.clicked.connect(self.inject_random_fault)
        self.resolve_selected_button.clicked.connect(self.resolve_selected_faults)
        self.clear_faults_button.clicked.connect(self.clear_all_faults)
        self.run_diagnostic_button.clicked.connect(self.run_full_diagnostic)
        self.run_test_button.clicked.connect(self.run_selected_test)
        self.generate_report_button.clicked.connect(self.generate_report)
        self.save_report_button.clicked.connect(self.save_report)
        
        # Boutons de visualisation
        self.refresh_3d_button.clicked.connect(self.refresh_3d_view)
        self.show_faults_button.clicked.connect(self.show_faults_view)
        self.export_model_button.clicked.connect(self.export_3d_model)
        
        # Boutons de scénarios
        self.run_scenario_button.clicked.connect(self.run_selected_scenario)
        self.scenario_combo.currentIndexChanged.connect(self.update_scenario_description)
        self.start_auto_button.clicked.connect(self.start_auto_simulation)
        self.stop_auto_button.clicked.connect(self.stop_auto_simulation)
        
        # Actions de la barre d'outils
        self.refresh_action.triggered.connect(self.refresh_3d_view)
        self.diagnostic_action.triggered.connect(self.run_full_diagnostic)
        
        # Timer pour la mise à jour automatique
        self.auto_refresh_timer = QTimer(self)
        self.auto_refresh_timer.timeout.connect(self.update_ui)
        self.auto_refresh_timer.start(1000)  # Mise à jour toutes les secondes
    
    def _setup_timers(self):
        """Configurer les timers"""
        # Timer pour la simulation automatique
        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.update_simulation)
    
    def update_ui(self):
        """Mettre à jour l'interface utilisateur"""
        # Mettre à jour l'état
        state_text = f"État: {self.elevator.state.value.upper()}"
        
        # Couleur en fonction de l'état
        if self.elevator.state == ElevatorState.EMERGENCY_STOP:
            state_text = f"<span style='color: red;'>{state_text}</span>"
        elif self.elevator.state == ElevatorState.MOVING_UP or self.elevator.state == ElevatorState.MOVING_DOWN:
            state_text = f"<span style='color: blue;'>{state_text}</span>"
        elif self.elevator.state == ElevatorState.MAINTENANCE:
            state_text = f"<span style='color: orange;'>{state_text}</span>"
        
        self.state_label.setText(state_text)
        
        # Mettre à jour la position
        self.position_label.setText(f"Position: Étage {self.elevator.car.current_floor}")
        
        # Mettre à jour le mode maintenance
        maintenance_text = "Mode maintenance: " + ("Oui" if self.elevator.maintenance_mode else "Non")
        self.maintenance_mode_label.setText(maintenance_text)
        
        # Mettre à jour le tableau des pannes
        self.update_faults_table()
        
        # Mettre à jour les statistiques
        active_faults = len(self.elevator.get_active_faults())
        total_faults = len(self.elevator.faults)
        self.faults_stats_label.setText(f"Pannes actives: {active_faults} | Pannes totales: {total_faults}")
    
    def update_faults_table(self):
        """Mettre à jour le tableau des pannes"""
        self.faults_table.setRowCount(0)
        
        for i, fault in enumerate(self.elevator.faults):
            self.faults_table.insertRow(i)
            
            # Type
            type_item = QTableWidgetItem(fault.fault_type.value)
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            self.faults_table.setItem(i, 0, type_item)
            
            # Sévérité
            severity_item = QTableWidgetItem(fault.severity.value)
            severity_item.setFlags(severity_item.flags() & ~Qt.ItemIsEditable)
            
            # Couleur en fonction de la sévérité
            if fault.severity == FaultSeverity.CRITICAL:
                severity_item.setBackground(QColor(255, 100, 100))
            elif fault.severity == FaultSeverity.MAJOR:
                severity_item.setBackground(QColor(255, 150, 100))
            elif fault.severity == FaultSeverity.MODERATE:
                severity_item.setBackground(QColor(255, 200, 100))
            else:
                severity_item.setBackground(QColor(200, 255, 100))
            
            self.faults_table.setItem(i, 1, severity_item)
            
            # Composant
            component_item = QTableWidgetItem(fault.affected_component)
            component_item.setFlags(component_item.flags() & ~Qt.ItemIsEditable)
            self.faults_table.setItem(i, 2, component_item)
            
            # Description
            desc_item = QTableWidgetItem(fault.description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemIsEditable)
            self.faults_table.setItem(i, 3, desc_item)
            
            # Résolue
            resolved_item = QTableWidgetItem("✓" if fault.is_resolved else "✗")
            resolved_item.setFlags(resolved_item.flags() & ~Qt.ItemIsEditable)
            resolved_item.setTextAlignment(Qt.AlignCenter)
            
            if fault.is_resolved:
                resolved_item.setBackground(QColor(200, 255, 200))
            else:
                resolved_item.setBackground(QColor(255, 200, 200))
            
            self.faults_table.setItem(i, 4, resolved_item)
    
    def move_to_floor(self):
        """Déplacer vers l'étage sélectionné"""
        floor_index = self.floor_combo.currentIndex()
        floor_number = floor_index + 1
        
        if self.elevator.send_to_floor(floor_number):
            self.status_bar.showMessage(f"Déplacement vers l'étage {floor_number}")
        else:
            self.status_bar.showMessage(f"Impossible de se déplacer vers l'étage {floor_number}")
        
        self.update_ui()
    
    def move_direction(self, direction: Direction):
        """Déplacer dans une direction"""
        current_floor = self.elevator.car.current_floor
        
        if direction == Direction.UP:
            target_floor = min(current_floor + 1, self.elevator.num_floors)
        else:
            target_floor = max(current_floor - 1, 1)
        
        if self.elevator.send_to_floor(target_floor):
            self.status_bar.showMessage(f"Déplacement vers l'étage {target_floor}")
        
        self.update_ui()
    
    def open_door(self):
        """Ouvrir les portes"""
        self.elevator.door_system.open()
        self.status_bar.showMessage("Ouverture des portes...")
        self.update_ui()
    
    def close_door(self):
        """Fermer les portes"""
        self.elevator.door_system.close()
        self.status_bar.showMessage("Fermeture des portes...")
        self.update_ui()
    
    def emergency_stop(self):
        """Arrêt d'urgence"""
        self.elevator.emergency_stop()
        self.status_bar.showMessage("ARRÊT D'URGENCE ACTIVÉ!")
        self.update_ui()
    
    def reset_emergency(self):
        """Réinitialiser l'arrêt d'urgence"""
        self.elevator.reset_emergency()
        self.status_bar.showMessage("Arrêt d'urgence réinitialisé")
        self.update_ui()
    
    def toggle_maintenance(self):
        """Basculer le mode maintenance"""
        if self.elevator.maintenance_mode:
            self.elevator.exit_maintenance_mode()
            self.status_bar.showMessage("Mode maintenance désactivé")
        else:
            self.elevator.enter_maintenance_mode()
            self.status_bar.showMessage("Mode maintenance activé")
        
        self.update_ui()
    
    def inject_random_fault(self):
        """Injecter une panne aléatoire"""
        fault = self.simulator.inject_random_fault()
        self.status_bar.showMessage(f"Panne injectée: {fault.fault_type.value}")
        self.update_ui()
    
    def resolve_selected_faults(self):
        """Résoudre les pannes sélectionnées"""
        selected_rows = self.faults_table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.information(self, "Information", "Aucune panne sélectionnée")
            return
        
        for row in selected_rows:
            row_index = row.row()
            if 0 <= row_index < len(self.elevator.faults):
                self.elevator.resolve_fault(row_index)
        
        self.status_bar.showMessage(f"{len(selected_rows)} panne(s) résolue(s)")
        self.update_ui()
    
    def clear_all_faults(self):
        """Effacer toutes les pannes"""
        self.elevator.faults = []
        for comp in self.elevator.get_all_components():
            comp.faults = []
            comp.status = "operational"
        
        self.elevator.state = ElevatorState.IDLE
        self.status_bar.showMessage("Toutes les pannes ont été effacées")
        self.update_ui()
    
    def run_full_diagnostic(self):
        """Exécuter un diagnostic complet"""
        self.status_bar.showMessage("Exécution du diagnostic complet...")
        
        results = self.diagnostic_engine.run_comprehensive_diagnostic()
        
        # Afficher les résultats dans l'onglet des tests
        self._display_test_results(results)
        
        self.status_bar.showMessage("Diagnostic terminé")
    
    def run_selected_test(self):
        """Exécuter le test sélectionné"""
        test_index = self.test_combo.currentIndex()
        test_name = self.test_combo.currentText().lower()
        
        if test_index == 0:  # Tous les tests
            self.run_full_diagnostic()
            return
        
        # Mapper les noms aux IDs des tests
        test_mapping = {
            "statut des composants": "component_status",
            "détection de pannes": "fault_detection",
            "test du moteur": "motor",
            "test du frein": "brake",
            "test des portes": "door",
            "test de sécurité": "safety",
            "test de communication": "communication"
        }
        
        test_id = test_mapping.get(test_name, "")
        if test_id:
            test = self.diagnostic_engine.run_test(test_id)
            if test:
                results = {test_id: self.diagnostic_engine._test_to_dict(test)}
                self._display_test_results(results)
                self.status_bar.showMessage(f"Test {test_name} exécuté")
        
        self.update_ui()
    
    def _display_test_results(self, results: Dict):
        """Afficher les résultats des tests"""
        self.test_results_table.setRowCount(0)
        
        # Si system_info est présent, l'ignorer
        test_results = {k: v for k, v in results.items() if k != 'system_info'}
        
        for i, (test_name, test_data) in enumerate(test_results.items()):
            self.test_results_table.insertRow(i)
            
            # Nom du test
            name_item = QTableWidgetItem(test_data.get('name', test_name))
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.test_results_table.setItem(i, 0, name_item)
            
            # Statut
            status_item = QTableWidgetItem(test_data.get('status', 'Unknown'))
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            self.test_results_table.setItem(i, 1, status_item)
            
            # Résultat
            result_item = QTableWidgetItem(test_data.get('result', 'Unknown'))
            result_item.setFlags(result_item.flags() & ~Qt.ItemIsEditable)
            
            if test_data.get('result') == "PASSED":
                result_item.setBackground(QColor(200, 255, 200))
            elif test_data.get('result') == "FAILED":
                result_item.setBackground(QColor(255, 200, 200))
            
            self.test_results_table.setItem(i, 2, result_item)
            
            # Détails
            details = test_data.get('details', {})
            details_text = ", ".join([f"{k}: {v}" for k, v in list(details.items())[:3]])
            details_item = QTableWidgetItem(details_text)
            details_item.setFlags(details_item.flags() & ~Qt.ItemIsEditable)
            self.test_results_table.setItem(i, 3, details_item)
    
    def update_scenario_description(self):
        """Mettre à jour la description du scénario"""
        scenario_type = self.scenario_combo.currentData()
        scenarios = self.simulator.get_available_scenarios()
        
        for scenario in scenarios:
            if scenario['type'] == scenario_type:
                self.scenario_description_label.setText(scenario['description'])
                return
        
        self.scenario_description_label.setText("")
    
    def run_selected_scenario(self):
        """Exécuter le scénario sélectionné"""
        scenario_type = self.scenario_combo.currentData()
        
        if not scenario_type:
            QMessageBox.warning(self, "Avertissement", "Aucun scénario sélectionné")
            return
        
        try:
            scenario_enum = ScenarioType(scenario_type)
            faults = self.simulator.run_scenario(scenario_enum)
            self.status_bar.showMessage(f"Scénario '{scenario_type}' exécuté avec {len(faults)} pannes")
        except ValueError:
            QMessageBox.warning(self, "Erreur", f"Scénario inconnu: {scenario_type}")
        
        self.update_ui()
    
    def start_auto_simulation(self):
        """Démarrer la simulation automatique"""
        self.simulation_mode_combo.setCurrentIndex(1)  # Automatique
        
        # Configurer le simulateur
        probability = self.fault_probability_spin.value() / 100.0
        self.simulator.fault_probability = probability
        self.simulator.start_automatic_simulation()
        
        # Démarrer le timer
        self.simulation_timer.start(100)  # 100ms
        self.simulation_running = True
        
        self.status_bar.showMessage("Simulation automatique démarrée")
    
    def stop_auto_simulation(self):
        """Arrêter la simulation automatique"""
        self.simulator.stop_automatic_simulation()
        self.simulation_timer.stop()
        self.simulation_running = False
        
        self.status_bar.showMessage("Simulation automatique arrêtée")
    
    def update_simulation(self):
        """Mettre à jour la simulation"""
        if self.simulation_running:
            self.simulator.update(0.1)  # Delta time de 100ms
            self.update_ui()
    
    def generate_report(self):
        """Générer un rapport de diagnostic"""
        report = self.diagnostic_engine.generate_diagnostic_report()
        self.report_text.setPlainText(report)
        self.status_bar.showMessage("Rapport généré")
    
    def save_report(self):
        """Enregistrer le rapport"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport", "", 
            "Fichiers texte (*.txt);;Tous les fichiers (*)", 
            options=options
        )
        
        if file_path:
            report = self.report_text.toPlainText()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report)
            self.status_bar.showMessage(f"Rapport enregistré vers {file_path}")
    
    def refresh_3d_view(self):
        """Rafraîchir la vue 3D"""
        try:
            from models.elevator_3d_model import Elevator3DModel
            model = Elevator3DModel(self.elevator)
            model.visualize()
            self.status_bar.showMessage("Vue 3D rafraîchie")
        except ImportError as e:
            QMessageBox.warning(self, "Erreur", 
                              f"Impossible de charger PyVista: {str(e)}\n\n"
                              "Assurez-vous que PyVista est installé: pip install pyvista")
    
    def show_faults_view(self):
        """Montrer la vue des pannes"""
        try:
            from models.elevator_3d_model import Elevator3DModel
            model = Elevator3DModel(self.elevator)
            model.visualize_faults()
            self.status_bar.showMessage("Vue des pannes affichée")
        except ImportError as e:
            QMessageBox.warning(self, "Erreur", 
                              f"Impossible de charger PyVista: {str(e)}")
    
    def export_3d_model(self):
        """Exporter le modèle 3D"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter le modèle 3D", "", 
            "STL Files (*.stl);;OBJ Files (*.obj);;Tous les fichiers (*)", 
            options=options
        )
        
        if file_path:
            try:
                from models.elevator_3d_model import Elevator3DModel
                model = Elevator3DModel(self.elevator)
                
                if file_path.endswith('.stl'):
                    model.export_to_stl(file_path)
                elif file_path.endswith('.obj'):
                    model.export_to_obj(file_path)
                else:
                    model.export_to_stl(file_path + '.stl')
                
                self.status_bar.showMessage(f"Modèle exporté vers {file_path}")
            except ImportError as e:
                QMessageBox.warning(self, "Erreur", 
                                  f"Impossible d'exporter le modèle: {str(e)}")


def main():
    """Point d'entrée de l'application"""
    app = QApplication(sys.argv)
    
    # Définir le style
    app.setStyle('Fusion')
    
    # Créer et afficher la fenêtre principale
    window = ElevatorApp()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
