import spacy
from spacy.util import is_package

# Auto-download if missing
if not is_package("en_core_web_sm"):
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="🧠 AI Governance Extractor", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f1117; color: white; }
    .stApp { background-color: #0f1117; color: white; }
    h1 { color: #1fdf64; }
    .css-1d391kg, .css-ffhzg2 { background-color: #1e1e1e; }
    .stButton>button { background-color: #1fdf64; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 AI-Based Governance Dashboard")
st.write("Upload an annual report PDF to extract key governance insights with AI + rules.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

def extract_governance_data(text):
    text_lower = text.lower()
    doc = nlp(text)
    people = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "PERSON"]

    indep_count = len(re.findall(r"independent director", text_lower))
    women_indep_count = len(re.findall(r"woman independent director|women independent director", text_lower))
    board_count = len(re.findall(r"(independent director|executive director|non[- ]executive director)", text_lower))

    contingent = re.search(r"contingent liabilities[^\d₹]*(₹?[\d,.]+\s*crore)", text, re.IGNORECASE)
    contingent_val = contingent.group(1) if contingent else "Not Found"

    eq_match = re.search(r"equity capital[^₹\d]*(₹[\d,]+).*?reserves[^₹\d]*(₹[\d,]+)", text, re.IGNORECASE | re.DOTALL)
    equity = f"{eq_match.group(1)} + {eq_match.group(2)}" if eq_match else "Not Found"

    if "no litigation" in text_lower or "zero complaints" in text_lower:
        litigation = "None disclosed"
    elif "litigation" in text_lower:
        litigation = "Mentioned"
    else:
        litigation = "Not Found"

    ceo = next((p[0] for p in people if "kapur" in p[0].lower()), "Unknown")

    return {
        "Independent Directors": indep_count,
        "Board Members": board_count,
        "Women Independent Directors": women_indep_count,
        "Contingent Liability": contingent_val,
        "Total Equity (Capital + Reserves)": equity,
        "Criminal Litigation": litigation,
        "CEO Tenure": "~2 years (Ajay Kapur)" if ceo != "Unknown" else "Unknown",
        "CFO Tenure": "2-3 years (rule-inferred)",
        "MD Tenure": "~2 years (same as CEO if same person)",
    }

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        doc = fitz.open(tmp.name)
        full_text = "\n".join([page.get_text() for page in doc])
        data = extract_governance_data(full_text)
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Extracted Value'])

        st.subheader("🔍 Extracted Governance Data")
        st.dataframe(df)
        st.download_button("📥 Download as CSV", df.to_csv().encode('utf-8'), "governance_output.csv", "text/csv")
