# Paediatrics Ward Rounds — GMC Amritsar

Bedside ward-rounds app for the Department of Paediatrics, Government Medical College, Amritsar (Guru Nanak Dev Hospital). Works offline on phones and can be installed to the home screen.

> **Decision support only.** Scores and colours are for clinician review; the treating doctor decides. Normal ranges and PEWS thresholds are a starting set and must be checked against departmental protocol before ward use. **Do not enter real patient data in a public deployment.**

## Phase 1 (this version)
- Admit patients: demographics, bed (shared beds like `12A`), IPD no., unit, consultant, weight, diagnosis, neonatal details, referral source and transport, health scheme (Ayushman Bharat / MMSBY, JSSK).
- Vitals entry with a live score preview: HR, RR, SpO₂, oxygen, work of breathing, temperature, CRT, SBP, AVPU, GCS, blood sugar, urine output, convulsion, apnoea.
- **Automatic colour coding** from a PEWS-style score using age-specific ranges (neonate, infant, 1–4 y, 5–11 y, 12 y+):
  - Green 0–2 · Yellow 3–4 · Orange 5–6 (or any single parameter scoring 3) · Red ≥ 7
  - Danger signs force **Red**: SpO₂ < 90 %, hypotension for age, CRT > 3 s, convulsion, apnoea, GCS ≤ 8, AVPU P/U, hypoglycaemia (< 45 mg/dL neonates, < 54 mg/dL others).
- Manual colour override with mandatory reason, shown on the ward list.
- Ward list sorted sickest first, with trend (better / same / worse) and time since last vitals.
- Vitals log, score trend chart, score breakdown, SOAP progress notes with the previous note alongside.
- Discharge / readmit / delete. Five sample patients load on first open (remove with one tap).

Data is stored in the browser on that device only (`localStorage`). There is no server or sync yet.

## Run it
Open `index.html` in a browser, or enable **GitHub Pages** (Settings → Pages → Deploy from branch → `main` / root) and open the site URL on your phone, then "Add to Home Screen".

## Files
- `src/app.html` — app source (markup, styles, script)
- `build.py` — builds `index.html` from the source: `python3 build.py`
- `manifest.webmanifest`, `sw.js`, `icon.svg` — install + offline support

## Next phases
- **Phase 2:** easily-missed alerts (antibiotic days, cannula > 72 h, pending results, critical labs), weight-based drug dose checker, Holliday-Segar fluid calculator, emergency drug infusion calculator.
- **Phase 3:** protocol pathways (IAP / WHO / NNF), investigation panels, SBAR handover, discharge summary with Punjabi instructions, ward dashboard, user logins, sync.
