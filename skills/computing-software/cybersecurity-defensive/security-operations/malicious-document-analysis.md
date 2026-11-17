---
id: computing-software.cybersecurity-defensive.security-operations.malicious-document-analysis
name: malicious-document-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [malware-analysis, maldoc-analysis, oletools, olevba, oleid, office-macros, pdf-analysis, pdfid, phishing-attachments]
level: advanced
status: docs-checked
description: "Triage suspicious Office and PDF attachments with oletools, XLMMacroDeobfuscator, pdfid and pdf-parser to extract macros, DDE links and embedded objects safely."
sources:
  - https://github.com/decalage2/oletools/wiki/olevba
  - https://github.com/decalage2/oletools/wiki/oleid
  - https://github.com/decalage2/oletools/wiki/oleobj
  - https://github.com/decalage2/oletools/wiki/msodde
  - https://github.com/DissectMalware/XLMMacroDeobfuscator
  - https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdfid.py
  - https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdf-parser.py
  - https://learn.microsoft.com/en-us/microsoft-365-apps/security/internet-macros-blocked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Malicious document analysis

**Goal:** decide whether an attachment is malicious and extract the next-stage URL or payload, without opening it in Office or a PDF reader. Work in an isolated analysis VM, never on a host with Office and macros enabled.

## Office (OLE and OOXML) with oletools
```
oleid invoice.doc                  # indicators: VBA macros, embedded objects/Flash, encryption, file type
olevba --decode invoice.docm       # extract macros, show obfuscated strings with decoded content, flag keywords
olevba --json invoice.xlsm > macros.json
msodde invoice.docx                # DDE / DDEAUTO links (also -a for all fields)
oleobj invoice.doc                 # extract embedded objects from OLE files
```
- `oleid` analyses OLE files for characteristics usual in malicious files: file type, VBA macros, embedded Flash, embedded OLE objects, Office encryption.
- `olevba` handles OLE (97-2003) and OOXML (2007+), XML, MHT, SLK, text VBA source and password-protected zip archives. It detects auto-executable macros, suspicious keywords, anti-sandbox tricks, decodes Hex/Base64/StrReverse/Dridex strings, deobfuscates expressions combining Chr, Asc, Val, StrReverse and Environ, and extracts IOCs (URLs, IP addresses, e-mail addresses, executable names). `--reveal` shows source with deobfuscated strings replaced; `--deobf` tries expression deobfuscation (slow).
- Keywords olevba lists in its sample output: `AutoOpen` and `Workbook_Open` (AutoExec, run on open); `Shell` (may run an executable), `Environ` (reads environment variables), `URLDownloadToFileA` (may download from the Internet).
- Password-protected Office files are still analysable by olevba because VBA macro code is never encrypted, only the document content.
- `msodde` extracts DDE and DDEAUTO links from Word, Excel, RTF, CSV and XML, and deobfuscates Word QUOTE obfuscation. `-p PASSWORD` tries decryption of encrypted files.
- Excel 4.0 (XLM) macros: olevba uses XLMMacroDeobfuscator when installed (`pip install oletools[full]`); or run it directly: `xlmdeobfuscator --file document.xlsm` (xls, xlsm, xlsb; no Excel needed).
- Since 2022 Microsoft 365 Apps block macros in files from the internet by default, using Mark of the Web (added by Windows to downloads and email attachments on NTFS). Files that lose the mark, or policy exceptions, can still run macros, so keep analysing.

## PDF with Didier Stevens' tools
```
pdfid suspicious.pdf                                   # keyword counts
pdf-parser --search javascript suspicious.pdf          # search indirect objects (not streams)
pdf-parser --object 12 --filter --raw suspicious.pdf   # show object 12, decode stream filters, raw output
pdf-parser --stats suspicious.pdf
```
- `pdfid` counts keywords including `/JS`, `/JavaScript`, `/AA`, `/OpenAction`, `/AcroForm`, `/RichMedia`, `/Launch`, `/EmbeddedFile`, `/XFA`, `/Encrypt`, `/ObjStm` and `/JBIG2Decode`.
- `pdf-parser --filter` passes streams through FlateDecode, ASCIIHexDecode, ASCII85Decode, LZWDecode and RunLengthDecode only. To find link targets, search objects for `URI`.

## Output
IOCs: payload URLs (defanged), dropped file hashes, macro hash, sender infrastructure. Actions: block URLs/domains, purge the message from all mailboxes, hunt for clicks and executions.

## Checked
Confirmed on 2026-11-08 against the oletools wiki pages (olevba, oleid, oleobj, msodde) and README, the XLMMacroDeobfuscator README, the pdfid.py and pdf-parser.py source, and Microsoft's "Macros from the internet are blocked by default" article. Removed as not stated in those pages: `Document_Open`, WScript.Shell and MSXML2 keywords, remote template injection, OneNote, LNK, ISO/IMG and HTML smuggling guidance (onedump.py, LECmd, lnkparse could not be read), the msoffcrypto default-password note, `/URI` as a pdfid keyword, and the CySA+ objective reference.
Method: docs-only read of cited pages, 2026-11-08
