"""
Unit tests for ENGIPIT foundation design calculations.

These tests validate the calculation modules against known values and manual calculations.
"""

import unittest
import math
from app import (
    ShallowFoundationCalculator,
    DeepFoundationCalculator,
    RetainingWallCalculator
)


class TestShallowFoundationCalculator(unittest.TestCase):
    """Test cases for shallow foundation calculations."""
    
    def test_bearing_capacity_factors_zero_friction(self):
        """Test bearing capacity factors for cohesive soil (φ=0°)."""
        Nc, Nq, Ngamma = ShallowFoundationCalculator.calculate_bearing_capacity_factors(0)
        
        # For φ=0°, Nc=5.14, Nq=1, Nγ=0
        self.assertAlmostEqual(Nc, 5.14, places=2)
        self.assertAlmostEqual(Nq, 1.0, places=1)
        self.assertAlmostEqual(Ngamma, 0.0, places=1)
    
    def test_bearing_capacity_factors_friction_30(self):
        """Test bearing capacity factors for φ=30°."""
        Nc, Nq, Ngamma = ShallowFoundationCalculator.calculate_bearing_capacity_factors(30)
        
        # Theoretical values for φ=30°: Nc≈30.14, Nq≈18.4, Nγ≈22.4
        self.assertAlmostEqual(Nc, 30.14, places=0)
        self.assertAlmostEqual(Nq, 18.4, places=0)
        self.assertAlmostEqual(Ngamma, 22.4, places=0)
    
    def test_ultimate_bearing_capacity_pure_cohesion(self):
        """Test ultimate bearing capacity for pure cohesive soil."""
        # Test case: B=2m, L=2m, Df=1m, γ=18kN/m³, c=50kPa, φ=0°
        qu = ShallowFoundationCalculator.calculate_ultimate_bearing_capacity(
            width=2.0,
            length=2.0,
            depth=1.0,
            unit_weight=18.0,
            cohesion=50.0,
            friction_angle=0.0
        )
        
        # Expected: qu = c*Nc + γ*Df*Nq + 0.5*γ*B*Nγ
        # qu = 50*5.14 + 18*1*1 + 0.5*18*2*0 = 257 + 18 = 275 kPa
        expected = 50 * 5.14 + 18 * 1 * 1
        self.assertAlmostEqual(qu, expected, places=0)
    
    def test_ultimate_bearing_capacity_cohesionless(self):
        """Test ultimate bearing capacity for cohesionless soil."""
        # Test case: B=2m, L=2m, Df=1m, γ=18kN/m³, c=0kPa, φ=30°
        qu = ShallowFoundationCalculator.calculate_ultimate_bearing_capacity(
            width=2.0,
            length=2.0,
            depth=1.0,
            unit_weight=18.0,
            cohesion=0.0,
            friction_angle=30.0
        )
        
        # For φ=30°: Nc≈30.14, Nq≈18.4, Nγ≈22.4
        # qu = 0*30.14 + 18*1*18.4 + 0.5*18*2*22.4
        # qu ≈ 331.2 + 403.2 ≈ 734.4 kPa
        self.assertGreater(qu, 700)
        self.assertLess(qu, 800)
    
    def test_allowable_bearing_capacity(self):
        """Test allowable bearing capacity calculation."""
        qu = 300.0  # kPa
        qa = ShallowFoundationCalculator.calculate_allowable_bearing_capacity(qu, factor_of_safety=3.0)
        
        self.assertAlmostEqual(qa, 100.0, places=1)
    
    def test_applied_pressure(self):
        """Test applied pressure calculation."""
        load = 1000.0  # kN
        width = 2.0  # m
        length = 2.0  # m
        
        pressure = ShallowFoundationCalculator.calculate_applied_pressure(load, width, length)
        
        # Expected: 1000 / (2*2) = 250 kPa
        self.assertAlmostEqual(pressure, 250.0, places=1)


class TestDeepFoundationCalculator(unittest.TestCase):
    """Test cases for deep foundation (pile) calculations."""
    
    def test_pile_end_bearing_capacity(self):
        """Test pile end bearing capacity calculation."""
        # Test case: D=0.6m, L=15m, γ=18kN/m³, φ=30°, c=10kPa
        Qb = DeepFoundationCalculator.calculate_pile_end_bearing(
            pile_diameter=0.6,
            unit_weight=18.0,
            pile_length=15.0,
            friction_angle=30.0,
            cohesion=10.0
        )
        
        # Should be positive and reasonable
        self.assertGreater(Qb, 0)
        self.assertLess(Qb, 10000)  # Reasonable upper bound
    
    def test_pile_skin_friction_capacity(self):
        """Test pile skin friction capacity calculation."""
        # Test case: D=0.6m, L=15m, γ=18kN/m³, φ=30°, c=10kPa, type=bored
        Qs = DeepFoundationCalculator.calculate_pile_skin_friction(
            pile_diameter=0.6,
            pile_length=15.0,
            unit_weight=18.0,
            friction_angle=30.0,
            cohesion=10.0,
            pile_type="bored"
        )
        
        # Should be positive and reasonable
        self.assertGreater(Qs, 0)
        self.assertLess(Qs, 10000)  # Reasonable upper bound
    
    def test_pile_capacity_total(self):
        """Test total pile capacity calculation."""
        # Test case: D=0.6m, L=15m, γ=18kN/m³, φ=30°, c=10kPa, type=bored
        Qu, Qa, Qb, Qs = DeepFoundationCalculator.calculate_pile_capacity(
            pile_diameter=0.6,
            pile_length=15.0,
            unit_weight=18.0,
            friction_angle=30.0,
            cohesion=10.0,
            pile_type="bored",
            factor_of_safety=2.5
        )
        
        # Verify relationships
        self.assertAlmostEqual(Qu, Qb + Qs, places=1)
        self.assertAlmostEqual(Qa, Qu / 2.5, places=1)
        self.assertGreater(Qu, Qa)
    
    def test_pile_type_difference(self):
        """Test that driven and bored piles have different capacities."""
        params = {
            "pile_diameter": 0.6,
            "pile_length": 15.0,
            "unit_weight": 18.0,
            "friction_angle": 30.0,
            "cohesion": 10.0,
            "factor_of_safety": 2.5
        }
        
        Qu_driven, _, _, _ = DeepFoundationCalculator.calculate_pile_capacity(**params, pile_type="driven")
        Qu_bored, _, _, _ = DeepFoundationCalculator.calculate_pile_capacity(**params, pile_type="bored")
        
        # Driven piles should generally have higher capacity
        self.assertGreater(Qu_driven, Qu_bored)
    
    def test_pile_group_efficiency_wide_spacing(self):
        """Test pile group efficiency for wide spacing."""
        efficiency = DeepFoundationCalculator.calculate_pile_group_efficiency(
            num_piles=4,
            spacing=3.6,  # 6 * 0.6 diameter
            diameter=0.6
        )
        
        # For s/d ≥ 6, efficiency should be 1.0
        self.assertAlmostEqual(efficiency, 1.0, places=2)
    
    def test_pile_group_efficiency_close_spacing(self):
        """Test pile group efficiency for close spacing."""
        efficiency = DeepFoundationCalculator.calculate_pile_group_efficiency(
            num_piles=4,
            spacing=1.8,  # 3 * 0.6 diameter
            diameter=0.6
        )
        
        # For s/d = 3, efficiency should be around 0.7
        self.assertAlmostEqual(efficiency, 0.7, places=1)
    
    def test_pile_group_efficiency_very_close_spacing(self):
        """Test pile group efficiency for very close spacing."""
        efficiency = DeepFoundationCalculator.calculate_pile_group_efficiency(
            num_piles=4,
            spacing=1.2,  # 2 * 0.6 diameter
            diameter=0.6
        )
        
        # For s/d = 2, efficiency should be less than 0.7
        self.assertLess(efficiency, 0.7)
        self.assertGreater(efficiency, 0)


class TestRetainingWallCalculator(unittest.TestCase):
    """Test cases for retaining wall calculations."""
    
    def test_active_pressure_coefficient(self):
        """Test active earth pressure coefficient calculation."""
        # For φ=30°, Ka = tan²(45-15) = tan²(30) = 0.333
        Ka = RetainingWallCalculator.calculate_active_earth_pressure_coefficient(30.0)
        
        self.assertAlmostEqual(Ka, 0.333, places=2)
    
    def test_passive_pressure_coefficient(self):
        """Test passive earth pressure coefficient calculation."""
        # For φ=30°, Kp = tan²(45+15) = tan²(60) = 3.0
        Kp = RetainingWallCalculator.calculate_passive_earth_pressure_coefficient(30.0)
        
        self.assertAlmostEqual(Kp, 3.0, places=1)
    
    def test_pressure_coefficients_relationship(self):
        """Test relationship between Ka and Kp."""
        friction_angle = 30.0
        Ka = RetainingWallCalculator.calculate_active_earth_pressure_coefficient(friction_angle)
        Kp = RetainingWallCalculator.calculate_passive_earth_pressure_coefficient(friction_angle)
        
        # Kp should be greater than Ka
        self.assertGreater(Kp, Ka)
        
        # For Rankine theory: Ka * Kp ≈ 1.0
        self.assertAlmostEqual(Ka * Kp, 1.0, places=1)
    
    def test_total_active_force_no_surcharge(self):
        """Test total active force calculation without surcharge."""
        # Test case: H=5m, γ=18kN/m³, φ=30°, c=0kPa, q=0kPa
        Fa, location = RetainingWallCalculator.calculate_total_active_force(
            wall_height=5.0,
            unit_weight=18.0,
            friction_angle=30.0,
            cohesion=0.0,
            surcharge=0.0
        )
        
        # Ka for φ=30° ≈ 0.333
        # Fa = 0.5 * Ka * γ * H² = 0.5 * 0.333 * 18 * 25 = 75 kN/m
        expected_force = 0.5 * 0.333 * 18 * 5**2
        self.assertAlmostEqual(Fa, expected_force, places=0)
        
        # Location should be H/3 from base for triangular distribution
        self.assertAlmostEqual(location, 5.0/3.0, places=1)
    
    def test_total_active_force_with_surcharge(self):
        """Test total active force calculation with surcharge."""
        # Test case: H=5m, γ=18kN/m³, φ=30°, c=0kPa, q=10kPa
        Fa_with, location_with = RetainingWallCalculator.calculate_total_active_force(
            wall_height=5.0,
            unit_weight=18.0,
            friction_angle=30.0,
            cohesion=0.0,
            surcharge=10.0
        )
        
        Fa_without, location_without = RetainingWallCalculator.calculate_total_active_force(
            wall_height=5.0,
            unit_weight=18.0,
            friction_angle=30.0,
            cohesion=0.0,
            surcharge=0.0
        )
        
        # Force with surcharge should be greater
        self.assertGreater(Fa_with, Fa_without)
        
        # Location should be different (higher due to rectangular surcharge component)
        self.assertGreater(location_with, location_without)


class TestIntegration(unittest.TestCase):
    """Integration tests for realistic scenarios."""
    
    def test_shallow_foundation_safe_design(self):
        """Test a safe shallow foundation design."""
        width = 2.5
        length = 2.5
        depth = 1.5
        unit_weight = 18.0
        cohesion = 15.0
        friction_angle = 30.0
        load = 1000.0
        
        qu = ShallowFoundationCalculator.calculate_ultimate_bearing_capacity(
            width, length, depth, unit_weight, cohesion, friction_angle
        )
        qa = ShallowFoundationCalculator.calculate_allowable_bearing_capacity(qu)
        applied = ShallowFoundationCalculator.calculate_applied_pressure(load, width, length)
        
        # Should be safe
        safety_factor = qa / applied
        self.assertGreater(safety_factor, 1.0)
    
    def test_single_pile_adequate_capacity(self):
        """Test a single pile with adequate capacity."""
        Qu, Qa, Qb, Qs = DeepFoundationCalculator.calculate_pile_capacity(
            pile_diameter=0.8,
            pile_length=20.0,
            unit_weight=18.0,
            friction_angle=32.0,
            cohesion=15.0,
            pile_type="bored",
            factor_of_safety=2.5
        )
        
        # Both end bearing and skin friction should contribute
        self.assertGreater(Qb, 0)
        self.assertGreater(Qs, 0)
        
        # Allowable capacity should be reasonable
        self.assertGreater(Qa, 500)  # At least 500 kN
        self.assertLess(Qa, 5000)  # But not unreasonably high
    
    def test_pile_group_behavior(self):
        """Test pile group behavior with efficiency."""
        num_piles = 9
        spacing = 2.4
        diameter = 0.8
        
        # Single pile capacity
        Qu_single, Qa_single, _, _ = DeepFoundationCalculator.calculate_pile_capacity(
            pile_diameter=diameter,
            pile_length=20.0,
            unit_weight=18.0,
            friction_angle=32.0,
            cohesion=15.0,
            pile_type="bored",
            factor_of_safety=2.5
        )
        
        # Group efficiency
        efficiency = DeepFoundationCalculator.calculate_pile_group_efficiency(num_piles, spacing, diameter)
        
        # Group capacity
        Qu_group = Qu_single * num_piles * efficiency
        Qa_group = Qu_group / 2.5
        
        # Group capacity should be less than sum of individual capacities
        self.assertLess(Qa_group, Qa_single * num_piles)


if __name__ == "__main__":
    unittest.main()
