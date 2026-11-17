---
id: computing-software.ai-ml-engineering.tensorflow-keras.tensorboard-logging-and-profiling
name: tensorboard-logging-and-profiling
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, tensorboard, tf-summary, profiler, model-fit, training-visualization, tf-profiler]
level: practitioner
status: docs-checked
description: "Log Keras and custom-loop training to TensorBoard: callback options, tf.summary writers, histograms, hparams, and capturing a profile of a few steps."
sources:
  - https://www.tensorflow.org/tensorboard/get_started
  - https://keras.io/api/callbacks/tensorboard/
  - https://www.tensorflow.org/tensorboard/tensorboard_profiling_keras
  - https://www.tensorflow.org/tensorboard/hyperparameter_tuning_with_hparams
  - https://github.com/keras-team/keras/blob/master/keras/src/callbacks/tensorboard.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# TensorBoard logging and profiling for Keras

**Goal:** see loss curves, weights and a performance profile without guessing.

## Built-in callback
```python
import datetime
log_dir = f"logs/fit/{datetime.datetime.now():%Y%m%d-%H%M%S}"
tb = keras.callbacks.TensorBoard(
    log_dir=log_dir,
    histogram_freq=1,          # weight histograms every epoch
    update_freq="epoch",       # or an int N to log every N batches
    profile_batch=(10, 20),    # profile batches 10-20; 0 disables
)
model.fit(train_ds, validation_data=val_ds, epochs=10, callbacks=[tb])
```
Run `tensorboard --logdir logs` (in notebooks: `%load_ext tensorboard` then `%tensorboard --logdir logs`).

- Use one log subdirectory per run (the TensorBoard guide uses a timestamped `logs/fit/<time>` directory) so runs can be compared side by side.
- `update_freq="epoch"` logs per epoch; an integer N logs batch-level summaries every N batches.
- Profiling needs `pip install -U tensorboard_plugin_profile`. On Keras 3 the callback raises a ValueError for `profile_batch` on the torch backend, and the JAX backend needs Python 3.12 or newer.

## Custom loops and extra scalars
```python
writer = tf.summary.create_file_writer(log_dir + "/train")
with writer.as_default():
    for step, (x, y) in enumerate(train_ds):
        loss = train_step(x, y)
        if step % 100 == 0:
            tf.summary.scalar("loss", loss, step=step)
            tf.summary.scalar("lr", optimizer.learning_rate, step=step)
```
- Pass `step=` explicitly, as the TensorBoard guide does.
- `tf.summary.image` for sample predictions, `tf.summary.histogram` for activations, `tf.summary.text` for generated samples.

## Hyperparameter dashboard
```python
from tensorboard.plugins.hparams import api as hp
with tf.summary.create_file_writer(f"logs/hparam/{run_id}").as_default():
    hp.hparams({"lr": lr, "dropout": d})
    tf.summary.scalar("val_auc", val_auc, step=1)
```
The HParams tab then gives parallel-coordinates and table views across runs.

## Reading the profile
- **Overview page:** shows whether the program is input bound; if so, optimise the `tf.data` pipeline (the profiling tutorial caches and prefetches the dataset) before touching the model.
- **Trace viewer:** gaps between GPU kernels are host overhead or input waits.
- **Kernel stats / TF op stats:** top ops by device time; look for unexpected `Cast`, host-device copies, or ops falling back to CPU.

## Verify
- [ ] Train and validation curves both appear under the run name.
- [ ] Profile tab shows a step-time breakdown for the chosen batches.
- [ ] Runs compared side by side by directory, not overwritten.

## Checked

Checked 2026-10-25 against tensorflow/tensorboard docs and Keras source (master, 2026-10). Confirmed the `TensorBoard` callback arguments `log_dir`, `histogram_freq`, `update_freq` and `profile_batch` (int or tuple) and the torch and JAX profiling restrictions (Keras source), `%load_ext tensorboard` and `%tensorboard --logdir`, `tf.summary.create_file_writer` with `tf.summary.scalar(..., step=...)`, `hp.hparams` from `tensorboard.plugins.hparams.api`, the `tensorboard_plugin_profile` install, and the overview and trace viewer guidance (TensorBoard docs, tensorflow/tensorboard master). Removed the quoted overview message, the GCS, tunnelling and older-version gotchas, and the filesystem performance claim.

Method: documentation only; no commands were run.
