import os
import re
import pandas as pd

class ReportParser:
    """Class to handle parsing and saving incident reports."""

    SECTIONS = ['Summary', 'Impact', 'Detection', 'Timeline', 'Conclusions', 'Actionables']

    def __init__(self, input_dir="assignment_data", output_dir="parsed_data"):
        # Set up paths relative to the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_dir = os.path.join(base_dir, "..", input_dir)
        self.output_file = os.path.join(base_dir, "..", output_dir, "parsed_incident_reports.csv")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

    def parse_report(self, report, filename):
        """Extract structured data from a single Wikitext report."""
        data = {section: None for section in self.SECTIONS}  # Default to None for missing sections
        for section in self.SECTIONS:
            match = re.search(rf"=+\s*{section}\s*=+\s*(.*?)(?=\n=+|$)", report, re.S)
            data[section] = match.group(1).strip() if match else None
        
        data['Date'] = self.extract_date_from_filename(filename)
        data['Component'] = self.extract_component(data['Impact'])
        data['Symptom'] = self.extract_symptom(data['Impact'], data['Detection'])
        data['Service'] = self.extract_service(data['Impact'], data['Detection'])
        data['UserImpact'] = self.extract_user_impact(data)
        data['RootCauseCategory'] = self.extract_root_cause(data)
        data['Filename'] = filename

        return data

    def parse_all_reports(self):
        """Parse all Wikitext files in the input directory."""
        all_reports = []
        if not os.path.exists(self.input_dir):
            print(f"Error: Directory '{self.input_dir}' does not exist.")
            return pd.DataFrame()

        for filename in os.listdir(self.input_dir):
            if filename.endswith(".wikitext"):
                filepath = os.path.join(self.input_dir, filename)
                print(f"Processing file: {filepath}")
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        report = file.read()
                        parsed_data = self.parse_report(report, filename)
                        all_reports.append(parsed_data)
                except Exception as e:
                    print(f"Error reading file '{filename}': {e}")

        return pd.DataFrame(all_reports)

    def extract_component(self, impact):
        """Extract component from Impact section."""
        keywords = ['network', 'database', 'storage', 'kubernetes', 'load balancer',
                    'api', 'dns', 'cache', 'server', 'auth', 'filesystem', 'MediaWiki',
                    'caching', 'search', 'job queues & messaging', 'development tools' ]
        
        return self._extract_keyword(impact, keywords)

    def extract_symptom(self, impact, detection):
        """Extract symptom from Impact or Detection sections."""
        keywords = ['high latency', 'error rates', 'timeouts', 'service unavailable',
                    'failed connections', 'slow response', 'memory leaks', 'cpu spikes',
                    'disk usage', 'traffic surge', 'authentication failure', 'request drop', 
                    'service availability', 'user reports', 'database issues', 'monitoring', 'applications errors']
        
        return self._extract_keyword(impact or detection, keywords)

    def extract_service(self, impact, detection):
        """Extract service from Impact or Detection sections."""
        keywords = ['mediawiki', 'storage', 'networking', 'caching', 'api', 'cdn',
                    'search', 'database', 'analytics', 'logging', 'authentication', 
                    'wikidata', 'query services', 'cdn']
        
        return self._extract_keyword(impact or detection, keywords)

    def extract_user_impact(self, data):
        """Extract user impact from various sections."""
        for section in ['Impact', 'Detection', 'Summary']:
            if data.get(section):
                keywords = ['service disruption', 'downtime', 'error messages', 'slow performance',
                            'data loss', 'unresponsive', 'service unavailable', 'authentication failure']
                result = self._extract_keyword(data[section], keywords)
                if result:
                    return result
        return 'Unknown'

    def extract_root_cause(self, data):
        """Extract root cause category."""
        for section in ['Conclusions', 'Impact']:
            if data.get(section):
                keywords = ['API','network','connectivity','network','DNS','load balancing',
                            'configuration issues', 'network issue', 'database', 'traffic surge',
                            'software bug', 'resource exhaustion', 'authentication error', 
                            'hardware', 'security', 'cache','storage', 'hardware', 'DNS', 'provider']
                result = self._extract_keyword(data[section], keywords)
                if result:
                    return result
        return 'Unknown'

    def extract_date_from_filename(self, filename):
        """Extract date from the filename."""
        match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        return match.group(1) if match else None

    def _extract_keyword(self, text, keywords):
        """Utility to extract a keyword from text."""
        if text:
            for keyword in keywords:
                if re.search(rf'\b{keyword}\w*', text, re.I):
                    return keyword.capitalize()
        return 'Unknown'

    def save_to_csv(self, dataframe):
        """Save parsed data to a CSV file."""
        if dataframe.empty:
            print("No data to save. Check input files and directory path.")
        else:
            dataframe.to_csv(self.output_file, index=False)
            print(f"Parsing complete! Data saved to {self.output_file}")

    def run(self):
        """Execute the full parsing workflow."""
        print("Parsing reports...")
        df = self.parse_all_reports()
        self.save_to_csv(df)


# Run the script if executed directly
if __name__ == "__main__":
    parser = ReportParser()
    parser.run()
