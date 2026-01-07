"""
ENGIPIT - Geotechnical Foundation Design Toolset

A comprehensive VIKTOR application for rapid design calculations of foundation systems.
This toolset enables civil engineers specialized in geotechnics to perform various
foundation design calculations including shallow foundations, deep foundations, and
retaining walls.
"""

from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, Section, NumberField, OptionField
from viktor.views import PlotlyView, PlotlyResult, DataGroup, DataItem, DataView, DataResult
import plotly.graph_objects as go
from typing import Tuple
import math


class Parametrization(ViktorParametrization):
    """Parametrization for foundation design calculations."""
    
    # Foundation Type Selection
    foundation_type = Section("Foundation Type")
    foundation_type.type_selection = OptionField(
        "Select Foundation Type",
        options=[
            "shallow_foundation",
            "deep_foundation_single_pile",
            "deep_foundation_pile_group",
            "retaining_wall"
        ],
        default="shallow_foundation",
        variant="radio-inline"
    )
    
    # Soil Properties
    soil_properties = Section("Soil Properties")
    soil_properties.unit_weight = NumberField(
        "Unit Weight of Soil",
        suffix="kN/m³",
        default=18.0,
        min=10.0,
        max=25.0
    )
    soil_properties.cohesion = NumberField(
        "Cohesion (c)",
        suffix="kPa",
        default=10.0,
        min=0.0,
        max=100.0
    )
    soil_properties.friction_angle = NumberField(
        "Internal Friction Angle (φ)",
        suffix="°",
        default=30.0,
        min=0.0,
        max=45.0
    )
    
    # Shallow Foundation Parameters
    shallow_foundation = Section("Shallow Foundation", visible=lambda params, **kwargs: params.foundation_type.type_selection == "shallow_foundation")
    shallow_foundation.foundation_width = NumberField(
        "Foundation Width (B)",
        suffix="m",
        default=2.0,
        min=0.5,
        max=10.0
    )
    shallow_foundation.foundation_length = NumberField(
        "Foundation Length (L)",
        suffix="m",
        default=2.0,
        min=0.5,
        max=20.0
    )
    shallow_foundation.foundation_depth = NumberField(
        "Foundation Depth (Df)",
        suffix="m",
        default=1.0,
        min=0.5,
        max=5.0
    )
    shallow_foundation.applied_load = NumberField(
        "Applied Vertical Load (Q)",
        suffix="kN",
        default=1000.0,
        min=0.0,
        max=10000.0
    )
    
    # Deep Foundation Parameters - Single Pile
    single_pile = Section("Single Pile", visible=lambda params, **kwargs: params.foundation_type.type_selection == "deep_foundation_single_pile")
    single_pile.pile_diameter = NumberField(
        "Pile Diameter",
        suffix="m",
        default=0.6,
        min=0.3,
        max=2.0
    )
    single_pile.pile_length = NumberField(
        "Pile Length",
        suffix="m",
        default=15.0,
        min=5.0,
        max=50.0
    )
    single_pile.pile_type = OptionField(
        "Pile Type",
        options=["driven", "bored"],
        default="bored",
        variant="radio-inline"
    )
    single_pile.applied_load_pile = NumberField(
        "Applied Load per Pile",
        suffix="kN",
        default=1000.0,
        min=0.0,
        max=5000.0
    )
    
    # Deep Foundation Parameters - Pile Group
    pile_group = Section("Pile Group", visible=lambda params, **kwargs: params.foundation_type.type_selection == "deep_foundation_pile_group")
    pile_group.pile_diameter_group = NumberField(
        "Pile Diameter",
        suffix="m",
        default=0.6,
        min=0.3,
        max=2.0
    )
    pile_group.pile_length_group = NumberField(
        "Pile Length",
        suffix="m",
        default=15.0,
        min=5.0,
        max=50.0
    )
    pile_group.num_piles = NumberField(
        "Number of Piles",
        default=4,
        min=2,
        max=20,
        step=1
    )
    pile_group.pile_spacing = NumberField(
        "Pile Spacing",
        suffix="m",
        default=1.8,
        min=1.5,
        max=5.0
    )
    pile_group.total_load = NumberField(
        "Total Applied Load",
        suffix="kN",
        default=4000.0,
        min=0.0,
        max=50000.0
    )
    
    # Retaining Wall Parameters
    retaining_wall = Section("Retaining Wall", visible=lambda params, **kwargs: params.foundation_type.type_selection == "retaining_wall")
    retaining_wall.wall_height = NumberField(
        "Wall Height (H)",
        suffix="m",
        default=5.0,
        min=2.0,
        max=15.0
    )
    retaining_wall.wall_thickness = NumberField(
        "Wall Thickness",
        suffix="m",
        default=0.4,
        min=0.2,
        max=1.0
    )
    retaining_wall.surcharge = NumberField(
        "Surcharge Load",
        suffix="kPa",
        default=10.0,
        min=0.0,
        max=50.0
    )


class ShallowFoundationCalculator:
    """Calculator for shallow foundation bearing capacity and settlement."""
    
    @staticmethod
    def calculate_bearing_capacity_factors(friction_angle: float) -> Tuple[float, float, float]:
        """
        Calculate Terzaghi bearing capacity factors.
        
        Args:
            friction_angle: Internal friction angle in degrees
            
        Returns:
            Tuple of (Nc, Nq, Nγ) bearing capacity factors
        """
        phi_rad = math.radians(friction_angle)
        
        # Nq factor
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + friction_angle / 2))) ** 2
        
        # Nc factor
        Nc = (Nq - 1) / math.tan(phi_rad) if friction_angle > 0 else 5.14
        
        # Nγ factor (Terzaghi)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)
        
        return Nc, Nq, Ngamma
    
    @staticmethod
    def calculate_ultimate_bearing_capacity(
        width: float,
        length: float,
        depth: float,
        unit_weight: float,
        cohesion: float,
        friction_angle: float
    ) -> float:
        """
        Calculate ultimate bearing capacity using Terzaghi's equation.
        
        Args:
            width: Foundation width in meters
            length: Foundation length in meters
            depth: Foundation depth in meters
            unit_weight: Unit weight of soil in kN/m³
            cohesion: Cohesion in kPa
            friction_angle: Internal friction angle in degrees
            
        Returns:
            Ultimate bearing capacity in kPa
        """
        Nc, Nq, Ngamma = ShallowFoundationCalculator.calculate_bearing_capacity_factors(friction_angle)
        
        # Terzaghi's bearing capacity equation
        # qu = c*Nc + γ*Df*Nq + 0.5*γ*B*Nγ
        qu = (cohesion * Nc + 
              unit_weight * depth * Nq + 
              0.5 * unit_weight * width * Ngamma)
        
        return qu
    
    @staticmethod
    def calculate_allowable_bearing_capacity(ultimate_capacity: float, factor_of_safety: float = 3.0) -> float:
        """
        Calculate allowable bearing capacity.
        
        Args:
            ultimate_capacity: Ultimate bearing capacity in kPa
            factor_of_safety: Factor of safety (default: 3.0)
            
        Returns:
            Allowable bearing capacity in kPa
        """
        return ultimate_capacity / factor_of_safety
    
    @staticmethod
    def calculate_applied_pressure(load: float, width: float, length: float) -> float:
        """
        Calculate applied pressure on foundation.
        
        Args:
            load: Applied load in kN
            width: Foundation width in meters
            length: Foundation length in meters
            
        Returns:
            Applied pressure in kPa
        """
        area = width * length
        return load / area


class DeepFoundationCalculator:
    """Calculator for deep foundation (pile) capacity."""
    
    @staticmethod
    def calculate_pile_end_bearing(
        pile_diameter: float,
        unit_weight: float,
        pile_length: float,
        friction_angle: float,
        cohesion: float
    ) -> float:
        """
        Calculate pile end bearing capacity.
        
        Args:
            pile_diameter: Pile diameter in meters
            unit_weight: Unit weight of soil in kN/m³
            pile_length: Pile length in meters
            friction_angle: Internal friction angle in degrees
            cohesion: Cohesion in kPa
            
        Returns:
            End bearing capacity in kN
        """
        area = math.pi * (pile_diameter / 2) ** 2
        
        # Effective stress at pile tip
        sigma_v = unit_weight * pile_length
        
        # Bearing capacity factor
        phi_rad = math.radians(friction_angle)
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + friction_angle / 2))) ** 2
        
        # End bearing capacity
        qb = cohesion * 9 + sigma_v * Nq  # Simplified approach
        Qb = qb * area
        
        return Qb
    
    @staticmethod
    def calculate_pile_skin_friction(
        pile_diameter: float,
        pile_length: float,
        unit_weight: float,
        friction_angle: float,
        cohesion: float,
        pile_type: str
    ) -> float:
        """
        Calculate pile skin friction capacity.
        
        Args:
            pile_diameter: Pile diameter in meters
            pile_length: Pile length in meters
            unit_weight: Unit weight of soil in kN/m³
            friction_angle: Internal friction angle in degrees
            cohesion: Cohesion in kPa
            pile_type: Type of pile ("driven" or "bored")
            
        Returns:
            Skin friction capacity in kN
        """
        perimeter = math.pi * pile_diameter
        
        # Average effective stress along pile
        sigma_v_avg = unit_weight * pile_length / 2
        
        # Skin friction coefficient
        K = 0.8 if pile_type == "driven" else 0.7
        delta = 0.75 * friction_angle if pile_type == "driven" else 0.6 * friction_angle
        
        # Unit skin friction
        fs = cohesion + K * sigma_v_avg * math.tan(math.radians(delta))
        
        # Total skin friction
        Qs = fs * perimeter * pile_length
        
        return Qs
    
    @staticmethod
    def calculate_pile_capacity(
        pile_diameter: float,
        pile_length: float,
        unit_weight: float,
        friction_angle: float,
        cohesion: float,
        pile_type: str,
        factor_of_safety: float = 2.5
    ) -> Tuple[float, float, float, float]:
        """
        Calculate total pile capacity.
        
        Args:
            pile_diameter: Pile diameter in meters
            pile_length: Pile length in meters
            unit_weight: Unit weight of soil in kN/m³
            friction_angle: Internal friction angle in degrees
            cohesion: Cohesion in kPa
            pile_type: Type of pile ("driven" or "bored")
            factor_of_safety: Factor of safety (default: 2.5)
            
        Returns:
            Tuple of (ultimate capacity, allowable capacity, end bearing, skin friction) in kN
        """
        Qb = DeepFoundationCalculator.calculate_pile_end_bearing(
            pile_diameter, unit_weight, pile_length, friction_angle, cohesion
        )
        
        Qs = DeepFoundationCalculator.calculate_pile_skin_friction(
            pile_diameter, pile_length, unit_weight, friction_angle, cohesion, pile_type
        )
        
        Qu = Qb + Qs
        Qa = Qu / factor_of_safety
        
        return Qu, Qa, Qb, Qs
    
    @staticmethod
    def calculate_pile_group_efficiency(num_piles: int, spacing: float, diameter: float) -> float:
        """
        Calculate pile group efficiency factor.
        
        Args:
            num_piles: Number of piles in group
            spacing: Pile spacing in meters
            diameter: Pile diameter in meters
            
        Returns:
            Group efficiency factor (0-1)
        """
        s_d_ratio = spacing / diameter
        
        # Simplified efficiency calculation
        if s_d_ratio >= 6:
            efficiency = 1.0
        elif s_d_ratio >= 3:
            efficiency = 0.7 + 0.3 * (s_d_ratio - 3) / 3
        else:
            efficiency = 0.7 * s_d_ratio / 3
        
        return min(efficiency, 1.0)


class RetainingWallCalculator:
    """Calculator for retaining wall earth pressures and stability."""
    
    @staticmethod
    def calculate_active_earth_pressure_coefficient(friction_angle: float) -> float:
        """
        Calculate active earth pressure coefficient using Rankine theory.
        
        Args:
            friction_angle: Internal friction angle in degrees
            
        Returns:
            Active earth pressure coefficient Ka
        """
        Ka = math.tan(math.radians(45 - friction_angle / 2)) ** 2
        return Ka
    
    @staticmethod
    def calculate_passive_earth_pressure_coefficient(friction_angle: float) -> float:
        """
        Calculate passive earth pressure coefficient using Rankine theory.
        
        Args:
            friction_angle: Internal friction angle in degrees
            
        Returns:
            Passive earth pressure coefficient Kp
        """
        Kp = math.tan(math.radians(45 + friction_angle / 2)) ** 2
        return Kp
    
    @staticmethod
    def calculate_total_active_force(
        wall_height: float,
        unit_weight: float,
        friction_angle: float,
        cohesion: float,
        surcharge: float
    ) -> Tuple[float, float]:
        """
        Calculate total active earth pressure force.
        
        Args:
            wall_height: Height of wall in meters
            unit_weight: Unit weight of soil in kN/m³
            friction_angle: Internal friction angle in degrees
            cohesion: Cohesion in kPa
            surcharge: Surcharge load in kPa
            
        Returns:
            Tuple of (total force in kN/m, force location from base in m)
        """
        Ka = RetainingWallCalculator.calculate_active_earth_pressure_coefficient(friction_angle)
        
        # Active pressure at base
        pa_soil = Ka * unit_weight * wall_height
        pa_surcharge = Ka * surcharge
        
        # Total force components
        Fa_soil = 0.5 * pa_soil * wall_height
        Fa_surcharge = pa_surcharge * wall_height
        
        # Total force
        Fa_total = Fa_soil + Fa_surcharge
        
        # Location of resultant from base
        moment_soil = Fa_soil * (wall_height / 3)
        moment_surcharge = Fa_surcharge * (wall_height / 2)
        location = (moment_soil + moment_surcharge) / Fa_total
        
        return Fa_total, location


class Controller(ViktorController):
    """Main controller for foundation design calculations."""
    
    label = "Foundation Design"
    parametrization = Parametrization
    
    @DataView("Results", duration_guess=1)
    def calculate_results(self, params, **kwargs) -> DataResult:
        """
        Calculate and display foundation design results.
        
        Args:
            params: Input parameters from parametrization
            
        Returns:
            DataResult with calculation results
        """
        foundation_type = params.foundation_type.type_selection
        
        if foundation_type == "shallow_foundation":
            return self._calculate_shallow_foundation(params)
        elif foundation_type == "deep_foundation_single_pile":
            return self._calculate_single_pile(params)
        elif foundation_type == "deep_foundation_pile_group":
            return self._calculate_pile_group(params)
        elif foundation_type == "retaining_wall":
            return self._calculate_retaining_wall(params)
        
        return DataResult(DataGroup())
    
    def _calculate_shallow_foundation(self, params) -> DataResult:
        """Calculate shallow foundation results."""
        width = params.shallow_foundation.foundation_width
        length = params.shallow_foundation.foundation_length
        depth = params.shallow_foundation.foundation_depth
        load = params.shallow_foundation.applied_load
        unit_weight = params.soil_properties.unit_weight
        cohesion = params.soil_properties.cohesion
        friction_angle = params.soil_properties.friction_angle
        
        # Calculate bearing capacity
        qu = ShallowFoundationCalculator.calculate_ultimate_bearing_capacity(
            width, length, depth, unit_weight, cohesion, friction_angle
        )
        qa = ShallowFoundationCalculator.calculate_allowable_bearing_capacity(qu)
        applied_pressure = ShallowFoundationCalculator.calculate_applied_pressure(load, width, length)
        
        # Calculate bearing capacity factors
        Nc, Nq, Ngamma = ShallowFoundationCalculator.calculate_bearing_capacity_factors(friction_angle)
        
        # Safety factor
        safety_factor = qa / applied_pressure if applied_pressure > 0 else float('inf')
        
        # Create result groups
        input_group = DataGroup(
            DataItem("Foundation Width (B)", width, suffix="m"),
            DataItem("Foundation Length (L)", length, suffix="m"),
            DataItem("Foundation Depth (Df)", depth, suffix="m"),
            DataItem("Foundation Area", width * length, suffix="m²"),
            DataItem("Applied Load", load, suffix="kN"),
        )
        
        soil_group = DataGroup(
            DataItem("Unit Weight (γ)", unit_weight, suffix="kN/m³"),
            DataItem("Cohesion (c)", cohesion, suffix="kPa"),
            DataItem("Friction Angle (φ)", friction_angle, suffix="°"),
        )
        
        factors_group = DataGroup(
            DataItem("Bearing Capacity Factor Nc", round(Nc, 2)),
            DataItem("Bearing Capacity Factor Nq", round(Nq, 2)),
            DataItem("Bearing Capacity Factor Nγ", round(Ngamma, 2)),
        )
        
        results_group = DataGroup(
            DataItem("Ultimate Bearing Capacity (qu)", round(qu, 2), suffix="kPa"),
            DataItem("Allowable Bearing Capacity (qa)", round(qa, 2), suffix="kPa"),
            DataItem("Applied Pressure", round(applied_pressure, 2), suffix="kPa"),
            DataItem("Safety Factor", round(safety_factor, 2)),
            DataItem("Status", "✓ SAFE" if safety_factor >= 1.0 else "✗ UNSAFE", suffix=""),
        )
        
        return DataResult(
            DataGroup(
                input_group,
                soil_group,
                factors_group,
                results_group,
            )
        )
    
    def _calculate_single_pile(self, params) -> DataResult:
        """Calculate single pile results."""
        diameter = params.single_pile.pile_diameter
        length = params.single_pile.pile_length
        pile_type = params.single_pile.pile_type
        load = params.single_pile.applied_load_pile
        unit_weight = params.soil_properties.unit_weight
        cohesion = params.soil_properties.cohesion
        friction_angle = params.soil_properties.friction_angle
        
        # Calculate pile capacity
        Qu, Qa, Qb, Qs = DeepFoundationCalculator.calculate_pile_capacity(
            diameter, length, unit_weight, friction_angle, cohesion, pile_type
        )
        
        # Safety factor
        safety_factor = Qa / load if load > 0 else float('inf')
        
        # Create result groups
        input_group = DataGroup(
            DataItem("Pile Diameter", diameter, suffix="m"),
            DataItem("Pile Length", length, suffix="m"),
            DataItem("Pile Type", pile_type.capitalize(), suffix=""),
            DataItem("Applied Load", load, suffix="kN"),
        )
        
        soil_group = DataGroup(
            DataItem("Unit Weight (γ)", unit_weight, suffix="kN/m³"),
            DataItem("Cohesion (c)", cohesion, suffix="kPa"),
            DataItem("Friction Angle (φ)", friction_angle, suffix="°"),
        )
        
        capacity_group = DataGroup(
            DataItem("End Bearing Capacity (Qb)", round(Qb, 2), suffix="kN"),
            DataItem("Skin Friction Capacity (Qs)", round(Qs, 2), suffix="kN"),
            DataItem("Ultimate Capacity (Qu)", round(Qu, 2), suffix="kN"),
            DataItem("Allowable Capacity (Qa)", round(Qa, 2), suffix="kN"),
        )
        
        results_group = DataGroup(
            DataItem("Safety Factor", round(safety_factor, 2)),
            DataItem("Utilization Ratio", round(load / Qa * 100, 1), suffix="%"),
            DataItem("Status", "✓ SAFE" if safety_factor >= 1.0 else "✗ UNSAFE", suffix=""),
        )
        
        return DataResult(
            DataGroup(
                input_group,
                soil_group,
                capacity_group,
                results_group,
            )
        )
    
    def _calculate_pile_group(self, params) -> DataResult:
        """Calculate pile group results."""
        diameter = params.pile_group.pile_diameter_group
        length = params.pile_group.pile_length_group
        num_piles = int(params.pile_group.num_piles)
        spacing = params.pile_group.pile_spacing
        total_load = params.pile_group.total_load
        unit_weight = params.soil_properties.unit_weight
        cohesion = params.soil_properties.cohesion
        friction_angle = params.soil_properties.friction_angle
        
        # Calculate single pile capacity (assumed bored pile)
        Qu_single, Qa_single, Qb, Qs = DeepFoundationCalculator.calculate_pile_capacity(
            diameter, length, unit_weight, friction_angle, cohesion, "bored"
        )
        
        # Calculate group efficiency
        efficiency = DeepFoundationCalculator.calculate_pile_group_efficiency(num_piles, spacing, diameter)
        
        # Group capacity
        Qu_group = Qu_single * num_piles * efficiency
        Qa_group = Qu_group / 2.5
        
        # Load per pile
        load_per_pile = total_load / num_piles
        
        # Safety factor
        safety_factor = Qa_group / total_load if total_load > 0 else float('inf')
        
        # Create result groups
        input_group = DataGroup(
            DataItem("Pile Diameter", diameter, suffix="m"),
            DataItem("Pile Length", length, suffix="m"),
            DataItem("Number of Piles", num_piles, suffix=""),
            DataItem("Pile Spacing", spacing, suffix="m"),
            DataItem("Total Applied Load", total_load, suffix="kN"),
        )
        
        soil_group = DataGroup(
            DataItem("Unit Weight (γ)", unit_weight, suffix="kN/m³"),
            DataItem("Cohesion (c)", cohesion, suffix="kPa"),
            DataItem("Friction Angle (φ)", friction_angle, suffix="°"),
        )
        
        single_pile_group = DataGroup(
            DataItem("Single Pile Ultimate Capacity", round(Qu_single, 2), suffix="kN"),
            DataItem("Single Pile Allowable Capacity", round(Qa_single, 2), suffix="kN"),
        )
        
        group_group = DataGroup(
            DataItem("Group Efficiency Factor", round(efficiency, 3)),
            DataItem("Group Ultimate Capacity", round(Qu_group, 2), suffix="kN"),
            DataItem("Group Allowable Capacity", round(Qa_group, 2), suffix="kN"),
            DataItem("Load per Pile", round(load_per_pile, 2), suffix="kN"),
        )
        
        results_group = DataGroup(
            DataItem("Safety Factor", round(safety_factor, 2)),
            DataItem("Average Pile Utilization", round(load_per_pile / Qa_single * 100, 1), suffix="%"),
            DataItem("Status", "✓ SAFE" if safety_factor >= 1.0 else "✗ UNSAFE", suffix=""),
        )
        
        return DataResult(
            DataGroup(
                input_group,
                soil_group,
                single_pile_group,
                group_group,
                results_group,
            )
        )
    
    def _calculate_retaining_wall(self, params) -> DataResult:
        """Calculate retaining wall results."""
        height = params.retaining_wall.wall_height
        thickness = params.retaining_wall.wall_thickness
        surcharge = params.retaining_wall.surcharge
        unit_weight = params.soil_properties.unit_weight
        cohesion = params.soil_properties.cohesion
        friction_angle = params.soil_properties.friction_angle
        
        # Calculate earth pressure coefficients
        Ka = RetainingWallCalculator.calculate_active_earth_pressure_coefficient(friction_angle)
        Kp = RetainingWallCalculator.calculate_passive_earth_pressure_coefficient(friction_angle)
        
        # Calculate active force
        Fa_total, Fa_location = RetainingWallCalculator.calculate_total_active_force(
            height, unit_weight, friction_angle, cohesion, surcharge
        )
        
        # Create result groups
        input_group = DataGroup(
            DataItem("Wall Height (H)", height, suffix="m"),
            DataItem("Wall Thickness", thickness, suffix="m"),
            DataItem("Surcharge Load", surcharge, suffix="kPa"),
        )
        
        soil_group = DataGroup(
            DataItem("Unit Weight (γ)", unit_weight, suffix="kN/m³"),
            DataItem("Cohesion (c)", cohesion, suffix="kPa"),
            DataItem("Friction Angle (φ)", friction_angle, suffix="°"),
        )
        
        pressure_group = DataGroup(
            DataItem("Active Pressure Coefficient (Ka)", round(Ka, 3)),
            DataItem("Passive Pressure Coefficient (Kp)", round(Kp, 3)),
        )
        
        force_group = DataGroup(
            DataItem("Total Active Force", round(Fa_total, 2), suffix="kN/m"),
            DataItem("Force Location from Base", round(Fa_location, 2), suffix="m"),
            DataItem("Active Pressure at Base", round(Ka * unit_weight * height, 2), suffix="kPa"),
        )
        
        return DataResult(
            DataGroup(
                input_group,
                soil_group,
                pressure_group,
                force_group,
            )
        )
    
    @PlotlyView("Foundation Visualization", duration_guess=1)
    def visualize_foundation(self, params, **kwargs) -> PlotlyResult:
        """
        Create visualization of the foundation design.
        
        Args:
            params: Input parameters from parametrization
            
        Returns:
            PlotlyResult with foundation visualization
        """
        foundation_type = params.foundation_type.type_selection
        
        if foundation_type == "shallow_foundation":
            return self._visualize_shallow_foundation(params)
        elif foundation_type in ["deep_foundation_single_pile", "deep_foundation_pile_group"]:
            return self._visualize_deep_foundation(params, foundation_type)
        elif foundation_type == "retaining_wall":
            return self._visualize_retaining_wall(params)
        
        # Default empty plot
        fig = go.Figure()
        fig.update_layout(title="Select a foundation type to view visualization")
        return PlotlyResult(fig.to_json())
    
    def _visualize_shallow_foundation(self, params) -> PlotlyResult:
        """Visualize shallow foundation."""
        width = params.shallow_foundation.foundation_width
        length = params.shallow_foundation.foundation_length
        depth = params.shallow_foundation.foundation_depth
        
        fig = go.Figure()
        
        # Foundation (top view)
        fig.add_trace(go.Scatter(
            x=[0, length, length, 0, 0],
            y=[0, 0, width, width, 0],
            fill="toself",
            fillcolor="rgba(128, 128, 128, 0.5)",
            line=dict(color="black", width=2),
            name="Foundation"
        ))
        
        fig.update_layout(
            title=f"Shallow Foundation - Top View<br>Dimensions: {length}m × {width}m, Depth: {depth}m",
            xaxis_title="Length (m)",
            yaxis_title="Width (m)",
            showlegend=True,
            width=600,
            height=500,
            yaxis=dict(scaleanchor="x", scaleratio=1)
        )
        
        return PlotlyResult(fig.to_json())
    
    def _visualize_deep_foundation(self, params, foundation_type: str) -> PlotlyResult:
        """Visualize deep foundation (pile)."""
        if foundation_type == "deep_foundation_single_pile":
            diameter = params.single_pile.pile_diameter
            length = params.single_pile.pile_length
            num_piles = 1
            spacing = 0
        else:
            diameter = params.pile_group.pile_diameter_group
            length = params.pile_group.pile_length_group
            num_piles = int(params.pile_group.num_piles)
            spacing = params.pile_group.pile_spacing
        
        fig = go.Figure()
        
        # Draw piles (side view)
        if num_piles == 1:
            # Single pile
            fig.add_trace(go.Scatter(
                x=[-diameter/2, -diameter/2, diameter/2, diameter/2, -diameter/2],
                y=[0, -length, -length, 0, 0],
                fill="toself",
                fillcolor="rgba(139, 69, 19, 0.5)",
                line=dict(color="brown", width=2),
                name="Pile"
            ))
        else:
            # Pile group
            n_rows = int(math.sqrt(num_piles))
            n_cols = int(math.ceil(num_piles / n_rows))
            
            pile_num = 0
            for row in range(n_rows):
                for col in range(n_cols):
                    if pile_num >= num_piles:
                        break
                    
                    x_center = col * spacing
                    
                    fig.add_trace(go.Scatter(
                        x=[x_center - diameter/2, x_center - diameter/2, x_center + diameter/2, x_center + diameter/2, x_center - diameter/2],
                        y=[0, -length, -length, 0, 0],
                        fill="toself",
                        fillcolor="rgba(139, 69, 19, 0.5)",
                        line=dict(color="brown", width=2),
                        name=f"Pile {pile_num + 1}",
                        showlegend=False
                    ))
                    
                    pile_num += 1
        
        # Ground level
        max_width = (num_piles - 1) * spacing + diameter if num_piles > 1 else diameter
        fig.add_trace(go.Scatter(
            x=[-max_width/2 - 1, max_width/2 + 1],
            y=[0, 0],
            line=dict(color="green", width=3, dash="dash"),
            name="Ground Level"
        ))
        
        title = "Single Pile - Side View" if num_piles == 1 else f"Pile Group - Side View ({num_piles} piles)"
        fig.update_layout(
            title=f"{title}<br>Pile: Ø{diameter}m × {length}m",
            xaxis_title="Width (m)",
            yaxis_title="Depth (m)",
            showlegend=True,
            width=600,
            height=600,
            yaxis=dict(scaleanchor="x", scaleratio=1)
        )
        
        return PlotlyResult(fig.to_json())
    
    def _visualize_retaining_wall(self, params) -> PlotlyResult:
        """Visualize retaining wall."""
        height = params.retaining_wall.wall_height
        thickness = params.retaining_wall.wall_thickness
        unit_weight = params.soil_properties.unit_weight
        friction_angle = params.soil_properties.friction_angle
        
        fig = go.Figure()
        
        # Wall
        fig.add_trace(go.Scatter(
            x=[0, thickness, thickness, 0, 0],
            y=[0, 0, height, height, 0],
            fill="toself",
            fillcolor="rgba(128, 128, 128, 0.7)",
            line=dict(color="black", width=2),
            name="Wall"
        ))
        
        # Soil (retained side)
        fig.add_trace(go.Scatter(
            x=[thickness, thickness + height, thickness + height, thickness],
            y=[0, 0, height, height],
            fill="toself",
            fillcolor="rgba(139, 69, 19, 0.3)",
            line=dict(color="brown", width=1),
            name="Retained Soil"
        ))
        
        # Earth pressure distribution
        Ka = RetainingWallCalculator.calculate_active_earth_pressure_coefficient(friction_angle)
        pa_max = Ka * unit_weight * height
        
        # Pressure diagram
        pressure_scale = 2.0  # Scale factor for visualization
        x_pressure = [thickness, thickness + pa_max * pressure_scale]
        y_pressure = [0, 0]
        
        fig.add_trace(go.Scatter(
            x=[thickness, thickness, thickness + pa_max * pressure_scale],
            y=[height, 0, 0],
            fill="toself",
            fillcolor="rgba(255, 0, 0, 0.2)",
            line=dict(color="red", width=2, dash="dash"),
            name="Active Pressure"
        ))
        
        fig.update_layout(
            title=f"Retaining Wall - Side View<br>Height: {height}m, Thickness: {thickness}m",
            xaxis_title="Distance (m)",
            yaxis_title="Height (m)",
            showlegend=True,
            width=700,
            height=600,
            yaxis=dict(scaleanchor="x", scaleratio=1)
        )
        
        return PlotlyResult(fig.to_json())
