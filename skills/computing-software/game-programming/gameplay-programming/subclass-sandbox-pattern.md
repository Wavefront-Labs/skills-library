---
id: computing-software.game-programming.gameplay-programming.subclass-sandbox-pattern
name: subclass-sandbox-pattern
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, subclass-sandbox, template-method, superpowers, base-class-api, game-programming]
level: practitioner
status: docs-checked
description: "Use the Subclass Sandbox pattern: a base class exposing protected primitives so many small subclasses implement one activate() without engine coupling."
sources: ["https://gameprogrammingpatterns.com/subclass-sandbox.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subclass Sandbox pattern

**Goal:** dozens of small behaviours (superpowers, abilities, pickups) written by many people, each
coupled only to one base class instead of to audio, physics, particles and the scene graph
(Nystrom, GPP "Subclass Sandbox").

## Shape
```cpp
class Superpower {
public:
    virtual ~Superpower() = default;
protected:
    virtual void activate() = 0;                        // the sandbox method subclasses implement
    // Provided operations: the only API subclasses use.
    void move(double x, double y, double z)  { /* calls physics */ }
    void playSound(SoundId s, double volume) { soundPlayer().play(s, volume); }
    void spawnParticles(ParticleType t, int n);
    double getHeroX() const; double getHeroZ() const;
    SoundPlayer& soundPlayer() { return *soundPlayer_; }   // or forward via a service locator
private:
    static SoundPlayer* soundPlayer_;                    // set once by the engine
};

class SkyLaunch : public Superpower {
protected:
    void activate() override {
        if (getHeroZ() == 0) { playSound(SOUND_SPROING, 1.0); spawnParticles(PARTICLE_DUST, 10); move(0, 0, 20); }
        else { playSound(SOUND_SWOOP, 1.0); move(0, 0, getHeroZ() - 20); }
    }
};
```

## Decisions
- **What to provide:** operations used by many subclasses, or ones that touch engine systems whose
  coupling you want centralised. Trivial pass-throughs that just forward one call add little.
- **Avoid a bloated base:** group provided ops into helper objects (`soundPlayer().play()`,
  `particles().spawn()`) so the base stays small.
- **How the base gets its dependencies:** constructor injection makes every subclass constructor
  pass them. The book weighs constructor arguments (every derived constructor must pass them along),
  two-stage initialization, and private static state in the base class that the game must
  initialize once.

## When not to use
The pattern pushes coupling up into the base class, which can grow large; the book suggests
splitting provided operations into separate classes the base hands off to (the Component
pattern can help). It yields a shallow but wide hierarchy, so it suits many small,
programmer-written behaviours.

## Checked
2026-11-01. Confirmed against Game Programming Patterns, Subclass Sandbox chapter: protected
non-virtual provided operations, abstract protected sandbox method, coupling moved to the base,
shallow-but-wide hierarchy, the constructor / two-stage init / static state options, Component
suggestion. Removed: Unreal and Unity ability-system equivalents, template-method cooldown
advice, Type Object comparison.
Method: documentation only; no commands were run.

## Verify
- [ ] Subclass files include only the base header, not audio/physics headers.
- [ ] Changing the sound API touches only the base class.
