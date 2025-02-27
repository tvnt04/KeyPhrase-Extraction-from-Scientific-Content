import pdfkit

def create_pdf(phrases):
    """Generates a PDF report of extracted keyphrases and POS tags."""
    
    # Ensure pdfkit uses the correct wkhtmltopdf path
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    html_content = "<h1>Extracted Keyphrases with POS Tags</h1><ul>"
    for phrase, details in phrases.items():
        definition = details["definition"]
        pos_tag = details["pos"]
        html_content += f"<li><b>{phrase}</b> ({pos_tag}): {definition}</li>"
    html_content += "</ul>"

    pdf_path = "keyphrases_report.pdf"
    pdfkit.from_string(html_content, pdf_path, configuration=config)
    
    return pdf_path
