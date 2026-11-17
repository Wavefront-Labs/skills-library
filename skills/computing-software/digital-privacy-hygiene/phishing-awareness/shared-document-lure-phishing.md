---
id: computing-software.digital-privacy-hygiene.phishing-awareness.shared-document-lure-phishing
name: shared-document-lure-phishing
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, shared-document-phishing, credential-phishing, phishing]
level: practitioner
status: draft
description: "Spot phishing that arrives as real Google Docs, OneDrive, Dropbox or DocuSign share notifications, and open shared files safely from the service itself."
sources:
  - "https://support.google.com/docs/answer/10200637"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
  - "https://www.docusign.com/trust/alerts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Shared document lure phishing

**Goal:** don't hand over your password via a real-looking "X shared a file with you" message.

## How it works
Attackers use legitimate services so emails pass filters: a real Google Docs share or comment mention, a real
Dropbox/OneDrive share, or a DocuSign/Adobe Sign-styled email. The document contains a link ("View invoice",
"Open secure file") to a credential phishing page.

## Checks
- **Who shared it?** The notification shows the real sharing account; is it someone you deal with, from their usual
  address? Compromised accounts of real contacts are common.
- **Did you expect it?** Unsolicited invoices, "payroll update", "contract to sign".
- **Where does the button go?** It should stay on docs.google.com / sharepoint.com / dropbox.com. A document page
  that then asks you to "log in to view" on another domain is phishing.
- **DocuSign:** go to docusign.com > Access documents and enter the security code from the email, rather than
  clicking.

## Safe habit
Open shared files from the service's own app or "Shared with me" list, not from email links. If the file asks for a
login again after you're already signed in, stop.

## If you clicked and entered credentials
Change password, revoke sessions, check for OAuth grants and mailbox rules (see credential compromise response).

## Gotchas
- Google lets you report "spam" on shared docs; do it to help block the sender.
- Real colleagues' accounts get used; confirm by message on another channel.
