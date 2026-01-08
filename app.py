"""
ENGIPIT - Geotechnical Foundation Design Toolset

A comprehensive application for rapid design calculations of foundation systems.
This toolset enables civil engineers specialized in geotechnics to perform various
foundation design calculations including shallow foundations, deep foundations, and
retaining walls.
"""

from typing import Tuple
import math


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
