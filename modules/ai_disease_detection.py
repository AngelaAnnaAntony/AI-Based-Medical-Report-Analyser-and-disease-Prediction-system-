def detect_diseases_ai(values):
    def safe(v):
        return v if isinstance(v, (int, float)) else 0
    results = []

    glucose = safe(values.get("Glucose"))
    hb = safe(values.get("Hemoglobin"))
    alt = safe(values.get("ALT"))

    # Simulated AI logic (advanced pattern)
    if glucose > 140 and hb < 10:
        results.append({
        "Disease": "Possible Diabetes with Anemia",
        "Doctor": "Endocrinologist",
        "Recommendation": "Monitor sugar and improve iron intake"
    })

    if alt > 150:
        results.append({
        "Disease": "Severe Liver Disorder",
        "Doctor": "Gastroenterologist",
        "Recommendation": "Immediate medical attention required"
        })

    return results