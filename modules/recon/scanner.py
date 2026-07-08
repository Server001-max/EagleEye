import socket
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from config.settings import Config

class PortScanner:
    def __init__(self, target: str):
        self.target = target
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 
                            443, 445, 993, 995, 1723, 3306, 3389, 5432, 
                            5900, 6379, 8080, 8443, 9000, 27017]
        self.open_ports = []
    
    def scan_port(self, port: int) -> Dict[str, Any]:
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                return {
                    'port': port,
                    'status': 'open',
                    'service': service
                }
        except:
            pass
        return None
    
    def get_service_name(self, port: int) -> str:
        """Get service name from port number"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 135: 'RPC', 139: 'NetBIOS', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S', 1723: 'PPTP',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC',
            6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 9000: 'PHP-FPM',
            27017: 'MongoDB'
        }
        return services.get(port, 'Unknown')
    
    def scan(self) -> List[Dict[str, Any]]:
        """Scan all common ports"""
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            results = list(tqdm(
                executor.map(self.scan_port, self.common_ports),
                total=len(self.common_ports),
                desc="Scanning Ports"
            ))
        
        self.open_ports = [r for r in results if r is not None]
        return self.open_ports
    
    def scan_ports(self, ports: List[int]) -> List[Dict[str, Any]]:
        """Scan specific ports"""
        results = []
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            future_to_port = {executor.submit(self.scan_port, port): port for port in ports}
            for future in tqdm(as_completed(future_to_port), total=len(ports), desc="Scanning Custom Ports"):
                result = future.result()
                if result:
                    results.append(result)
        return results
