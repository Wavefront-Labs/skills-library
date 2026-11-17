---
id: creative-arts.game-design.puzzle-design.cipher-and-word-puzzles
name: cipher-and-word-puzzles
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, puzzle-types, cipher-puzzles, wordplay-puzzles, substitution-cipher, escape-room, codes, anagrams]
level: practitioner
status: draft
description: "Design cipher and word puzzles (substitution, pigpen, Caesar, acrostics, anagrams) that are solvable: confirmable extraction, partial keys, and checking for ambiguous answers."
sources:
  - https://en.wikipedia.org/wiki/Substitution_cipher
  - https://www.puzzledpint.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cipher and word puzzles

**Goal:** puzzles where decoding feels like discovery, players know when they are on the
right track, and the answer is unambiguous.

## Common types
| Type | Mechanism | Difficulty knob |
|---|---|---|
| Caesar / shift | each letter shifted by n | give n, or a hint to find it |
| Simple substitution | letter-to-letter mapping | provide partial key; length of text |
| Symbol ciphers (pigpen, semaphore, Braille, Morse) | known public codes | provide or hint the key |
| Acrostic | first letters spell the answer | how hidden the list is |
| Anagram | rearrange letters | length; enumeration given (e.g. 5,4) |
| Indexing | take the nth letter of each answer | numbers given or hidden |
| Wordplay / cryptic clue | definition + wordplay | cryptic conventions knowledge |

## Design rules
1. **Confirmable progress:** partial decoding should already produce recognisable words,
   so players know they are right before finishing.
2. **Extraction is explicit or signposted:** if the answer is "the first letters", give
   a hint (blank lines with numbers, an "ordered" cue).
3. **One answer:** check that no alternative reading fits (especially anagrams and
   indexing).
4. **Accessible keys:** public codes (Morse, Braille) are fine if the puzzle signals the
   code or provides it in-world.
5. **Length:** long substitution texts are tedious by hand; keep ciphertext short in
   escape rooms (time limit), longer in puzzle hunts.

## Testing
- Solve it yourself from a cold copy after a few days.
- Test-solve with people who have not seen it; time them; note wrong paths.
- For anagrams, run the letters through an anagram solver to find unintended answers.

## Gotchas
- Fonts can make symbols ambiguous (0/O, 1/l/I); choose clear typography.
- Colour-dependent codes exclude colour-blind players; add shape or pattern.
- Ciphers requiring outside knowledge (a specific book) need that resource provided.

## Verify
- [ ] Partial decoding yields recognisable words.
- [ ] Extraction method signposted.
- [ ] Alternative answers checked (solver for anagrams).
- [ ] Cold test-solve completed and timed.
