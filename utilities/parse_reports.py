import os
import re
import pandas as pd

# Define sections to extract
SECTIONS = ['Summary', 'Impact', 'Detection', 'Timeline', 'Conclusions', 'Actionables']

def parse_report(report, filename):
    """Extract structured data from a single Wikitext report."""
    data = {section: None for section in SECTIONS}  # Default to None for missing sections
    for section in SECTIONS:
        match = re.search(rf"=+\s*{section}\s*=+\s*(.*?)(?=\n=+|$)", report, re.S)
        if match:
            data[section] = match.group(1).strip()
            print(f"Section '{section}' found.")
        else:
            print(f"Section '{section}' not found in this report.")
    
    # Extract date from filename
    data['Date'] = extract_date_from_filename(filename)

    # Extract component from Impact section
    if data['Impact']:
        data['Component'] = extract_component_from_impact(data['Impact'])
    else:
        data['Component'] = 'Unknown'

    # Extract symptom from Impact or Detection sections
    if data['Impact']:
        data['Symptom'] = extract_symptom_from_impact_or_detection(data['Impact'])
    elif data['Detection']:
        data['Symptom'] = extract_symptom_from_impact_or_detection(data['Detection'])
    else:
        data['Symptom'] = 'Unknown'

    # Extract service from Impact or Detection sections
    if data['Impact']:
        data['Service'] = extract_service_from_impact_or_detection(data['Impact'])
    elif data['Detection']:
        data['Service'] = extract_service_from_impact_or_detection(data['Detection'])
    else:
        data['Service'] = 'Unknown'

    # Extract user impact from Impact, Detection, or Summary sections
    if data['Impact']:
        data['UserImpact'] = extract_user_impact(data['Impact'])
    elif data['Detection']:
        data['UserImpact'] = extract_user_impact(data['Detection'])
    elif data['Summary']:
        data['UserImpact'] = extract_user_impact(data['Summary'])
    else:
        data['UserImpact'] = 'Unknown'

    # Extract root cause category from Conclusions or Impact sections
    if data['Conclusions']:
        data['RootCauseCategory'] = extract_root_cause_category(data['Conclusions'])
    elif data['Impact']:
        data['RootCauseCategory'] = extract_root_cause_category(data['Impact'])
    else:
        data['RootCauseCategory'] = 'Unknown'

    return data

def extract_component_from_impact(impact_text):
    """Extract component or root cause from the Impact section."""
    component_keywords = [
        'network', 'database', 'storage', 'kubernetes', 'load balancer',
        'api', 'dns', 'cache', 'server', 'auth', 'filesystem', 'MediaWiki',
        'caching', 'search', 'job queues & messaging', 'development tools' 
    ]
    for keyword in component_keywords:
        if re.search(rf'\b{keyword}\w*', impact_text, re.I):  # Allow partial matches
            return keyword.capitalize()
    return 'Unknown'

def extract_symptom_from_impact_or_detection(text):
    """Extract symptom information from the Impact or Detection section."""
    symptom_keywords = [
        'high latency', 'error rates', 'timeouts', 'service unavailable',
        'failed connections', 'slow response', 'memory leaks', 'cpu spikes',
        'disk usage', 'traffic surge', 'authentication failure', 'request drop', 
        'service availability', 'user reports', 'database issues', 'monitoring', 'applications errors'
    ]
    for keyword in symptom_keywords:
        if re.search(rf'\b{keyword}\w*', text, re.I):  # Allow partial matches
            return keyword.capitalize()
    return 'Unknown'

def extract_service_from_impact_or_detection(text):
    """Extract service information from the Impact or Detection section."""
    service_keywords = [
        'mediawiki', 'storage', 'networking', 'caching', 'api', 'cdn',
        'search', 'database', 'analytics', 'logging', 'authentication', 
        'wikidata', 'query services', 'cdn'
    ]
    for keyword in service_keywords:
        if re.search(rf'\b{keyword}\w*', text, re.I):  # Allow partial matches
            return keyword.capitalize()
    return 'Unknown'

def extract_user_impact(text):
    """Extract user impact information from relevant sections."""
    user_impact_keywords = [
        'service disruption', 'downtime', 'error messages', 'slow performance',
        'data loss', 'unresponsive', 'service unavailable', 'authentication failure'
    ]
    for keyword in user_impact_keywords:
        if re.search(rf'\b{keyword}\w*', text, re.I):  # Allow partial matches
            return keyword.capitalize()
    return 'Unknown'

def extract_date_from_filename(filename):
    """Extract date from filename."""
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    return None

def extract_root_cause_category(text):
    """Extract root cause category from relevant sections."""
    root_cause_keywords = [
        'configuration errors', 'network issue', 'database failure', 'traffic surge',
        'software bug', 'resource exhaustion', 'authentication error', 
        'hardware failure', 'security breach', 'cache miss', 'software bugs' , 'storage issues',
        'hardware failures'
    ]
    for keyword in root_cause_keywords:
        if re.search(rf'\b{keyword}\w*', text, re.I):  # Allow partial matches
            return keyword.capitalize()
    return 'Unknown'  # Default if no root cause is found

def parse_all_reports(directory):
    """Parse all Wikitext files in a given directory."""
    all_reports = []
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return pd.DataFrame()

    for filename in os.listdir(directory):
        if filename.endswith(".wikitext"):
            filepath = os.path.join(directory, filename)
            print(f"Processing file: {filepath}")
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    report = file.read()
                    parsed_data = parse_report(report, filename)
                    parsed_data['Filename'] = filename
                    all_reports.append(parsed_data)
            except Exception as e:
                print(f"Error reading file '{filename}': {e}")
    
    return pd.DataFrame(all_reports)

def main():
    """Main function to execute the script."""
    #directory = "assignment_data/"  # Adjust to your directory path
    #output_file = "parsed_data/parsed_incident_reports.csv"
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct paths relative to the script's location
    input_directory = os.path.join(base_dir, "..", "assignment_data")
    output_file = os.path.join(base_dir, "..", "parsed_data", "parsed_incident_reports.csv")
    
    # Check if input directory exists
    if not os.path.exists(input_directory):
        print(f"Error: Directory '{input_directory}' does not exist.")
        return
    
    print("Parsing reports...")
    df = parse_all_reports(input_directory)
    
    if df.empty:
        print("No data was parsed. Check the input files and directory path.")
    else:
        print("Saving parsed data to CSV...")
        df.to_csv(output_file, index=False)
        print(f"Parsing complete! Data saved to {output_file}")

# Run the script only if executed directly
if __name__ == "__main__":
    main()
