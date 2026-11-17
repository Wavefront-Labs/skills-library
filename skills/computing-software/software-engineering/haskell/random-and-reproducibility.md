---
id: computing-software.software-engineering.haskell.random-and-reproducibility
name: random-and-reproducibility
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, random, stdgen, splitmix, randomrio, newstdgen, uniformr, mwc-random, reproducible-randomness, crypton-entropy, random-and-reproducibility]
level: practitioner
status: docs-checked
description: "Generate random values with the random package (mkStdGen, randomR, uniformRM, globalStdGen, split), seed for reproducibility, and get secrets from entropy, not StdGen."
sources: ["https://hackage.haskell.org/package/random/docs/System-Random.html", "https://hackage.haskell.org/package/entropy", "https://hackage.haskell.org/package/mwc-random", "https://hackage.haskell.org/package/pcg-random"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Randomness

**Goal:** get random values reproducibly, and know when not to use `random`.

```haskell
import System.Random

main = do
  let g = mkStdGen 42                          -- deterministic seed
      (x, g') = randomR (1, 6 :: Int) g        -- random 1.x API; uniformR in the newer 'Uniform' API
      xs = take 5 (randomRs (1, 6 :: Int) g')
  n <- randomRIO (1, 100 :: Int)               -- uses the global generator (IO)
  r <- uniformRM (0, 1 :: Double) globalStdGen -- random >= 1.2 monadic API
  print (x, xs, n, r)
  let (g1, g2) = split g                        -- independent streams
```

## Facts
- `StdGen` is the standard pseudo-random generator; it is an instance of `RandomGen` and uses the SplitMix implementation from the `splitmix` package. `Uniform` and `UniformRange` classes drive `uniformR`/`uniformRM`; `randomR`, `randomRs` and `randomRIO` also exist.
- The generator used before random 1.2 (L'Ecuyer) was replaced by SplitMix in 1.2, so the same seed gives different values than older versions; pin the version if you store seeds.
- `split` turns one generator into two, for independent streams per task; `globalStdGen` is the shared global generator.
- Other pseudo-random packages: `mwc-random` (fast, high quality) and `pcg-random`.

## Security
`StdGen` is a deterministic pseudo-random generator seeded by you, so it is the wrong source for tokens, keys and nonces. The `entropy` package provides `getEntropy` to get random bytes from the system.

## Gotchas
- Check the `System.Random` docs for whether a range includes its endpoints before relying on it for `Double`.

## Self-check
- [ ] Tests that depend on randomness print or fix the seed.
- [ ] Secrets are generated from the system entropy source.

## Checked
2026-11-03. Confirmed against the `System.Random` Haddock page (`mkStdGen`, `randomR`, `randomRs`, `randomRIO`, `uniformRM`, `globalStdGen`, `split`, SplitMix, L'Ecuyer replaced in 1.2, `Uniform`/`UniformRange`) and the entropy, mwc-random and pcg-random package pages (`getEntropy`). Removed: shuffle and weighted-choice advice, `random-fu`, `crypton`'s `getRandomBytes`, the performance and clock-seeding gotchas, and the "not cryptographically secure" wording (rewritten to what the pages state).
Method: documentation only; no commands were run.
