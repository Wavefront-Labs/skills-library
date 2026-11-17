---
id: computing-software.ai-ml-engineering.hugging-face.trainer-with-deepspeed-and-fsdp
name: trainer-with-deepspeed-and-fsdp
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, trainer-deepspeed, deepspeed, fsdp, accelerate-config, zero-stages, distributed-training]
level: practitioner
status: docs-checked
description: "Scale Trainer with DeepSpeed ZeRO or FSDP: ds_config \"auto\" values, ZeRO stage choice, offload, fsdp/fsdp_config args, launching, saving full weights and common errors."
sources:
  - https://huggingface.co/docs/transformers/main/en/deepspeed
  - https://huggingface.co/docs/transformers/main/en/fsdp
  - https://huggingface.co/docs/accelerate/usage_guides/fsdp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trainer with DeepSpeed / FSDP

**When:** model + optimizer state do not fit on one GPU, or you want ZeRO-style sharding across GPUs with the familiar Trainer API.

## DeepSpeed
Minimal ZeRO-3 config (`ds_z3.json`), letting Trainer fill values marked "auto" from TrainingArguments:
```json
{
  "bf16": {"enabled": "auto"},
  "zero_optimization": {"stage": 3, "overlap_comm": true, "contiguous_gradients": true,
                        "stage3_gather_16bit_weights_on_model_save": true,
                        "offload_optimizer": {"device": "none"}},
  "gradient_accumulation_steps": "auto", "gradient_clipping": "auto",
  "train_batch_size": "auto", "train_micro_batch_size_per_gpu": "auto"
}
```
```python
args = TrainingArguments(..., bf16=True, deepspeed="ds_z3.json")
```
Launch: `deepspeed --num_gpus 8 train.py` or `accelerate launch` / `torchrun`.

Stage choice: ZeRO-1 shards optimizer state, ZeRO-2 adds gradients, ZeRO-3 adds parameters (needed for models that do not fit). Offload (`"device": "cpu"`) trades speed for memory.

## FSDP
```python
args = TrainingArguments(..., bf16=True,
    fsdp="full_shard auto_wrap",
    fsdp_config={"transformer_layer_cls_to_wrap": ["LlamaDecoderLayer"],
                 "activation_checkpointing": True, "use_orig_params": True,
                 "state_dict_type": "SHARDED_STATE_DICT"})
```
Or configure via `accelerate config` (writes a YAML), then `accelerate launch train.py`. The current Transformers FSDP guide covers FSDP2.

## Saving
- ZeRO-3 / FSDP shard weights across ranks. For a loadable HF checkpoint, gather 16-bit weights on save (`stage3_gather_16bit_weights_on_model_save`) or `FULL_STATE_DICT` for FSDP at the end.

## Common errors
- Setting both FSDP `activation_checkpointing` and Trainer gradient checkpointing raises an error: use `activation_checkpointing` with FSDP.
- Mismatch between config values and TrainingArguments: use "auto" to avoid conflicts.

## Verify
- [ ] Per-GPU memory reported with `nvidia-smi` matches expectations for the stage.
- [ ] Saved checkpoint loads with `from_pretrained` on a single device.

## Checked
Date: 2026-10-28.
- Confirmed in the Transformers DeepSpeed and FSDP pages and the Accelerate FSDP guide: ZeRO stages, `overlap_comm`, `contiguous_gradients`, `offload_optimizer`, `stage3_gather_16bit_weights_on_model_save`, `--num_gpus`, `transformer_layer_cls_to_wrap`, `state_dict_type` (FULL and SHARDED), `activation_checkpointing`, `accelerate config` and `accelerate launch`.
- Removed as unconfirmed: `fsdp_version: 2`, `zero_to_fp32.py`, resume note, `.to("cuda")`/`device_map` warning, PEFT `use_orig_params` note.
Method: documentation only; no commands were run.
