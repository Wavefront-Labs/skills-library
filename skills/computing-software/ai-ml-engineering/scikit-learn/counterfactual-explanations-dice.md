---
id: computing-software.ai-ml-engineering.scikit-learn.counterfactual-explanations-dice
name: counterfactual-explanations-dice
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, counterfactual-explanations, dice-ml, algorithmic-recourse, explainable-ai, what-if]
level: practitioner
status: verified
description: "Generate counterfactual explanations with DiCE for scikit-learn models: what minimal feature changes flip a prediction, with immutable features, ranges and diversity."
sources:
  - https://github.com/interpretml/DiCE
  - https://interpret.ml/DiCE/
  - https://arxiv.org/abs/1905.07697
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Counterfactual explanations (DiCE)

A counterfactual answers "what is the smallest realistic change to this applicant's features that would change the decision?" Useful for recourse (adverse-action explanations) and model debugging.

## Setup
```python
import dice_ml
d = dice_ml.Data(dataframe=train_df, continuous_features=["age", "income", "debt"], outcome_name="approved")
m = dice_ml.Model(model=pipe, backend="sklearn", model_type="classifier")   # full Pipeline taking raw columns
exp = dice_ml.Dice(d, m, method="random")        # "random", "genetic", or "kdtree" for sklearn models
cf = exp.generate_counterfactuals(query_df.iloc[[0]], total_CFs=4, desired_class="opposite",
                                  features_to_vary=["income", "debt", "loan_amount"],
                                  permitted_range={"income": [0, 200000], "debt": [0, 50000]})
cf.visualize_as_dataframe(show_only_changes=True)
```

## Make them actionable
- `features_to_vary`: exclude immutable or protected attributes (age, race, sex) and things the person cannot change.
- `permitted_range` keeps values realistic.
- Diversity (`total_CFs` > 1) shows several distinct routes. `diversity_weight` and `proximity_weight` are accepted only by `method="genetic"`; `random` and `kdtree` raise `TypeError ... unexpected keyword argument` for them (tested, dice-ml 0.12). `posthoc_sparsity_param` was accepted by all three and pushes toward fewer changed features.
- Methods: `kdtree` returns real training points of the other class (always plausible), `genetic` optimises proximity/sparsity, `random` is fast. With `features_to_vary` and `permitted_range` set, `kdtree` raised `No counterfactuals found for any of the query points` in a test where `random` and `genetic` succeeded, because it can only return existing training rows that satisfy the constraints.

## Global insight
`exp.global_feature_importance(query_df.sample(200), total_CFs=10)` and `exp.local_feature_importance(query_df.iloc[:5], total_CFs=10)` estimate (both require `total_CFs` >= 10; with 5 they raised an error, tested; `visualize_as_dataframe` also needs `ipython` installed) how often each feature changes in counterfactuals: an importance view grounded in decision changes.

## Validate
- Re-run the model on each counterfactual to confirm the class flips, and again after any rounding of values.
- Check plausibility with domain experts; enforce constraints (e.g. debt cannot decrease below 0, education cannot decrease) in post-filters if the method cannot express them.
- Counterfactuals describe the model, not causal effects: raising income in reality may also change other features.

## Gotchas
- Pipelines with one-hot encoding: give DiCE raw columns and let the pipeline encode; otherwise it may produce impossible one-hot combinations.
- Regulated use (credit adverse action): involve your compliance or legal team and the governing regulator's rules for adverse-action notices; this skill is not legal advice.
- Regulated use, continued: document method and constraints; explanations must be consistent and reproducible (`random_seed` is a `generate_counterfactuals` argument for `method="random"` only; it raised `TypeError` with `genetic` and `kdtree`, tested).
