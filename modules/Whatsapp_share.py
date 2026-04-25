import urllib.parse

def generate_whatsapp_link():
    message = """
Hello,
Here is my AI Medical Report Analysis result.
Please find the attached PDF report.
Generated using AI-Based Medical Report Analyser.
"""
    encoded_message = urllib.parse.quote(message)
    link = f"https://wa.me/?text={encoded_message}"
    return link