from fpdf import FPDF
from datetime import datetime
import json
import os

SEVERITY_COLORS = {
    "CRITICAL": (220, 53, 69),
    "HIGH":     (255, 128, 0),
    "MEDIUM":   (255, 193, 7),
    "NONE":     (40, 167, 69),
    "N/A":      (150, 150, 150),
}

class RedTeamReport(FPDF):
    def header(self):
        self.set_font("Helvetica","B",10)
        self.set_text_color(100,100,100)
        self.cell(0,8,"LLM RED TEAM REPORT - CONFIDENTIAL",align="R",new_x="LMARGIN",new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica","",8)
        self.set_text_color(150,150,150)
        self.cell(0,8,f"Page {self.page_no()} | Generated {datetime.now().strftime('%Y-%m-%d')}",align="C")

def generate_pdf(results, output_path):
    pdf = RedTeamReport()
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=15)

    # Title
    pdf.set_font("Helvetica","B",20)
    pdf.set_text_color(30,30,30)
    pdf.cell(0,12,"LLM Security Assessment Report",new_x="LMARGIN",new_y="NEXT")
    pdf.set_font("Helvetica","",11)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,7,f"Target: VulnBot (AcmeCorp Customer Support AI)",new_x="LMARGIN",new_y="NEXT")
    pdf.cell(0,7,f"Date: {datetime.now().strftime('%B %d, %Y')}",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(6)

    # Summary stats
    total = len(results)
    vuln  = sum(1 for r in results if r.get("verdict")=="VULNERABLE")
    part  = sum(1 for r in results if r.get("verdict")=="PARTIAL")
    passed= sum(1 for r in results if r.get("verdict")=="PASS")
    score = int((passed / max(total,1)) * 100)

    pdf.set_font("Helvetica","B",13)
    pdf.set_text_color(30,30,30)
    pdf.cell(0,10,"Executive Summary",new_x="LMARGIN",new_y="NEXT")
    pdf.set_font("Helvetica","",11)
    pdf.set_text_color(60,60,60)
    pdf.multi_cell(0,7,
        f"This automated red team assessment fired {total} adversarial payloads across 3 attack "
        f"categories (prompt injection, data extraction, jailbreak). The target model demonstrated "
        f"a security score of {score}%. {vuln} critical vulnerabilities were confirmed, "
        f"{part} partial bypasses detected, and {passed} attacks were successfully blocked."
    )
    pdf.ln(5)

    # Results table
    pdf.set_font("Helvetica","B",13)
    pdf.set_text_color(30,30,30)
    pdf.cell(0,10,"Detailed Findings",new_x="LMARGIN",new_y="NEXT")

    # Table header
    pdf.set_fill_color(240,240,240)
    pdf.set_font("Helvetica","B",9)
    pdf.cell(15,8,"#",border=1,fill=True)
    pdf.cell(30,8,"Category",border=1,fill=True)
    pdf.cell(85,8,"Payload (truncated)",border=1,fill=True)
    pdf.cell(25,8,"Verdict",border=1,fill=True)
    pdf.cell(25,8,"Severity",border=1,fill=True,new_x="LMARGIN",new_y="NEXT")

    pdf.set_font("Helvetica","",8)
    for i, r in enumerate(results):
        if pdf.get_y() > 260:
            pdf.add_page()
        sev   = r.get("severity","N/A")
        col   = SEVERITY_COLORS.get(sev, (150,150,150))
        pdf.set_text_color(30,30,30)
        pdf.cell(15,7,str(i+1),border=1)
        pdf.cell(30,7,r.get("category","")[:18],border=1)
        
        # safely encode payload to avoid latin-1 unicode errors in fpdf
        payload_text = r.get("payload","")[:55].encode('latin-1', 'replace').decode('latin-1') + "..."
        pdf.cell(85,7,payload_text,border=1)
        
        verdict = r.get("verdict","")
        pdf.set_text_color(*col)
        pdf.cell(25,7,verdict,border=1)
        pdf.cell(25,7,sev,border=1,new_x="LMARGIN",new_y="NEXT")
        pdf.set_text_color(30,30,30)

    # Make absolute path to ensure saving succeeds
    abs_path = os.path.abspath(output_path)
    # Ensure dir exists
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    
    pdf.output(abs_path)
    print(f"[+] PDF report saved to {abs_path}")