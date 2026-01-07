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

1. **Open ENGIPIT** in your VIKTOR workspace
2. **Create Project Entity**
3. **Fill in project details**:
   - Project Name
   - Project Number
   - Client Name
   - Location and Address
   - Project Description
   - Team members (PM, Engineers)
   - Project Status
   - Timeline

### Step 2: Navigate Your Project

Once created, you'll see:
- **Project Overview**: Summary of project info
- **Child Entities**: Soil investigations and designs
- **Status Dashboard**: Current status and timeline

---

## Soil Investigation Workflow

### Step 1: Create Soil Investigation

1. **Within your Project**, add Soil Investigation child entity
2. **Fill in investigation details**:
   - Name (e.g., "Site Investigation - Phase 1")
   - Consultant name
   - Investigation Date
   - Site Description

### Step 2: Add Boreholes

For each borehole location:
1. Add Borehole child entity to Soil Investigation
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

In Soil Investigation entity, set site-wide representative values for quick design use.

---

## Foundation Design Workflow

### Step 1: Create Foundation Design

1. **Within your Project**, add Foundation Design child entity
2. **Fill in design info**:
   - Foundation name
   - Foundation type (shallow, deep, retaining wall)
   - Design standard (Fascicule 62, Eurocode 7)
   - Status (preliminary, detailed, final)

### Step 2: Link to Soil Data

**Option A**: Use Project Investigation - automatic soil property retrieval  
**Option B**: Manual Input - enter soil properties directly

### Step 3: Enter Design Parameters

Enter parameters based on foundation type:
- **Shallow**: Width, length, depth, applied load
- **Deep**: Pile diameter, length, type, spacing, total load
- **Retaining**: Wall height, thickness, surcharge

### Step 4: Review Results

View design summary, safety factors, and visualizations.

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
