---
id: computing-software.ai-ml-engineering.model-training.config-management-with-hydra
name: config-management-with-hydra
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, hydra-config, omegaconf, experiment-configuration, multirun, reproducibility]
level: practitioner
status: verified
description: "Manage experiment configs with Hydra: config groups and defaults, CLI overrides, multirun sweeps, dataclass structured configs and logging the resolved config."
sources:
  - https://hydra.cc/docs/intro/
  - https://hydra.cc/docs/tutorials/structured_config/intro/
  - https://omegaconf.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Config management with Hydra

**Goal:** every run fully described by a composable config, overridable from the command line, saved with the outputs.

Checked by running hydra-core 1.3.7 with omegaconf 2.3.1 (the default `python -m` tooling here is 3.14, where `@hydra.main` crashes at startup with `ValueError: badly formed help string` from argparse; everything below was run on Python 3.12.15, so pin Python 3.13 or older for Hydra 1.3.x).

## Layout
```
conf/
  config.yaml
  model/{resnet.yaml, vit.yaml}
  data/{cifar.yaml, imagenet.yaml}
  optim/{adamw.yaml, sgd.yaml}
```
```yaml
# conf/config.yaml
defaults:
  - model: resnet
  - data: cifar
  - optim: adamw
  - _self_
seed: 42
trainer: {epochs: 30, precision: bf16}
```
```python
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    model = hydra.utils.instantiate(cfg.model)      # builds objects from _target_ keys (ran with `_target_: collections.OrderedDict`; `${data.num_classes}` resolved to 10)
if __name__ == "__main__":
    main()
```

## Overrides
```bash
python train.py model=vit optim.lr=3e-4 trainer.epochs=50
python train.py +experiment=long_run          # add a config not in defaults (ran: needs a `# @package _global_` header in conf/experiment/long_run.yaml to set `trainer.epochs`; `experiment=long_run` without the plus fails with "Could not override 'experiment'. No match in the defaults list")
python train.py -m optim.lr=1e-4,3e-4,1e-3 model=resnet,vit   # multirun: 6 jobs (ran: "Launching 6 jobs locally", job dirs 0 to 5 plus multirun.yaml)
```
Sweeper plugins (Optuna, Ax) and launcher plugins (Submitit for Slurm, Ray, joblib) turn multirun into HPO or cluster jobs. Ran the Optuna one: `pip install hydra-optuna-sweeper` (1.3.0, which pulled optuna 2.10.1), then `python train.py -m hydra/sweeper=optuna hydra.sweeper.n_trials=4 'optim.lr=interval(1e-4,1e-3)'` and the task function must return the float to minimise; the `hydra.sweeper.params.` prefix form is rejected. Slurm, Ray, joblib and Ax launchers were not run.

## Structured configs (type safety)
```python
from dataclasses import dataclass
from hydra.core.config_store import ConfigStore
@dataclass
class OptimConfig:
    lr: float = 1e-3
    weight_decay: float = 0.01
cs = ConfigStore.instance(); cs.store(group="optim", name="base_adamw", node=OptimConfig)
```
Type errors in overrides fail fast (`optim.lr=abc`) only once the schema is part of the composition: with the YAML files above and no link, `optim.lr=abc` was accepted silently (printed `lr: abc`). Link it by starting `conf/optim/adamw.yaml` with `defaults: [base_adamw, _self_]`; then a bad value raises a validation error (provider `schema`), and a key missing from the dataclass raises `ConfigKeyError`. Dataclass fields that are other dataclasses need `field(default_factory=...)`, otherwise Python raises `mutable default ... not allowed`.

## Outputs and tracking
- Each run gets `outputs/<date>/<time>/` with `.hydra/config.yaml`, `hydra.yaml`, `overrides.yaml` and logs (ran: the `.hydra` folder held exactly those three files; `hydra.run.dir=out1` redirected it); set `hydra.run.dir` to something meaningful.
- Log the resolved config to MLflow/W&B (`OmegaConf.to_container(cfg, resolve=True)`).
- Interpolation (`${data.num_classes}`) avoids duplicated values.

## Pitfalls
- Hydra changes the working directory in older defaults: with `version_base=None` the cwd stayed at the launch directory, with `version_base="1.1"` it moved into the run directory and `hydra.utils.get_original_cwd()` still returned the launch directory (ran both). Use that function or `hydra.job.chdir=False`.

## Verify
- [ ] Re-running with the saved `.hydra/config.yaml` (`--config-path out1/.hydra --config-name config`) reproduces the run's config exactly (ran: the second run's saved `config.yaml` was identical to the first's).
