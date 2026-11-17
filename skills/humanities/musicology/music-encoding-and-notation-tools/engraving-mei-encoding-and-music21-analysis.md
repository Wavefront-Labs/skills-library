---
id: humanities.musicology.music-encoding-and-notation-tools.engraving-mei-encoding-and-music21-analysis
name: engraving-mei-encoding-and-music21-analysis
category: humanities
field: musicology
product: music-encoding-and-notation-tools
tags: [music-encoding-and-notation-tools, notation-software, music-engraving, musescore, sibelius, dorico, finale, lilypond, musicxml, mei, music-encoding-initiative, verovio, tei, critical-apparatus, app-lem-rdg, omr, optical-music-recognition, audiveris, music21, python, humdrum, kern, computational-musicology, corpus-analysis, digital-edition, mei-friend, xml]
level: practitioner
status: draft
description: "Use notation and encoding tools for scholarship: MusicXML/MEI exchange, MEI variant markup rendered with Verovio, OMR cleanup, and music21 corpus queries for computational musicology."
sources: ["Music Encoding Initiative Guidelines (MEI 5)", "Verovio documentation (book.verovio.org)", "music21 User's Guide (web.mit.edu/music21)", "W3C MusicXML 4.0 specification", "Audiveris handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Engraving, MEI encoding and music21 analysis

**Goal:** pick the right format for the job, move music between tools without silent
loss, and encode editions and corpora that can be queried, not just printed.

## 1. Which tool, which format
| Need | Use |
|---|---|
| Printed edition, engraving quality | Dorico, Sibelius, MuseScore 4, LilyPond |
| Interchange between notation programs | **MusicXML** (`.musicxml`/`.mxl`) |
| Scholarly encoding, variants, editorial markup | **MEI** (`.mei`) |
| Large-corpus analysis | **music21** (Python), Humdrum `**kern` |
| Web display of encodings | **Verovio** (MEI, MusicXML, Humdrum → SVG) |
Finale was discontinued by its maker in 2024; plan to migrate Finale files via
MusicXML while they still open (check current status).

## 2. Moving between tools
- Export **MusicXML**, re-import, and **diff visually**: lyrics, slurs across systems,
  ornaments, tuplets, cue notes, and part/score layout are what usually break.
- Layout doesn't survive interchange reliably; content mostly does. Fix layout last.
- Keep the native file *and* the MusicXML/MEI as the archival copy.

## 3. MEI for editions
MEI encodes the musical content plus scholarly apparatus (modelled on TEI):
```xml
<app>
  <lem source="#A"><note pname="f" oct="5" accid="s" dur="4"/></lem>
  <rdg source="#B"><note pname="f" oct="5" dur="4"/></rdg>
</app>
<supplied reason="omitted" resp="#editor"><dynam>p</dynam></supplied>
```
Declare sources (`<source xml:id="A">`) in the header (`<meiHead>`). Edit in an XML
editor (Oxygen) or **mei-friend** in the browser, validate against the MEI schema
(RNG), and render with Verovio:
```
pip install verovio
python -c "import verovio; tk=verovio.toolkit(); tk.loadFile('edition.mei'); open('p1.svg','w').write(tk.renderToSVG(1))"
```
For the editorial reasoning behind `app`/`lem`/`rdg` see
humanities.musicology.music-source-studies.collation-and-critical-editions-of-music.

## 4. OMR (scanning scores to data)
Audiveris (open source) or commercial tools (e.g. PhotoScore, ScanScore) turn scans into
MusicXML. Expect errors in: rhythms in dense passages, ties vs slurs, accidentals,
clef changes, text. Budget proofreading time per page; scan at 300–400 dpi greyscale,
deskewed. Proofread against the source, not against what "sounds right".

## 5. music21 for corpus questions
```python
from music21 import corpus, converter, roman
s = corpus.parse('bach/bwv66.6')          # or converter.parse('file.musicxml')
k = s.analyze('key')                      # Krumhansl-type key estimate
print(k, k.correlationCoefficient)
ch = s.chordify()
for c in ch.recurse().getElementsByClass('Chord'):
    print(c.measureNumber, roman.romanNumeralFromChord(c, k).figure)
```
Use it to count intervals, find cadential patterns, extract melodies, or check set
classes (`chord.Chord([...]).forteClass`). Automated Roman numerals and key-finding are
**estimates**; spot-check against your own analysis and report the error rate.

## Gotchas
- MusicXML from different programs differs in detail; test your exact export path.
- Encoding conventions (how you mark ficta, editorial slurs) must be written down
  before a team starts, or the corpus becomes inconsistent.
- music21 API names change between versions (e.g. `.flat` → `.flatten()`); pin the version.
- Status: draft; code snippets are indicative and should be run against your installed versions.

## Verify
- [ ] Round-tripped files were visually checked for the usual losses.
- [ ] MEI validates against the schema and renders in Verovio.
- [ ] Every `rdg`/`lem` cites declared sources.
- [ ] OMR output was proofread bar by bar against the scan.
- [ ] Computational results report library version and a manual spot-check.
