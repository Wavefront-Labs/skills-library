---
id: computing-software.digital-forensics-incident-response.evidence-handling.parsing-mobile-extractions-with-ileapp-and-aleapp
name: parsing-mobile-extractions-with-ileapp-and-aleapp
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [ileapp, aleapp, mobile-forensics, ios-forensics, android-forensics, dfir]
level: practitioner
status: draft
description: "Parse iOS and Android extractions with iLEAPP and ALEAPP: supported inputs, running modules, reading reports, timeline/KML outputs and validation."
sources: ["https://github.com/abrignoni/iLEAPP", "https://github.com/abrignoni/ALEAPP"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parsing mobile extractions with iLEAPP and ALEAPP

**Goal:** free, open-source parsers (Alexis Brignoni et al.) that turn FFS and backup extractions
into HTML/TSV reports covering hundreds of artefacts; ideal for validation of commercial tools.

## Inputs
- iLEAPP: iOS full file system as folder, `.tar`/`.zip` (e.g. from commercial FFS), iTunes backup
  folder (decrypt encrypted backups first), and some logical outputs.
- ALEAPP: Android FFS folder/tar/zip, Android backups, Google Takeout (with RLEAPP for returns).

## Run
```bash
python ileapp.py -t tar -i extraction.tar -o out/          # types: fs, tar, zip, itunes, gz
python aleapp.py -t zip -i android_ffs.zip -o out/
python ileappGUI.py                                         # GUI: pick modules
```
- `-p` / profile options to select modules; run all on first pass, then targeted.
- Outputs: `index.html` report by category, TSV per artefact, timeline database
  (`_Timeline/tl.db`), KML for location artefacts, and a processing log listing modules that errored.

## High-value modules (iOS)
KnowledgeC / Biome app usage, Screen Time, Photos.sqlite (with locations), SMS/iMessage
(`sms.db`), Safari history, Interactions, location (Cache.sqlite, routined), WiFi, installed apps
and app containers, notifications.

## Validation workflow
- Compare counts and sample records with the commercial tool (Cellebrite/Magnet/Oxygen) for
  key artefacts; differences are case-relevant (deleted records, unsupported versions).
- Open the source database in a SQLite browser and run the module's query by hand for any
  record you rely on in a report.

## Gotchas
- Artefact schemas change with each iOS/Android release; check the module supports the OS version.
- Times: Apple Cocoa epoch (2001-01-01) vs Unix; the report converts, raw TSV may not.

## Verify
Every reported artefact is traced to source path and record, and the processing log shows no errors for relied-on modules.
