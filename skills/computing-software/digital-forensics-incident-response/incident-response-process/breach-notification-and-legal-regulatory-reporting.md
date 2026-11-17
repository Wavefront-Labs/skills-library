---
id: computing-software.digital-forensics-incident-response.incident-response-process.breach-notification-and-legal-regulatory-reporting
name: breach-notification-and-legal-regulatory-reporting
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [breach-notification, gdpr, article-33, regulatory-reporting, notifiable-breach, personal-data, privileged-investigation, dfir, compliance]
level: advanced
status: docs-checked
description: "Feed the GDPR Article 33 notification clock after a breach: the 72-hour rule, minimum content, phased and late notification, documentation, and the facts counsel needs from IR."
sources: ["https://gdpr-info.eu/art-33-gdpr/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Breach notification and legal/regulatory reporting

**Goal:** the forensic finding ("the attacker accessed this database") and the legal conclusion
("this is notifiable, by this date") are different judgments made by different people. The IR
team produces precise facts fast enough for counsel to make the second call on time. This skill
is grounded in the text of GDPR Article 33 only; it is not legal advice.

## 1. What Article 33 says
- The controller must notify the competent supervisory authority of a personal data breach
  **without undue delay and, where feasible, not later than 72 hours after having become aware
  of it**, unless the breach is **unlikely to result in a risk to the rights and freedoms of
  natural persons**.
- If notification is not made within 72 hours it must be accompanied by **reasons for the delay**.
- A **processor** must notify the controller without undue delay after becoming aware of a breach.
- The notification must at least: describe the nature of the breach, including where possible the
  categories and approximate number of data subjects and of personal data records concerned;
  give the name and contact details of the data protection officer or other contact point;
  describe the likely consequences; and describe the measures taken or proposed to address the
  breach, including mitigation where appropriate.
- **Phased notification:** where it is not possible to provide all the information at the same
  time, it may be provided in phases without undue further delay. So do not wait for a complete
  scoping report if the clock is running; send what is known and supplement.
- The controller must **document any personal data breach** (facts, effects, remedial action
  taken) in a way that lets the supervisory authority verify compliance with the article. This
  applies even to breaches that are not notified.
- Where the data subjects must also be told, that is Article 34 (see the notification letters
  skill).

## 2. What IR gives counsel
The legal "notifiable" and "aware" determinations are counsel's. Supply, with the honest
confidence level and what is still unknown:
- the time the organisation became aware, written down and agreed with counsel, so the clock is
  not defaulted to the date the final report was written;
- data categories and approximate record and person counts matching the Article 33 content list;
- whether data was only reachable, accessed, or actually exfiltrated, and whether it was
  protected (for example encrypted with uncompromised keys), since that bears on the risk
  assessment;
- measures taken and proposed, and likely consequences, in terms usable in the notification.

State uncertainty plainly ("confirmed exfiltration of one table; cannot yet rule out others in
the same database") rather than rounding up to "contained".

## 3. Other regimes
Other jurisdictions and sectors (US state laws, sector rules, securities disclosure rules, card
brand rules) have their own triggers, deadlines and content, and are not covered by the source
for this skill. Establish with counsel which apply, based on where affected individuals are,
the data type and the organisation's sector, and read the current legal text for each.

## 4. Privilege
Counsel may direct the forensic work so that it is privileged. Confirm at kickoff whether the
engagement is privileged and follow counsel's communication protocol before writing findings
down.

## Verify
- [ ] The awareness date and time are documented and agreed with counsel.
- [ ] The first notification covers the four Article 33 content items, with gaps stated.
- [ ] A reasons-for-delay statement is ready if 72 hours will pass.
- [ ] The breach is recorded in the breach documentation whether or not it is notified.

## Checked
Checked 2026-11-08 against the full text of GDPR Article 33 on gdpr-info.eu. Removed because that
page does not state them: the interpretation of "aware" as reasonable certainty, Article 33(4)
paragraph numbering, the HIPAA 60-day, PCI and SEC 8-K four-day rules, claims about US state law
variation and safe harbours, and the privilege-waiver warning.
Method: docs-only read of cited pages, 2026-11-08
