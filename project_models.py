"""
Project Management Models for ENGIPIT

This module defines the data models for managing geotechnical and structural design projects,
including soil investigation databases and project hierarchies.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SoilType(Enum):
    """Classification of soil types according to standard geotechnical classification."""
    CLAY = "Clay"
    SILT = "Silt"
    SAND = "Sand"
    GRAVEL = "Gravel"
    PEAT = "Peat"
    ROCK = "Rock"
    FILL = "Fill"
    MIXED = "Mixed"


class TestType(Enum):
    """Types of geotechnical field and laboratory tests."""
    SPT = "Standard Penetration Test"
    CPT = "Cone Penetration Test"
    VANE = "Vane Shear Test"
    TRIAXIAL = "Triaxial Test"
    DIRECT_SHEAR = "Direct Shear Test"
    CONSOLIDATION = "Consolidation Test"
    ATTERBERG = "Atterberg Limits"
    GRAIN_SIZE = "Grain Size Distribution"


@dataclass
class SoilLayer:
    """
    Represents a single soil layer in a borehole.
    
    Attributes:
        depth_top: Top depth of layer (m below surface)
        depth_bottom: Bottom depth of layer (m below surface)
        soil_type: Classification of soil
        description: Detailed description of soil layer
        unit_weight: Bulk unit weight (kN/m³)
        cohesion: Cohesion (kPa)
        friction_angle: Internal friction angle (degrees)
        water_content: Water content (%)
        plasticity_index: Plasticity index (%)
        liquid_limit: Liquid limit (%)
        spt_n: SPT N-value (blows per 300mm)
        cpt_qc: CPT cone resistance (MPa)
    """
    depth_top: float
    depth_bottom: float
    soil_type: SoilType
    description: str = ""
    unit_weight: Optional[float] = None
    cohesion: Optional[float] = None
    friction_angle: Optional[float] = None
    water_content: Optional[float] = None
    plasticity_index: Optional[float] = None
    liquid_limit: Optional[float] = None
    spt_n: Optional[int] = None
    cpt_qc: Optional[float] = None
    
    @property
    def thickness(self) -> float:
        """Calculate layer thickness."""
        return self.depth_bottom - self.depth_top
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'depth_top': self.depth_top,
            'depth_bottom': self.depth_bottom,
            'soil_type': self.soil_type.value,
            'description': self.description,
            'unit_weight': self.unit_weight,
            'cohesion': self.cohesion,
            'friction_angle': self.friction_angle,
            'water_content': self.water_content,
            'plasticity_index': self.plasticity_index,
            'liquid_limit': self.liquid_limit,
            'spt_n': self.spt_n,
            'cpt_qc': self.cpt_qc,
        }


@dataclass
class Borehole:
    """
    Represents a single borehole in a soil investigation.
    
    Attributes:
        id: Unique identifier for the borehole
        name: Name/number of the borehole (e.g., "BH-01")
        location_x: X coordinate (m)
        location_y: Y coordinate (m)
        ground_level: Ground level elevation (m)
        water_level: Groundwater level depth below surface (m)
        total_depth: Total depth of borehole (m)
        date: Date of investigation
        layers: List of soil layers encountered
        notes: Additional notes or observations
    """
    id: str
    name: str
    location_x: float
    location_y: float
    ground_level: float = 0.0
    water_level: Optional[float] = None
    total_depth: float = 0.0
    date: Optional[datetime] = None
    layers: List[SoilLayer] = field(default_factory=list)
    notes: str = ""
    
    def add_layer(self, layer: SoilLayer) -> None:
        """Add a soil layer to the borehole."""
        self.layers.append(layer)
        self.layers.sort(key=lambda x: x.depth_top)
    
    def get_layer_at_depth(self, depth: float) -> Optional[SoilLayer]:
        """
        Get the soil layer at a specific depth.
        
        Args:
            depth: Depth below surface (m)
            
        Returns:
            SoilLayer if found, None otherwise
        """
        for layer in self.layers:
            if layer.depth_top <= depth < layer.depth_bottom:
                return layer
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'id': self.id,
            'name': self.name,
            'location_x': self.location_x,
            'location_y': self.location_y,
            'ground_level': self.ground_level,
            'water_level': self.water_level,
            'total_depth': self.total_depth,
            'date': self.date.isoformat() if self.date else None,
            'layers': [layer.to_dict() for layer in self.layers],
            'notes': self.notes,
        }


@dataclass
class SoilInvestigation:
    """
    Represents a complete soil investigation for a project.
    
    This is the core of the soil investigation database, similar to the bedrock
    repository concept. It contains all boreholes, tests, and geotechnical data
    for a specific project site.
    
    Attributes:
        id: Unique identifier
        name: Name of the investigation
        project_id: Reference to parent project
        site_description: Description of the site
        investigation_date: Date of investigation
        consultant: Name of geotechnical consultant
        boreholes: List of boreholes
        representative_properties: Site-wide representative soil properties
    """
    id: str
    name: str
    project_id: str
    site_description: str = ""
    investigation_date: Optional[datetime] = None
    consultant: str = ""
    boreholes: List[Borehole] = field(default_factory=list)
    representative_properties: Dict[str, Any] = field(default_factory=dict)
    
    def add_borehole(self, borehole: Borehole) -> None:
        """Add a borehole to the investigation."""
        self.boreholes.append(borehole)
    
    def get_borehole(self, borehole_id: str) -> Optional[Borehole]:
        """Get a specific borehole by ID."""
        for borehole in self.boreholes:
            if borehole.id == borehole_id:
                return borehole
        return None
    
    def get_average_properties(self, depth_range: Optional[tuple] = None) -> Dict[str, float]:
        """
        Calculate average soil properties across all boreholes.
        
        Args:
            depth_range: Optional tuple (depth_top, depth_bottom) to limit averaging
            
        Returns:
            Dictionary with average properties
        """
        properties = {
            'unit_weight': [],
            'cohesion': [],
            'friction_angle': [],
        }
        
        for borehole in self.boreholes:
            for layer in borehole.layers:
                # Check if layer is in depth range
                if depth_range:
                    if layer.depth_top > depth_range[1] or layer.depth_bottom < depth_range[0]:
                        continue
                
                if layer.unit_weight is not None:
                    properties['unit_weight'].append(layer.unit_weight)
                if layer.cohesion is not None:
                    properties['cohesion'].append(layer.cohesion)
                if layer.friction_angle is not None:
                    properties['friction_angle'].append(layer.friction_angle)
        
        # Calculate averages
        result = {}
        for key, values in properties.items():
            if values:
                result[key] = sum(values) / len(values)
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'site_description': self.site_description,
            'investigation_date': self.investigation_date.isoformat() if self.investigation_date else None,
            'consultant': self.consultant,
            'boreholes': [borehole.to_dict() for borehole in self.boreholes],
            'representative_properties': self.representative_properties,
        }


class ProjectStatus(Enum):
    """Status of a geotechnical/structural design project."""
    INITIATED = "Initiated"
    INVESTIGATION = "Soil Investigation"
    PRELIMINARY_DESIGN = "Preliminary Design"
    DETAILED_DESIGN = "Detailed Design"
    REVIEW = "Under Review"
    APPROVED = "Approved"
    CONSTRUCTION = "Construction"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"


class FoundationType(Enum):
    """Types of foundation systems."""
    SHALLOW = "Shallow Foundation"
    DEEP_PILE = "Deep Foundation (Piles)"
    DEEP_CAISSON = "Deep Foundation (Caissons)"
    RETAINING_WALL = "Retaining Wall"
    COMBINED = "Combined Foundation"
    MAT = "Mat Foundation"


@dataclass
class FoundationDesign:
    """
    Represents a foundation design calculation within a project.
    
    Attributes:
        id: Unique identifier
        name: Name of the foundation element
        foundation_type: Type of foundation
        soil_investigation_id: Reference to soil investigation used
        design_parameters: Dictionary of design input parameters
        results: Dictionary of calculation results
        design_standard: Design standard used (e.g., "Fascicule 62 Titre V")
        safety_factor: Overall safety factor achieved
        status: Design status (e.g., "Preliminary", "Final")
        notes: Design notes and assumptions
    """
    id: str
    name: str
    foundation_type: FoundationType
    project_id: str
    soil_investigation_id: Optional[str] = None
    design_parameters: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)
    design_standard: str = "Fascicule 62 Titre V"
    safety_factor: Optional[float] = None
    status: str = "Preliminary"
    notes: str = ""
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'id': self.id,
            'name': self.name,
            'foundation_type': self.foundation_type.value,
            'project_id': self.project_id,
            'soil_investigation_id': self.soil_investigation_id,
            'design_parameters': self.design_parameters,
            'results': self.results,
            'design_standard': self.design_standard,
            'safety_factor': self.safety_factor,
            'status': self.status,
            'notes': self.notes,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'modified_date': self.modified_date.isoformat() if self.modified_date else None,
        }


@dataclass
class GeotechnicalProject:
    """
    Main project entity for geotechnical and structural design work.
    
    This represents the top-level project organization, containing soil investigations,
    foundation designs, and project metadata. This structure enables proper project
    management for engineering firms.
    
    Attributes:
        id: Unique project identifier
        name: Project name
        client: Client name/organization
        location: Project location description
        address: Full project address
        coordinates: GPS coordinates (latitude, longitude)
        project_number: Internal project reference number
        status: Current project status
        start_date: Project start date
        target_completion: Target completion date
        project_manager: Name of project manager
        structural_engineer: Name of structural engineer
        geotechnical_engineer: Name of geotechnical engineer
        description: Project description
        soil_investigations: List of soil investigations
        foundation_designs: List of foundation designs
        documents: List of associated documents
        notes: General project notes
    """
    id: str
    name: str
    client: str = ""
    location: str = ""
    address: str = ""
    coordinates: Optional[tuple] = None
    project_number: str = ""
    status: ProjectStatus = ProjectStatus.INITIATED
    start_date: Optional[datetime] = None
    target_completion: Optional[datetime] = None
    project_manager: str = ""
    structural_engineer: str = ""
    geotechnical_engineer: str = ""
    description: str = ""
    soil_investigations: List[SoilInvestigation] = field(default_factory=list)
    foundation_designs: List[FoundationDesign] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    notes: str = ""
    
    def add_soil_investigation(self, investigation: SoilInvestigation) -> None:
        """Add a soil investigation to the project."""
        investigation.project_id = self.id
        self.soil_investigations.append(investigation)
    
    def add_foundation_design(self, design: FoundationDesign) -> None:
        """Add a foundation design to the project."""
        design.project_id = self.id
        self.foundation_designs.append(design)
    
    def get_active_soil_investigation(self) -> Optional[SoilInvestigation]:
        """Get the most recent soil investigation."""
        if not self.soil_investigations:
            return None
        return max(self.soil_investigations, 
                  key=lambda x: x.investigation_date if x.investigation_date else datetime.min)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'id': self.id,
            'name': self.name,
            'client': self.client,
            'location': self.location,
            'address': self.address,
            'coordinates': self.coordinates,
            'project_number': self.project_number,
            'status': self.status.value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'target_completion': self.target_completion.isoformat() if self.target_completion else None,
            'project_manager': self.project_manager,
            'structural_engineer': self.structural_engineer,
            'geotechnical_engineer': self.geotechnical_engineer,
            'description': self.description,
            'soil_investigations': [inv.to_dict() for inv in self.soil_investigations],
            'foundation_designs': [design.to_dict() for design in self.foundation_designs],
            'documents': self.documents,
            'notes': self.notes,
        }


# Utility functions for project management

def create_example_project() -> GeotechnicalProject:
    """
    Create an example project with sample soil investigation data.
    
    This demonstrates the complete project structure and can be used
    for testing and documentation purposes.
    """
    
    # Create project
    project = GeotechnicalProject(
        id="PROJ-001",
        name="Office Building Foundation Design",
        client="ABC Development Corp",
        location="Brussels, Belgium",
        address="Rue de la Loi 123, 1000 Brussels",
        project_number="2026-GEO-001",
        status=ProjectStatus.DETAILED_DESIGN,
        start_date=datetime(2026, 1, 1),
        project_manager="Jane Smith",
        geotechnical_engineer="John Doe",
        description="5-story office building with basement"
    )
    
    # Create soil investigation
    investigation = SoilInvestigation(
        id="SI-001",
        name="Site Investigation - Phase 1",
        project_id=project.id,
        site_description="Urban site with previous industrial use",
        investigation_date=datetime(2026, 1, 15),
        consultant="GeoTech Consultants NV"
    )
    
    # Create borehole
    borehole = Borehole(
        id="BH-01",
        name="BH-01",
        location_x=50.0,
        location_y=100.0,
        ground_level=10.0,
        water_level=3.5,
        total_depth=15.0,
        date=datetime(2026, 1, 15)
    )
    
    # Add soil layers
    borehole.add_layer(SoilLayer(
        depth_top=0.0,
        depth_bottom=2.0,
        soil_type=SoilType.FILL,
        description="Brown sandy fill with brick fragments",
        unit_weight=18.0,
        cohesion=5.0,
        friction_angle=28.0,
        spt_n=8
    ))
    
    borehole.add_layer(SoilLayer(
        depth_top=2.0,
        depth_bottom=5.0,
        soil_type=SoilType.SAND,
        description="Medium dense brown fine sand",
        unit_weight=19.0,
        cohesion=0.0,
        friction_angle=32.0,
        spt_n=15
    ))
    
    borehole.add_layer(SoilLayer(
        depth_top=5.0,
        depth_bottom=10.0,
        soil_type=SoilType.CLAY,
        description="Stiff grey silty clay",
        unit_weight=20.0,
        cohesion=50.0,
        friction_angle=22.0,
        spt_n=25
    ))
    
    borehole.add_layer(SoilLayer(
        depth_top=10.0,
        depth_bottom=15.0,
        soil_type=SoilType.SAND,
        description="Dense grey sand with gravel",
        unit_weight=21.0,
        cohesion=0.0,
        friction_angle=38.0,
        spt_n=35
    ))
    
    investigation.add_borehole(borehole)
    project.add_soil_investigation(investigation)
    
    return project
