---
id: computing-software.systems-network-administration.wireshark.export-imf-dicom-ftp-data-objects
name: export-imf-dicom-ftp-data-objects
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, export-objects, export-imf-objects, dicom, ftp-data, email-forensics]
level: practitioner
status: verified
description: "Extract emails (IMF), DICOM images and FTP-DATA files from captures with Wireshark Export Objects and tshark --export-objects, and check integrity."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export IMF, DICOM and FTP-DATA objects

File > Export Objects supports DICOM, FTP-DATA, HTTP, IMF, SMB, TFTP. HTTP/SMB are common;
these three are the less obvious ones.

## IMF (Internet Message Format, SMTP/IMAP/POP)
- Requires cleartext SMTP (port 25 without STARTTLS) or decrypted TLS.
- Export Objects > IMF lists each message by subject; save as `.eml` and open in a mail client or
  parse with Python's `email` package (there is no `python -m email`):
  `msg = email.message_from_binary_file(open(p,'rb'), policy=email.policy.default)`, then
  `for part in msg.iter_attachments(): part.get_filename(), part.get_content()`.
- If messages show as fragments, check TCP reassembly and `smtp.desegment_data` (reassemble the DATA command).
  (`smtp.decryption` only decodes Base64 AUTH parameters.)

## DICOM (medical imaging, TCP 104/11112)
- Export Objects lists DICOM among its object types (User's Guide); with the default `dicom.export_minsize` of 4096 bytes smaller items
  (including DICOM commands and responses) are not listed (set it to 0 to see them), and `dicom.export_header` adds a
  DICOM File Meta Header.
- The dissector registers TCP 104 (IANA acr-nema; 11112 is IANA `dicom`) and also recognised an A-ASSOCIATE
  request on port 11112 without Decode As; use Decode As > TCP port > DICOM if yours is not recognised.
- Treat output as patient data (PHI): handle under your data protection procedure.

## FTP-DATA
- Wireshark links the data connection to the control channel (PORT/PASV/EPSV), so the object name
  comes from the RETR/STOR command. Capture must include the control session.
- Passive mode on non-standard ports: if FTP-DATA is not recognised, check that the PASV reply was
  captured (and not on a different VLAN/interface). Checked with a `227 Entering Passive Mode (203,0,113,50,200,10)`
  reply (port 200*256+10 = 51210): the file was exported as `f.txt` from the RETR command.

## tshark
```
tshark -r in.pcapng -q --export-objects imf,./mail
tshark -r in.pcapng -q --export-objects ftp-data,./ftp
tshark -r in.pcapng -q --export-objects dicom,./dcm
sha256sum ./ftp/*
tshark --export-objects help         # lists dicom, ftp-data, http, imf, smb, tftp in 4.4.1
```

## Gotchas
- Truncated captures (snaplen) produce partial files with no warning; check the object size column.
- Duplicate object names are suffixed (`a`, `a(1)` in a test with two HTTP responses); keep the packet number for
  chain-of-custody notes.

## Verify
- [ ] Exported file size equals the protocol's announced size (SIZE reply, MIME length, DICOM length).

## Checked
Run with TShark 4.4.1 on synthetic captures: `--export-objects imf,./mail` wrote `Hi there.eml` from a plain SMTP DATA
transfer and the Python snippet read its subject and body; `--export-objects ftp-data,./ftp` wrote `f.txt` (16 bytes)
named from RETR over a passive data connection; `--export-objects help` listed dicom, ftp-data, http, imf, smb, tftp;
`python -m email` fails ("No module named email.__main__"); `smtp.decryption`, `smtp.desegment_data`,
`dicom.export_minsize` (4096) and `dicom.export_header` read with their help text from `tshark -G currentprefs`.
A hand-built A-ASSOCIATE request was decoded as DICOM on port 11112 with and without `-d`. IANA service-name CSV
confirmed `acr-nema` 104 and `dicom` 11112. The DICOM export behaviour is taken from the User's Guide and the preference
help text; no DICOM data transfer was generated.
