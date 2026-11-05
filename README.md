# Paediatrics Ward Rounds — GMC Amritsar

Bedside ward-rounds app for the Department of Paediatrics, Government Medical College, Amritsar (Guru Nanak Dev Hospital). Works offline on phones and can be installed to the home screen.

> **Decision support only.** Scores and colours are for clinician review; the treating doctor decides. Normal ranges and PEWS thresholds are a starting set and must be checked against departmental protocol before ward use. **Do not enter real patient data in a public deployment.**

## Phase 1
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

## Phase 2 (this version adds)
- **Easily-missed alerts** on every patient, sorted urgent → to check → info, with a count on the ward list:
  - Antibiotics: day count, 48–72 h review, day-7 duration check, no stop date, stop date reached, on antibiotics with no culture.
  - Dose outside the usual mg/kg range or above maximum single/daily dose; NSAID in dengue; no weight recorded.
  - Investigations pending > 24 h, results not yet seen, critical values (age-aware ranges for neonates).
  - Cannula > 72 h; urinary/central/umbilical line days.
  - IV + feeds running > 120 % or < 80 % of target fluids.
  - Red/orange child with no blood sugar in 6 h.
  - Sepsis / DKA / SAM diagnosed but protocol not marked started.
  - Newborn vitamin K, BCG, OPV-0, Hep B-0; nutrition plan; consent; referral pending; parents counselled; I/O charted; weight today.
- **Medicines** with live weight-based dose check against ~55 commonly used paediatric drugs (doses per IAP Drug Formulary / Harriet Lane / BNFc practice), grouped by system, with Indian formulations so the dose is shown in **mL of syrup, drops or injection**. Age- and weight-banded fixed doses for zinc, vitamin A, albendazole, salbutamol and ipratropium nebs, and newborn vitamin K.
- **Investigations**: order, duplicate-order warning (needs a second tap), result entry with low/high/critical flags, mark seen.
- **Lines and tubes** with insertion time and removal.
- **Daily checklist**: weight, I/O, counselling, consent, nutrition, referral, protocols, newborn care.
- **Calculators**: maintenance fluids (Holliday-Segar, neonatal day-of-life schedule, % restriction), infusions (adrenaline, noradrenaline, dopamine, dobutamine, milrinone, midazolam, insulin) with standard mixes and mL/h, resuscitation dose card with ETT size, and a stand-alone dose check.

> The formulary, lab ranges and alert thresholds in `src/app.html` (`FORM`, `LABS`, `INF`, `alerts()`) are a starting set. Have them checked against the departmental protocol and IAP drug formulary before ward use.

## Next phase
- **Phase 3:** protocol pathways (IAP / WHO / NNF), investigation panels by diagnosis, bilirubin nomogram, SBAR handover, discharge summary with Punjabi instructions, ward dashboard, growth charts, user logins, sync.
