---
id: law-government.criminal-law.charging-and-case-assessment.charging-decision-and-evidence-sufficiency
name: charging-decision-and-evidence-sufficiency
category: law-government
field: criminal-law
product: charging-and-case-assessment
tags: [charging-and-case-assessment, criminal-law, prosecution, prosecutor, charging-decision, charge-selection, evidence-sufficiency, elements-of-the-offence, probable-cause, declination, no-bill, grand-jury, indictment, information, public-interest-test, full-code-test, crown-prosecution-service, justice-manual, prosecutorial-discretion, case-screening, overcharging, lesser-included-offence]
level: practitioner
status: docs-checked
description: "Screen a criminal referral and choose charges: elements matrix, admissible-evidence test, conviction-likelihood standard, public-interest factors, declination memo."
sources: ["https://www.justice.gov/jm/jm-9-27000-principles-federal-prosecution", "https://www.cps.gov.uk/publication/code-crown-prosecutors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Charging decision and evidence sufficiency

**Goal:** turn a police or agency referral into a defensible charging decision — file,
decline, or send back for more investigation — with a written record of why.

## 1. Know which standard you are applying
Probable cause is the legal floor to file in US systems, but most prosecution
guidance sets a higher *internal* bar:
- **US federal (Justice Manual 9-27.220):** commence or recommend prosecution when the conduct is a federal
  offense and the admissible evidence will probably be sufficient to obtain and sustain a conviction, unless
  there is no substantial federal interest, the person is subject to effective prosecution elsewhere, or there is
  an adequate non-criminal alternative.
- **England & Wales Full Code Test (Code for Crown Prosecutors, 8th edition):** (1) evidential stage — a *realistic prospect of
  conviction* on each charge; (2) public-interest stage. Fail stage 1 and you stop.
State offices often have their own written policy; find it before you start.

## 2. Build an elements matrix
For each candidate charge, one row per statutory element (including mens rea and any
jurisdictional or aggravating element that changes the grade). Columns: the evidence
proving it, its source, whether it is **admissible** (hearsay, search legality,
confession voluntariness, chain of custody), and the defence's likely attack.
An element with only inadmissible or single-witness-uncorroborated support is a red cell.

## 3. Stress-test the evidence
- Assume suppression motions succeed where there is a colourable issue; does the case survive?
- Identify witnesses with credibility problems, prior statements, or reasons to recant.
- Check exculpatory material now — you will owe it to the defence anyway (Brady/disclosure).
- Confirm the limitation period and venue.
- Ask what the jury will see as the *story*; a technically complete case with an
  unsympathetic narrative often fails.

## 4. Select the charges
- Charge what you can prove, at the grade you can prove. Avoid stacking counts purely
  as bargaining leverage.
- Consider lesser-included offences and how they will go to the jury.
- Check multiplicity/duplicity (same act charged twice; two offences in one count).
- Weigh collateral consequences (immigration, registration, licensing) where policy
  permits considering them.

## 5. Public-interest / discretion factors
Seriousness, harm to victim, victim's views, culpability and role, criminal history,
age and health, availability of diversion or civil/administrative remedies,
deterrence, resource cost. Record which factors you relied on.

## 6. Write the decision memo
Facts summary → charges considered → elements matrix result → evidentiary risks →
discretion factors → decision → what further investigation would change it.
For a declination, state the reason category (insufficient evidence, interests of
justice, referred elsewhere) so it is auditable and the victim can be informed.

## Gotchas
- Grand jury presentation (where used) is not a merits test of your case; a true bill
  says nothing about trial strength.
- Charging decisions made before forensic results return are a common source of later dismissals.
- Victims' rights statutes in many jurisdictions require consultation or notice before
  declining or reducing — check yours.
- Uncertain: exact internal standards and supervisor-approval thresholds vary by office;
  treat the standards above as representative, not binding on your office.

## Verify
- [ ] Every element of every charge has at least one admissible source.
- [ ] Case still stands if the weakest suppression issue is lost.
- [ ] Limitation period, venue and jurisdiction confirmed.
- [ ] Exculpatory material identified and logged for disclosure.
- [ ] Memo records evidential conclusion and discretion factors separately.
- [ ] Victim consultation/notice obligations checked.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States federal prosecutors (Justice Manual); England and Wales (Crown Prosecution Service).
- Confirmed against official sources (see `sources`): Justice Manual 9-27.220 (admissible evidence will probably be sufficient to obtain and sustain a conviction; the three exceptions: no substantial federal interest, effective prosecution elsewhere, adequate non-criminal alternative); 9-27.230 lists substantial-federal-interest factors; Code for Crown Prosecutors (8th edition, page dated 26 October 2018) paragraphs 4.2, 4.6 and 4.9 (evidential stage: realistic prospect of conviction; public interest stage).
- Corrected or removed: The Justice Manual summary previously said "charge only if ... and a substantial federal interest is served"; it now states the three exceptions. Removed the ABA Prosecution Function standards 3-4.3 and 3-4.4 (the ABA site returned HTTP 403, so they could not be read) and the claim that juries discount overcharged cases.

Method: documentation only; no commands were run.
