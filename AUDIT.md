# Audit — Paediatrics Ward Rounds app

**Date:** 6 November 2026 · **Version audited:** commit `ff12875` (Phases 1–2 + formulary + neonatal intervals) · **Fixed in:** the commit that adds this file

## Method
- Line-by-line review of every clinical rule: PEWS scoring and danger signs, ~55-drug formulary, neonatal interval tables, lab ranges, fluid, infusion and resuscitation calculators, and the alert engine.
- Automated tests (jsdom) running the real app: 60+ clinical test cases with known correct answers, every screen opened for every sample patient, every form submitted, script-injection payloads in all 20 free-text fields, blocked and corrupt storage, and impossible inputs.
- Visual check at phone width (400 px).

## Findings and fixes

### Safety-critical (could hide a sick child or allow a large dosing error)
| # | Finding | Fix |
|---|---|---|
| 1 | **Manual colour override never expired.** A child set to green stayed green after a convulsion and SpO₂ 85 %. | An override now lapses when new vitals are entered, and can never hide danger signs. The patient screen says when and why it lapsed. |
| 2 | **Bradycardia not a danger sign.** An infant with HR 45 scored orange. | HR < 60 (or < 80 in neonates) forces red. Also HR > 220 (≤ 1 y) / > 180 (older) for SVT/shock, and RR < 10 in children. |
| 3 | **Incomplete vitals showed green.** Entering only a heart rate gave "Stable". | A new grey **Incomplete vitals** level lists what is missing; it sorts above Stable. |
| 4 | **Dose check ignored the unit.** 250 mcg ipratropium was read as 250 mg; a dose entered in mL was read as mg. | Doses are converted (mcg → mg; mL × formulation strength → mg). If conversion isn't possible the app says so instead of passing it. A 10× mL error (21 mL instead of 2.1 mL of drops) is now flagged. |
| 5 | **No guard against 10-fold weight errors.** 25 kg entered for a 3-day-old was accepted and every dose "checked" against it. | Weight-for-age plausibility check on admission and daily weight (needs a second tap to confirm), plus an urgent alert on the patient. |
| 6 | **IV paracetamol in < 10 kg** allowed 60 mg/kg/day. | IV route under 10 kg now uses 7.5–10 mg/kg/dose, max 30 mg/kg/day. |
| 7 | **Gentamicin given 8-hourly at a once-daily dose** (15 mg/kg/day) passed. | Daily maximum added (7.5 mg/kg/day; amikacin 22.5). Divided dosing (2–2.5 mg/kg 8-hourly) is accepted. |
| 8 | **Preterm babies flagged hypotensive on normal BP** (SBP 45 at 28 wk triggered red). | Preterm neonates use the MAP < gestational age (weeks) rule; a MAP field was added. The SBP 60 cut-off applies to term neonates only. |
| 9 | **Neonatal interval tables used fractional PMA**, so babies at 29⅓ weeks fell into the next band (e.g. gentamicin q24 instead of q36). | Completed weeks of PMA used, as NeoFax intends. Re-verified against 11 NeoFax cases. |
| 10 | **Impossible vitals accepted** (SpO₂ 990, temp 375, GCS 40). | Plausible-range validation with a message naming the field. |

### Clinically wrong but lower risk
| # | Finding | Fix |
|---|---|---|
| 11 | Neonatal fever (≥ 37.5 °C) scored 0. | Scores 1 (≥ 38.5 scores 2) and prompts a sepsis screen. |
| 12 | Bilirubin: a child with TSB 5 mg/dL showed normal; neonatal TSB judged against a fixed 12. | Children: upper limit 1.2. Neonates: prompts plotting on the AAP 2022 hour-specific chart; critical > 20. |
| 13 | Creatinine 0.9 in a 6-month-old showed normal. | Age-specific upper limits (neonate 1.0, infant 0.5, 1–4 y 0.6, 5–11 y 0.9, 12 y + 1.2). |
| 14 | TLC 15 in a 1-year-old flagged high; neonatal K⁺ 6.0 flagged high. | Age-specific TLC and neonatal K⁺ / calcium ranges. |
| 15 | Artesunate accepted 3 mg/kg in children ≥ 20 kg. | 3 mg/kg if < 20 kg, 2.4 mg/kg if ≥ 20 kg. |
| 16 | Neonatal calcium gluconate 2 mL/kg flagged as overdose. | Neonates 100–200 mg/kg. |
| 17 | Normal doses flagged low/high: amoxicillin 25 mg/kg/day, metronidazole for amoebiasis, fluconazole 3 mg/kg, iron prophylaxis. | Ranges widened to match standard use. |
| 18 | Neonatal fluids calculated on current weight in the first days. | Birth weight used until regained (first 14 days). |
| 19 | ETT size: a 7 kg infant got the neonatal "weight + 6" depth; no age gave a neonatal tube for a 20 kg child. | Separate infant rule (3.5–4.0 mm, depth 3 × size); asks for age when missing. |
| 20 | Defibrillation shown as 4 J/kg only. | 2 J/kg first, then 4 J/kg. |
| 21 | Vitamin K note didn't warn about the 10 mg/mL adult ampoule. | Warning added. |

### Software
| # | Finding | Fix |
|---|---|---|
| 22 | If the browser blocks storage (private mode), nothing was saved and no one was told. | Red "Not saving" banner. |
| 23 | Unreadable stored data was silently replaced with sample patients. | The unreadable data is kept in a backup key before starting fresh. |
| 24 | Future admission dates, negative weights, out-of-range gestation accepted. | Validated. |

### Passed with no change needed
- **Script injection:** blocked in all 20 free-text fields across every screen.
- **Infusion calculator:** all 7 standard mixes give the stated rate (e.g. adrenaline 0.6 × wt mg in 100 mL → 1 mL/h = 0.1 mcg/kg/min).
- **Resuscitation doses:** adrenaline, atropine, adenosine, amiodarone, dextrose, bicarbonate, calcium, 3 % saline correct with maximums.
- **Holliday-Segar**, age-specific HR/RR bands, PALS minimum SBP, aminoglycoside/vancomycin/meropenem/acyclovir NeoFax intervals, mL volumes for Indian formulations.
- **Phone layout:** no horizontal scrolling at 400 px.

## Remaining risks (not fixable in code alone)
1. **Clinical sign-off.** Doses, ranges and thresholds follow standard references (IAP practice, Harriet Lane, BNFc, NeoFax, PALS, AAP 2022) but must be checked by the HOD / neonatology consultant against the department's protocols and the current IAP Drug Formulary before use.
2. **PEWS is not validated** for this population. Thresholds (yellow 3, orange 5, red 7) should be audited against real outcomes before being relied on.
3. **Data privacy.** Data sits unencrypted in the phone's browser with no login or PIN. Until Phase 3 adds logins, do not store identifiable patient data, or use initials + IPD number only, on a locked personal phone.
4. **No backup or sync.** Clearing browser data or losing the phone loses everything; each phone has its own list.
5. **Colour = physiology only.** Critical labs and dosing errors show as red alert badges, not as the patient's colour. This is deliberate, but users should know.
6. **Device clock** drives antibiotic days, cannula hours and neonatal ages; a wrong phone clock gives wrong alerts.
7. Neonatal intervals use NeoFax; some units use the newer Red Book ampicillin schedule. Confirm which the unit follows.
