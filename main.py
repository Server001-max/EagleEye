#!/usr/bin/env python3
"""
🦅 EagleEye - Autonomous AI Pentesting Framework
A powerful automated security testing tool powered by local LLMs
"""

import sys
import argparse
import time
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from utils.helpers import Helpers
from modules.recon import SubdomainFinder, PortScanner
from modules.ai import LLMHandler, ExploitGenerator
from modules.exploit import SQLInjectionExploit, XSSExploit
from modules.report import ReportGenerator
from config.settings import Config

# Initialize colorama
init(autoreset=True)
console = Console()

def print_banner():
    """Print the EagleEye banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗  ██████╗  ██████╗ ██╗     ███████╗██╗   ██╗  ║
║   ██╔════╝ ██╔════╝ ██╔════╝ ██║     ██╔════╝╚██╗ ██╔╝  ║
║   █████╗   ██║  ███╗██║  ███╗██║     █████╗   ╚████╔╝   ║
║   ██╔══╝   ██║   ██║██║   ██║██║     ██╔══╝    ╚██╔╝    ║
║   ███████╗ ╚██████╔╝╚██████╔╝███████╗███████╗   ██║     ║
║   ╚══════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝     ║
║                                                           ║
║        Autonomous AI Pentesting Framework v1.0           ║
╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("🔒 For authorized security testing only", style="bold yellow")
    console.print("⚠️  Use responsibly and ethically\n", style="bold red")

def check_ollama():
    """Check if Ollama is running and model is available"""
    console.print("[*] Checking Ollama availability...", style="yellow")
    handler = LLMHandler()
    
    if handler.check_availability():
        console.print(f"[+] Ollama is running with model: {Config.OLLAMA_MODEL}", style="green")
        return True
    else:
        console.print("[!] Ollama not available!", style="red")
        console.print("[!] Please install Ollama and pull the model:", style="yellow")
        console.print("    curl -fsSL https://ollama.com/install.sh | sh")
        console.print(f"    ollama pull {Config.OLLAMA_MODEL}")
        console.print("    ollama serve")
        return False

def run_recon(target: str) -> dict:
    """Run reconnaissance phase"""
    console.print("\n[+] Phase 1: Reconnaissance", style="bold blue")
    
    results = {
        'subdomains': [],
        'open_ports': []
    }
    
    # Extract domain
    domain = Helpers.extract_domain(target)
    console.print(f"[*] Target Domain: {domain}", style="cyan")
    
    # Subdomain enumeration
    console.print("[*] Enumerating subdomains...", style="cyan")
    finder = SubdomainFinder(domain)
    subdomains = finder.find()
    results['subdomains'] = subdomains
    
    if subdomains:
        console.print(f"[+] Found {len(subdomains)} subdomains", style="green")
        for sub in subdomains[:10]:
            console.print(f"    - {sub}")
        if len(subdomains) > 10:
            console.print(f"    ... and {len(subdomains) - 10} more")
    else:
        console.print("[!] No subdomains found", style="yellow")
    
    # Port scanning
    console.print("[*] Scanning for open ports...", style="cyan")
    scanner = PortScanner(target)
    ports = scanner.scan()
    results['open_ports'] = ports
    
    if ports:
        console.print(f"[+] Found {len(ports)} open ports", style="green")
        for port in ports[:10]:
            console.print(f"    - {port.get('port')}: {port.get('service')}")
        if len(ports) > 10:
            console.print(f"    ... and {len(ports) - 10} more")
    else:
        console.print("[!] No open ports found", style="yellow")
    
    return results

def run_ai_analysis(target: str, recon_results: dict) -> dict:
    """Run AI analysis phase"""
    console.print("\n[+] Phase 2: AI Analysis", style="bold blue")
    
    # Prepare data for AI
    target_data = {
        'target': target,
        'subdomains': recon_results.get('subdomains', []),
        'open_ports': [p.get('port') for p in recon_results.get('open_ports', [])],
        'services': [p.get('service') for p in recon_results.get('open_ports', [])]
    }
    
    # Initialize AI handler
    handler = LLMHandler()
    console.print("[*] Analyzing target with AI...", style="cyan")
    
    analysis = handler.analyze_target(target_data)
    
    if 'error' in analysis:
        console.print(f"[!] AI Analysis error: {analysis['error']}", style="red")
        return {}
    
    console.print("[+] AI Analysis complete", style="green")
    
    # Display AI results
    if 'vulnerabilities' in analysis:
        console.print("\n[bold cyan]Potential Vulnerabilities:[/bold cyan]")
        for vuln in analysis.get('vulnerabilities', []):
            console.print(f"  - {vuln}")
    
    if 'cves' in analysis:
        console.print("\n[bold cyan]Related CVEs:[/bold cyan]")
        for cve in analysis.get('cves', []):
            console.print(f"  - {cve}")
    
    if 'risk_score' in analysis:
        risk = analysis.get('risk_score')
        color = "green" if risk <= 3 else "yellow" if risk <= 7 else "red"
        console.print(f"\n[bold]Risk Score:[/bold] [{color}]{risk}/10[/{color}]")
    
    if 'recommendations' in analysis:
        console.print("\n[bold cyan]Recommendations:[/bold cyan]")
        for rec in analysis.get('recommendations', []):
            console.print(f"  - {rec}")
    
    return analysis

def run_exploit_scan(target: str) -> dict:
    """Run exploit scanning phase"""
    console.print("\n[+] Phase 3: Exploit Scanning", style="bold blue")
    
    results = {
        'sqli': {},
        'xss': {}
    }
    
    # SQL Injection testing
    console.print("[*] Testing for SQL Injection...", style="cyan")
    sqli = SQLInjectionExploit(target)
    sqli_results = sqli.scan()
    results['sqli'] = sqli_results
    
    if sqli_results.get('vulnerable'):
        console.print("[!] SQL Injection vulnerability detected!", style="red")
        for result in sqli_results.get('results', []):
            if result.get('vulnerable'):
                console.print(f"    - Parameter: {result.get('parameter')}")
                console.print(f"      Payload: {result.get('payload')}")
    else:
        console.print("[+] No SQL Injection found", style="green")
    
    # XSS testing
    console.print("[*] Testing for XSS...", style="cyan")
    xss = XSSExploit(target)
    xss_results = xss.scan()
    results['xss'] = xss_results
    
    if xss_results.get('vulnerable'):
        console.print("[!] XSS vulnerability detected!", style="red")
        for result in xss_results.get('results', []):
            if result.get('vulnerable'):
                console.print(f"    - Parameter: {result.get('parameter')}")
                console.print(f"      Payload: {result.get('payload')}")
    else:
        console.print("[+] No XSS found", style="green")
    
    return results

def generate_report(target: str, recon_results: dict, ai_analysis: dict, exploit_results: dict):
    """Generate final report"""
    console.print("\n[+] Phase 4: Report Generation", style="bold blue")
    
    report = ReportGenerator(target)
    
    # Add all findings
    report.add_subdomains(recon_results.get('subdomains', []))
    report.add_ports(recon_results.get('open_ports', []))
    
    # Add vulnerabilities
    vulns = []
    if exploit_results.get('sqli', {}).get('vulnerable'):
        vulns.append("SQL Injection")
    if exploit_results.get('xss', {}).get('vulnerable'):
        vulns.append("XSS")
    report.add_vulnerabilities(vulns)
    
    # Add AI analysis
    report.add_ai_analysis(ai_analysis)
    
    # Add exploit code if vulnerabilities found
    if vulns:
        generator = ExploitGenerator()
        for vuln in vulns:
            exploit = generator.generate_payload(vuln.lower(), target)
            report.add_exploit(exploit)
    
    # Save report
    txt_file = report.save_report('txt')
    json_file = report.save_report('json')
    
    console.print(f"[+] Report saved to: {txt_file}", style="green")
    console.print(f"[+] JSON report saved to: {json_file}", style="green")
    
    # Print summary
    print_summary(report)

def print_summary(report):
    """Print a summary of findings"""
    data = report.data
    
    console.print("\n" + "=" * 60, style="bold cyan")
    console.print("📊 SCAN SUMMARY", style="bold white")
    console.print("=" * 60, style="bold cyan")
    
    # Create summary table
    table = Table(title="EagleEye Scan Results")
    table.add_column("Category", style="cyan")
    table.add_column("Findings", style="white")
    
    sub_count = len(data.get('subdomains', []))
    port_count = len(data.get('open_ports', []))
    vuln_count = len(data.get('vulnerabilities', []))
    
    table.add_row("Subdomains Found", str(sub_count))
    table.add_row("Open Ports", str(port_count))
    table.add_row("Vulnerabilities", f"[{'red' if vuln_count > 0 else 'green'}]{vuln_count}[/{'red' if vuln_count > 0 else 'green'}]")
    
    if data.get('ai_analysis', {}).get('risk_score'):
        risk = data['ai_analysis']['risk_score']
        color = "green" if risk <= 3 else "yellow" if risk <= 7 else "red"
        table.add_row("Risk Score", f"[{color}]{risk}/10[/{color}]")
    
    console.print(table)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="EagleEye - Autonomous AI Pentesting Framework",
        epilog="Example: python main.py -t https://example.com"
    )
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target URL or IP address to scan'
    )
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Skip AI analysis phase'
    )
    parser.add_argument(
        '--output',
        choices=['txt', 'json', 'both'],
        default='both',
        help='Output format for reports'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check Ollama
    if not args.no_ai:
        if not check_ollama():
            console.print("[!] Continuing without AI analysis", style="yellow")
            args.no_ai = True
    
    try:
        start_time = time.time()
        
        # Phase 1: Reconnaissance
        recon_results = run_recon(args.target)
        
        # Phase 2: AI Analysis
        ai_analysis = {}
        if not args.no_ai:
            ai_analysis = run_ai_analysis(args.target, recon_results)
        
        # Phase 3: Exploit Scanning
        exploit_results = run_exploit_scan(args.target)
        
        # Phase 4: Report Generation
        generate_report(args.target, recon_results, ai_analysis, exploit_results)
        
        # Completion
        elapsed = time.time() - start_time
        console.print(f"\n[+] Scan completed in {Helpers.format_duration(elapsed)}", style="bold green")
        console.print("[+] Thank you for using EagleEye! 🦅", style="bold cyan")
        
    except KeyboardInterrupt:
        console.print("\n[!] Scan interrupted by user", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[!] Error: {str(e)}", style="red")
        sys.exit(1)

if __name__ == "__main__":
    main()
