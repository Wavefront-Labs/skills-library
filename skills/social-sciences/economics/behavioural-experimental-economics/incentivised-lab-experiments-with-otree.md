---
id: social-sciences.economics.behavioural-experimental-economics.incentivised-lab-experiments-with-otree
name: incentivised-lab-experiments-with-otree
category: social-sciences
field: economics
product: behavioural-experimental-economics
tags: [behavioural-experimental-economics, experimental-economics, behavioural-economics, lab-experiments, field-experiments, online-experiments, otree, ztree, incentive-compatibility, induced-value, random-incentive-system, pay-one-randomly, no-deception, public-goods-game, ultimatum-game, dictator-game, trust-game, risk-elicitation, holt-laury, bomb-risk-task, time-preferences, belief-elicitation, binarized-scoring-rule, strategy-method, prolific, orsee, hroot, matching-groups, session-effects, pre-registration]
level: advanced
status: gated
description: "Design and run an incentivised economics experiment: induced values, payment rules, standard game paradigms, oTree implementation, recruitment, matching groups and analysis at the right level."
sources: ["Smith (1976), American Economic Review 66(2)", "Chen, Schonger & Wickens (2016), Journal of Behavioral and Experimental Finance 9", "Holt & Laury (2002), American Economic Review 92(5)", "oTree documentation (otree.readthedocs.io)", "Friedman & Sunder, Experimental Methods (Cambridge 1994)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incentivised economics experiments — design, oTree, analysis

**Goal:** an experiment where participants' choices respond to the incentives you
designed, with clean treatment comparisons and inference at the level of independent
observations.

## 1. Design principles (induced value)
- **Monotonicity and salience:** payoffs increase in performance and depend on choices
  participants understand. Payments must be large enough to matter — typical lab rates aim
  above local hourly wages; online platforms set minimum hourly rates (Prolific publishes
  its own floor).
- **Dominance:** the reward outweighs subjective costs of thinking (boredom, effort).
- **No deception** — a strong norm in experimental economics; many labs and journals reject
  studies that deceive. Use neutral framing ("option A") unless framing is the treatment.
- **Between vs within subjects:** between avoids order and demand effects; within gains
  power. If within, counterbalance order.

## 2. Payment rules
- **Pay one randomly selected decision/round** (random incentive system) to avoid wealth
  and portfolio effects; it is standard, though its validity under non-expected-utility
  preferences is debated.
- Show-up fee plus earnings; pay privately.
- **Beliefs:** elicit with incentivised rules. Quadratic scoring is not incentive
  compatible for risk-averse people; the **binarized scoring rule** is robust to risk
  attitudes. Keep the explanation simple ("the closer your guess, the higher your chance of
  winning the bonus").

## 3. Standard paradigms
| Construct | Task |
|---|---|
| Altruism | Dictator game |
| Fairness/punishment | Ultimatum game (often via **strategy method**: responders state a minimum acceptable offer) |
| Trust/reciprocity | Trust (investment) game |
| Cooperation | Linear public goods game, with/without punishment |
| Risk | Holt–Laury price list (watch multiple switching), bomb risk elicitation task |
| Time preference | Convex time budgets or price lists with front-end delay |
Reuse published instructions and parameters where possible for comparability.

## 4. Implementing in oTree
oTree (Python/Django-based, browser-run) is the current default; z-Tree remains in many
physical labs.
- Structure: an **app** per stage with `Constants`/`C`, `Subsession`, `Group`, `Player`
  models and `Page` classes; `SESSION_CONFIGS` in `settings.py` set treatments, with
  `participation_fee` and `real_world_currency_per_point` in `SESSION_CONFIG_DEFAULTS` (or overridden per config) (checked in a fresh oTree 6.0.15 project from `otree startproject`).
- Set treatment per session (config) or randomise per participant in `creating_session`;
  store it as a player field.
- Use **WaitPages** for group synchronisation; plan dropouts online (timeouts with
  `timeout_seconds` and default decisions; flag bots replacing dropouts).
- Comprehension quiz before the main task; require correct answers to proceed.
- Test with bots (`otree test <session_config>`; each app needs a bot module, and the stock sample apps in 6.0.15 raised ModuleNotFoundError for `tests` when run), then a pilot session.
- Deploy on a server (e.g. Heroku-like host or institutional server) with HTTPS; export data as CSV.

## 5. Recruitment and sessions
Lab pool via ORSEE or hroot; online via Prolific (better data quality than MTurk in
several comparisons). Exclude prior participants of related studies. Randomise sessions
to treatments, and balance time-of-day and experimenter.

## 6. Analysis
- **Independence:** in repeated interactions with re-matching, observations within a
  **matching group** are not independent. The unit is the matching group (or session for
  some designs). Use stranger matching within fixed matching groups of, e.g., 8–12 so you
  get several independent units per session.
- Non-parametric tests on independent-unit averages (Mann–Whitney, permutation), plus
  regressions with SEs clustered at the matching group/session (few clusters → wild bootstrap).
- Pre-register hypotheses, primary outcomes and exclusion criteria (AsPredicted, OSF, AEA registry).

## Gotchas
- Lab currency ("points") with confusing exchange rates; state both clearly.
- Session effects — two sessions per treatment is the bare minimum.
- Online attention: add timing checks; avoid treating fast but valid responders as inattentive.

## Verify
- [ ] Incentives salient, monotonic and large enough; payment rule explained.
- [ ] No deception; instructions neutral; comprehension checked.
- [ ] Treatment assignment stored in the data; bots tested.
- [ ] Matching-group structure provides enough independent units for the power analysis.
- [ ] Pre-registration time-stamped before data collection.

*Checked 2026-10-19 with oTree 6.0.15 (pip, Python 3.12): `otree startproject` sample apps use `class C(BaseConstants)`, `Subsession`, `Group`, `Player`, `WaitPage`, `creating_session` and `timeout_seconds` exists in the API stubs; CLI has devserver, prodserver, resetdb, test. The scoring-rule claims (quadratic scoring not incentive compatible under risk aversion; binarized scoring) and the Prolific/MTurk quality comparison were not re-read (gated: unconfirmed, source is paywalled or blocked). oTree names change between versions; check your version's docs.*
