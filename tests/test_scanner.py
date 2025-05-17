import pytest
from src.scanner import check_dependencies, check_code_quality, check_vulnerabilities
from src.policy_checker import PolicyChecker

class TestScanner:
    def test_dependency_check(self):
        result = check_dependencies()
        assert isinstance(result, dict)
        assert 'vulnerabilities' in result
    
    def test_code_quality_check(self):
        result = check_code_quality()
        assert isinstance(result, dict)
        assert 'issues' in result
    
    def test_vulnerability_check(self):
        result = check_vulnerabilities()
        assert isinstance(result, dict)
        assert all(k in result for k in ['critical', 'high', 'medium'])

class TestPolicyChecker:
    @pytest.fixture
    def checker(self):
        return PolicyChecker('config/policies.yaml', 'config/whitelist.yaml')
    
    def test_validate(self, checker):
        scan_results = {
            'dependencies': {'vulnerabilities': [
                {'id': 'CVE-2021-12345', 'severity': 'high'},
                {'id': 'CVE-2023-99999', 'severity': 'critical'}
            ]},
            'code_quality': {'issues': [1, 2, 3]}
        }
        
        violations = checker.validate(scan_results)
        assert any("CVE-2023-99999" in v for v in violations)
        assert not any("CVE-2021-12345" in v for v in violations)