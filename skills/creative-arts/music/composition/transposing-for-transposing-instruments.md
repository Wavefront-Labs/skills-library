---
id: creative-arts.music.composition.transposing-for-transposing-instruments
name: transposing-for-transposing-instruments
category: creative-arts
field: music
product: composition
tags: [composition, arranging, music-theory, pitch-notation, music-notation, transposing-instruments, written-pitch, concert-pitch, transposition-chart, b-flat-instruments, e-flat-instruments, f-horn, clarinet, trumpet, alto-saxophone, tenor-saxophone, key-signature-transposition]
level: practitioner
status: draft
description: "Transpose parts between concert and written pitch for B-flat, E-flat, F and octave-transposing instruments, including key signatures, ranges and the checks that catch mistakes."
sources: ["https://www.abrsm.org/en-gb/exams/music-theory-exams", "https://viva.pressbooks.pub/openmusictheory/chapter/transposing-instruments/", "Samuel Adler, The Study of Orchestration (4th ed.), Appendix and instrument chapters", "Trinity College London Theory of Music Grade 5 syllabus (transposition)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transposing for transposing instruments

**Goal:** produce a written part that sounds the intended concert pitch, and read a
transposed score back to concert pitch.

## 1. The rule
An instrument "in X" sounds **X when it reads C**. If X is below C, the part is written
**higher** than concert by the interval from X up to C (B-flat: up a major 2nd). If X is
above C (E-flat clarinet, piccolo trumpet), the part is written lower.

| Instrument | Sounds | Write the part |
|---|---|---|
| Clarinet in B-flat, trumpet in B-flat, soprano sax | M2 lower | **up a major 2nd** |
| Clarinet in A | m3 lower | up a minor 3rd |
| Horn in F, cor anglais | P5 lower | **up a perfect 5th** |
| Alto sax, E-flat tenor horn (brass band) | M6 lower | up a major 6th |
| E-flat clarinet | m3 **higher** | down a minor 3rd |
| Tenor sax, bass clarinet (treble clef) | M9 lower | up a major 9th |
| Baritone sax | octave + M6 lower | up an octave + M6 |
| Guitar, double bass, contrabassoon | octave lower | up an octave |
| Piccolo, glockenspiel | octave(s) higher | down an octave (two for glock) |

## 2. Key signatures
- Transpose the **key**, then write that key signature: concert E-flat major for B-flat clarinet = F major (one flat).
- Alto sax: concert E-flat becomes C major. Horn in F: concert E-flat becomes B-flat major.
- If the transposed key has more than 6-7 accidentals, use the enharmonic key (concert B major for B-flat trumpet = C-sharp major (7 sharps): write D-flat major (5 flats)).
- Modern horn parts are often written **without key signature** with accidentals; follow the house style or the player's request.

## 3. Procedure
1. Write the concert line. 2. Transpose the key signature. 3. Move every note by the interval (by letter name first, then fix accidentals relative to the new key). 4. Check ranges in **written** pitch against the instrument's written range. 5. In software, enter at concert pitch and let the part transpose; turn on "transposing score" only for printing.

## Gotchas
- Interval direction errors are the most common fault: B-flat instruments are written **higher** than concert.
- Accidentals: concert F-sharp in a B-flat part becomes G-sharp, but concert B-natural in E-flat context needs checking letter by letter (C-sharp, not D-flat).
- Bass clef parts for bass clarinet or baritone (British brass band treble-clef parts are B-flat transposing; orchestral euphonium bass clef is concert).

## Verify
- Play the written part on a piano and transpose down the interval: it must match concert.
- In Dorico/Sibelius/MuseScore toggle concert pitch: notes should match your concert sketch.
