#!/usr/bin/env python3
"""
WHO SMART Guidelines Access Script

This script provides functions to access and process WHO SMART Guidelines
using Python and the FHIR client library.
"""

import requests
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

try:
    from fhirclient import client
    from fhirclient.models.patient import Patient
    from fhirclient.models.observation import Observation
    FHIR_CLIENT_AVAILABLE = True
except ImportError:
    print("Warning: fhirclient not installed. Install with: pip install fhirclient")
    FHIR_CLIENT_AVAILABLE = False


class SMARTGuidelinesClient:
    """Client for accessing WHO SMART Guidelines"""
    
    def __init__(self, fhir_base_url: str = "https://r4.smarthealthit.org"):
        """
        Initialize SMART Guidelines client
        
        Args:
            fhir_base_url: Base URL for FHIR server
        """
        self.fhir_base_url = fhir_base_url
        self.smart_client = None
        
        if FHIR_CLIENT_AVAILABLE:
            settings = {
                'app_id': 'smart_guidelines_explorer',
                'api_base': fhir_base_url
            }
            self.smart_client = client.FHIRClient(settings=settings)
    
    def fetch_smart_guideline(self, guideline_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch SMART guideline from WHO repositories
        
        Args:
            guideline_name: Name of guideline (e.g., 'anc', 'immunizations')
            
        Returns:
            Dictionary containing guideline data or None if not found
        """
        # Updated URL patterns based on actual WHO repository structure
        url_patterns = [
            f"http://build.fhir.org/ig/WorldHealthOrganization/smart-{guideline_name}/ImplementationGuide-smart-{guideline_name}.json",
            f"http://build.fhir.org/ig/WorldHealthOrganization/smart-{guideline_name}/ImplementationGuide.json",
            f"https://worldhealthorganization.github.io/smart-{guideline_name}/ImplementationGuide-smart-{guideline_name}.json",
            f"https://worldhealthorganization.github.io/smart-{guideline_name}/ImplementationGuide.json",
            f"http://smart.who.int/{guideline_name}/ImplementationGuide/smart.who.int.{guideline_name}.json"
        ]
        
        for url in url_patterns:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"Successfully fetched {guideline_name} from: {url}")
                    return response.json()
            except requests.RequestException as e:
                continue
        
        print(f"Could not fetch guideline '{guideline_name}' from any known URL pattern")
        return None
    
    def process_dak_content(self, guideline_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process Digital Adaptation Kit content
        
        Args:
            guideline_data: Raw guideline data from FHIR server
            
        Returns:
            Processed DAK information
        """
        if not guideline_data:
            return None
        
        dak_info = {
            'title': guideline_data.get('title', 'Unknown Title'),
            'version': guideline_data.get('version', 'Unknown Version'),
            'description': guideline_data.get('description', ''),
            'status': guideline_data.get('status', 'unknown'),
            'date': guideline_data.get('date', ''),
            'publisher': guideline_data.get('publisher', ''),
            'resources': [],
            'dependencies': []
        }
        
        # Process dependencies
        for dep in guideline_data.get('dependsOn', []):
            dak_info['dependencies'].append({
                'uri': dep.get('uri', ''),
                'version': dep.get('version', '')
            })
        
        # Process contained resources
        for resource in guideline_data.get('contained', []):
            resource_type = resource.get('resourceType', 'Unknown')
            dak_info['resources'].append({
                'type': resource_type,
                'id': resource.get('id', ''),
                'title': resource.get('title', resource.get('name', ''))
            })
        
        return dak_info
    
    def search_patients(self, family_name: str = None) -> List[Dict[str, Any]]:
        """
        Search for patients using FHIR client
        
        Args:
            family_name: Patient family name filter
            
        Returns:
            List of patient resources
        """
        if not FHIR_CLIENT_AVAILABLE or not self.smart_client:
            print("FHIR client not available")
            return []
        
        try:
            search_params = {}
            if family_name:
                search_params['family'] = family_name
            
            patients = Patient.where(struct=search_params).perform_resources(self.smart_client.server)
            return [patient.as_json() for patient in patients]
            
        except Exception as e:
            print(f"Error searching patients: {e}")
            return []
    
    def get_guideline_observations(self, patient_id: str, category: str = "survey") -> List[Dict[str, Any]]:
        """
        Get guideline-specific observations for a patient
        
        Args:
            patient_id: Patient identifier
            category: Observation category filter
            
        Returns:
            List of observation resources
        """
        if not FHIR_CLIENT_AVAILABLE or not self.smart_client:
            print("FHIR client not available")
            return []
        
        try:
            observations = Observation.where(struct={
                'patient': patient_id,
                'category': category
            }).perform_resources(self.smart_client.server)
            
            return [obs.as_json() for obs in observations]
            
        except Exception as e:
            print(f"Error fetching observations: {e}")
            return []
    
    def authenticate_oauth2(self, client_id: str, client_secret: str, 
                           redirect_uri: str, scope: str = "patient/*.read") -> Optional[str]:
        """
        Perform OAuth2 authentication for protected FHIR resources
        
        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            redirect_uri: Redirect URI for OAuth2 flow
            scope: OAuth2 scope
            
        Returns:
            Access token or None if authentication fails
        """
        auth_url = f"{self.fhir_base_url}/oauth2/authorize"
        token_url = f"{self.fhir_base_url}/oauth2/token"
        
        # Step 1: Build authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope
        }
        
        full_auth_url = f"{auth_url}?{urlencode(auth_params)}"
        print(f"Visit this URL to authorize: {full_auth_url}")
        
        # In a real application, you would redirect the user and capture the code
        auth_code = input("Enter the authorization code: ")
        
        # Step 2: Exchange code for token
        token_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }
        
        try:
            response = requests.post(token_url, data=token_data)
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                print(f"Token exchange failed: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error during token exchange: {e}")
            return None


    def get_guideline_summary(self, guideline_name: str) -> Dict[str, Any]:
        """
        Get a summary of available guideline information from GitHub
        
        Args:
            guideline_name: Name of guideline
            
        Returns:
            Dictionary with guideline summary information
        """
        github_url = f"https://api.github.com/repos/WorldHealthOrganization/smart-{guideline_name}"
        
        try:
            response = requests.get(github_url, timeout=10)
            if response.status_code == 200:
                repo_data = response.json()
                return {
                    'name': repo_data.get('name', ''),
                    'description': repo_data.get('description', 'No description available'),
                    'updated_at': repo_data.get('updated_at', ''),
                    'html_url': repo_data.get('html_url', ''),
                    'topics': repo_data.get('topics', []),
                    'language': repo_data.get('language', ''),
                    'size': repo_data.get('size', 0)
                }
        except requests.RequestException:
            pass
        
        return {'name': guideline_name, 'description': 'Repository information not available'}
    
    def check_guideline_availability(self, guideline_name: str) -> Dict[str, Any]:
        """
        Check which guideline resources are available
        
        Args:
            guideline_name: Name of guideline
            
        Returns:
            Dictionary with availability status
        """
        endpoints = {
            'build_site': f"http://build.fhir.org/ig/WorldHealthOrganization/smart-{guideline_name}/",
            'github_pages': f"https://worldhealthorganization.github.io/smart-{guideline_name}/",
            'github_repo': f"https://github.com/WorldHealthOrganization/smart-{guideline_name}"
        }
        
        availability = {}
        for name, url in endpoints.items():
            try:
                response = requests.head(url, timeout=5)
                availability[name] = {
                    'url': url,
                    'status': response.status_code,
                    'accessible': response.status_code == 200
                }
            except requests.RequestException:
                availability[name] = {
                    'url': url,
                    'status': 'error',
                    'accessible': False
                }
        
        return availability
    
    def fetch_guideline_html(self, guideline_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch and parse HTML content from guideline implementation guides
        
        Args:
            guideline_name: Name of guideline
            
        Returns:
            Dictionary with extracted HTML content information
        """
        # Try different HTML endpoints
        html_urls = [
            f"http://build.fhir.org/ig/WorldHealthOrganization/smart-{guideline_name}/",
            f"https://worldhealthorganization.github.io/smart-{guideline_name}/"
        ]
        
        for url in html_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return self.parse_implementation_guide_html(response.text, url)
            except requests.RequestException:
                continue
        
        return None
    
    def parse_implementation_guide_html(self, html_content: str, source_url: str) -> Dict[str, Any]:
        """
        Parse HTML content to extract key information
        
        Args:
            html_content: Raw HTML content
            source_url: Source URL for reference
            
        Returns:
            Dictionary with parsed information
        """
        info = {
            'source_url': source_url,
            'title': 'Unknown Title',
            'version': 'Unknown Version',
            'description': '',
            'sections': [],
            'resources': [],
            'links': []
        }
        
        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if desc_match:
            info['description'] = desc_match.group(1).strip()
        
        # Extract version information
        version_patterns = [
            r'Version[:\s]+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
            r'version["\']?\s*[:=]\s*["\']?([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
            r'v([0-9]+\.[0-9]+(?:\.[0-9]+)?)'
        ]
        
        for pattern in version_patterns:
            version_match = re.search(pattern, html_content, re.IGNORECASE)
            if version_match:
                info['version'] = version_match.group(1)
                break
        
        # Extract section headings
        section_patterns = [
            r'<h[1-6][^>]*>([^<]+)</h[1-6]>',
            r'<div[^>]*class[^>]*header[^>]*>([^<]+)</div>'
        ]
        
        sections = set()
        for pattern in section_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                clean_section = re.sub(r'[^\w\s-]', '', match.strip())
                if len(clean_section) > 3 and len(clean_section) < 100:
                    sections.add(clean_section)
        
        info['sections'] = sorted(list(sections))[:10]  # Limit to first 10
        
        # Extract FHIR resource references
        fhir_patterns = [
            r'(StructureDefinition|ValueSet|CodeSystem|ConceptMap|ImplementationGuide)/([a-zA-Z0-9._-]+)',
            r'FHIR\s+([A-Z][a-zA-Z]+)\s*:?\s*([a-zA-Z0-9._-]+)?'
        ]
        
        resources = set()
        for pattern in fhir_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    resource_type, resource_id = match[0], match[1]
                    if resource_id:
                        resources.add(f"{resource_type}: {resource_id}")
        
        info['resources'] = sorted(list(resources))[:15]  # Limit to first 15
        
        # Extract useful links
        link_pattern = r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        links = re.findall(link_pattern, html_content, re.IGNORECASE)
        
        useful_links = []
        for href, text in links:
            clean_text = re.sub(r'\s+', ' ', text.strip())
            if (len(clean_text) > 3 and len(clean_text) < 50 and 
                any(keyword in clean_text.lower() for keyword in ['guide', 'resource', 'profile', 'example', 'download'])):
                useful_links.append({'url': href, 'text': clean_text})
        
        info['links'] = useful_links[:10]  # Limit to first 10
        
        return info
    
    def fetch_downloads_info(self, guideline_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch download information from the downloads.html page
        
        Args:
            guideline_name: Name of guideline
            
        Returns:
            Dictionary with download information
        """
        download_urls = [
            f"http://build.fhir.org/ig/WorldHealthOrganization/smart-{guideline_name}/downloads.html",
            f"https://worldhealthorganization.github.io/smart-{guideline_name}/downloads.html"
        ]
        
        for url in download_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return self.parse_downloads_html(response.text, url)
            except requests.RequestException:
                continue
        
        return None
    
    def parse_downloads_html(self, html_content: str, source_url: str) -> Dict[str, Any]:
        """
        Parse downloads HTML to extract available files
        
        Args:
            html_content: Raw HTML content
            source_url: Source URL for reference
            
        Returns:
            Dictionary with download information
        """
        downloads = {
            'source_url': source_url,
            'files': [],
            'formats': set(),
            'packages': []
        }
        
        # Find download links
        download_patterns = [
            r'<a[^>]*href=["\']([^"\']*\.(?:zip|tgz|tar\.gz|json|xml|xlsx))["\'][^>]*>([^<]+)</a>',
            r'<a[^>]*href=["\']([^"\']*(?:package|full|validation|definitions)[^"\']*)["\'][^>]*>([^<]+)</a>',
            r'href=["\']([^"\']*(?:downloads?|files?|exports?)[^"\']*)["\']'
        ]
        
        for pattern in download_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    url, description = match[0], match[1]
                    # Clean up the description
                    clean_desc = re.sub(r'\s+', ' ', description.strip())
                    if len(clean_desc) > 3:
                        file_ext = url.split('.')[-1].lower() if '.' in url else 'unknown'
                        downloads['files'].append({
                            'url': url,
                            'description': clean_desc,
                            'format': file_ext
                        })
                        downloads['formats'].add(file_ext)
        
        # Look for package references
        package_patterns = [
            r'(FHIR\s+(?:package|bundle|specification))',
            r'(Implementation\s+Guide\s+(?:package|bundle))',
            r'(NPM\s+package)',
            r'(Validation\s+pack)',
            r'(Full\s+specification)'
        ]
        
        for pattern in package_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            downloads['packages'].extend([match for match in matches if match])
        
        downloads['formats'] = list(downloads['formats'])
        return downloads


def main():
    """Main function demonstrating SMART Guidelines access"""
    
    print("WHO SMART Guidelines Explorer")
    print("=" * 40)
    
    # Initialize client
    smart_client = SMARTGuidelinesClient()
    
    # Available guidelines to explore
    guidelines = ['anc', 'base', 'immunizations', 'trust']
    
    print("\nFetching available SMART Guidelines...")
    
    for guideline in guidelines:
        print(f"\n--- {guideline.upper()} Guideline ---")
        
        # First get repository summary
        summary = smart_client.get_guideline_summary(guideline)
        print(f"Repository: {summary['description']}")
        if summary.get('updated_at'):
            print(f"Last updated: {summary['updated_at']}")
        
        # Check availability of different endpoints
        availability = smart_client.check_guideline_availability(guideline)
        accessible_endpoints = [name for name, info in availability.items() if info['accessible']]
        
        if accessible_endpoints:
            print(f"Available endpoints: {', '.join(accessible_endpoints)}")
            for name in accessible_endpoints:
                print(f"  - {name}: {availability[name]['url']}")
        
        # Try to fetch actual guideline data (JSON)
        guideline_data = smart_client.fetch_smart_guideline(guideline)
        
        if guideline_data:
            # Process DAK content from JSON
            dak_content = smart_client.process_dak_content(guideline_data)
            
            if dak_content:
                print(f"Title: {dak_content['title']}")
                print(f"Version: {dak_content['version']}")
                print(f"Status: {dak_content['status']}")
                print(f"Publisher: {dak_content['publisher']}")
                
                if dak_content['resources']:
                    print("Resources:")
                    for resource in dak_content['resources'][:3]:  # Show first 3
                        print(f"  - {resource['type']}: {resource['title']}")
                
                if dak_content['dependencies']:
                    print("Dependencies:")
                    for dep in dak_content['dependencies']:
                        print(f"  - {dep['uri']}")
        else:
            # Try to fetch HTML content instead
            print("Fetching HTML content...")
            html_content = smart_client.fetch_guideline_html(guideline)
            
            if html_content:
                print(f"Title: {html_content['title']}")
                print(f"Version: {html_content['version']}")
                print(f"Source: {html_content['source_url']}")
                
                if html_content['description']:
                    print(f"Description: {html_content['description']}")
                
                if html_content['sections']:
                    print("Key sections:")
                    for section in html_content['sections'][:5]:
                        print(f"  - {section}")
                
                if html_content['resources']:
                    print("FHIR resources found:")
                    for resource in html_content['resources'][:5]:
                        print(f"  - {resource}")
                
                if html_content['links']:
                    print("Useful links:")
                    for link in html_content['links'][:3]:
                        print(f"  - {link['text']}: {link['url']}")
                
                # Check for downloads
                downloads_info = smart_client.fetch_downloads_info(guideline)
                if downloads_info and downloads_info['files']:
                    print("Available downloads:")
                    for file_info in downloads_info['files'][:5]:
                        print(f"  - {file_info['description']} ({file_info['format']})")
                    if downloads_info['formats']:
                        print(f"Available formats: {', '.join(downloads_info['formats'])}")
            else:
                print("Could not access guideline content (JSON or HTML)")
                print("Manual web browser access required")
    
    # Demonstrate FHIR client usage (if available)
    if FHIR_CLIENT_AVAILABLE:
        print("\n--- FHIR Client Demo ---")
        try:
            patients = smart_client.search_patients()
            print(f"Found {len(patients)} patients in demo server")
            
            if patients:
                patient = patients[0]
                patient_id = patient.get('id', '')
                print(f"Sample patient ID: {patient_id}")
                
                # Get observations for this patient
                observations = smart_client.get_guideline_observations(f"Patient/{patient_id}")
                print(f"Found {len(observations)} observations for patient")
                
        except Exception as e:
            print(f"FHIR demo error: {e}")
    else:
        print("\n--- FHIR Client Not Available ---")
        print("Install fhirclient to enable FHIR server interaction:")
        print("pip install fhirclient")
    
    print("\n" + "=" * 40)
    print("Exploration complete!")


if __name__ == "__main__":
    main()