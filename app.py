from flask import Flask, render_template, request, send_file
from flask_talisman import Talisman  # Enforces HTTPS
from keyphrase_extractor import extract_keyphrases
from generate_pdf import create_pdf
import os

app = Flask(__name__)
Talisman(app)  # Force HTTPS for security

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_phrases = {}
    text = ""
    
    if request.method == "POST":
        text = request.form["text"]
        extracted_phrases = extract_keyphrases(text)  # Extracts keyphrases with POS tags

    return render_template("index.html", phrases=extracted_phrases, text=text)

@app.route("/download", methods=["POST"])
def download():
    text = request.form["text"]
    phrases = extract_keyphrases(text)
    
    # Generate PDF file
    pdf_path = create_pdf(phrases)
    
    # Ensure the file exists before sending
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "Error: PDF file was not created", 500

if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)  # Enables HTTPS
