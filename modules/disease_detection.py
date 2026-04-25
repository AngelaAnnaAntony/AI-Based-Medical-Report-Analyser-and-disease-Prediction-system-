import re

# ---------------- SAFE VALUE ----------------
def safe(v):
    return v if isinstance(v, (int, float)) else None


# ---------------- SEVERITY ----------------
def get_severity(value, low=None, high=None):
    if value is None:
        return "Unknown"

    if low is not None and value < low:
        diff = low - value
        if diff < 2:
            return "Mild"
        elif diff < 5:
            return "Moderate"
        else:
            return "Severe"

    if high is not None and value > high:
        diff = value - high
        if diff < 10:
            return "Mild"
        elif diff < 30:
            return "Moderate"
        else:
            return "Severe"

    return "Normal"


# ---------------- MAIN DETECTION ----------------
def detect_diseases(values, report_types):

    results = []

    # SAFE values
    hb = safe(values.get("Hemoglobin"))
    wbc = safe(values.get("WBC"))
    platelets = safe(values.get("Platelets"))
    rbc = safe(values.get("RBC"))

    glucose = safe(values.get("Glucose"))
    hba1c = safe(values.get("HbA1c"))

    chol = safe(values.get("Total Cholesterol"))
    ldl = safe(values.get("LDL"))
    hdl = safe(values.get("HDL"))
    tg = safe(values.get("Triglycerides"))

    alt = safe(values.get("ALT"))
    ast = safe(values.get("AST"))
    bilirubin = safe(values.get("Bilirubin Total"))

    mcv = safe(values.get("MCV"))
    mchc = safe(values.get("MCHC"))

    report_str = " ".join(report_types).lower()

   # ---------------- ANEMIA (CBC) ----------------
    # FIX 2: Check for both "blood" and "cbc"
    if "blood" in report_str or "cbc" in report_str:
        # Check that it's not None before doing math on it!
        if hb is not None and hb < 12:
            severity = get_severity(hb, low=12)
            results.append({"Disease": f"Anemia ({severity})", "Doctor": "Hematologist", "Recommendation": "Increase iron-rich foods and consult doctor."})

        if wbc is not None and wbc > 11000:
            results.append({"Disease": "Possible Infection", "Doctor": "General Physician", "Recommendation": "Further tests required."})

        if platelets is not None and platelets < 150000:
            results.append({"Disease": "Low Platelet Count", "Doctor": "Hematologist", "Recommendation": "Avoid injuries, consult doctor."})

        if rbc is not None and rbc < 4:
            results.append({"Disease": "Low RBC Count", "Doctor": "Hematologist", "Recommendation": "Increase iron and vitamin intake."})

        if mcv is not None and mcv < 80:
            results.append({"Disease": "Microcytic Anemia", "Doctor": "Hematologist", "Recommendation": "Iron supplementation needed."})

        if mchc is not None and mchc < 31:
            results.append({"Disease": "Hypochromic Anemia", "Doctor": "Hematologist", "Recommendation": "Iron-rich diet recommended."})

    # ---------------- DIABETES ----------------
    if "diabetes" in report_str:
        if glucose is not None and glucose > 125:
            severity = get_severity(glucose, high=125)
            results.append({"Disease": f"Diabetes ({severity})", "Doctor": "Endocrinologist", "Recommendation": "Control diet and monitor sugar levels."})

        if hba1c is not None and hba1c > 6.5:
            results.append({"Disease": "Diabetes", "Doctor": "Endocrinologist", "Recommendation": "Follow diabetes management plan."})

    # ---------------- CHOLESTEROL (LIPID) ----------------
    if "lipid" in report_str or "cholesterol" in report_str:
        if chol is not None and chol > 200:
            severity = get_severity(chol, high=200)
            results.append({"Disease": f"High Cholesterol ({severity})", "Doctor": "Cardiologist", "Recommendation": "Avoid oily food and exercise."})

        if ldl is not None and ldl > 130:
            results.append({"Disease": "High LDL", "Doctor": "Cardiologist", "Recommendation": "Reduce saturated fat."})

        if hdl is not None and hdl < 40:
            results.append({"Disease": "Low HDL", "Doctor": "Cardiologist", "Recommendation": "Increase physical activity."})

        if tg is not None and tg > 150:
            results.append({"Disease": "High Triglycerides", "Doctor": "Cardiologist", "Recommendation": "Avoid sugary foods."})

    # ---------------- LIVER (LFT) ----------------
    # FIX 2: Check for both "liver" and "lft"
    if "liver" in report_str or "lft" in report_str:
        if (alt is not None and alt > 55) or (ast is not None and ast > 40):
            # Find which one is highest for the severity check
            max_val = max([v for v in (alt, ast) if v is not None])
            severity = get_severity(max_val, high=55)
            results.append({"Disease": f"Liver Disorder ({severity})", "Doctor": "Gastroenterologist", "Recommendation": "Avoid alcohol, eat healthy."})

        if bilirubin is not None and bilirubin > 1.2:
            results.append({"Disease": "Jaundice Risk", "Doctor": "Gastroenterologist", "Recommendation": "Drink fluids and consult doctor."})

    # ---------------- DEFAULT ----------------
    if not results:
        results.append({
            "Disease": "No major abnormality detected",
            "Doctor": "General Physician",
            "Recommendation": "Maintain healthy lifestyle."
        })

    return results

# ---------------- PATIENT DETAILS ----------------
def extract_patient_details(text):

    name = None
    age = None
    gender = None

    lines = text.split("\n")

    for line in lines:

        clean = line.strip()
        l = clean.lower()

        # -------- NAME (STRICT) --------
        if ("name" in l or "patient" in l) and len(clean) < 50:
            match = re.search(r"(name|patient)\s*[:\-]?\s*([A-Za-z .]+)", clean, re.IGNORECASE)
            if match:
                extracted = match.group(2).strip()

                # ❗ avoid wrong sentences
                if len(extracted.split()) <= 4:
                    name = extracted

        # -------- AGE (STRICT) --------
        if "age" in l:
            match = re.search(r"age\s*[:\-]?\s*(\d{1,3})", clean, re.IGNORECASE)
            if match:
                age = match.group(1)

        # -------- GENDER --------
        if "sex" in l or "gender" in l:
            match = re.search(r"(male|female)", clean, re.IGNORECASE)
            if match:
                gender = match.group(1).capitalize()

    return name, age, gender