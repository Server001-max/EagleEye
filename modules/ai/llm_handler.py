import ollama
import json
from typing import Dict, Any, Optional
from config.settings import Config

class LLMHandler:
    def __init__(self, model: str = Config.OLLAMA_MODEL):
        self.model = model
        self.client = ollama.Client(host=f'http://{Config.OLLAMA_HOST}:{Config.OLLAMA_PORT}')
    
    def analyze_target(self, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze target with local LLM via Ollama"""
        prompt = f"""
        You are an elite cybersecurity expert. Analyze this target and provide a detailed security assessment:
        
        Target: {target_data.get('target', 'Unknown')}
        Subdomains Found: {target_data.get('subdomains', [])}
        Open Ports: {target_data.get('open_ports', [])}
        Services Detected: {target_data.get('services', [])}
        
        Provide your analysis in valid JSON format with these exact fields:
        - "vulnerabilities": list of potential vulnerabilities with descriptions
        - "cves": list of relevant CVE IDs
        - "attack_vectors": list of possible attack vectors
        - "risk_score": integer from 1 to 10
        - "recommendations": list of security recommendations
        
        Return ONLY the JSON object, no other text.
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
                options={
                    'temperature': 0.5,
                    'top_k': 10,
                    'top_p': 0.9
                }
            )
            return self._parse_json_response(response['response'])
        except Exception as e:
            return {"error": f"Ollama error: {str(e)}", "vulnerabilities": [], "cves": [], "attack_vectors": [], "risk_score": 0, "recommendations": []}
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response"""
        try:
            # Remove markdown code blocks if present
            response = response.replace('```json', '').replace('```', '').strip()
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        return {
            "vulnerabilities": ["Unable to parse AI response"],
            "cves": [],
            "attack_vectors": [],
            "risk_score": 5,
            "recommendations": ["Check AI model output format"],
            "raw_response": response[:500]
        }
    
    def generate_exploit(self, vulnerability: str, target: str) -> str:
        """Generate exploit code using local LLM"""
        prompt = f"""
        Generate a Python proof-of-concept exploit code for:
        Vulnerability: {vulnerability}
        Target: {target}
        
        The code should be educational, include error handling, and show clear output.
        Return only the Python code, no explanations.
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
                options={
                    'temperature': 0.3
                }
            )
            return response['response']
        except Exception as e:
            return f"# Error generating exploit: {e}"
    
    def check_availability(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = self.client.generate(
                model=self.model,
                prompt="test",
                stream=False
            )
            return True
        except:
            return False
