---
id: computing-software.ai-ml-engineering.hugging-face.custom-training-loop-with-accelerate
name: custom-training-loop-with-accelerate
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, accelerate, accelerate-launch, distributed-training, mixed-precision, custom-training-loop]
level: practitioner
status: gated
description: "Turn a plain PyTorch loop into multi-GPU mixed-precision training with Accelerate: prepare, backward, accumulate, gather_for_metrics, save_state and accelerate launch."
sources:
  - https://huggingface.co/docs/accelerate/basic_tutorials/migration
  - https://huggingface.co/docs/accelerate/usage_guides/gradient_accumulation
  - https://huggingface.co/docs/accelerate/basic_tutorials/launch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom training loop with Accelerate

## Minimal changes to a PyTorch loop
```python
from accelerate import Accelerator
accelerator = Accelerator(mixed_precision="bf16", gradient_accumulation_steps=4, log_with="tensorboard",
                          project_dir="runs")
model, opt, train_dl, eval_dl, sched = accelerator.prepare(model, opt, train_dl, eval_dl, sched)
for epoch in range(epochs):
    model.train()
    for batch in train_dl:                              # already on the right device
        with accelerator.accumulate(model):             # handles no_sync and step skipping
            loss = model(**batch).loss
            accelerator.backward(loss)                  # replaces loss.backward(); handles scaling
            if accelerator.sync_gradients:
                accelerator.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step(); opt.zero_grad()
    model.eval(); preds, refs = [], []
    for batch in eval_dl:
        with torch.no_grad(): logits = model(**batch).logits
        p, r = accelerator.gather_for_metrics((logits.argmax(-1), batch["labels"]))
        preds.append(p); refs.append(r)
    accelerator.print(epoch, metric(torch.cat(preds), torch.cat(refs)))
```
- Remove manual `.to(device)`, `GradScaler`, DDP wrapping and `DistributedSampler`; `prepare` does them.
- `gather_for_metrics` drops the duplicated samples added to make the last batch even across processes; plain `gather` would count them twice (single process only here: eval counted exactly 37 of 37 samples; the multi-process duplicate case was not run) (gated: unconfirmed, source is paywalled or blocked).
- Under `accumulate`, `opt.step()` is a no-op on non-sync steps; the prepared scheduler also accounts for it. Ran on CPU (accelerate 1.15.0, 37 samples, batch 4, accumulation 4): 10 batches per epoch synced at batches 4, 8 and 10 (the last batch of the dataloader always syncs), so after 2 epochs the scheduler had stepped 6 times (lr 0.0094 on a 100-step linear decay from 0.01).

## Launch
```bash
accelerate config                 # interactive: GPUs, mixed precision, DeepSpeed/FSDP
accelerate launch --num_processes 4 train.py
accelerate launch --config_file fsdp.yaml train.py
```
`accelerate launch` can use torch.distributed.run (torchrun) as the launcher (its `--help` mentions it); the same script ran here on plain `python` and under `accelerate launch --cpu`. Multi-GPU, multi-node, TPU, DeepSpeed and FSDP were not run (no GPU hosts). Note `accelerate launch --cpu --num_processes 2` ran only ONE process here (`accelerator.num_processes == 1`), and `--cpu` cannot be combined with `--multi_gpu`, so do not use CPU launches to test multi-process behaviour (gated: unconfirmed, source is paywalled or blocked).

## Checkpointing
```python
accelerator.save_state("ckpt/step_1000")       # wrote model.safetensors, optimizer.bin, scheduler.bin, random_states_0.pkl (a scaler file appears only with fp16)
accelerator.load_state("ckpt/step_1000")
accelerator.wait_for_everyone()
unwrapped = accelerator.unwrap_model(model)
unwrapped.save_pretrained("final", is_main_process=accelerator.is_main_process, save_function=accelerator.save,
                          state_dict=accelerator.get_state_dict(model))   # get_state_dict gathers FSDP/ZeRO-3 shards
```
Resume mid-epoch: `accelerator.skip_first_batches(train_dl, num_batches)` (ran: skipping 2 of 10 batches left 8). `save_pretrained` exists only on `PreTrainedModel`s; a plain `nn.Module` has none. `get_state_dict` gathering FSDP/ZeRO-3 shards was not run (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Only the main process should write files or log: `if accelerator.is_main_process:`; use `accelerator.print`.
- Create the optimizer from the model's parameters before `prepare` (FSDP needs care: prepare model first in some setups, see FSDP guide).
- Total steps for the scheduler: compute from `len(train_dl)` after prepare (it's divided across processes).
- Mixed precision set in both the launch config and code: the code argument wins (ran: `accelerate launch --mixed_precision no` with `Accelerator(mixed_precision="bf16")` reported `bf16`; with no code argument the launch value was used). Creating one `Accelerator(mixed_precision=...)` also sets `ACCELERATE_MIXED_PRECISION` for any later `Accelerator()` in the same process.

## Verify
Run with 1 and 2 processes on a small subset; loss curves should match closely at the same effective batch size; metrics count equals dataset size.
