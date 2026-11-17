---
id: computing-software.firmware-embedded-development.stm32.gpdma-linked-lists
name: gpdma-linked-lists
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-dma, gpdma-linked-list, gpdma, lli-nodes, dma-queue, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Program STM32 GPDMA (U5, H5, H7RS, N6) linked-list transfers with HAL DMAEx queues: nodes, circular queues, 2D addressing and replacing classic circular/double-buffer modes."
sources:
  - https://www.st.com/resource/en/application_note/an5593-how-to-use-the-gpdma-for-stm32u575585-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0456-stm32u5-series-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPDMA linked lists

GPDMA has no "circular mode" or "double-buffer" bit like DMA v1/v2. Continuous and multi-buffer
transfers are built from **linked-list items (LLI)**: each node holds the channel register values
for the next block, and the hardware reloads from the node when a block completes.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## HAL queue workflow
```c
DMA_NodeTypeDef node_a, node_b;           /* must live in RAM reachable by GPDMA (not TCM on H7RS) */
DMA_QListTypeDef q;
DMA_NodeConfTypeDef nc = {0};
nc.NodeType = DMA_GPDMA_LINEAR_NODE;
nc.Init.Request = GPDMA1_REQUEST_ADC1;
nc.Init.Direction = DMA_PERIPH_TO_MEMORY;
nc.Init.SrcInc = DMA_SINC_FIXED; nc.Init.DestInc = DMA_DINC_INCREMENTED;
nc.Init.SrcDataWidth = DMA_SRC_DATAWIDTH_HALFWORD; nc.Init.DestDataWidth = DMA_DEST_DATAWIDTH_HALFWORD;
nc.Init.TransferEventMode = DMA_TCEM_BLOCK_TRANSFER;     /* TC event per node */
nc.SrcAddress = (uint32_t)&ADC1->DR;
nc.DstAddress = (uint32_t)buf_a; nc.DataSize = N * 2;   /* bytes */
HAL_DMAEx_List_BuildNode(&nc, &node_a);
HAL_DMAEx_List_InsertNode_Tail(&q, &node_a);
nc.DstAddress = (uint32_t)buf_b;
HAL_DMAEx_List_BuildNode(&nc, &node_b);
HAL_DMAEx_List_InsertNode_Tail(&q, &node_b);
HAL_DMAEx_List_SetCircularMode(&q);                     /* last node links back to first */

HAL_DMAEx_List_Init(&handle_GPDMA1_Channel0);           /* channel in linked-list mode */
HAL_DMAEx_List_LinkQ(&handle_GPDMA1_Channel0, &q);
__HAL_LINKDMA(&hadc1, DMA_Handle, handle_GPDMA1_Channel0);
HAL_ADC_Start_DMA(&hadc1, (uint32_t *)buf_a, N);        /* HAL starts the linked channel */
```
Each node's TC interrupt tells you which buffer just filled: ping-pong without half-transfer tricks.
CubeMX can generate queues (`linked_list.c`, "LinkedList" in the GPDMA config).

## Notes
- `DataSize` is in **bytes** for GPDMA (not item count as in DMA v1).
- Only some channels (12-15 on U5) support 2D addressing (`DMA_GPDMA_2D_NODE`) for strided
  transfers (image blocks, interleaved audio).
- Nodes are read by the DMA from memory: keep them in the same security domain and, with D-cache
  (H5/H7RS), in non-cacheable memory or cleaned before start.
- Modifying a running circular queue: use `HAL_DMAEx_List_ReplaceNode` only on nodes not
  currently being loaded, or stop the channel.
- Port-0/port-1 allocation (`SrcAllocatedPort`, `DestAllocatedPort`) affects bus contention on
  high-throughput designs.

## Verify
- [ ] TC callback alternates between buffers at the expected rate.
- [ ] Long run with node RAM checked for corruption (nodes intact after hours).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
