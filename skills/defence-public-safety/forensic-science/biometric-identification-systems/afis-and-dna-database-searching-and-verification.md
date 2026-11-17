---
id: defence-public-safety.forensic-science.biometric-identification-systems.afis-and-dna-database-searching-and-verification
name: afis-and-dna-database-searching-and-verification
category: defence-public-safety
field: forensic-science
product: biometric-identification-systems
tags: [biometric-identification-systems, biometrics, afis, abis, ngi, ident1, fingerprint-database, latent-search, tenprint-search, candidate-list, encoding, minutiae-markup, codis, ndnad, dna-database, database-hit, cold-hit, familial-search, partial-match, prum, interpol, facial-comparison, facial-recognition, fisswg, morphological-comparison, one-to-many, one-to-one, false-positive, threshold, human-review, unsolved-latent-file, data-retention, audit-trail]
level: practitioner
status: draft
description: "Search and verify on forensic biometric databases (AFIS, DNA databases, facial comparison): good encoding, reading candidate lists, treating hits as leads, human verification and retention rules."
sources: ["NIST ANSI/NIST-ITL data format standard for biometric interchange", "FBI CODIS and NDIS operational procedures (public summaries)", "FISWG facial comparison guidelines", "UK Biometrics and Forensics Ethics Group / Biometrics Commissioner reports"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AFIS and DNA database searching and verification

**Goal:** get the most investigative value from one-to-many biometric databases —
fingerprint (AFIS/ABIS), DNA and facial — while never letting a computer ranking stand
in for an examiner's conclusion. System names and menus differ by vendor and country;
the principles below are vendor-neutral. Interface specifics should be confirmed against
your system's training.

## 1. The core concept: systems rank, people identify
- A one-to-many search returns a **candidate list** ranked by similarity score. The top
  candidate is often wrong for poor latents; the true source may be at rank 5 or absent.
- Scores aren't probabilities and aren't comparable across systems or record types.
- Every reported association needs a qualified human comparison (ACE-V for prints —
  see `defence-public-safety.forensic-science.fingerprint-analysis.ace-v-friction-ridge-examination`;
  a confirmatory reference sample for DNA; FISWG-style morphological review for faces).

## 2. Fingerprint (AFIS) workflow
1. **Tenprint enrolment:** check sequence (fingers in the right boxes — rolled vs plain
   impressions cross-checked), quality, and that the subject's identity record is linked.
   A wrong-finger tenprint quietly poisons every future latent search.
2. **Latent encoding:** orient the mark, set the core/delta and pattern if known; review
   or manually mark minutiae (auto-extraction over-marks noise on poor latents).
   Indicate finger position or palm area if known — it narrows the search.
3. **Search** against tenprint and palm files, and against the **unsolved latent file**
   (links scenes together even without a suspect).
4. **Review the candidate list** to the depth your lab policy requires (often 10–20+);
   don't stop at the first plausible candidate.
5. Unidentified latents of sufficient quality are **registered** for future automatic
   reverse searches as new tenprints enter.

## 3. DNA database workflow
- Only profiles meeting the database's loci, quality and eligibility rules are uploaded
  (crime-scene profiles vs offender/arrestee reference profiles have different rules).
- Search stringency: high-stringency (full match) vs moderate/low (partial or mixed
  profiles) — matches at lower stringency need careful review and often more testing.
- A **hit report** goes to the investigator as an **intelligence lead**; a fresh
  reference sample from the person is analysed and compared before evidential use.
- **Familial searching** and international exchange (e.g. Prüm, Interpol) need specific
  authorisation and have legal/ethical policies — check before requesting.

## 4. Facial comparison
- Automated facial recognition returns candidates; examiners do **morphological
  comparison** of features (not photo-anthropometric measurement alone), noting image
  quality limits: pose, resolution, lighting, ageing.
- Report on a graded scale, never "match" from an algorithm score. Known demographic
  differentials in algorithm error rates are a reason for careful thresholding and
  human review.

## 5. Governance
- Every search is logged with user, purpose and case reference — audits happen.
- **Retention and deletion** rules (e.g. records of people not convicted) are statutory
  in many countries; acting on a record that should have been deleted creates legal risk.
- Quality: periodic proficiency tests, monitoring of false-positive investigations, and
  error logs for mis-sequenced enrolments.

## Gotchas
- Duplicate identities: one person enrolled under several names — check aliases before
  telling an investigator "no previous record".
- Latent searched only against the "obvious" finger — search all positions if unknown.
- Contamination hits: a DNA database hit to a police officer or lab worker is a
  contamination indicator; check elimination databases first.
- A no-hit result means "not in the database", not "not the offender".

## Verify
- [ ] Tenprints sequence-checked before enrolment.
- [ ] Latent encoding reviewed manually; search scope (fingers, palms, unsolved file) recorded.
- [ ] Candidate list reviewed to policy depth; identification made by a qualified examiner and verified.
- [ ] DNA hits reported as leads pending confirmatory sample.
- [ ] Search purpose logged; retention rules respected.
