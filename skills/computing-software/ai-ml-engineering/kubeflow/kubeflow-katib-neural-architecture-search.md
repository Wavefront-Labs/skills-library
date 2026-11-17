---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-neural-architecture-search
name: kubeflow-katib-neural-architecture-search
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [nas, neural-architecture-search, enas, darts, nasconfig]
level: advanced
status: docs-checked
description: "Run Katib neural architecture search (alpha): nasConfig with graphConfig and operations, and the ENAS and DARTS algorithm settings."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/nas/configure-experiment.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/nas/configure-algorithm.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/reference/architecture.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/katib-config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib neural architecture search

NAS is alpha with limited support. It optimizes the model structure, node weights and hyperparameters, whereas hyperparameter tuning optimizes only hyperparameters. Common Experiment fields (objective, trial counts, trialTemplate) work as in HP tuning.

NAS-specific field `nasConfig`:
- `graphConfig`: structure of the neural network DAG: number of layers, `input_sizes` for the input layer and `output_sizes` for the output layer.
- `operations`: the operations the algorithm may choose per layer; each has `parameters` defined like HP tuning parameters.

The pages point to an ENAS example YAML as the reference and a list of all NAS examples.

Algorithms:
- `enas` (Efficient NAS): RL controller. Settings include `controller_hidden_size` (64), `controller_temperature` (5.0), `controller_tanh_const` (2.25), `controller_entropy_weight` (1e-5), `controller_baseline_decay` (0.999), `controller_learning_rate` (5e-5), `controller_skip_target` (0.4), `controller_skip_weight` (0.8), `controller_train_steps` (50), `controller_log_every_steps` (10). The `enas-gpu.yaml` example tries to show all possible operations, so its large search space is not likely to give a good result.
- `darts` (Differentiable Architecture Search): settings include `num_epochs` (50), `w_lr` (0.025), `w_lr_min` (0.001), `w_momentum` (0.9), `w_weight_decay` (3e-4), `w_grad_clip` (5.0), `alpha_lr` (3e-4), `alpha_weight_decay` (1e-3), `batch_size` (128), `num_workers` (4), `init_channels` (16), `print_step` (50), `num_nodes` (4), `stem_multiplier` (3).

Suggestion images are `suggestion-enas` and `suggestion-darts` in `katib-config` (per the Katib Config algorithm table).

## Checked

2026-11-08. Confirmed against the NAS Experiment and algorithm pages and the architecture page: nasConfig, graphConfig, operations, every ENAS and DARTS default listed. Removed the unconfirmed enas-cpu.yaml filename and examples path.
Method: docs-only read of cited pages, 2026-11-08
