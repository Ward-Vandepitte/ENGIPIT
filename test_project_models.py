"""
Unit tests for project management models.

Tests the data models for projects, soil investigations, boreholes, and foundation designs.
"""

import unittest
from datetime import datetime
from project_models import (
    SoilType, TestType, ProjectStatus, FoundationType,
    SoilLayer, Borehole, SoilInvestigation,
    FoundationDesign, GeotechnicalProject,
    create_example_project
)


class TestSoilLayer(unittest.TestCase):
    """Test SoilLayer data model."""
    
    def test_soil_layer_creation(self):
        """Test creating a soil layer."""
        layer = SoilLayer(
            depth_top=0.0,
            depth_bottom=2.0,
            soil_type=SoilType.SAND,
            description="Medium dense sand",
            unit_weight=19.0,
            cohesion=0.0,
            friction_angle=32.0,
            spt_n=15
        )
        
        self.assertEqual(layer.depth_top, 0.0)
        self.assertEqual(layer.depth_bottom, 2.0)
        self.assertEqual(layer.soil_type, SoilType.SAND)
        self.assertEqual(layer.thickness, 2.0)
    
    def test_layer_thickness(self):
        """Test thickness calculation."""
        layer = SoilLayer(
            depth_top=2.5,
            depth_bottom=5.0,
            soil_type=SoilType.CLAY
        )
        
        self.assertEqual(layer.thickness, 2.5)
    
    def test_layer_to_dict(self):
        """Test converting layer to dictionary."""
        layer = SoilLayer(
            depth_top=0.0,
            depth_bottom=2.0,
            soil_type=SoilType.SAND,
            unit_weight=19.0
        )
        
        layer_dict = layer.to_dict()
        self.assertIsInstance(layer_dict, dict)
        self.assertEqual(layer_dict['depth_top'], 0.0)
        self.assertEqual(layer_dict['soil_type'], 'Sand')


class TestBorehole(unittest.TestCase):
    """Test Borehole data model."""
    
    def test_borehole_creation(self):
        """Test creating a borehole."""
        borehole = Borehole(
            id="BH-01",
            name="BH-01",
            location_x=100.0,
            location_y=200.0,
            ground_level=10.0,
            water_level=3.5,
            total_depth=15.0
        )
        
        self.assertEqual(borehole.id, "BH-01")
        self.assertEqual(borehole.location_x, 100.0)
        self.assertEqual(borehole.water_level, 3.5)
    
    def test_add_layer(self):
        """Test adding layers to borehole."""
        borehole = Borehole(
            id="BH-01",
            name="BH-01",
            location_x=0.0,
            location_y=0.0
        )
        
        layer1 = SoilLayer(
            depth_top=0.0,
            depth_bottom=2.0,
            soil_type=SoilType.SAND
        )
        layer2 = SoilLayer(
            depth_top=2.0,
            depth_bottom=5.0,
            soil_type=SoilType.CLAY
        )
        
        borehole.add_layer(layer1)
        borehole.add_layer(layer2)
        
        self.assertEqual(len(borehole.layers), 2)
        self.assertEqual(borehole.layers[0].soil_type, SoilType.SAND)
    
    def test_get_layer_at_depth(self):
        """Test retrieving layer at specific depth."""
        borehole = Borehole(
            id="BH-01",
            name="BH-01",
            location_x=0.0,
            location_y=0.0
        )
        
        layer1 = SoilLayer(
            depth_top=0.0,
            depth_bottom=2.0,
            soil_type=SoilType.SAND
        )
        layer2 = SoilLayer(
            depth_top=2.0,
            depth_bottom=5.0,
            soil_type=SoilType.CLAY
        )
        
        borehole.add_layer(layer1)
        borehole.add_layer(layer2)
        
        # Test depth in first layer
        layer_at_1m = borehole.get_layer_at_depth(1.0)
        self.assertEqual(layer_at_1m.soil_type, SoilType.SAND)
        
        # Test depth in second layer
        layer_at_3m = borehole.get_layer_at_depth(3.0)
        self.assertEqual(layer_at_3m.soil_type, SoilType.CLAY)
        
        # Test depth beyond layers
        layer_at_10m = borehole.get_layer_at_depth(10.0)
        self.assertIsNone(layer_at_10m)
    
    def test_borehole_to_dict(self):
        """Test converting borehole to dictionary."""
        borehole = Borehole(
            id="BH-01",
            name="BH-01",
            location_x=100.0,
            location_y=200.0
        )
        
        borehole_dict = borehole.to_dict()
        self.assertIsInstance(borehole_dict, dict)
        self.assertEqual(borehole_dict['id'], "BH-01")
        self.assertEqual(borehole_dict['location_x'], 100.0)


class TestSoilInvestigation(unittest.TestCase):
    """Test SoilInvestigation data model."""
    
    def test_investigation_creation(self):
        """Test creating a soil investigation."""
        investigation = SoilInvestigation(
            id="SI-001",
            name="Site Investigation Phase 1",
            project_id="PROJ-001",
            site_description="Urban site",
            consultant="GeoTech Consultants"
        )
        
        self.assertEqual(investigation.id, "SI-001")
        self.assertEqual(investigation.project_id, "PROJ-001")
        self.assertEqual(len(investigation.boreholes), 0)
    
    def test_add_borehole(self):
        """Test adding boreholes to investigation."""
        investigation = SoilInvestigation(
            id="SI-001",
            name="Investigation",
            project_id="PROJ-001"
        )
        
        borehole = Borehole(
            id="BH-01",
            name="BH-01",
            location_x=0.0,
            location_y=0.0
        )
        
        investigation.add_borehole(borehole)
        self.assertEqual(len(investigation.boreholes), 1)
    
    def test_get_borehole(self):
        """Test retrieving specific borehole."""
        investigation = SoilInvestigation(
            id="SI-001",
            name="Investigation",
            project_id="PROJ-001"
        )
        
        borehole1 = Borehole(id="BH-01", name="BH-01", location_x=0.0, location_y=0.0)
        borehole2 = Borehole(id="BH-02", name="BH-02", location_x=10.0, location_y=10.0)
        
        investigation.add_borehole(borehole1)
        investigation.add_borehole(borehole2)
        
        retrieved = investigation.get_borehole("BH-02")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.location_x, 10.0)
    
    def test_get_average_properties(self):
        """Test calculating average properties."""
        investigation = SoilInvestigation(
            id="SI-001",
            name="Investigation",
            project_id="PROJ-001"
        )
        
        # Create borehole with layers
        borehole = Borehole(id="BH-01", name="BH-01", location_x=0.0, location_y=0.0)
        
        layer1 = SoilLayer(
            depth_top=0.0,
            depth_bottom=2.0,
            soil_type=SoilType.SAND,
            unit_weight=18.0,
            friction_angle=30.0
        )
        layer2 = SoilLayer(
            depth_top=2.0,
            depth_bottom=5.0,
            soil_type=SoilType.CLAY,
            unit_weight=20.0,
            cohesion=50.0,
            friction_angle=22.0
        )
        
        borehole.add_layer(layer1)
        borehole.add_layer(layer2)
        investigation.add_borehole(borehole)
        
        avg_props = investigation.get_average_properties()
        
        self.assertIn('unit_weight', avg_props)
        self.assertAlmostEqual(avg_props['unit_weight'], 19.0, places=1)
        self.assertIn('friction_angle', avg_props)


class TestFoundationDesign(unittest.TestCase):
    """Test FoundationDesign data model."""
    
    def test_design_creation(self):
        """Test creating a foundation design."""
        design = FoundationDesign(
            id="FD-001",
            name="Foundation A",
            foundation_type=FoundationType.SHALLOW,
            project_id="PROJ-001",
            soil_investigation_id="SI-001"
        )
        
        self.assertEqual(design.id, "FD-001")
        self.assertEqual(design.foundation_type, FoundationType.SHALLOW)
        self.assertEqual(design.design_standard, "Fascicule 62 Titre V")
    
    def test_design_to_dict(self):
        """Test converting design to dictionary."""
        design = FoundationDesign(
            id="FD-001",
            name="Foundation A",
            foundation_type=FoundationType.SHALLOW,
            project_id="PROJ-001"
        )
        
        design_dict = design.to_dict()
        self.assertIsInstance(design_dict, dict)
        self.assertEqual(design_dict['id'], "FD-001")


class TestGeotechnicalProject(unittest.TestCase):
    """Test GeotechnicalProject data model."""
    
    def test_project_creation(self):
        """Test creating a project."""
        project = GeotechnicalProject(
            id="PROJ-001",
            name="Office Building Project",
            client="ABC Corp",
            location="Brussels"
        )
        
        self.assertEqual(project.id, "PROJ-001")
        self.assertEqual(project.name, "Office Building Project")
        self.assertEqual(project.status, ProjectStatus.INITIATED)
    
    def test_add_soil_investigation(self):
        """Test adding soil investigation to project."""
        project = GeotechnicalProject(
            id="PROJ-001",
            name="Project"
        )
        
        investigation = SoilInvestigation(
            id="SI-001",
            name="Investigation",
            project_id=""
        )
        
        project.add_soil_investigation(investigation)
        
        self.assertEqual(len(project.soil_investigations), 1)
        self.assertEqual(investigation.project_id, "PROJ-001")
    
    def test_add_foundation_design(self):
        """Test adding foundation design to project."""
        project = GeotechnicalProject(
            id="PROJ-001",
            name="Project"
        )
        
        design = FoundationDesign(
            id="FD-001",
            name="Foundation",
            foundation_type=FoundationType.SHALLOW,
            project_id=""
        )
        
        project.add_foundation_design(design)
        
        self.assertEqual(len(project.foundation_designs), 1)
        self.assertEqual(design.project_id, "PROJ-001")
    
    def test_get_active_soil_investigation(self):
        """Test getting most recent soil investigation."""
        project = GeotechnicalProject(
            id="PROJ-001",
            name="Project"
        )
        
        investigation1 = SoilInvestigation(
            id="SI-001",
            name="Phase 1",
            project_id="PROJ-001",
            investigation_date=datetime(2025, 1, 1)
        )
        investigation2 = SoilInvestigation(
            id="SI-002",
            name="Phase 2",
            project_id="PROJ-001",
            investigation_date=datetime(2025, 6, 1)
        )
        
        project.add_soil_investigation(investigation1)
        project.add_soil_investigation(investigation2)
        
        active = project.get_active_soil_investigation()
        self.assertEqual(active.id, "SI-002")
    
    def test_project_to_dict(self):
        """Test converting project to dictionary."""
        project = GeotechnicalProject(
            id="PROJ-001",
            name="Project"
        )
        
        project_dict = project.to_dict()
        self.assertIsInstance(project_dict, dict)
        self.assertEqual(project_dict['id'], "PROJ-001")


class TestExampleProject(unittest.TestCase):
    """Test example project creation."""
    
    def test_create_example_project(self):
        """Test creating example project with full structure."""
        project = create_example_project()
        
        # Check project
        self.assertEqual(project.id, "PROJ-001")
        self.assertGreater(len(project.name), 0)
        
        # Check soil investigations
        self.assertEqual(len(project.soil_investigations), 1)
        investigation = project.soil_investigations[0]
        
        # Check boreholes
        self.assertEqual(len(investigation.boreholes), 1)
        borehole = investigation.boreholes[0]
        
        # Check layers
        self.assertGreater(len(borehole.layers), 0)
        
        # Check first layer
        first_layer = borehole.layers[0]
        self.assertIsNotNone(first_layer.soil_type)
        self.assertIsNotNone(first_layer.unit_weight)


if __name__ == '__main__':
    unittest.main()
