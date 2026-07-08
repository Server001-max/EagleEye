import socket
import dns.resolver
from typing import List, Set, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config.settings import Config

class SubdomainFinder:
    def __init__(self, domain: str):
        self.domain = domain
        self.wordlist = Config.SUBDOMAIN_WORDLIST
        self.subdomains: Set[str] = set()
        self.resolved_ips: Dict[str, str] = {}
    
    def check_subdomain(self, sub: str) -> bool:
        """Check if subdomain exists"""
        try:
            full_domain = f"{sub}.{self.domain}"
            ip = socket.gethostbyname(full_domain)
            self.resolved_ips[full_domain] = ip
            return True
        except:
            return False
    
    def find(self) -> List[str]:
        """Find all subdomains"""
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            results = list(tqdm(
                executor.map(self.check_subdomain, self.wordlist),
                total=len(self.wordlist),
                desc="Scanning Subdomains"
            ))
        
        for sub, exists in zip(self.wordlist, results):
            if exists:
                self.subdomains.add(f"{sub}.{self.domain}")
        
        return list(self.subdomains)
    
    def resolve_ip(self, subdomain: str) -> str:
        """Get IP of subdomain"""
        return self.resolved_ips.get(subdomain, "N/A")
    
    def get_all_with_ips(self) -> Dict[str, str]:
        """Get all subdomains with their IPs"""
        return {sub: self.resolved_ips.get(sub, "N/A") for sub in self.subdomains}
