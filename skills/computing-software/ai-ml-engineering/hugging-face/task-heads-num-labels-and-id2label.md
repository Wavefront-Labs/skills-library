---
id: computing-software.ai-ml-engineering.hugging-face.task-heads-num-labels-and-id2label
name: task-heads-num-labels-and-id2label
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, id2label, task-heads, num-labels, ignore-mismatched-sizes]
level: practitioner
status: verified
description: "Attach task heads in transformers with AutoModelFor* classes, set num_labels, id2label, label2id and problem_type, and swap heads with ignore_mismatched_sizes."
sources:
  - https://huggingface.co/docs/transformers/main_classes/configuration
  - https://huggingface.co/docs/transformers/tasks/sequence_classification
  - https://huggingface.co/docs/transformers/model_doc/auto
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task heads, num_labels and id2label

`AutoModelFor<Task>` classes add a task-specific head on a base model: `ForSequenceClassification`, `ForTokenClassification`, `ForQuestionAnswering`, `ForCausalLM`, `ForMaskedLM`, `ForImageClassification`, etc. Head weights not in the checkpoint are randomly initialised and reported at load time: in transformers 5.20 as a `LOAD REPORT` table listing the head's `classifier.weight`/`classifier.bias` as `MISSING` ("newly initialized because missing from the checkpoint. Consider training on your downstream task") and unused checkpoint keys such as the BERT pooler as `UNEXPECTED`; older releases print "Some weights of ... were not initialized from the model checkpoint ... You should probably TRAIN this model". Either way it is expected for a new head.

## Configure labels
```python
labels = ["negative", "neutral", "positive"]
id2label = {i: l for i, l in enumerate(labels)}; label2id = {l: i for i, l in id2label.items()}
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-base", num_labels=len(labels), id2label=id2label, label2id=label2id)
```
- `id2label` is saved in `config.json` and used by pipelines to print label names. Without it, outputs read `LABEL_0`, `LABEL_1` (checked, including a text-classification pipeline). Saved ids become string keys in the JSON (`{"0": "negative", ...}`) and are ints again after loading.
- Dataset labels must be integers matching these ids; `ClassLabel` features in `datasets` give you the names (`ds.features["label"].names`).

## problem_type
Sequence classification picks the loss from `config.problem_type`:
- `"single_label_classification"` (int labels, CrossEntropy), default when `num_labels > 1` and labels are ints. `config.problem_type` stays `None` after loading and is filled in on the first forward pass that has labels (checked), so read it after a training step, not before.
- `"multi_label_classification"` (float multi-hot labels, BCEWithLogits). Set it explicitly (`problem_type="multi_label_classification"` in `from_pretrained`) and pass float labels; int labels raise `RuntimeError: result type Float can't be cast to the desired output type Long` (checked).
- `"regression"` (`num_labels=1`, MSE, float labels; checked that `problem_type` becomes `regression` after a forward pass).

## Replace a head from a fine-tuned checkpoint
Loading a fine-tuned checkpoint with a different `num_labels` raises a `RuntimeError` ("You set `ignore_mismatched_sizes` to `False`, thus raising an error") unless you pass the flag; also pass new `id2label`/`label2id`, otherwise the old map of the wrong length conflicts with `num_labels` (a warning is logged):
```python
model = AutoModelForSequenceClassification.from_pretrained(
    "some/2-class-model", num_labels=5, id2label=..., label2id=..., ignore_mismatched_sizes=True)
```
The mismatched classifier is reinitialised; the rest is reused.

## Token classification
Same `id2label` mechanics with BIO tags (`B-PER`, `I-PER`, `O`); align labels to sub-tokens with `word_ids()` and `-100` for ignored positions.

## Custom heads
Load `AutoModel` (no head) and add your own `nn.Module` on top of `last_hidden_state` (pooled CLS or mean pooling with the attention mask). Save base and head together or register a custom config/model class.

## Verify
`model.config.id2label`, `model.config.problem_type` (after one forward pass), and the classifier's output dimension (`model.classifier.out_features` for BERT, `model.classifier.out_proj.out_features` where the head has an `out_proj`, `model.score.out_features` for decoder models) match the task; a pipeline prediction prints real label names.
