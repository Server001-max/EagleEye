import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Local AI Settings (Ollama)
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
    OLLAMA_PORT = os.getenv('OLLAMA_PORT', 11434)
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:7b')
    
    # Attack Settings
    MAX_THREADS = 10
    TIMEOUT = 10
    USER_AGENT = "EagleEye/1.0 (Security Research)"
    
    # Report Settings
    REPORT_DIR = "reports/"
    LOG_LEVEL = "INFO"
    
    # Recon Settings
    SUBDOMAIN_WORDLIST = [
        "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", 
        "webdisk", "ns2", "cpanel", "whm", "autodiscover", "autoconfig", 
        "m", "imap", "test", "ns", "blog", "pop3", "dev", "www2", "admin", 
        "forum", "news", "vpn", "ns3", "mail2", "new", "mysql", "old", 
        "lists", "support", "mobile", "mx", "static", "docs", "beta", 
        "shop", "sql", "secure", "demo", "cp", "calendar", "wiki", "web", 
        "media", "email", "images", "img", "download", "dns", "piwik", 
        "stats", "dashboard", "portal", "manage", "start", "info", "apps", 
        "video", "srv", "app", "server", "ftp2", "chat", "api", "cdn", 
        "files", "crm", "site", "store"
    ]
