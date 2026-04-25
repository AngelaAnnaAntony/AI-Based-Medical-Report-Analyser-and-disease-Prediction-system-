import re

# ---------- CLEAN TEXT ----------
def clean_text(text):
    text = text.replace("|", " ")
    text = text.replace(":", " ")
    text = text.replace(",", "")
    return text


# ---------- GET NUMBER ----------
def get_number(line):
    match = re.search(r"\d+\.?\d*", line)
    if match:
        return float(match.group())
    return None


# ---------- MAIN EXTRACTION ----------
def extract_medical_values(text):

    text = clean_text(text)
    lines = text.split("\n")

    values = {}

    for line in lines:

        l = line.lower()

        # CBC
        if "hemoglobin" in l or "hb" in l:
            values["Hemoglobin"] = get_number(line)

        elif "wbc" in l or "tlc" in l:
            values["WBC"] = get_number(line)

        elif "rbc" in l:
            values["RBC"] = get_number(line)

        elif "platelet" in l:
            values["Platelets"] = get_number(line)

        elif "mcv" in l:
            values["MCV"] = get_number(line)

        elif "mchc" in l:
            values["MCHC"] = get_number(line)

        elif "mch" in l:
            values["MCH"] = get_number(line)

        elif "rdw" in l:
            values["RDW"] = get_number(line)

        # Diabetes
        elif "glucose" in l:
            values["Glucose"] = get_number(line)

        elif "hba1c" in l:
            values["HbA1c"] = get_number(line)

        # Lipid
        elif "cholesterol" in l and "total" in l:
            values["Total Cholesterol"] = get_number(line)

        elif "hdl" in l:
            values["HDL"] = get_number(line)

        elif "ldl" in l:
            values["LDL"] = get_number(line)

        elif "triglyceride" in l:
            values["Triglycerides"] = get_number(line)

        # Liver
        elif "sgpt" in l or "alt" in l:
            values["ALT"] = get_number(line)

        elif "sgot" in l or "ast" in l:
            values["AST"] = get_number(line)

        elif "bilirubin" in l and "total" in l:
            values["Bilirubin Total"] = get_number(line)

    return values

def detect_report_type(text):

    t = text.lower()
    types = []

    if any(x in t for x in ["hemoglobin", "rbc", "platelet"]):
        types.append("CBC")

    if any(x in t for x in ["bilirubin", "sgpt", "sgot"]):
        types.append("LFT")

    if any(x in t for x in ["cholesterol", "hdl", "ldl"]):
        types.append("Lipid Profile")

    if any(x in t for x in ["glucose", "hba1c"]):
        types.append("Diabetes")

    return types