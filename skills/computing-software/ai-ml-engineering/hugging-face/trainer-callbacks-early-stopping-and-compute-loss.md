---
id: computing-software.ai-ml-engineering.hugging-face.trainer-callbacks-early-stopping-and-compute-loss
name: trainer-callbacks-early-stopping-and-compute-loss
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, trainer-callbacks, compute-loss, early-stopping, custom-trainer]
level: practitioner
status: verified
description: "Extend the transformers Trainer with callbacks (EarlyStoppingCallback, custom TrainerCallback) and subclass compute_loss for weighted, multi-task or distillation losses."
sources:
  - https://huggingface.co/docs/transformers/main_classes/callback
  - https://huggingface.co/docs/transformers/main_classes/trainer
  - https://huggingface.co/docs/transformers/trainer#customize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trainer callbacks, early stopping and compute_loss

## Early stopping
```python
from transformers import EarlyStoppingCallback, TrainingArguments, Trainer
args = TrainingArguments("out", eval_strategy="steps", eval_steps=500, save_strategy="steps", save_steps=500,
                         load_best_model_at_end=True, metric_for_best_model="eval_f1", greater_is_better=True,
                         save_total_limit=2)
trainer = Trainer(model=model, args=args, train_dataset=tr, eval_dataset=va, compute_metrics=compute_metrics,
                  callbacks=[EarlyStoppingCallback(early_stopping_patience=3, early_stopping_threshold=0.001)])
```
Meant to be used with `load_best_model_at_end=True`, matching eval and save strategies (save steps a round multiple of eval steps) and `metric_for_best_model`. Checked in transformers 5.20 on a tiny BERT (CPU, 20 epochs of 8 steps): training stopped at step 16 of 160 with `best_model_checkpoint` `checkpoint-4`; `save_steps=6` with `eval_steps=4` raises `ValueError: --load_best_model_at_end requires the saving steps to be a round multiple of the evaluation steps`; `EarlyStoppingCallback` without `load_best_model_at_end=True` is not an error, it only logs a warning that the best model will not be loaded automatically. `metric_for_best_model="f1"` and `"eval_f1"` both trained and recorded a best metric.

## Custom callback
Callbacks observe and set control flags; they can't change the training step itself.
```python
from transformers import TrainerCallback
class LogGradNorm(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kw):
        if state.is_world_process_zero and logs: print(state.global_step, logs)
    def on_evaluate(self, args, state, control, metrics=None, **kw):
        if metrics and metrics.get("eval_loss", 0) > 10: control.should_training_stop = True
```
Events (all present on `TrainerCallback` in 5.20): `on_train_begin`, `on_epoch_begin/end`, `on_step_begin/end`, `on_optimizer_step`, `on_evaluate`, `on_save`, `on_log`, `on_predict`. `TrainerControl` has `should_training_stop`, `should_epoch_stop`, `should_save`, `should_evaluate` and `should_log`; the `LogGrad` callback above fired on logging and the `on_evaluate` hook ran during the early-stopping run. Integrations (W&B, MLflow, TensorBoard) are callbacks enabled by `report_to`.

## Custom loss via compute_loss
```python
class WeightedTrainer(Trainer):
    def __init__(self, *a, class_weights=None, **kw):
        super().__init__(*a, **kw); self.class_weights = class_weights
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        loss = torch.nn.functional.cross_entropy(outputs.logits, labels, weight=self.class_weights.to(outputs.logits.device))
        return (loss, outputs) if return_outputs else loss
```
- Keep the `num_items_in_batch` parameter in the signature (recent versions pass it for correct loss normalisation with gradient accumulation); use it to divide summed token losses.
- Distillation: compute teacher logits under `torch.no_grad()` inside compute_loss (teacher on the same device, in eval mode), blend KL and CE.
- Extra inputs the model doesn't accept (sample weights): set `remove_unused_columns=False` and pop them in compute_loss.
- Alternatively pass `compute_loss_func=` to Trainer in recent versions instead of subclassing (the parameter exists in 5.20's `Trainer.__init__`; not exercised here). The `WeightedTrainer` above trained for two epochs on CPU (final training loss 0.692 on random data) with a `labels` column.

## Verify
Logged `train_loss` matches your manual loss on a batch; early stopping shows as a shortened run (compare `trainer.state.global_step` with the planned steps); the final model equals the best checkpoint (`trainer.state.best_model_checkpoint`).
