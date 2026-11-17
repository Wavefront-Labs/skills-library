---
id: computing-software.digital-forensics-incident-response.incident-response-process.ransom-note-extension-and-encryptor-triage
name: ransom-note-extension-and-encryptor-triage
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ransom-note, ransomware, ransomware-identification, encryptor-triage, dfir]
level: practitioner
status: draft
description: "Triage a ransomware event from its ransom note, file extension and encryptor: identify the family safely, check for decryptors, find patient zero and the encryption start time."
sources: ["https://id-ransomware.malwarehunterteam.com/", "https://www.nomoreransom.org/", "https://www.cisa.gov/stopransomware/ransomware-guide", "https://github.com/cert-polska/mquery"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ransom note, extension and encryptor triage

The first hour of a ransomware case needs three answers: which family (drives decryptor options, leak-site risk, typical TTPs), when encryption began, and from where.

## Collect safely
- Copy one ransom note, two or three encrypted files with their originals if available (e.g. from backup), and note the new extension. Do not open notes in a browser on a production host (some are HTML with tracking).
- Do not contact the actor or visit the Tor portal from a corporate network; leave negotiation to counsel and specialists.
- If a running encryptor process exists, image memory before killing it; keys can sometimes be recovered.

## Identify the family
1. Upload the note and one encrypted sample (not sensitive originals) to ID Ransomware, or compare manually: note filename (`README.txt`, `RESTORE-MY-FILES.TXT`), contact method, victim ID format, extension pattern (fixed `.lockbit`, random per victim, appended email).
2. Inspect an encrypted file header/footer: many families append a marker or encrypted key blob of fixed size.
3. Check NoMoreRansom and vendor decryptor lists for that family and version.
4. Search threat intel for the actor's leak site and whether they exfiltrate first (double extortion changes notification duties).

## Find timing and origin
- Encryption start: earliest modified time of encrypted files / note creation in `$MFT` or `$UsnJrnl`; Defender/EDR detection times; shadow-copy deletion events (`vssadmin delete shadows`, `wmic shadowcopy delete`), service stops.
- Spread method: encrypted files on shares point to a host writing over SMB; check file server logs (5145) for the writing account and source IP. ESXi: `/var/log/hostd.log` and `shell.log`.
- Recover the encryptor binary from the source host (often in `%SystemDrive%\Windows\Temp`, `%SystemDrive%\Users\Public`, a GPO scheduled task or PsExec-pushed service) and hash it.

## Gotchas
- The extension is a weak identifier; affiliates re-use builders (LockBit, Babuk and Conti leaks) so family names can mislead.
- Wipers disguised as ransomware exist; no working contact or a destroyed key blob suggests a wiper.
- Encryption time is the end of the intrusion, not the start; the investigation continues backwards days or weeks.

## Verify
Family identification is supported by at least two indicators (note format plus file marker or binary analysis), and patient zero is backed by file-system or log evidence.
