from reportlab.pdfgen import canvas
import json
from datetime import datetime

def generate_report(scan_results, violations, format='pdf'):
    """Generate report in specified format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format.lower() == 'json':
        report_path = f'reports/scan_report_{timestamp}.json'
        with open(report_path, 'w') as f:
            json.dump({
                'scan_results': scan_results,
                'violations': violations,
                'timestamp': timestamp
            }, f, indent=2)
    else:
        report_path = f'reports/scan_report_{timestamp}.pdf'
        generate_pdf_report(report_path, scan_results, violations)
    
    return report_path

def generate_pdf_report(path, scan_results, violations):
    """Generate PDF report using ReportLab"""
    c = canvas.Canvas(path)
    
    # Report header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Security Scan Report")
    
    # Scan summary
    c.setFont("Helvetica", 12)
    y_position = 750
    c.drawString(100, y_position, "Scan Summary:")
    y_position -= 20
    
    for category, results in scan_results.items():
        c.drawString(120, y_position, f"{category.capitalize()}:")
        y_position -= 15
        for key, value in results.items():
            c.drawString(140, y_position, f"{key}: {value}")
            y_position -= 15
        y_position -= 10
    
    # Violations section
    if violations:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, "Policy Violations Detected!")
        y_position -= 20
        c.setFont("Helvetica", 10)
        for violation in violations:
            c.drawString(120, y_position, f"- {violation}")
            y_position -= 15
    
    c.save()