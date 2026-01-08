# ENGIPIT Quick Start Guide

## Overview

This quick start guide helps you get up and running with ENGIPIT's geotechnical foundation design toolset and project management system.

## For Different User Types

### 🔷 Project Managers
**Your focus**: Project setup, team coordination, and status tracking
- Start here: [Project Creation Workflow](#project-creation-workflow)
- See: [docs/PROJECT_MANAGEMENT.md](docs/PROJECT_MANAGEMENT.md)

### 🔷 Geotechnical Engineers
**Your focus**: Soil investigations, data analysis, and foundation recommendations
- Start here: [Soil Investigation Workflow](#soil-investigation-workflow)
- See: [docs/PROJECT_MANAGEMENT.md](docs/PROJECT_MANAGEMENT.md)

### 🔷 Structural Engineers
**Your focus**: Foundation design calculations and structural integration
- Start here: [Foundation Design Workflow](#foundation-design-workflow)
- See: [DOCUMENTATION.md](DOCUMENTATION.md)

### 🔷 Developers
**Your focus**: Code contribution and system extensions
- Start here: [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)
- See: [APP_GOALS.md](APP_GOALS.md)

---

## Project Creation Workflow

### Step 1: Create a New Project

1. **Use the project models** to create a new project
2. **Create a GeotechnicalProject instance**
3. **Fill in project details**:
   - Project Name
   - Project Number
   - Client Name
   - Location and Address
   - Project Description
   - Team members (PM, Engineers)
   - Project Status
   - Timeline

### Step 2: Access Your Project Data

Once created, you can:
- Access project properties using the data model
- Add soil investigations and foundation designs
- Serialize to JSON for storage
- Query and analyze project data

---

## Soil Investigation Workflow

### Step 1: Create Soil Investigation

1. **Create a SoilInvestigation instance** for your project
2. **Fill in investigation details**:
   - Name (e.g., "Site Investigation - Phase 1")
   - Consultant name
   - Investigation Date
   - Site Description

### Step 2: Add Boreholes

For each borehole location:
1. Create a Borehole instance
2. Enter borehole information:
   - Name (e.g., "BH-01")
   - Location coordinates (X, Y)
   - Ground level elevation
   - Water level depth
   - Total drilling depth

### Step 3: Define Soil Layers

For each borehole, add soil layers:
- Depth range (top and bottom)
- Soil type classification
- Description
- Physical properties (unit weight, cohesion, friction angle)
- Test results (SPT N-value, etc.)

### Step 4: Set Representative Properties

Calculate and set site-wide representative values from your borehole data for quick design use.

---

## Foundation Design Workflow

### Step 1: Create Foundation Design

1. **Create a FoundationDesign instance** for your project
2. **Fill in design info**:
   - Foundation name
   - Foundation type (shallow, deep, retaining wall)
   - Design standard (Fascicule 62, Eurocode 7)
   - Status (preliminary, detailed, final)

### Step 2: Link to Soil Data

**Option A**: Link to existing SoilInvestigation - automatic property retrieval  
**Option B**: Manual Input - enter soil properties directly in design parameters

### Step 3: Enter Design Parameters

Enter parameters based on foundation type:
- **Shallow**: Width, length, depth, applied load
- **Deep**: Pile diameter, length, type, spacing, total load
- **Retaining**: Wall height, thickness, surcharge

### Step 4: Review Results

Access and review:
- Design calculations and results stored in the FoundationDesign object
- Safety factors and utilization ratios
- Design checks and compliance status

---

## Quick Reference

### Entity Hierarchy
```
Project
├── Soil Investigation
│   └── Borehole (multiple)
│       └── Soil Layers
└── Foundation Design (multiple)
```

### Common Workflows

**Workflow 1: Complete Project**
1. Create Project → 2. Add Soil Investigation → 3. Add Boreholes → 4. Create Foundation Designs

**Workflow 2: Quick Design**
1. Create Project → 2. Create Foundation Design → 3. Use manual soil input

---

*Last Updated: January 7, 2026*  
*Version: 2.0*
