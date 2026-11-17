---
id: defence-public-safety.criminal-tradecraft.extortion.responding-to-extortion-and-sextortion-threats
name: responding-to-extortion-and-sextortion-threats
category: defence-public-safety
field: criminal-tradecraft
product: extortion
tags: [criminal-tradecraft, extortion, blackmail, sextortion, financially-motivated-sextortion, threat-assessment, threat-management, crisis-management-team, cyber-extortion, ransomware-extortion, data-leak-extortion, ddos-extortion, product-contamination-threat, product-extortion, protection-racket, kidnap-and-ransom, k-and-r, evidence-preservation, do-not-pay, take-it-down, stopncii, ncmec, ceop, esafety, ic3, victim-support, security-consultant, fraud-investigator, defensive]
level: practitioner
status: draft
description: "Response playbook for extortion threats against businesses and individuals: triage, evidence preservation, crisis team, police contact, why not to engage or pay, and sextortion victim support."
sources: ["FBI and NCA public sextortion and ransomware advisories (public)", "NCMEC Take It Down and StopNCII.org service descriptions (public)", "Business continuity / crisis-management practice for product-extortion threats (public summaries)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Responding to extortion and sextortion threats

**Goal:** when a business or a person receives a demand backed by a threat — to leak data,
release intimate images, contaminate products, harm people or disrupt services — take control
of the response in the first hours: confirm and preserve, escalate to the right people, avoid the
mistakes extortionists rely on, and support the victim. For security consultants, fraud and
incident leads, HR, safeguarding staff and the person targeted.

## 1. How extortion works (enough to recognise it)
All extortion combines **a threat, a demand, a deadline and a pressure on secrecy**. The deadline
and the "don't tell anyone" instruction exist to stop the victim getting help — so getting help
is the first counter-move. Common forms:
- **Data/ransomware extortion** — systems encrypted and/or stolen data threatened with publication.
- **DDoS extortion** — pay or the website goes down; often a bluff backed by a short demo attack.
- **Product contamination** — threat to tamper with goods on sale.
- **Personal/reputational blackmail** — threatened disclosure of real or fabricated information.
- **Sextortion** — intimate images (often obtained by a fake online persona) used to demand money
  or more images. **Financially motivated sextortion of teenage boys** has risen sharply since ~2022
  and is linked to suicides; treat it as a safeguarding emergency.
- **Bulk "I hacked your webcam" emails** quoting an old leaked password — almost always a bluff
  with no images; report and change the password.

## 2. First hour — triage
1. **Don't reply, negotiate or pay yet.** Don't delete anything.
2. **Assess credibility:** proof offered (a sample of data, an image, a product altered)? specific
   knowledge? a mass template? Bulk-sent bluffs are common; targeted threats with proof are not.
3. **Safety first:** any threat to life or of contamination of products on sale → call police
   immediately; product threats may need precautionary withdrawal decisions within hours.
4. **Preserve evidence:** screenshots *with* URLs, usernames, profile IDs and timestamps; original
   emails with full headers; payment addresses (crypto wallet, account); call logs. Store securely.
   Don't forward intimate images of a minor to anyone — report them instead (see §4); possessing or
   sharing them may itself be an offence.
5. **Escalate** to the crisis-management team (business) or a trusted adult/adviser (individual).

## 3. Business response
- **Crisis team:** decision-maker, legal, security, comms, IT/incident response, HR. One person
  owns contact with the extortionist if any contact is decided; nobody else engages.
- **Law enforcement early.** Police can share intelligence about the group, and in many places
  paying certain groups breaches **sanctions law** — check before any payment decision.
- **Insurance:** cyber or kidnap-and-ransom (K&R) policies often require notifying the insurer
  before acting and may supply specialist responders; read the policy terms.
- **Paying** does not guarantee deletion, decryption or silence and marks you as a payer. Many
  authorities advise against it; the decision is ultimately legal and commercial, but take it
  informed, documented and never under the extortionist's deadline alone.
- **Ransomware specifics:** isolate systems, preserve logs, restore from tested backups — see
  `computing-software.digital-forensics-incident-response.incident-response-process.incident-lifecycle-playbook`.
- **Regulatory clocks:** a data leak may trigger breach-notification duties (e.g. 72 h under GDPR).
- **Prevention:** threat-reporting route for staff, backups, DDoS protection, tamper-evident
  packaging and product-security audits, limited public exposure of executives' personal details.

## 4. Sextortion — supporting the victim
- Say clearly: **it is not your fault, you are not in trouble, and help works.**
- **Stop contact; don't pay** — payment almost always leads to more demands. Block, but only after
  preserving the evidence.
- Report the account on the platform; report to police.
- **Under-18s:** use **NCMEC Take It Down** (hash-based removal) and report to CyberTipline (US);
  **CEOP / Report Remove** (UK, with Childline); **eSafety Commissioner** (Australia).
- **Adults:** **StopNCII.org** creates hashes on the victim's device so partner platforms block the image.
- Check on wellbeing; involve a counsellor or crisis line. Watch for signs of self-harm.

## 5. Gotchas
- Deadlines are pressure tools; real decisions take the time they need.
- "Proof" may be fabricated, AI-generated or an old breach dump — verify before believing it.
- Don't publicly announce the threat without legal/comms advice; it can trigger copycats.
- Extortion often follows a fraud or intrusion — look for the original compromise.

## Verify
- [ ] Nobody replied, paid or deleted before triage.
- [ ] Credibility was assessed and evidence preserved with IDs, headers and timestamps.
- [ ] Police contacted; sanctions and insurer requirements checked before any payment discussion.
- [ ] One named owner for any contact; crisis team convened.
- [ ] Sextortion victims were given the right removal service and wellbeing support.
