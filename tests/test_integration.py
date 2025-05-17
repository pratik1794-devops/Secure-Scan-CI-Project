import pytest
from src.jenkins_integration import notify_jenkins
from src.report_generator import generate_report

class TestIntegration:
    @pytest.mark.skip(reason="Requires Jenkins environment")
    def test_jenkins_notification(self, monkeypatch):
        monkeypatch.setenv('JENKINS_URL', 'http://jenkins.example.com')
        monkeypatch.setenv('JENKINS_USER', 'admin')
        monkeypatch.setenv('JENKINS_TOKEN', 'token')
        monkeypatch.setenv('BUILD_NUMBER', '1')
        monkeypatch.setenv('JOB_NAME', 'test-job')
        
        assert notify_jenkins("test_report.pdf", True)
    
    def test_report_generation(self, tmp_path):
        scan_results = {
            'dependencies': {'vulnerabilities': []},
            'code_quality': {'issues': []},
            'vulnerabilities': {'critical': 0, 'high': 0, 'medium': 0}
        }
        
        # Test PDF generation
        pdf_path = generate_report(scan_results, [], 'pdf')
        assert pdf_path.endswith('.pdf')
        
        # Test JSON generation
        json_path = generate_report(scan_results, [], 'json')
        assert json_path.endswith('.json')