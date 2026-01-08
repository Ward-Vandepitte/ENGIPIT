# ENGIPIT - Geotechnical Foundation Design Toolset

A comprehensive application for rapid design calculations of foundation systems, specifically developed for civil engineers specialized in geotechnics. Now with integrated project management and soil investigation database.

## 🎯 Project Overview

ENGIPIT provides a complete toolset for designing and analyzing various foundation systems including:
- **Project Management** - Hierarchical project organization with team collaboration
- **Soil Investigation Database** - Comprehensive borehole data management (inspired by bedrock repositories)
- **Shallow Foundations** - Bearing capacity and safety factor analysis
- **Deep Foundations (Single Pile)** - End bearing and skin friction calculations
- **Deep Foundations (Pile Groups)** - Group efficiency and load distribution
- **Retaining Walls** - Earth pressure analysis using Rankine theory
- **Standards Compliance** - Fascicule 62 Titre V and other design standards

## ✨ Key Features

### Project Management Structure (NEW)

1. **Project Entity**
   - Project information (name, number, client, location)
   - Project team management (PM, geotechnical engineer, structural engineer)
   - Status tracking (from investigation to construction)
   - Timeline management

2. **Soil Investigation Database**
   - Complete geotechnical site investigation storage
   - Multiple boreholes per project
   - Detailed soil layer stratification
   - Test results integration (SPT, CPT)
   - Representative property calculations
   - Visual soil profile displays
   - Similar to bedrock repository concept

3. **Foundation Design Integration**
   - Link designs to soil investigations
   - Automatic soil parameter retrieval
   - Design history and version tracking
   - Standards-based calculations

### Foundation Types Supported

1. **Shallow Foundation Design**
   - Terzaghi bearing capacity calculations
   - Bearing capacity factors (Nc, Nq, Nγ)
   - Ultimate and allowable bearing capacity
   - Applied pressure analysis
   - Safety factor assessment

2. **Single Pile Design**
   - End bearing capacity calculations
   - Skin friction capacity (driven and bored piles)
   - Total pile capacity with safety factors
   - Utilization ratio tracking

3. **Pile Group Design**
   - Group efficiency factors based on spacing
   - Load distribution per pile
   - Group ultimate and allowable capacity
   - Average pile utilization

4. **Retaining Wall Design**
   - Active and passive earth pressure coefficients
   - Total active force calculations
   - Force location determination
   - Surcharge load effects

### Calculation Methods

- **Terzaghi's Bearing Capacity Theory** for shallow foundations
- **Classical Pile Theory** for deep foundations (end bearing + skin friction)
- **Rankine Earth Pressure Theory** for retaining walls
- Industry-standard safety factors (FOS = 3.0 for shallow, 2.5 for deep)

### Interactive Visualizations

Each foundation type includes visual representations:
- Shallow foundations: Top view with dimensions
- Single piles: Side view with ground level
- Pile groups: Side view showing all piles
- Retaining walls: Side view with pressure distribution

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ward-Vandepitte/ENGIPIT.git
   cd ENGIPIT
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Use the project management models to organize your projects
2. Create soil investigations with borehole data
3. Link foundation designs to soil investigations
4. Perform calculations using the foundation design modules
5. Export results and generate reports

## 📖 Documentation

- **[PROJECT_MANAGEMENT.md](docs/PROJECT_MANAGEMENT.md)** - **NEW** Project management structure documentation:
  - Entity hierarchy and architecture
  - Soil investigation database design
  - Usage workflows
  - Fascicule 62 integration
  - Comparison with bedrock repository concept

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete technical documentation including:
  - Detailed feature descriptions
  - Calculation methodologies
  - Input/output specifications
  - Design standards and safety factors
  - Usage guidelines and best practices
  - Future enhancement roadmap

- **[APP_GOALS.md](APP_GOALS.md)** - Project objectives and end goals
- **[AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)** - Development guidelines and standards

## 🧪 Testing

The project includes comprehensive unit tests covering all modules:

```bash
source venv/bin/activate
# Test foundation calculations
python -m unittest test_app -v
# Test project management models
python -m unittest test_project_models -v
# Run all tests
python -m unittest discover -v
```

**Test Coverage:**
- 21 unit tests for foundation calculation modules
- 19 unit tests for project management models
- Total: 40 tests (100% passing ✓)
- Validation against theoretical values
- Integration tests for realistic scenarios

## 🏗️ Project Structure

```
ENGIPIT/
├── app.py                          # Foundation calculation modules
├── project_models.py               # Project management data models (NEW)
├── test_app.py                     # Foundation calculation tests
├── test_project_models.py          # Project management tests (NEW)
├── requirements.txt                # Python dependencies
├── docs/
│   ├── PROJECT_MANAGEMENT.md       # Project structure documentation (NEW)
│   └── standards/                   # Design standards PDFs
│       ├── fascicule_62_titre_v... # French geotechnical standard
│       ├── SB260...                # Belgian standard
│       └── ...                     # Other standards
├── DOCUMENTATION.md               # Technical documentation
├── README.md                      # This file
├── APP_GOALS.md                  # Project goals and objectives
├── AGENT_INSTRUCTIONS.md         # Development guidelines
└── LICENSE                        # Project license
```

## 🔬 Technical Details

### Calculation Modules

1. **ShallowFoundationCalculator**
   - `calculate_bearing_capacity_factors()` - Compute Nc, Nq, Nγ
   - `calculate_ultimate_bearing_capacity()` - Terzaghi's equation
   - `calculate_allowable_bearing_capacity()` - Apply safety factor
   - `calculate_applied_pressure()` - Load/area calculation

2. **DeepFoundationCalculator**
   - `calculate_pile_end_bearing()` - Base resistance
   - `calculate_pile_skin_friction()` - Shaft resistance
   - `calculate_pile_capacity()` - Total capacity
   - `calculate_pile_group_efficiency()` - Group effects

3. **RetainingWallCalculator**
   - `calculate_active_earth_pressure_coefficient()` - Ka
   - `calculate_passive_earth_pressure_coefficient()` - Kp
   - `calculate_total_active_force()` - Force and location

### Project Management Models

- **GeotechnicalProject**: Complete project organization
- **SoilInvestigation**: Soil investigation database
- **Borehole**: Individual borehole with soil layers
- **SoilLayer**: Layer-specific soil properties
- **FoundationDesign**: Design data and results

## 🛣️ Roadmap

Future enhancements planned:
- Settlement analysis (immediate and consolidation)
- Multi-layer soil profiles
- Groundwater effects and buoyancy
- Advanced loading (moment and horizontal loads)
- Additional foundation types (mat, combined footings)
- Code compliance modules (Eurocode 7, ACI 318)
- Optimization algorithms for foundation sizing
- Cost estimation and material takeoffs

## 📋 Important Documentation

### For All Team Members and Agents

Before contributing to this project, you **MUST** review the following documents:

- **[APP_GOALS.md](APP_GOALS.md)** - Defines the step-by-step end goals for this application. All development work must align with these goals.
- **[AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)** - Contains mandatory instructions that all agents and subagents must follow. Non-compliance will result in rejected work.

These documents ensure:
- ✅ Consistent development approach across all contributors
- ✅ Alignment with project objectives
- ✅ High quality and maintainable code
- ✅ Clear communication and collaboration

## 🤝 Contributing

Contributions are welcome! Please:
1. Review [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) for development standards
2. Ensure alignment with [APP_GOALS.md](APP_GOALS.md)
3. Add tests for new functionality
4. Update documentation as needed
5. Follow PEP 8 coding standards

## 📚 Additional Resources

- [Project End Goals](APP_GOALS.md)
- [Agent Instructions](AGENT_INSTRUCTIONS.md)
- [Project Management Documentation](docs/PROJECT_MANAGEMENT.md)

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project implements classical geotechnical engineering theories:
- Terzaghi's Bearing Capacity Theory
- Rankine Earth Pressure Theory
- Classical Pile Foundation Theory

## 📞 Support

For issues, questions, or contributions, please refer to the project repository or create an issue on GitHub.

---

**Status**: ✅ Active Development  
**Version**: 2.0 (with Project Management)  
**Progress**:
- ✅ End Goal 1: Foundation design toolset (completed)
- ✅ End Goal 2: Project management structure (completed)
- 🔄 End Goal 3: Fascicule 62 Titre V integration (in progress)

*Last Updated: January 7, 2026*
*Version: 2.0*
