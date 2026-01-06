"""
Example usage of ENGIPIT foundation design calculations.

This file demonstrates how to use the calculation modules directly
for testing and validation purposes.
"""

from app import (
    ShallowFoundationCalculator,
    DeepFoundationCalculator,
    RetainingWallCalculator
)


def example_shallow_foundation():
    """Example shallow foundation calculation."""
    print("=" * 60)
    print("SHALLOW FOUNDATION EXAMPLE")
    print("=" * 60)
    
    # Input parameters
    width = 2.5  # m
    length = 2.5  # m
    depth = 1.5  # m
    unit_weight = 18.0  # kN/m³
    cohesion = 15.0  # kPa
    friction_angle = 30.0  # degrees
    applied_load = 1200.0  # kN
    
    print(f"\nInput Parameters:")
    print(f"  Foundation: {width}m × {length}m at {depth}m depth")
    print(f"  Applied Load: {applied_load} kN")
    print(f"  Soil: γ={unit_weight} kN/m³, c={cohesion} kPa, φ={friction_angle}°")
    
    # Calculate bearing capacity factors
    Nc, Nq, Ngamma = ShallowFoundationCalculator.calculate_bearing_capacity_factors(friction_angle)
    print(f"\nBearing Capacity Factors:")
    print(f"  Nc = {Nc:.2f}")
    print(f"  Nq = {Nq:.2f}")
    print(f"  Nγ = {Ngamma:.2f}")
    
    # Calculate ultimate bearing capacity
    qu = ShallowFoundationCalculator.calculate_ultimate_bearing_capacity(
        width, length, depth, unit_weight, cohesion, friction_angle
    )
    print(f"\nUltimate Bearing Capacity: qu = {qu:.2f} kPa")
    
    # Calculate allowable bearing capacity
    qa = ShallowFoundationCalculator.calculate_allowable_bearing_capacity(qu)
    print(f"Allowable Bearing Capacity: qa = {qa:.2f} kPa (FOS = 3.0)")
    
    # Calculate applied pressure
    applied_pressure = ShallowFoundationCalculator.calculate_applied_pressure(
        applied_load, width, length
    )
    print(f"Applied Pressure: {applied_pressure:.2f} kPa")
    
    # Safety factor
    safety_factor = qa / applied_pressure
    print(f"\nSafety Factor: {safety_factor:.2f}")
    print(f"Status: {'✓ SAFE' if safety_factor >= 1.0 else '✗ UNSAFE'}")


def example_single_pile():
    """Example single pile calculation."""
    print("\n" + "=" * 60)
    print("SINGLE PILE EXAMPLE")
    print("=" * 60)
    
    # Input parameters
    diameter = 0.8  # m
    length = 20.0  # m
    pile_type = "bored"
    unit_weight = 18.0  # kN/m³
    cohesion = 15.0  # kPa
    friction_angle = 32.0  # degrees
    applied_load = 1500.0  # kN
    
    print(f"\nInput Parameters:")
    print(f"  Pile: Ø{diameter}m × {length}m ({pile_type})")
    print(f"  Applied Load: {applied_load} kN")
    print(f"  Soil: γ={unit_weight} kN/m³, c={cohesion} kPa, φ={friction_angle}°")
    
    # Calculate pile capacity
    Qu, Qa, Qb, Qs = DeepFoundationCalculator.calculate_pile_capacity(
        diameter, length, unit_weight, friction_angle, cohesion, pile_type
    )
    
    print(f"\nPile Capacity:")
    print(f"  End Bearing (Qb): {Qb:.2f} kN")
    print(f"  Skin Friction (Qs): {Qs:.2f} kN")
    print(f"  Ultimate Capacity (Qu): {Qu:.2f} kN")
    print(f"  Allowable Capacity (Qa): {Qa:.2f} kN (FOS = 2.5)")
    
    # Safety factor
    safety_factor = Qa / applied_load
    utilization = applied_load / Qa * 100
    print(f"\nSafety Factor: {safety_factor:.2f}")
    print(f"Utilization Ratio: {utilization:.1f}%")
    print(f"Status: {'✓ SAFE' if safety_factor >= 1.0 else '✗ UNSAFE'}")


def example_pile_group():
    """Example pile group calculation."""
    print("\n" + "=" * 60)
    print("PILE GROUP EXAMPLE")
    print("=" * 60)
    
    # Input parameters
    diameter = 0.8  # m
    length = 20.0  # m
    num_piles = 9
    spacing = 2.4  # m
    total_load = 12000.0  # kN
    unit_weight = 18.0  # kN/m³
    cohesion = 15.0  # kPa
    friction_angle = 32.0  # degrees
    
    print(f"\nInput Parameters:")
    print(f"  Pile: Ø{diameter}m × {length}m (bored)")
    print(f"  Group: {num_piles} piles at {spacing}m spacing")
    print(f"  Total Load: {total_load} kN")
    print(f"  Soil: γ={unit_weight} kN/m³, c={cohesion} kPa, φ={friction_angle}°")
    
    # Calculate single pile capacity
    Qu_single, Qa_single, _, _ = DeepFoundationCalculator.calculate_pile_capacity(
        diameter, length, unit_weight, friction_angle, cohesion, "bored"
    )
    
    print(f"\nSingle Pile Capacity:")
    print(f"  Ultimate: {Qu_single:.2f} kN")
    print(f"  Allowable: {Qa_single:.2f} kN")
    
    # Calculate group efficiency
    efficiency = DeepFoundationCalculator.calculate_pile_group_efficiency(
        num_piles, spacing, diameter
    )
    
    print(f"\nGroup Analysis:")
    print(f"  Spacing/Diameter Ratio: {spacing/diameter:.1f}")
    print(f"  Group Efficiency: {efficiency:.3f}")
    
    # Group capacity
    Qu_group = Qu_single * num_piles * efficiency
    Qa_group = Qu_group / 2.5
    load_per_pile = total_load / num_piles
    
    print(f"  Group Ultimate Capacity: {Qu_group:.2f} kN")
    print(f"  Group Allowable Capacity: {Qa_group:.2f} kN")
    print(f"  Load per Pile: {load_per_pile:.2f} kN")
    
    # Safety factor
    safety_factor = Qa_group / total_load
    utilization = load_per_pile / Qa_single * 100
    print(f"\nSafety Factor: {safety_factor:.2f}")
    print(f"Average Pile Utilization: {utilization:.1f}%")
    print(f"Status: {'✓ SAFE' if safety_factor >= 1.0 else '✗ UNSAFE'}")


def example_retaining_wall():
    """Example retaining wall calculation."""
    print("\n" + "=" * 60)
    print("RETAINING WALL EXAMPLE")
    print("=" * 60)
    
    # Input parameters
    height = 6.0  # m
    thickness = 0.5  # m
    surcharge = 15.0  # kPa
    unit_weight = 18.0  # kN/m³
    cohesion = 5.0  # kPa
    friction_angle = 32.0  # degrees
    
    print(f"\nInput Parameters:")
    print(f"  Wall: H={height}m, t={thickness}m")
    print(f"  Surcharge: {surcharge} kPa")
    print(f"  Soil: γ={unit_weight} kN/m³, c={cohesion} kPa, φ={friction_angle}°")
    
    # Calculate pressure coefficients
    Ka = RetainingWallCalculator.calculate_active_earth_pressure_coefficient(friction_angle)
    Kp = RetainingWallCalculator.calculate_passive_earth_pressure_coefficient(friction_angle)
    
    print(f"\nEarth Pressure Coefficients:")
    print(f"  Active (Ka): {Ka:.3f}")
    print(f"  Passive (Kp): {Kp:.3f}")
    
    # Calculate active force
    Fa_total, Fa_location = RetainingWallCalculator.calculate_total_active_force(
        height, unit_weight, friction_angle, cohesion, surcharge
    )
    
    print(f"\nActive Earth Pressure:")
    print(f"  Total Force: {Fa_total:.2f} kN/m")
    print(f"  Force Location from Base: {Fa_location:.2f} m")
    print(f"  Pressure at Base: {Ka * unit_weight * height:.2f} kPa")


if __name__ == "__main__":
    print("\n")
    print("*" * 60)
    print("ENGIPIT - GEOTECHNICAL FOUNDATION DESIGN EXAMPLES")
    print("*" * 60)
    
    example_shallow_foundation()
    example_single_pile()
    example_pile_group()
    example_retaining_wall()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60 + "\n")
