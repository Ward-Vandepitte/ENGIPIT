# ENGIPIT - Geotechnical Foundation Design Toolset

## Overview

ENGIPIT is a comprehensive VIKTOR application designed for civil engineers specialized in geotechnics. It provides rapid design calculations for various foundation systems, enabling quick and accurate assessment of foundation performance.

## Features

### 1. Shallow Foundation Design
Calculate bearing capacity and analyze shallow foundations using Terzaghi's bearing capacity theory.

**Capabilities:**
- Ultimate bearing capacity calculations using Terzaghi bearing capacity factors
- Allowable bearing capacity with configurable factor of safety (default: 3.0)
- Applied pressure calculations
- Safety factor analysis
- Foundation geometry optimization

**Input Parameters:**
- Foundation width (B) and length (L)
- Foundation depth (Df)
- Applied vertical load
- Soil properties (unit weight, cohesion, friction angle)

**Outputs:**
- Ultimate bearing capacity (qu)
- Allowable bearing capacity (qa)
- Applied pressure
- Safety factor
- Bearing capacity factors (Nc, Nq, Nγ)
- Safety status (SAFE/UNSAFE)

### 2. Deep Foundation Design - Single Pile
Calculate pile capacity for single piles including both driven and bored piles.

**Capabilities:**
- End bearing capacity calculations
- Skin friction capacity calculations
- Total pile capacity with configurable factor of safety (default: 2.5)
- Support for both driven and bored pile types
- Utilization ratio analysis

**Input Parameters:**
- Pile diameter
- Pile length
- Pile type (driven or bored)
- Applied load per pile
- Soil properties (unit weight, cohesion, friction angle)

**Outputs:**
- End bearing capacity (Qb)
- Skin friction capacity (Qs)
- Ultimate capacity (Qu)
- Allowable capacity (Qa)
- Safety factor
- Utilization ratio
- Safety status (SAFE/UNSAFE)

### 3. Deep Foundation Design - Pile Group
Analyze pile groups with efficiency factors and group behavior.

**Capabilities:**
- Pile group efficiency calculations based on spacing
- Group capacity analysis
- Load distribution per pile
- Optimized pile group configurations

**Input Parameters:**
- Pile diameter and length
- Number of piles in group (2-20)
- Pile spacing
- Total applied load
- Soil properties (unit weight, cohesion, friction angle)

**Outputs:**
- Single pile capacities
- Group efficiency factor
- Group ultimate capacity
- Group allowable capacity
- Load per pile
- Safety factor
- Average pile utilization
- Safety status (SAFE/UNSAFE)

### 4. Retaining Wall Design
Calculate earth pressures and forces on retaining walls.

**Capabilities:**
- Active and passive earth pressure coefficients using Rankine theory
- Total active force calculations
- Force location determination
- Surcharge load effects
- Pressure distribution analysis

**Input Parameters:**
- Wall height (H)
- Wall thickness
- Surcharge load
- Soil properties (unit weight, cohesion, friction angle)

**Outputs:**
- Active pressure coefficient (Ka)
- Passive pressure coefficient (Kp)
- Total active force
- Force location from base
- Active pressure at base

## Visualization

Each foundation type includes an interactive visualization:

- **Shallow Foundation**: Top view showing foundation dimensions
- **Single Pile**: Side view with ground level reference
- **Pile Group**: Side view showing all piles in the group
- **Retaining Wall**: Side view with retained soil and pressure distribution

## Technical Background

### Shallow Foundation Calculations

The toolset uses **Terzaghi's Bearing Capacity Equation**:

```
qu = c·Nc + γ·Df·Nq + 0.5·γ·B·Nγ
```

Where:
- qu = ultimate bearing capacity
- c = soil cohesion
- γ = unit weight of soil
- Df = depth of foundation
- B = foundation width
- Nc, Nq, Nγ = bearing capacity factors (functions of friction angle φ)

**Bearing Capacity Factors:**
```
Nq = e^(π·tan φ) · tan²(45° + φ/2)
Nc = (Nq - 1) / tan φ  (for φ > 0°)
Nγ = 2(Nq + 1) · tan φ
```

**Allowable Bearing Capacity:**
```
qa = qu / FOS  (default FOS = 3.0)
```

### Deep Foundation (Pile) Calculations

**End Bearing Capacity:**
```
Qb = qb · Ab
qb = c·Nc + σv·Nq
```

Where:
- Qb = end bearing capacity
- Ab = pile base area = π·D²/4
- σv = effective stress at pile tip
- D = pile diameter

**Skin Friction Capacity:**
```
Qs = fs · As
fs = c + K·σv·tan δ
As = π·D·L
```

Where:
- Qs = skin friction capacity
- fs = unit skin friction
- As = pile shaft area
- L = pile length
- K = lateral earth pressure coefficient (0.8 for driven, 0.7 for bored)
- δ = interface friction angle (0.75φ for driven, 0.6φ for bored)

**Total Pile Capacity:**
```
Qu = Qb + Qs
Qa = Qu / FOS  (default FOS = 2.5)
```

**Pile Group Efficiency:**
```
η = group efficiency factor (0-1)
Simplified approach based on spacing/diameter ratio:
- η = 1.0 for s/d ≥ 6
- η = 0.7 + 0.3·(s/d - 3)/3 for 3 ≤ s/d < 6
- η = 0.7·s/d/3 for s/d < 3
```

### Retaining Wall Calculations

**Rankine Earth Pressure Theory:**

**Active Earth Pressure Coefficient:**
```
Ka = tan²(45° - φ/2)
```

**Passive Earth Pressure Coefficient:**
```
Kp = tan²(45° + φ/2)
```

**Total Active Force:**
```
Fa = 0.5·Ka·γ·H² + Ka·q·H
```

Where:
- Fa = total active force per unit length
- H = wall height
- q = surcharge load
- γ = unit weight of soil

**Force Location from Base:**
Calculated using moment equilibrium considering both soil weight and surcharge contributions.

## Design Standards and Safety Factors

The toolset implements commonly used factors of safety:

- **Shallow Foundations**: FOS = 3.0
- **Deep Foundations (Piles)**: FOS = 2.5

These values are based on typical geotechnical engineering practice and can be adjusted in the code if needed for specific project requirements or local building codes.

## Usage Guidelines

### Getting Started

1. Select the foundation type from the "Foundation Type" section
2. Enter soil properties (unit weight, cohesion, friction angle)
3. Enter foundation-specific parameters (dimensions, loads, etc.)
4. View results in the "Results" tab
5. View visualization in the "Foundation Visualization" tab

### Best Practices

1. **Soil Parameters**: Ensure soil parameters are based on proper geotechnical investigation
2. **Safety Factors**: Verify that safety factors meet or exceed 1.0 for safe designs
3. **Pile Spacing**: Maintain adequate pile spacing (typically 3D minimum) to avoid excessive group effects
4. **Verification**: Always verify computer-aided calculations with hand calculations for critical projects
5. **Local Codes**: Check that design complies with local building codes and standards

### Limitations

- Calculations assume homogeneous soil conditions
- Groundwater effects are not explicitly modeled (adjust soil parameters accordingly)
- Seismic loads are not included (static loads only)
- Settlement calculations are not included in this version
- Assumes vertical loads only (no moment or horizontal load effects)

## Future Enhancements

Potential additions for future versions:

1. **Settlement Analysis**
   - Immediate settlement calculations
   - Consolidation settlement analysis
   - Time-rate of settlement

2. **Advanced Loading**
   - Moment and horizontal load effects
   - Combined loading analysis
   - Load combinations per code requirements

3. **Soil Stratification**
   - Multi-layer soil profiles
   - Weighted average properties
   - Layer-by-layer analysis

4. **Groundwater Effects**
   - Buoyancy corrections
   - Effective stress adjustments
   - Seepage analysis

5. **Additional Foundation Types**
   - Mat foundations
   - Combined footings
   - Strap footings
   - Caisson foundations

6. **Code Compliance**
   - Eurocode 7 checks
   - ACI 318 requirements
   - Local code compliance modules

7. **Advanced Features**
   - Optimization algorithms for foundation sizing
   - Cost estimation
   - Material quantity takeoffs
   - Detailed report generation

## Technical Requirements

- VIKTOR platform (version 14.0.0 or higher)
- Python 3.8+
- Required packages: viktor, plotly

## Support and Contribution

For issues, questions, or contributions, please refer to the project repository.

## License

See LICENSE file for details.

## References

1. Terzaghi, K. (1943). Theoretical Soil Mechanics. John Wiley & Sons, New York.
2. Meyerhof, G. G. (1963). Some recent research on the bearing capacity of foundations. Canadian Geotechnical Journal.
3. Vesic, A. S. (1973). Analysis of ultimate loads of shallow foundations. Journal of Soil Mechanics & Foundations Div.
4. Rankine, W. J. M. (1857). On the stability of loose earth. Philosophical Transactions of the Royal Society of London.
5. Tomlinson, M., & Woodward, J. (2014). Pile Design and Construction Practice. CRC Press.

---

*Last Updated: January 6, 2026*
*Version: 1.0*
