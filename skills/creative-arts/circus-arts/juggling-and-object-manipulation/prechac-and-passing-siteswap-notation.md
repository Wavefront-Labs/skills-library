---
id: creative-arts.circus-arts.juggling-and-object-manipulation.prechac-and-passing-siteswap-notation
name: prechac-and-passing-siteswap-notation
category: creative-arts
field: circus-arts
product: juggling-and-object-manipulation
tags: [juggling-and-object-manipulation, circus-arts, club-passing, passing-patterns, prechac, passing-siteswap, siteswap-notation]
level: practitioner
status: draft
description: "Read passing siteswap and Prechac notation: how synchronised multi-juggler notation extends vanilla siteswap, how to mark passes, and how to verify a passing pattern on paper."
sources: ["Library of Juggling - https://libraryofjuggling.com", "Juggling Information Service - https://www.juggling.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prechac and passing siteswap

Passing siteswap extends vanilla siteswap so that several jugglers' patterns are written together. Each juggler's throw is a number as in vanilla siteswap; a throw to another juggler is marked as a pass, usually with a letter such as `p` after the number, optionally followed by the juggler it goes to.

## Reading it
- Write each juggler's sequence between angle brackets, with a vertical bar between jugglers: for example `<3p 3|3p 3>` for two jugglers each with the same sequence. Pass throws are labelled `3p`.
- The numbers keep their vanilla meaning: the number of beats until that club is thrown again. The average per juggler is the clubs in that juggler's hands, and the overall sum divided by the total throw count gives the number of clubs in the pattern.
- Throws alternate hands as in vanilla siteswap (right, left, right ...) for each juggler.

## Prechac notation
Prechac notation is a related system used in the passing community to describe passing patterns with fractional throw heights. I do not have a reliable verified spec to reproduce here; see the Library of Juggling (https://libraryofjuggling.com) and the passing siteswap pages at the Juggling Information Service (https://www.juggling.org).

## Checking a pattern
1. Write the sequence for both jugglers on a ladder diagram.
2. Verify that the average equals the number of clubs per juggler.
3. Check that no club lands twice on the same beat (the collision test of vanilla siteswap, applied to the combined sequences).
4. Run a simulator or generator and verify the output for the same notation.

## Practical use
- Use notation to share patterns between partners; always agree the handedness and who starts.
- Learn the pattern slowly by walking through the throws with one club first.

## Verify
- [ ] You can explain what each element of a passing siteswap line means.
- [ ] You can collision-check a short passing pattern on paper.
