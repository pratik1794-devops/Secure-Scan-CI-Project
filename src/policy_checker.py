import yaml

class PolicyChecker:
    def __init__(self, policy_file='config/policies.yaml', whitelist_file='config/whitelist.yaml'):
        with open(policy_file, 'r') as f:
            self.policies = yaml.safe_load(f)
        
        with open(whitelist_file, 'r') as f:
            self.whitelist = yaml.safe_load(f) or {}
    
    def validate(self, scan_results):
        violations = []
        
        # Check dependency vulnerabilities
        if 'dependencies' in scan_results:
            max_severity = self.policies.get('max_severity', 'high')
            allowed_cves = self.whitelist.get('cves', [])
            
            for vuln in scan_results['dependencies'].get('vulnerabilities', []):
                if vuln['id'] not in allowed_cves and vuln['severity'].lower() >= max_severity:
                    violations.append(f"Critical vulnerability found: {vuln['id']}")
        
        # Check code quality thresholds
        if 'code_quality' in scan_results:
            max_issues = self.policies.get('max_issues', 0)
            current_issues = len(scan_results['code_quality'].get('issues', []))
            
            if current_issues > max_issues:
                violations.append(f"Code quality issues exceed threshold: {current_issues}/{max_issues}")
        
        return violations