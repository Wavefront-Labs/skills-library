---
id: creative-arts.animation.storywriting.comedy-writing
name: comedy-writing
category: creative-arts
field: animation
product: storywriting
tags: [storywriting, comedy, jokes, humor, punch-up, rule-of-three, escalation, running-gag, callback, deadpan, dark-comedy, dialogue, adult-animation, sitcom, timing, subversion]
level: advanced
status: draft
description: "Comedy craft at the adult-animation bar: joke structure, rule of three, escalation ladders, character-logic comedy, punch-up passes, timing on the page vs the edit, callbacks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# comedy-writing

Goal: write and punch up comedy at the adult-animation bar — the register where a
joke must survive an audience that has seen every sitcom rhythm (think the
Rick & Morty / Venture Bros. density: fast, dark-capable, character-driven, never
winking at its own cleverness). This sits on top of
`creative-arts.animation.storywriting.screenwriting-craft` (structure, scene craft)
and hands timing downstream to `creative-arts.animation.editing.editorial-pacing`
and delivery to `creative-arts.animation.voice-tts.acting-performance`.

## Joke structure: setup, subversion

Every joke is a managed expectation. The **setup** installs a pattern; the
**punchline** breaks it at the last possible word.

- **Specificity is the setup's fuel.** "He had a bad childhood" sets up nothing;
  "his dad made him referee his parents' arguments" is already funny and sets up
  three more jokes. Vague setups force the punchline to do all the work.
- **The surprise goes at the end of the line.** English punchlines land on the
  final stressed word. "I've been stabbed before — emotionally, and also with a
  trowel" works; "with a trowel I was once stabbed, and also emotionally" is the
  same information, dead on arrival. Punch-up pass #1 is literally reordering
  sentences so the funny word is last.
- **Shortest path to the turn.** Every word between the pattern-break and the end
  of the line is decay. Cut "basically", "literally", "I mean" from punchlines
  always; they are padding the actor will add anyway if the character needs it.
- **Subversion types to rotate** (a script leaning on one type telegraphs):
  literalism (treating a figure of speech as fact), scale break (apocalyptic
  response to trivia, shrug at apocalypse), register break (clinical language for
  horror, profanity in bureaucracy), premise acceptance (character skips the shock
  a normal person would have — the Rick move: "yes it's an interdimensional
  parasite, the POINT is he owes me money"), and honesty spike (a character says
  the true thing social convention forbids).

## The rule of three

The minimum pattern is two; the break is the third. A, A′, **B**.
- Beats 1 and 2 must be *same shape, escalating slightly* — if beat 2 already
  breaks pattern, you wasted the three. "We've got sandwiches, we've got soup,
  we've got the crushing certainty that none of this matters" only works if
  sandwiches and soup were delivered flat.
- The third item should be **shorter or much longer** than the first two, never the
  same length — rhythm breaks with the logic.
- Fours are for when the joke *is* the overrun: the list that won't stop is a
  different gag (comic exhaustion), and it needs 6–8 items plus an interruption,
  not 4.
- Scene-level threes: the same rule runs at scene scale (two normal visits to the
  shopkeeper, the third goes wrong) and season scale (a runner's third appearance
  is where it mutates — see callbacks).

## Escalation ladders

A comic sequence is a ladder where each rung is a **new category of worse**, not a
bigger number.
- Wrong: fire → bigger fire → huge fire. Right: fire → the extinguisher is also on
  fire → the fire department arrives, for an unrelated arson, to arrest *him*.
  Escalate by *kind* (physical → social → existential), not degree.
- **Three to five rungs**, then out. Past five the audience is ahead of you; the
  topper has to be the thing they didn't price in.
- Each rung is caused by the character's **attempt to fix** the previous rung.
  Escalation that happens *to* a passive character is noise; escalation the
  character pumps by being themselves is story.
- The **topper** either cuts away at the peak (editorial's job — mark it
  `CUT TO:` and let `editorial-pacing` hold or kill it) or lands the ladder on the
  episode's theme (the fire was the inheritance he fought the whole episode for).
- The **relief rung**: after the topper, one flat beat of silence/normality before
  the next scene. Laughs need a floor to bounce off.

## Character-logic comedy vs gag comedy

The bar that separates sustainable series comedy from sketch:
- A **gag** is funny regardless of who's on screen (anvil falls). A **character-
  logic joke** is funny *because this specific person, with these specific wounds
  and this specific self-image, would say exactly this*. Gags spend; character
  logic compounds — the 40th episode's jokes get cheaper to set up because the
  audience co-owns the character model.
- Test: swap the line to another character. Still funny? It's a gag — fine in
  moderation, but if a whole scene survives the swap test, the scene has no
  comedic point of view.
- Build each regular a **comic engine**, one sentence: "X believes [flattering
  self-image] but is actually [truth], and under pressure chooses [signature wrong
  move]." Every character-logic joke is the gap between those clauses. Write the
  engine on a card; punch-up checks lines against it.
- Characters are never *in on* the joke. The moment a character acts funny on
  purpose (outside of characters who are canonically performers), the reality
  collapses and stakes die. The character pursues their want sincerely; the comedy
  is the collision (`twelve-principles` sincerity rule applies to writing too:
  play the want, not the laugh).

## Dialogue punch-up passes

Punch-up is a **separate pass** after the scene works dramatically — never punch up
a broken scene; jokes embalm structure problems. Run these in order:
1. **Funny-word-last pass** — reorder every intended laugh line.
2. **Specificity pass** — replace every generic noun in a setup or punch with the
   most characterful concrete one ("a car" → "a leased Kia he calls 'the
   business'").
3. **Cut-the-cushion pass** — delete hedges, repeated beats, and any line
   explaining a joke that just landed. If two laughs are adjacent, cut the weaker.
4. **Swap-test pass** — flag gags that any character could say; convert the best
   to character logic, keep two gags per scene max.
5. **Alt pass** — for each big laugh, write 3 alts fast without judging, then pick
   the one that's most *that character*; record runner candidates.
6. **Read-aloud pass** — comedy is breath-metered; any line you stumble reading,
   the performance will stumble (and local TTS scratch reads will stumble harder —
   test against the scratch-dialogue pipeline before locking).

## Comic timing: page vs edit

On the page you control *implied* rhythm; the edit controls real rhythm.
- Page tools: a line break is a micro-pause; a `(beat)` is a real pause — budget
  ~3 per episode or they stop meaning anything; white space around a line makes
  the reader hear it land; "..." is a character searching, not the writer
  stalling.
- Write the **air in**: a reaction shot is a written beat ("Dana stares.") — the
  funniest frame of many jokes is the listener, and if it isn't on the page,
  boards won't draw it and the edit can't cut to it.
- The edit owns the final laugh: cutting *on* the punch word versus one beat after
  changes the joke's species (sharp vs squirmy). Mark intent in the script
  (`CUT ON the word "trowel"`) and then defer — the rules for holding a deadpan
  stare 8 more frames or amputating a topper live in
  `creative-arts.animation.editing.editorial-pacing`. Write toppers you're willing
  to lose; the edit kills ~20% of written jokes for rhythm, and the script should
  survive that.

## Running gags and callbacks

- A runner needs: a strong first beat the audience *remembers*, a gap long enough
  to half-forget, and **mutation on return** — same shape, new context. Verbatim
  repetition works exactly twice; the third appearance must escalate or invert
  (the rule of three at season scale).
- Callback math: the laugh size is (surprise of recall) × (fit of new context).
  Late-episode callbacks to minute-one throwaways are the highest-value joke in
  television — plant 2–3 deliberately per episode by writing the throwaway *first*
  and the payoff in act three.
- Keep a **runner ledger** per season (gag, appearances, last mutation) — runners
  die from overuse at about appearance five unless they level up into plot
  (the best end state: the running gag turns out to be a gun on the mantel).

## Dark and deadpan registers

- Dark comedy is a **contract about aim**: the joke targets the absurdity of the
  horror, the systems around it, or the coping — hitting the victim's pain
  directly reads as cruelty and loses the room. You can joke *at* the funeral; you
  don't joke at the widow (unless the widow is the one joking — self-aimed dark
  comedy is the most durable kind).
- Earn dark beats with sincerity beats: a show that is only irony has no blood
  pressure, and its dark jokes stop registering. One genuinely felt moment per
  episode recharges the whole register (this is the Rick & Morty trick nobody
  copies: the sad beats are played completely straight).
- Deadpan is a *performance and edit* register: flat line, no musical sting, hold
  the shot ~8–16 frames past comfort. On the page, write it as "(flat)" once and
  trust it; for scoring, mark the moment **no sting** — the absence is the joke
  (brief `creative-arts.animation.sound-design.scoring` which silences are
  load-bearing).

## Comedy serving theme

Jokes are argument. Each episode's comic engine should restate its theme: if the
episode is about a character's terror of being ordinary, the jokes land hardest
when they puncture exactly that self-image — and the one moment nobody jokes
becomes the thematic X-ray. Audit the outline: if the biggest laugh and the
thematic turn are unrelated scenes, the laugh is borrowed from a different
episode. Comedy that mocks the theme's stakes ("none of this matters lol") is the
one register to ban — undercutting is fine beat to beat, but the *final* beat of
the episode must leave the theme standing.

## Worked punch-up example

Flat draft:
> MIRA: I'm not going back in the cave. It's dangerous and last time you left me
> there for hours.

Pass 2 (specificity) + pass 1 (funny word last):
> MIRA: I'm not going back in the cave. You left me there for six hours with
> nothing but a protein bar and your climbing harness.

Pass 5 (alts, pick the character-logic one — Mira's engine: *believes she's the
only professional on the team, actually desperate to be needed, under pressure
keeps score*):
> MIRA: I'm not going back in the cave. Last time you forgot me for six hours.
> JOEL: We came back!
> MIRA: For the harness, Joel. You came back for the harness.

The topper is a callback-ready runner ("the harness") — ledger it; its third
appearance should invert (Joel finally comes back for *her*, abandons the
harness, and it mattered).

## Verify

- [ ] Every intended laugh line ends on its funny/stressed word; no hedge words
      inside punchlines.
- [ ] Rule-of-three instances: beats 1–2 same shape and flat, beat 3 breaks
      pattern and length.
- [ ] Each escalation ladder: 3–5 rungs, each a new *category*, each caused by the
      character's fix attempt, with a relief beat after the topper.
- [ ] Swap test run: ≤ 2 pure gags per scene; every other laugh traceable to a
      character's stated comic engine.
- [ ] Punch-up only performed on scenes that already work with the jokes removed.
- [ ] Reaction beats written on the page where the listener is the joke; cut
      points marked but not enforced (editorial owns final timing).
- [ ] Runner ledger updated; every runner's next appearance has a planned
      mutation; at least 2 act-one plants pay off in act three.
- [ ] Dark jokes aim at absurdity/systems/coping, not victims; at least one
      sincere, unjoked beat survives per episode; final beat leaves theme intact.
- [ ] Read-aloud pass done; script still works if the weakest 20% of jokes are
      cut in the edit.
