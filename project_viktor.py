"""
VIKTOR Entity Structure for Project Management

This module defines the VIKTOR entity hierarchy for managing geotechnical projects
with integrated soil investigation databases and foundation design calculations.
"""

from viktor import ViktorController, File
from viktor.parametrization import (
    ViktorParametrization, 
    Section, 
    TextField, 
    NumberField,
    OptionField,
    DateField,
    TextAreaField,
    DynamicArray,
    Text,
    Table
)
from viktor.views import (
    DataView, 
    DataResult, 
    DataGroup, 
    DataItem,
    PlotlyView,
    PlotlyResult,
    TableView,
    TableResult
)
from viktor.core import File, UserException
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from project_models import (
    GeotechnicalProject,
    SoilInvestigation,
    Borehole,
    SoilLayer,
    FoundationDesign,
    SoilType,
    ProjectStatus,
    FoundationType,
    create_example_project
)


class ProjectParametrization(ViktorParametrization):
    """
    Parametrization for the main Project entity.
    
    This is the top-level entity in the hierarchy that contains all project
    information, soil investigations, and foundation designs.
    """
    
    # Project Information
    project_info = Section("Project Information")
    project_info.project_name = TextField("Project Name", default="New Project")
    project_info.project_number = TextField("Project Number", default="")
    project_info.client = TextField("Client", default="")
    project_info.location = TextField("Location", default="")
    project_info.address = TextAreaField("Address", default="")
    project_info.description = TextAreaField("Project Description", default="")
    
    # Project Team
    project_team = Section("Project Team")
    project_team.project_manager = TextField("Project Manager", default="")
    project_team.geotechnical_engineer = TextField("Geotechnical Engineer", default="")
    project_team.structural_engineer = TextField("Structural Engineer", default="")
    
    # Project Status
    project_status_section = Section("Project Status")
    project_status_section.status = OptionField(
        "Project Status",
        options=[
            "initiated", "investigation", "preliminary_design",
            "detailed_design", "review", "approved", "construction",
            "completed", "on_hold"
        ],
        default="initiated",
        variant="radio-inline"
    )
    project_status_section.start_date = DateField("Start Date", default=datetime.now())
    project_status_section.target_completion = DateField("Target Completion Date", 
                                                         default=datetime.now())
    
    # Notes
    notes_section = Section("Project Notes")
    notes_section.notes = TextAreaField("Notes", default="")


class SoilInvestigationParametrization(ViktorParametrization):
    """
    Parametrization for Soil Investigation entity.
    
    Child of Project entity. Contains borehole data and geotechnical investigation
    results that form the soil investigation database.
    """
    
    # Investigation Information
    investigation_info = Section("Investigation Information")
    investigation_info.name = TextField("Investigation Name", 
                                       default="Site Investigation")
    investigation_info.consultant = TextField("Geotechnical Consultant", default="")
    investigation_info.investigation_date = DateField("Investigation Date",
                                                      default=datetime.now())
    investigation_info.site_description = TextAreaField("Site Description", default="")
    
    # Representative Soil Properties
    representative_props = Section("Representative Soil Properties")
    representative_props.info = Text(
        "These are site-wide representative properties derived from the investigation."
    )
    representative_props.rep_unit_weight = NumberField(
        "Representative Unit Weight",
        suffix="kN/m³",
        default=18.0,
        min=10.0,
        max=25.0
    )
    representative_props.rep_cohesion = NumberField(
        "Representative Cohesion",
        suffix="kPa",
        default=10.0,
        min=0.0,
        max=200.0
    )
    representative_props.rep_friction_angle = NumberField(
        "Representative Friction Angle",
        suffix="°",
        default=30.0,
        min=0.0,
        max=50.0
    )
    
    # Notes
    notes_section = Section("Investigation Notes")
    notes_section.notes = TextAreaField("Notes and Observations", default="")


class BoreholeParametrization(ViktorParametrization):
    """
    Parametrization for Borehole entity.
    
    Child of SoilInvestigation entity. Contains detailed soil layer data
    for a single borehole location.
    """
    
    # Borehole Information
    borehole_info = Section("Borehole Information")
    borehole_info.name = TextField("Borehole Name", default="BH-01")
    borehole_info.location_x = NumberField("X Coordinate", suffix="m", default=0.0)
    borehole_info.location_y = NumberField("Y Coordinate", suffix="m", default=0.0)
    borehole_info.ground_level = NumberField("Ground Level", suffix="m", default=0.0)
    borehole_info.water_level = NumberField("Water Level (depth below surface)", 
                                           suffix="m", default=3.0, min=0.0)
    borehole_info.total_depth = NumberField("Total Depth", suffix="m", 
                                           default=10.0, min=0.0)
    borehole_info.date = DateField("Drilling Date", default=datetime.now())
    
    # Soil Layers
    soil_layers = Section("Soil Layers")
    soil_layers.info = Text(
        "Define soil layers encountered in this borehole. Layers should be in order "
        "from top to bottom."
    )
    soil_layers.layers = DynamicArray("Soil Layers")
    soil_layers.layers.depth_top = NumberField("Depth Top", suffix="m", default=0.0)
    soil_layers.layers.depth_bottom = NumberField("Depth Bottom", suffix="m", default=1.0)
    soil_layers.layers.soil_type = OptionField(
        "Soil Type",
        options=["clay", "silt", "sand", "gravel", "peat", "rock", "fill", "mixed"],
        default="sand",
        variant="dropdown"
    )
    soil_layers.layers.description = TextField("Description", default="")
    soil_layers.layers.unit_weight = NumberField("Unit Weight", suffix="kN/m³", 
                                                 default=18.0, min=10.0, max=25.0)
    soil_layers.layers.cohesion = NumberField("Cohesion", suffix="kPa", 
                                             default=0.0, min=0.0, max=200.0)
    soil_layers.layers.friction_angle = NumberField("Friction Angle", suffix="°",
                                                    default=30.0, min=0.0, max=50.0)
    soil_layers.layers.spt_n = NumberField("SPT N-value", default=10, min=0, max=100)
    
    # Notes
    notes_section = Section("Notes")
    notes_section.notes = TextAreaField("Additional Notes", default="")


class FoundationDesignParametrization(ViktorParametrization):
    """
    Parametrization for Foundation Design entity.
    
    Child of Project entity. Contains foundation design calculations
    linked to soil investigation data.
    """
    
    # Design Information
    design_info = Section("Design Information")
    design_info.name = TextField("Foundation Name", default="Foundation-01")
    design_info.foundation_type = OptionField(
        "Foundation Type",
        options=[
            "shallow_foundation",
            "deep_foundation_piles",
            "retaining_wall",
            "mat_foundation"
        ],
        default="shallow_foundation",
        variant="radio-inline"
    )
    design_info.design_standard = OptionField(
        "Design Standard",
        options=[
            "fascicule_62",
            "eurocode_7",
            "belgian_code",
            "other"
        ],
        default="fascicule_62",
        variant="dropdown"
    )
    design_info.status = OptionField(
        "Design Status",
        options=["preliminary", "detailed", "final", "approved"],
        default="preliminary",
        variant="radio-inline"
    )
    
    # Link to Soil Investigation
    soil_data_section = Section("Soil Data Source")
    soil_data_section.use_project_investigation = OptionField(
        "Soil Data Source",
        options=["project_investigation", "manual_input"],
        default="project_investigation",
        variant="radio-inline"
    )
    soil_data_section.info = Text(
        "Select 'Project Investigation' to use data from the project's soil investigation, "
        "or 'Manual Input' to specify soil properties directly."
    )
    
    # Manual Soil Properties (visible when manual_input selected)
    manual_soil = Section("Manual Soil Properties", 
                         visible=lambda params, **kwargs: 
                         params.soil_data_section.use_project_investigation == "manual_input")
    manual_soil.unit_weight = NumberField("Unit Weight", suffix="kN/m³", 
                                         default=18.0, min=10.0, max=25.0)
    manual_soil.cohesion = NumberField("Cohesion", suffix="kPa", 
                                      default=10.0, min=0.0, max=200.0)
    manual_soil.friction_angle = NumberField("Friction Angle", suffix="°",
                                            default=30.0, min=0.0, max=50.0)
    
    # Shallow Foundation Parameters
    shallow = Section("Shallow Foundation Parameters",
                     visible=lambda params, **kwargs: 
                     params.design_info.foundation_type == "shallow_foundation")
    shallow.width = NumberField("Width (B)", suffix="m", default=2.0, min=0.5, max=10.0)
    shallow.length = NumberField("Length (L)", suffix="m", default=2.0, min=0.5, max=20.0)
    shallow.depth = NumberField("Depth (Df)", suffix="m", default=1.0, min=0.5, max=5.0)
    shallow.applied_load = NumberField("Applied Load", suffix="kN", 
                                      default=1000.0, min=0.0, max=50000.0)
    
    # Deep Foundation Parameters
    deep = Section("Deep Foundation Parameters",
                  visible=lambda params, **kwargs: 
                  params.design_info.foundation_type == "deep_foundation_piles")
    deep.pile_diameter = NumberField("Pile Diameter", suffix="m", 
                                    default=0.6, min=0.3, max=2.0)
    deep.pile_length = NumberField("Pile Length", suffix="m", 
                                  default=15.0, min=5.0, max=50.0)
    deep.pile_type = OptionField("Pile Type", 
                                options=["driven", "bored"], 
                                default="bored",
                                variant="radio-inline")
    deep.num_piles = NumberField("Number of Piles", default=1, min=1, max=50)
    deep.pile_spacing = NumberField("Pile Spacing", suffix="m", 
                                   default=3.0, min=1.0, max=10.0,
                                   visible=lambda params, **kwargs: 
                                   params.deep.num_piles > 1)
    deep.total_load = NumberField("Total Applied Load", suffix="kN",
                                 default=5000.0, min=0.0, max=100000.0)
    
    # Retaining Wall Parameters
    wall = Section("Retaining Wall Parameters",
                  visible=lambda params, **kwargs: 
                  params.design_info.foundation_type == "retaining_wall")
    wall.height = NumberField("Wall Height", suffix="m", default=4.0, min=1.0, max=10.0)
    wall.thickness = NumberField("Wall Thickness", suffix="m", 
                                default=0.5, min=0.3, max=2.0)
    wall.surcharge = NumberField("Surcharge Load", suffix="kPa", 
                                default=10.0, min=0.0, max=100.0)
    
    # Design Notes
    notes_section = Section("Design Notes and Assumptions")
    notes_section.notes = TextAreaField("Notes", default="")


# Controller classes for each entity type

class ProjectController(ViktorController):
    """Controller for Project entity."""
    label = "Project"
    parametrization = ProjectParametrization
    
    @DataView("Project Overview", duration_guess=1)
    def project_overview(self, params, **kwargs):
        """Display project information and statistics."""
        
        # Get child entities
        entity = kwargs.get('entity')
        if entity:
            # Count soil investigations and foundation designs
            soil_inv_count = len(list(entity.children(entity_type_names=['SoilInvestigation'])))
            foundation_count = len(list(entity.children(entity_type_names=['FoundationDesign'])))
        else:
            soil_inv_count = 0
            foundation_count = 0
        
        # Project information
        project_data = DataGroup(
            DataItem("Project Name", params.project_info.project_name),
            DataItem("Project Number", params.project_info.project_number or "N/A"),
            DataItem("Client", params.project_info.client or "N/A"),
            DataItem("Location", params.project_info.location or "N/A"),
            DataItem("Status", params.project_status_section.status.replace('_', ' ').title()),
        )
        
        # Project team
        team_data = DataGroup(
            DataItem("Project Manager", params.project_team.project_manager or "N/A"),
            DataItem("Geotechnical Engineer", params.project_team.geotechnical_engineer or "N/A"),
            DataItem("Structural Engineer", params.project_team.structural_engineer or "N/A"),
        )
        
        # Project statistics
        stats_data = DataGroup(
            DataItem("Soil Investigations", soil_inv_count),
            DataItem("Foundation Designs", foundation_count),
            DataItem("Start Date", params.project_status_section.start_date.strftime("%Y-%m-%d") 
                    if params.project_status_section.start_date else "N/A"),
        )
        
        return DataResult(
            project_data,
            team_data,
            stats_data
        )


class SoilInvestigationController(ViktorController):
    """Controller for SoilInvestigation entity."""
    label = "Soil Investigation"
    parametrization = SoilInvestigationParametrization
    
    @DataView("Investigation Summary", duration_guess=1)
    def investigation_summary(self, params, **kwargs):
        """Display soil investigation summary."""
        
        # Get boreholes count
        entity = kwargs.get('entity')
        if entity:
            borehole_count = len(list(entity.children(entity_type_names=['Borehole'])))
        else:
            borehole_count = 0
        
        # Investigation information
        info_data = DataGroup(
            DataItem("Investigation Name", params.investigation_info.name),
            DataItem("Consultant", params.investigation_info.consultant or "N/A"),
            DataItem("Date", params.investigation_info.investigation_date.strftime("%Y-%m-%d")
                    if params.investigation_info.investigation_date else "N/A"),
            DataItem("Number of Boreholes", borehole_count),
        )
        
        # Representative properties
        props_data = DataGroup(
            DataItem("Unit Weight", params.representative_props.rep_unit_weight, suffix="kN/m³"),
            DataItem("Cohesion", params.representative_props.rep_cohesion, suffix="kPa"),
            DataItem("Friction Angle", params.representative_props.rep_friction_angle, suffix="°"),
        )
        
        return DataResult(info_data, props_data)


class BoreholeController(ViktorController):
    """Controller for Borehole entity."""
    label = "Borehole"
    parametrization = BoreholeParametrization
    
    @DataView("Borehole Data", duration_guess=1)
    def borehole_data(self, params, **kwargs):
        """Display borehole information."""
        
        # Borehole information
        info_data = DataGroup(
            DataItem("Borehole Name", params.borehole_info.name),
            DataItem("Location X", params.borehole_info.location_x, suffix="m"),
            DataItem("Location Y", params.borehole_info.location_y, suffix="m"),
            DataItem("Ground Level", params.borehole_info.ground_level, suffix="m"),
            DataItem("Water Level Depth", params.borehole_info.water_level, suffix="m"),
            DataItem("Total Depth", params.borehole_info.total_depth, suffix="m"),
            DataItem("Number of Layers", len(params.soil_layers.layers)),
        )
        
        return DataResult(info_data)
    
    @PlotlyView("Soil Profile", duration_guess=2)
    def soil_profile(self, params, **kwargs):
        """Visualize soil profile."""
        
        fig = go.Figure()
        
        # Create soil profile visualization
        if params.soil_layers.layers:
            for layer in params.soil_layers.layers:
                # Color based on soil type
                color_map = {
                    'clay': 'brown',
                    'silt': 'tan',
                    'sand': 'yellow',
                    'gravel': 'grey',
                    'peat': 'darkbrown',
                    'rock': 'darkgrey',
                    'fill': 'lightgrey',
                    'mixed': 'beige'
                }
                color = color_map.get(layer.soil_type, 'white')
                
                # Draw layer rectangle
                fig.add_trace(go.Scatter(
                    x=[0, 1, 1, 0, 0],
                    y=[-layer.depth_top, -layer.depth_top, -layer.depth_bottom, 
                       -layer.depth_bottom, -layer.depth_top],
                    fill='toself',
                    fillcolor=color,
                    line=dict(color='black', width=1),
                    name=f"{layer.soil_type.title()} ({layer.depth_top}-{layer.depth_bottom}m)",
                    hovertemplate=(
                        f"<b>{layer.soil_type.title()}</b><br>"
                        f"Depth: {layer.depth_top}-{layer.depth_bottom}m<br>"
                        f"γ: {layer.unit_weight} kN/m³<br>"
                        f"c: {layer.cohesion} kPa<br>"
                        f"φ: {layer.friction_angle}°<br>"
                        f"SPT: {layer.spt_n}<extra></extra>"
                    )
                ))
        
        # Add water level line
        if params.borehole_info.water_level:
            fig.add_hline(
                y=-params.borehole_info.water_level,
                line_dash="dash",
                line_color="blue",
                annotation_text="Water Level"
            )
        
        fig.update_layout(
            title=f"Soil Profile - {params.borehole_info.name}",
            xaxis_title="",
            yaxis_title="Depth (m)",
            showlegend=True,
            height=600,
            hovermode='closest'
        )
        
        fig.update_xaxis(showticklabels=False, range=[-0.5, 1.5])
        fig.update_yaxis(autorange="reversed")
        
        return PlotlyResult(fig.to_json())


class FoundationDesignController(ViktorController):
    """Controller for FoundationDesign entity."""
    label = "Foundation Design"
    parametrization = FoundationDesignParametrization
    
    @DataView("Design Summary", duration_guess=1)
    def design_summary(self, params, **kwargs):
        """Display foundation design summary."""
        
        # Design information
        info_data = DataGroup(
            DataItem("Foundation Name", params.design_info.name),
            DataItem("Type", params.design_info.foundation_type.replace('_', ' ').title()),
            DataItem("Design Standard", params.design_info.design_standard.replace('_', ' ').title()),
            DataItem("Status", params.design_info.status.title()),
        )
        
        # Soil data source
        soil_source_data = DataGroup(
            DataItem("Soil Data Source", 
                    "Project Investigation" if params.soil_data_section.use_project_investigation == "project_investigation" 
                    else "Manual Input"),
        )
        
        return DataResult(info_data, soil_source_data)
