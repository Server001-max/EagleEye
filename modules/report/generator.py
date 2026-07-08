import json
import os
from datetime import datetime
from typing import Dict, Any, List
from utils.helpers import Helpers
from config.settings import Config

class ReportGenerator:
    def __init__(self, target: str):
        self.target = target
        self.timestamp = Helpers.get_timestamp()
        self.data = {
            'target': target,
            'timestamp': self.timestamp,
            'subdomains': [],
            'open_ports': [],
            'vulnerabilities': [],
            'ai_analysis': {},
            'exploits': []
        }
    
    def add_subdomains(self, subdomains: List[str]):
        """Add subdomain findings to report"""
        self.data['subdomains'] = subdomains
    
    def add_ports(self, ports: List[Dict[str, Any]]):
        """Add port scan findings to report"""
        self.data['open_ports'] = ports
    
    def add_vulnerabilities(self, vulns: List[Dict[str, Any]]):
        """Add vulnerability findings to report"""
        self.data['vulnerabilities'] = vulns
    
    def add_ai_analysis(self, analysis: Dict[str, Any]):
        """Add AI analysis to report"""
        self.data['ai_analysis'] = analysis
    
    def add_exploit(self, exploit: str):
        """Add generated exploit to report"""
        self.data['exploits'].append(exploit)
    
    def generate_text_report(self) -> str:
        """Generate a text report"""
        report = Helpers.create_report_header(self.target, self.timestamp)
        report += "\n"
        
        # Subdomains
        report += "═══ SUBDOMAINS ═══\n"
        if self.data['subdomains']:
            for sub in self.data['subdomains']:
                report += f"  - {sub}\n"
        else:
            report += "  No subdomains found\n"
        report += "\n"
        
        # Open Ports
        report += "═══ OPEN PORTS ═══\n"
        if self.data['open_ports']:
            for port in self.data['open_ports']:
                report += f"  - {port.get('port')}: {port.get('service')} (open)\n"
        else:
            report += "  No open ports found\n"
        report += "\n"
        
        # Vulnerabilities
        report += "═══ VULNERABILITIES ═══\n"
        if self.data['vulnerabilities']:
            for vuln in self.data['vulnerabilities']:
                report += f"  - {vuln}\n"
        else:
            report += "  No vulnerabilities found\n"
        report += "\n"
        
        # AI Analysis
        report += "═══ AI ANALYSIS ═══\n"
        if self.data['ai_analysis']:
            analysis = self.data['ai_analysis']
            if 'vulnerabilities' in analysis:
                report += "  Potential Vulnerabilities:\n"
                for vuln in analysis.get('vulnerabilities', []):
                    report += f"    - {vuln}\n"
            if 'cves' in analysis:
                report += "  Related CVEs:\n"
                for cve in analysis.get('cves', []):
                    report += f"    - {cve}\n"
            if 'risk_score' in analysis:
                report += f"  Risk Score: {analysis.get('risk_score')}/10\n"
            if 'recommendations' in analysis:
                report += "  Recommendations:\n"
                for rec in analysis.get('recommendations', []):
                    report += f"    - {rec}\n"
        else:
            report += "  No AI analysis available\n"
        report += "\n"
        
        return report
    
    def generate_json_report(self) -> str:
        """Generate a JSON report"""
        return json.dumps(self.data, indent=2)
    
    def save_report(self, format: str = 'txt') -> str:
        """Save report to file"""
        os.makedirs(Config.REPORT_DIR, exist_ok=True)
        filename = f"{Config.REPORT_DIR}/report_{self.target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format == 'txt':
            content = self.generate_text_report()
            filename += '.txt'
        elif format == 'json':
            content = self.generate_json_report()
            filename += '.json'
        else:
            content = self.generate_text_report()
            filename += '.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
