import os
import jenkins

def notify_jenkins(report_path, scan_passed):
    """Send scan results to Jenkins"""
    try:
        server_url = os.getenv('JENKINS_URL')
        username = os.getenv('JENKINS_USER')
        password = os.getenv('JENKINS_TOKEN')
        
        if not all([server_url, username, password]):
            return False
            
        server = jenkins.Jenkins(server_url, username=username, password=password)
        build_number = os.getenv('BUILD_NUMBER')
        job_name = os.getenv('JOB_NAME')
        
        if build_number and job_name:
            server.set_build_result(
                job_name,
                int(build_number),
                'SUCCESS' if scan_passed else 'UNSTABLE',
                f'Security scan {"passed" if scan_passed else "failed"}. Report: {report_path}'
            )
            return True
    except Exception as e:
        print(f"Jenkins notification failed: {str(e)}")
    
    return False