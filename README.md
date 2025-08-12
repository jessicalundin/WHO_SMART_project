# WHO SMART Guidelines: Immunization and HIV Implementation Guide

## Overview

This repository focuses on **WHO SMART Guidelines for Immunization and HIV** - the World Health Organization's digital health implementation guides for vaccination programs and HIV care. SMART Guidelines represent WHO's approach to digital health guideline implementation:

- **S**tandards-based
- **M**achine-readable  
- **A**daptive
- **R**equirements-based
- **T**estable

These guidelines help countries implement WHO recommendations for immunization schedules and HIV care through standardized digital tools and FHIR (Fast Healthcare Interoperability Resources) specifications.

## Focus Areas

### Immunization Guidelines
- **Vaccination Schedules** - Digital implementation of WHO immunization schedules
- **Immunization Tracking** - Patient immunization status and history management
- **Vaccine Administration** - Standardized vaccine administration protocols
- **Adverse Event Monitoring** - Digital tracking of adverse events following immunization (AEFI)
- **Coverage Monitoring** - Population-level immunization coverage tracking

### HIV Guidelines  
- **HIV Testing and Diagnosis** - Digital protocols for HIV testing workflows
- **HIV Care and Treatment** - Antiretroviral therapy (ART) management protocols
- **Prevention Services** - Pre-exposure prophylaxis (PrEP) and prevention protocols
- **Monitoring and Evaluation** - HIV program monitoring and outcome tracking
- **Integration with Other Services** - Coordination with TB, maternal health, and other programs

## Repository Structure & Access Patterns

### Key WHO SMART Repositories for Immunization and HIV

#### Immunization
- **GitHub Repository**: [`smart-immunizations`](https://github.com/WorldHealthOrganization/smart-immunizations)
- **HTML Documentation**: [http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/](http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/)
- **GitHub Pages**: [https://worldhealthorganization.github.io/smart-immunizations/](https://worldhealthorganization.github.io/smart-immunizations/)
- **Downloads**: [http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/downloads.html](http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/downloads.html)

#### HIV Guidelines (In Development)
- **GitHub Repository**: [`smart-hiv`](https://github.com/WorldHealthOrganization/smart-hiv) (In Development)
- **HTML Documentation**: [http://build.fhir.org/ig/WorldHealthOrganization/smart-hiv/](http://build.fhir.org/ig/WorldHealthOrganization/smart-hiv/) (When Available)
- **GitHub Pages**: [https://worldhealthorganization.github.io/smart-hiv/](https://worldhealthorganization.github.io/smart-hiv/) (When Available)

#### Supporting Repositories
- **SMART Base**: [`smart-base`](https://github.com/WorldHealthOrganization/smart-base) - Foundation profiles and shared dependencies
  - HTML Documentation: [http://build.fhir.org/ig/WorldHealthOrganization/smart-base/](http://build.fhir.org/ig/WorldHealthOrganization/smart-base/)
- **SMART Trust**: [`smart-trust`](https://github.com/WorldHealthOrganization/smart-trust) - Trust Network Specification
  - HTML Documentation: [http://build.fhir.org/ig/WorldHealthOrganization/smart-trust/](http://build.fhir.org/ig/WorldHealthOrganization/smart-trust/)

### Available Downloads
All guidelines provide downloadable packages in multiple formats:
- **ZIP files** - Complete implementation guide bundles
- **TGZ files** - NPM-style FHIR packages for tooling integration
- **JSON** - FHIR resource definitions and examples
- **Turtle/RDF** - Semantic web formats for advanced interoperability

## Understanding FHIR Resources

### What Are These Resources For?
The FHIR resources found in WHO SMART Guidelines are **not for setting up FHIR servers directly**. Instead, they provide:

1. **Standardized Data Models** - Define how patient data should be structured
2. **Interoperability Specifications** - Ensure different healthcare systems can exchange data
3. **Implementation Guidance** - Help countries adapt WHO recommendations to local contexts
4. **Validation Rules** - Ensure data quality and compliance with guidelines

### Key FHIR Resource Types
- **StructureDefinition** - Data models and profiles (e.g., Patient, Observation profiles)
- **ValueSet/CodeSystem** - Standardized vocabularies and medical codes
- **ImplementationGuide** - Complete specification documents
- **ConceptMap** - Mappings between different coding systems
- **PlanDefinition** - Clinical decision support logic

### Implementation Patterns

#### For Healthcare System Implementers
```python
# 1. Download WHO implementation guide packages
# 2. Install in FHIR validation tools
# 3. Configure EMR/HIS systems to validate data against WHO profiles
# 4. Enable standardized data exchange with other systems
```

#### For Software Developers
```python
# 1. Use NPM packages in FHIR tooling ecosystems
# 2. Build SMART on FHIR applications following WHO standards
# 3. Create data transformation pipelines
# 4. Implement clinical decision support systems
```

#### For Standards Bodies & Countries
```python
# 1. Adapt WHO profiles for local requirements
# 2. Extend base profiles with country-specific data elements
# 3. Create national implementation guides
# 4. Establish local validation and certification processes
```

### NPM Package Usage
NPM packages are designed for **FHIR tooling ecosystems**:

- **HAPI FHIR** (Java) - Server-side validation and processing
- **FHIR.js** (JavaScript) - Client-side validation and data handling
- **fhir-parser** (Python) - Data processing and transformation
- **Forge/Simplifier** - Profile editing and management tools
- **FHIR Validator** - Command-line validation utilities

## Python Access Methods

### 1. Installation

Install the SMART on FHIR Python client:

```bash
pip install fhirclient
```

### 2. Basic Setup

```python
from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models.observation import Observation

# Configure FHIR client
settings = {
    'app_id': 'smart_guidelines_app',
    'api_base': 'https://r4.smarthealthit.org'  # Example FHIR server
}

smart = client.FHIRClient(settings=settings)
```

### 3. Accessing SMART Guideline Resources

```python
# Search for patients
patients = Patient.where(struct={'family': 'Smith'}).perform_resources(smart.server)

# Access guideline-specific observations
observations = Observation.where(struct={
    'patient': 'Patient/123',
    'category': 'survey'
}).perform_resources(smart.server)

# Retrieve specific guideline implementations
from fhirclient.models.plandefinition import PlanDefinition
guidelines = PlanDefinition.where({}).perform_resources(smart.server)
```

### 4. Authentication for Protected Resources

For accessing protected SMART on FHIR resources:

```python
import requests
from urllib.parse import urlencode

# OAuth2 authentication flow
auth_url = f"{fhir_base}/oauth2/authorize"
token_url = f"{fhir_base}/oauth2/token"

# Step 1: Get authorization code
auth_params = {
    'response_type': 'code',
    'client_id': 'your_client_id',
    'redirect_uri': 'your_redirect_uri',
    'scope': 'patient/*.read'
}

# Step 2: Exchange code for token
token_data = {
    'grant_type': 'authorization_code',
    'code': 'received_auth_code',
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret'
}

response = requests.post(token_url, data=token_data)
token = response.json()['access_token']

# Step 3: Use token in requests
headers = {'Authorization': f'Bearer {token}'}
```

### 5. Working with WHO SMART Guidelines for Immunization and HIV

The included `smart_explore.py` script demonstrates comprehensive access to WHO SMART Guidelines for Immunization and HIV:

```python
# Run the exploration script focused on immunization and HIV
python smart_explore.py

# Or use the SMARTGuidelinesClient class directly
from smart_explore import SMARTGuidelinesClient

client = SMARTGuidelinesClient()

# Get immunization guideline information
summary = client.get_guideline_summary("immunizations")
print(f"Repository: {summary['description']}")

# Check immunization endpoint availability
availability = client.check_guideline_availability("immunizations")
print(f"Available endpoints: {[name for name, info in availability.items() if info['accessible']]}")

# Fetch immunization HTML content
html_content = client.fetch_guideline_html("immunizations")
if html_content:
    print(f"Title: {html_content['title']}")
    print(f"Version: {html_content['version']}")
    print(f"Immunization sections: {html_content['sections'][:5]}")

# Get immunization download information
downloads = client.fetch_downloads_info("immunizations")
if downloads:
    print(f"Available formats: {downloads['formats']}")
    for file_info in downloads['files'][:3]:
        print(f"- {file_info['description']} ({file_info['format']})")

# Check HIV guidelines (when available)
hiv_summary = client.get_guideline_summary("hiv")
print(f"HIV Guidelines: {hiv_summary['description']}")
```

### 6. Accessing Downloadable Resources

```python
import requests

def download_implementation_guide(guideline_name, format_type="zip"):
    """
    Download WHO SMART guideline packages for immunization and HIV
    """
    base_url = f"http://build.fhir.org/ig/WorldHealthOrganization/smart-{guideline_name}"
    
    # Common download endpoints
    download_urls = {
        'zip': f"{base_url}/full-ig.zip",
        'tgz': f"{base_url}/package.tgz", 
        'json': f"{base_url}/definitions.json.zip"
    }
    
    url = download_urls.get(format_type)
    if not url:
        print(f"Format {format_type} not supported")
        return None
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = f"smart-{guideline_name}-{format_type}"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
            return filename
        else:
            print(f"Download failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

# Download immunization implementation guide
download_implementation_guide("immunizations", "zip")

# Download HIV implementation guide (when available)
download_implementation_guide("hiv", "zip")
```

### 7. Real-World Implementation Workflow

#### Immunization Program Implementation
```python
# Example: Implementing WHO Immunization Guidelines in a healthcare system

# Step 1: Download and validate immunization implementation guide
client = SMARTGuidelinesClient()
immunization_downloads = client.fetch_downloads_info("immunizations")

# Step 2: Install FHIR validation tools
# pip install fhir-validator  # (hypothetical - use actual FHIR tooling)

# Step 3: Configure your immunization information system
def configure_immunization_system(guideline_package):
    """
    Configure immunization system to validate data against WHO profiles
    """
    # Load WHO immunization profiles into validation engine
    # Configure vaccine administration forms to match WHO data elements
    # Set up automated immunization schedule tracking
    # Configure adverse event monitoring (AEFI)
    pass

# Step 4: Implement immunization decision support
def implement_immunization_decision_support(immunization_profiles):
    """
    Implement WHO immunization clinical decision support logic
    """
    # Parse immunization PlanDefinition resources
    # Configure vaccination schedule alerts and reminders
    # Set up catch-up vaccination protocols
    # Implement contraindication checking
    pass
```

#### HIV Program Implementation
```python
# Example: Implementing WHO HIV Guidelines in a healthcare system

# Step 1: Download and validate HIV implementation guide (when available)
hiv_downloads = client.fetch_downloads_info("hiv")

# Step 2: Configure HIV care and treatment system
def configure_hiv_system(guideline_package):
    """
    Configure HIV system to validate data against WHO profiles
    """
    # Load WHO HIV profiles into validation engine
    # Configure HIV testing and counseling workflows
    # Set up ART treatment monitoring protocols
    # Configure viral load and CD4 tracking
    pass

# Step 3: Implement HIV decision support
def implement_hiv_decision_support(hiv_profiles):
    """
    Implement WHO HIV clinical decision support logic
    """
    # Parse HIV PlanDefinition resources
    # Configure ART eligibility and regimen selection
    # Set up treatment failure detection
    # Implement adherence monitoring alerts
    pass

# Step 4: Enable interoperability
def setup_data_exchange(profiles):
    """
    Configure system for standardized data exchange
    """
    # Export patient data in WHO-compliant FHIR format
    # Enable interoperability with other healthcare systems
    # Support national health information exchange
    # Integrate with surveillance systems
    pass
```

## Quick Start

1. **Explore Guidelines**: Run `python smart_explore.py` to see immunization and HIV guidelines
2. **Access Content**: Visit build sites for human-readable documentation
   - Immunization: [http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/](http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/)
   - HIV: [http://build.fhir.org/ig/WorldHealthOrganization/smart-hiv/](http://build.fhir.org/ig/WorldHealthOrganization/smart-hiv/) (when available)
3. **Download Packages**: Use downloads.html pages for implementation packages
4. **Validate Data**: Install FHIR tooling to validate against WHO profiles
5. **Implement Standards**: Configure your immunization/HIV systems to use WHO data models

## Key Takeaways for Immunization and HIV Implementation

- **Purpose**: Standardize immunization and HIV data exchange globally
- **Target Users**: Immunization program managers, HIV program implementers, software developers
- **Implementation**: Download profiles → Install in validation tools → Configure immunization/HIV systems
- **Interoperability**: Enable immunization registries and HIV systems to exchange standardized data
- **Program Integration**: Support coordinated care between immunization, HIV, and other health programs
- **Surveillance**: Enable standardized reporting to national and international surveillance systems

## Resources

### WHO SMART Guidelines for Immunization and HIV
- **Main Website**: https://smart.who.int
- **Immunization GitHub**: https://github.com/WorldHealthOrganization/smart-immunizations
- **HIV GitHub**: https://github.com/WorldHealthOrganization/smart-hiv (In Development)
- **Immunization Build Site**: http://build.fhir.org/ig/WorldHealthOrganization/smart-immunizations/
- **HIV Build Site**: http://build.fhir.org/ig/WorldHealthOrganization/smart-hiv/ (When Available)
- **All WHO SMART Repositories**: https://github.com/WorldHealthOrganization?q=smart

### FHIR & Standards
- **FHIR Documentation**: https://www.hl7.org/fhir/
- **SMART on FHIR**: https://docs.smarthealthit.org/
- **Clinical Practice Guidelines**: http://hl7.org/fhir/uv/cpg/

### Development Tools
- **Python FHIR Client**: https://github.com/smart-on-fhir/client-py
- **HAPI FHIR**: https://hapifhir.io/
- **Simplifier/Forge**: https://simplifier.net/
- **NPM FHIR Packages**: https://www.npmjs.com/search?q=fhir
