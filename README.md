# 🧠 AI Governance Extractor Dashboard

Upload a company annual report PDF and extract key governance insights using AI (spaCy NER + rule-based parsing).

## Features
- Extracts:
  - Independent Directors
  - Board Members
  - Women Independent Directors
  - Contingent Liabilities
  - Equity Capital + Reserves
  - Litigation status
  - CEO/CFO/MD Tenure

## Installation (Local)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run governance_ner_dashboard.py
```

## Streamlit Cloud Deployment

Streamlit Cloud runs in a clean container, so the app includes automatic download of the spaCy model:
```python
os.system("python -m spacy download en_core_web_sm")
```
Make sure this repo includes `requirements.txt`, `README.md`, and `governance_ner_dashboard.py`.

## License
MIT License