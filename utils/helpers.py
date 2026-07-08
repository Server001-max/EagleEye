import requests
import re
from typing import List, Dict, Any
import json
import hashlib
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from config.settings import Config

class Helpers:
    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract domain from URL"""
        pattern = r'(?:https?://)?(?:www\.)?([^/]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else url
    
    @staticmethod
    def safe_request(url: str, timeout: int = 10) -> Dict[str, Any]:
        """Safe HTTP request with error handling"""
        try:
            headers = {
                'User-Agent': Config.USER_AGENT
            }
            response = requests.get(url, headers=headers, timeout=timeout, verify=False)
            return {
                'url': url,
                'status_code': response.status_code,
                'content': response.text[:5000]
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e)
            }
    
    @staticmethod
    def hash_text(text: str) -> str:
        """Hash text for secure storage"""
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    @staticmethod
    def extract_links(html: str) -> List[str]:
        """Extract all links from HTML"""
        pattern = r'href=[\'"]?([^\'" >]+)'
        return re.findall(pattern, html)
    
    @staticmethod
    def extract_parameters(url: str) -> Dict[str, List[str]]:
        """Extract URL parameters"""
        parsed = urlparse(url)
        return parse_qs(parsed.query)
    
    @staticmethod
    def create_report_header(target: str, timestamp: str) -> str:
        """Create report header"""
        return f"""
╔═══════════════════════════════════════════════════════════╗
║                    🦅 EAGLEEYE REPORT                    ║
╠═══════════════════════════════════════════════════════════╣
║  Target: {target:<56}║
║  Time:   {timestamp:<56}║
╚═══════════════════════════════════════════════════════════╝
        """
    
    @staticmethod
    def is_url_valid(url: str) -> bool:
        """Check if URL is valid"""
        try:
            response = requests.head(url, timeout=5, verify=False)
            return response.status_code < 400
        except:
            return False
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{int(minutes)}m {int(secs)}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{int(hours)}h {int(minutes)}m"
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp for reports"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
