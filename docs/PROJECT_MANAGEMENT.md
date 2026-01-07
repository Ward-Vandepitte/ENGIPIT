# Project Management Structure for ENGIPIT

## Overview

This document describes the project management structure implemented in ENGIPIT for managing geotechnical and structural design projects. The structure is designed to organize projects with integrated soil investigation databases and foundation design calculations.

## Design Philosophy

The project management structure is based on industry best practices for geotechnical engineering firms and follows these principles:

1. **Hierarchical Organization**: Projects contain soil investigations and foundation designs
2. **Soil Investigation Database**: Comprehensive storage of geotechnical data similar to specialized repositories
3. **Traceability**: Clear links between soil data and foundation designs
4. **Standards Compliance**: Designed to work with Fascicule 62 Titre V and other standards
5. **Collaboration**: Support for multi-disciplinary teams (geotechnical, structural, project management)

## Entity Hierarchy

```
Project (Top Level)
├── Soil Investigation 1
│   ├── Borehole 1
│   │   ├── Soil Layer 1
│   │   ├── Soil Layer 2
│   │   └── Soil Layer n
│   ├── Borehole 2
│   └── Borehole n
├── Soil Investigation 2 (if multiple phases)
├── Foundation Design 1
├── Foundation Design 2
└── Foundation Design n
```

### 1. Project Entity (Top Level)

The **Project** is the top-level entity that represents a complete geotechnical/structural design engagement.

**Key Attributes:**
- Project identification (name, number, client)
- Location information (address, coordinates)
- Project team (manager, engineers)
- Status tracking (initiated, investigation, design, etc.)
- Timeline (start date, target completion)

**Purpose:**
- Central hub for all project-related information
- Provides context for soil investigations and designs
- Enables project portfolio management
- Facilitates team coordination

**VIKTOR Implementation:**
- Entity Type: `Project`
- Controller: `ProjectController`
- Parametrization: `ProjectParametrization`

### 2. Soil Investigation Entity

The **Soil Investigation** entity represents a complete geotechnical site investigation. This is the core of the soil investigation database concept.

**Key Attributes:**
- Investigation metadata (name, date, consultant)
- Site description
- Representative soil properties (derived from all boreholes)
- Collection of boreholes

**Purpose:**
- Centralize all geotechnical investigation data
- Provide representative properties for quick design use
- Enable comparison between different investigation phases
- Serve as authoritative source for soil parameters

**VIKTOR Implementation:**
- Entity Type: `SoilInvestigation` (child of Project)
- Controller: `SoilInvestigationController`
- Parametrization: `SoilInvestigationParametrization`

**Database Features:**
- Multiple soil investigations per project (for different phases)
- Representative properties calculated from all boreholes
- Links to foundation designs that use the data
- Complete investigation history and metadata

### 3. Borehole Entity

The **Borehole** entity represents a single borehole location with detailed soil layering information.

**Key Attributes:**
- Location (X, Y coordinates, ground level)
- Water level depth
- Total drilling depth
- Drilling date
- Soil layers (stratification)

**Purpose:**
- Detailed storage of soil profile data
- Visual representation of soil conditions
- Provide layer-specific properties for calculations
- Document field investigation results

**VIKTOR Implementation:**
- Entity Type: `Borehole` (child of SoilInvestigation)
- Controller: `BoreholeController`
- Parametrization: `BoreholeParametrization`

**Features:**
- Dynamic array of soil layers
- Visual soil profile display
- Complete geotechnical properties per layer
- Test results (SPT, CPT) integrated with layers

### 4. Soil Layer (Data Structure)

**Soil Layers** are defined within each Borehole using a dynamic array structure.

**Key Attributes:**
- Depth range (top and bottom)
- Soil type classification
- Physical properties (unit weight)
- Strength parameters (cohesion, friction angle)
- Test results (SPT N-values, CPT data)
- Water content, plasticity, etc.

**Purpose:**
- Store detailed soil stratification
- Enable depth-specific calculations
- Link test results to specific depths
- Support multi-layer analysis

### 5. Foundation Design Entity

The **Foundation Design** entity represents a specific foundation calculation or design within a project.

**Key Attributes:**
- Design identification (name, type)
- Link to soil investigation
- Design parameters (dimensions, loads)
- Calculation results
- Design standard used
- Safety factors
- Status (preliminary, final, approved)

**Purpose:**
- Perform foundation calculations
- Link designs to soil data
- Track design iterations
- Generate design documentation
- Maintain design history

**VIKTOR Implementation:**
- Entity Type: `FoundationDesign` (child of Project)
- Controller: `FoundationDesignController`
- Parametrization: `FoundationDesignParametrization`

**Features:**
- Multiple foundation types (shallow, deep, retaining walls)
- Choose between project soil investigation or manual input
- Automatic parameter retrieval from soil database
- Standards-based calculations (Fascicule 62, Eurocode 7, etc.)
- Results tracking and documentation

## Data Flow

### From Soil Investigation to Foundation Design

```
1. Create Project
   ↓
2. Create Soil Investigation
   ↓
3. Add Boreholes with Soil Layers
   ↓
4. System calculates representative properties
   ↓
5. Create Foundation Design
   ↓
6. Link to Soil Investigation
   ↓
7. Automatically retrieve soil properties
   ↓
8. Perform design calculations
   ↓
9. Generate results and reports
```

### Soil Investigation Database Features

The soil investigation database provides:

1. **Centralized Data Storage**
   - All geotechnical data in one location
   - Consistent data structure
   - Easy access and retrieval

2. **Data Reusability**
   - Multiple foundation designs can use the same investigation
   - No need to re-enter soil properties
   - Consistent parameters across designs

3. **Traceability**
   - Clear link between test data and designs
   - Audit trail of data sources
   - Version control of investigations

4. **Visualization**
   - Soil profile plots
   - Borehole location maps
   - Property distribution charts

5. **Analysis Capabilities**
   - Representative property calculations
   - Statistical analysis of test results
   - Depth-based parameter selection

## Fascicule 62 Titre V Integration

The structure is designed to support Fascicule 62 Titre V calculations:

### Design Standards Support

The foundation design entity includes:
- Design standard selection (Fascicule 62, Eurocode 7, etc.)
- Standard-specific safety factors
- Load combination handling
- Compliance documentation

### Fascicule 62 Specific Features

1. **Soil Classification** (Article 3)
   - Soil type classification system
   - Parameter selection guidance

2. **Foundation Types** (Articles 4-6)
   - Shallow foundations (Article 4)
   - Deep foundations on piles (Article 5)
   - Retaining structures (Article 6)

3. **Safety Factors** (Article 2)
   - Partial safety factors
   - Load combinations
   - Serviceability limits

4. **Bearing Capacity** (Article 4.3)
   - Calculation methods per F62
   - Pressuremeter methods
   - SPT/CPT correlations

5. **Pile Design** (Article 5)
   - End bearing calculations
   - Shaft friction per F62 methods
   - Group effects

## Usage Workflow

### Starting a New Project

1. **Create Project Entity**
   - Enter project details
   - Define project team
   - Set project status

2. **Create Soil Investigation**
   - Name the investigation phase
   - Enter consultant information
   - Set investigation date

3. **Add Boreholes**
   - For each borehole location:
     - Enter coordinates and levels
     - Define water level
     - Add soil layers (top to bottom)
     - Include test results

4. **Review Investigation Summary**
   - Check soil profiles
   - Review representative properties
   - Verify data completeness

5. **Create Foundation Designs**
   - Link to soil investigation
   - Select foundation type
   - Enter design parameters
   - Perform calculations

6. **Generate Reports**
   - Design calculations
   - Soil investigation summary
   - Project overview

### Managing Multiple Projects

The entity structure supports:
- Multiple active projects
- Comparison between projects
- Resource allocation tracking
- Portfolio overview

## Data Models

The system uses Python dataclasses for data modeling:

### Core Models (in `project_models.py`)

1. **GeotechnicalProject**
   - Main project container
   - Links to all sub-entities
   - Project metadata

2. **SoilInvestigation**
   - Investigation container
   - Collection of boreholes
   - Representative properties

3. **Borehole**
   - Borehole data container
   - Collection of soil layers
   - Location and metadata

4. **SoilLayer**
   - Individual layer data
   - Geotechnical properties
   - Test results

5. **FoundationDesign**
   - Design data container
   - Links to soil data
   - Results storage

### Enumerations

- **SoilType**: Clay, Sand, Gravel, etc.
- **ProjectStatus**: Initiated, Investigation, Design, etc.
- **FoundationType**: Shallow, Deep, Retaining Wall, etc.
- **TestType**: SPT, CPT, Laboratory tests, etc.

## Comparison with Bedrock Repository

The soil investigation database implementation draws inspiration from the "bedrock repository" concept:

### Similar Features

1. **Structured Data Storage**
   - Hierarchical organization
   - Consistent data schemas
   - Clear relationships

2. **Borehole Management**
   - Multiple boreholes per site
   - Layer-by-layer data
   - Test result integration

3. **Data Accessibility**
   - Easy retrieval
   - Query capabilities
   - Visualization tools

4. **Reusability**
   - Data used across multiple analyses
   - Centralized source of truth
   - Version control support

### Enhanced Features

1. **Project Integration**
   - Direct link to foundation designs
   - Project-level organization
   - Team collaboration features

2. **Standards Compliance**
   - Built-in calculation methods
   - Standards-based workflows
   - Automatic compliance checking

3. **VIKTOR Platform Integration**
   - Interactive visualizations
   - User-friendly interface
   - Cloud-based collaboration

## Technical Implementation

### File Structure

```
ENGIPIT/
├── app.py                      # Original foundation calculations
├── project_models.py           # Data models (NEW)
├── project_viktor.py           # VIKTOR entity structure (NEW)
├── test_app.py                 # Original tests
├── test_project_models.py      # Project model tests (TO ADD)
├── docs/
│   ├── standards/              # Design standards PDFs
│   └── PROJECT_MANAGEMENT.md   # This document
└── requirements.txt
```

### Dependencies

The project management structure uses:
- `viktor`: VIKTOR framework
- `dataclasses`: Python data modeling
- `plotly`: Visualizations
- `typing`: Type hints
- `datetime`: Date/time handling
- `json`: Data serialization

### Storage Approach

VIKTOR entities store data using:
1. **Parameters**: User-input data via parametrization
2. **Entity Storage**: Persistent entity properties
3. **Files**: Attached documents and reports
4. **Parent-Child**: Hierarchical relationships

## Best Practices

### Data Entry

1. **Soil Investigation**
   - Enter data as soon as investigation is complete
   - Verify all layer boundaries and properties
   - Include representative properties

2. **Boreholes**
   - Use consistent naming (BH-01, BH-02, etc.)
   - Ensure layers are continuous (no gaps)
   - Include all available test results

3. **Foundation Designs**
   - Always link to soil investigation when available
   - Document assumptions and design basis
   - Track design revisions

### Quality Control

1. **Review soil profiles** for continuity
2. **Check representative properties** against borehole data
3. **Verify design inputs** match soil investigation
4. **Document deviations** from standard procedures
5. **Maintain audit trail** of design decisions

### Collaboration

1. **Project Manager**: Oversees project entity, tracks status
2. **Geotechnical Engineer**: Manages soil investigations, reviews designs
3. **Structural Engineer**: Creates foundation designs, reviews results
4. **Team Members**: Access shared data, contribute to designs

## Future Enhancements

Potential future additions to the project management structure:

1. **Advanced Features**
   - Automated report generation
   - Design optimization algorithms
   - Cost estimation integration
   - Schedule management

2. **Data Analysis**
   - Statistical analysis of soil properties
   - Spatial interpolation between boreholes
   - Correlation studies

3. **Integration**
   - Import/export from other systems
   - GIS integration
   - BIM connectivity

4. **Compliance**
   - Additional design standards
   - Code checking automation
   - Regulatory reporting

5. **Collaboration**
   - Real-time multi-user editing
   - Comment and review workflows
   - Version comparison tools

## Summary

The ENGIPIT project management structure provides:

✅ **Organized** project hierarchy  
✅ **Comprehensive** soil investigation database  
✅ **Integrated** foundation design workflows  
✅ **Standards-based** calculations (Fascicule 62)  
✅ **Collaborative** team environment  
✅ **Traceable** design documentation  
✅ **Scalable** for multiple projects  

This structure enables geotechnical engineering firms to efficiently manage their projects from investigation through design to construction, with all data centralized and readily accessible.

---

*Document Version: 1.0*  
*Last Updated: January 7, 2026*
