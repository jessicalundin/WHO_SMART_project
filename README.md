# WHO SMART Guidelines Access with Python

## Overview

**SMART Guidelines** are WHO's approach to digital health guideline implementation, standing for:
- **S**tandards-based
- **M**achine-readable  
- **A**daptive
- **R**equirements-based
- **T**estable

These guidelines help countries implement WHO health recommendations through standardized digital tools and FHIR (Fast Healthcare Interoperability Resources) specifications.

## Available Guidelines

### Currently Published
- **Antenatal Care (ANC) v0.3.0** - Pregnancy care guidelines with 8-visit contact schedule
- **SMART Base v0.2.0** - Foundation profiles and shared dependencies
- **Immunizations v0.2.0** - Vaccination schedules and immunization tracking
- **SMART Trust v1.1.6** - Trust Network Specification for health data exchange
- **Family Planning** - Reproductive health guidelines  
- **COVID-19 Digital Certificates** - Vaccination and test result documentation

### In Development
- **HIV** (2nd edition) - Enhanced HIV care and treatment protocols
- **TB** - Tuberculosis diagnosis and treatment guidelines
- **Clinical Care in Crises** - Emergency and humanitarian response protocols

## Repository Structure & Access Patterns

### Key WHO SMART Repositories
- [`smart-base`](https://github.com/WorldHealthOrganization/smart-base) - Foundation profiles and shared dependencies
- [`smart-anc`](https://github.com/WorldHealthOrganization/smart-anc) - Antenatal Care Implementation Guide
- [`smart-immunizations`](https://github.com/WorldHealthOrganization/smart-immunizations) - Immunization guidelines
- [`smart-trust`](https://github.com/WorldHealthOrganization/smart-trust) - Trust Network Specification

### Access Endpoints
Each guideline is available through multiple channels:
- **Build Sites**: `http://build.fhir.org/ig/WorldHealthOrganization/smart-{name}/`
- **GitHub Pages**: `https://worldhealthorganization.github.io/smart-{name}/`
- **Source Code**: `https://github.com/WorldHealthOrganization/smart-{name}`

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

### 5. Working with WHO SMART Guidelines

The included `smart_explore.py` script demonstrates comprehensive access to WHO SMART Guidelines:

```python
# Run the exploration script
python smart_explore.py

# Or use the SMARTGuidelinesClient class directly
from smart_explore import SMARTGuidelinesClient

client = SMARTGuidelinesClient()

# Get repository information
summary = client.get_guideline_summary("anc")
print(f"Repository: {summary['description']}")

# Check endpoint availability
availability = client.check_guideline_availability("anc")
print(f"Available endpoints: {[name for name, info in availability.items() if info['accessible']]}")

# Fetch HTML content when JSON isn't available
html_content = client.fetch_guideline_html("anc")
if html_content:
    print(f"Title: {html_content['title']}")
    print(f"Version: {html_content['version']}")
    print(f"Sections: {html_content['sections'][:5]}")

# Get download information
downloads = client.fetch_downloads_info("anc")
if downloads:
    print(f"Available formats: {downloads['formats']}")
    for file_info in downloads['files'][:3]:
        print(f"- {file_info['description']} ({file_info['format']})")
```

### 6. Accessing Downloadable Resources

```python
import requests

def download_implementation_guide(guideline_name, format_type="zip"):
    """
    Download WHO SMART guideline packages
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

# Download ANC implementation guide
download_implementation_guide("anc", "zip")
```

### 7. Real-World Implementation Workflow

```python
# Example: Implementing WHO ANC Guidelines in a healthcare system

# Step 1: Download and validate implementation guide
client = SMARTGuidelinesClient()
anc_downloads = client.fetch_downloads_info("anc")

# Step 2: Install FHIR validation tools
# pip install fhir-validator  # (hypothetical - use actual FHIR tooling)

# Step 3: Configure your EMR system
def configure_emr_validation(guideline_package):
    """
    Configure EMR to validate patient data against WHO profiles
    """
    # Load WHO profiles into validation engine
    # Configure data input forms to match WHO data elements
    # Set up automated quality checks
    pass

# Step 4: Implement clinical decision support
def implement_decision_support(anc_profiles):
    """
    Implement WHO ANC clinical decision support logic
    """
    # Parse PlanDefinition resources
    # Configure clinical alerts and reminders
    # Set up guideline-based care pathways
    pass

# Step 5: Enable data exchange
def setup_data_exchange(profiles):
    """
    Configure system for standardized data exchange
    """
    # Export patient data in WHO-compliant FHIR format
    # Enable interoperability with other healthcare systems
    # Support national health information exchange
    pass
```

## Quick Start

1. **Explore Guidelines**: Run `python smart_explore.py` to see available guidelines
2. **Access Content**: Visit build sites for human-readable documentation
3. **Download Packages**: Use downloads.html pages for implementation packages
4. **Validate Data**: Install FHIR tooling to validate against WHO profiles
5. **Implement Standards**: Configure your healthcare systems to use WHO data models

## Key Takeaways

- **Purpose**: Standardize healthcare data exchange
- **Target Users**: Healthcare implementers, software developers, standards bodies
- **Implementation**: Download profiles → Install in validation tools → Configure systems
- **Interoperability**: Enable different healthcare systems to exchange standardized data
- **Adaptation**: Countries can extend WHO profiles for local requirements

## Resources

### WHO SMART Guidelines
- **Main Website**: https://smart.who.int
- **GitHub Organization**: https://github.com/WorldHealthOrganization?q=smart
- **Build Sites**: http://build.fhir.org/ig/WorldHealthOrganization/smart-{name}/

### FHIR & Standards
- **FHIR Documentation**: https://www.hl7.org/fhir/
- **SMART on FHIR**: https://docs.smarthealthit.org/
- **Clinical Practice Guidelines**: http://hl7.org/fhir/uv/cpg/

### Development Tools
- **Python FHIR Client**: https://github.com/smart-on-fhir/client-py
- **HAPI FHIR**: https://hapifhir.io/
- **Simplifier/Forge**: https://simplifier.net/
- **NPM FHIR Packages**: https://www.npmjs.com/search?q=fhir

## Contributing

When working with WHO SMART Guidelines:
1. Follow FHIR R4 specifications and WHO data standards
2. Respect Creative Commons - IGO licensing
3. Submit feedback through GitHub repository issues
4. Ensure compliance with local health data regulations
5. Consider country-specific adaptations and extensions

## License

WHO SMART Guidelines are published under Creative Commons - IGO license. Please review individual repository licenses before use in production systems.