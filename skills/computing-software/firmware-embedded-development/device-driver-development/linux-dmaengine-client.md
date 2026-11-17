---
id: computing-software.firmware-embedded-development.device-driver-development.linux-dmaengine-client
name: linux-dmaengine-client
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [dmaengine, platform-driver, dma-slave, dma-map-single, cyclic-dma, firmware-embedded-development]
level: sme
status: docs-checked
description: "Use the Linux DMA engine slave API from a peripheral driver: dma_request_chan, slave config, prep/submit/issue, completion callbacks, cyclic mode, buffer mapping."
sources:
  - https://docs.kernel.org/driver-api/dmaengine/client.html
  - https://docs.kernel.org/core-api/dma-api-howto.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/dma/dma-common.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMA engine API (slave client)

## Device tree
```dts
spi@40013000 {
    dmas = <&dmamux1 37 0x400 0x05>, <&dmamux1 38 0x400 0x05>;   /* cells are controller specific */
    dma-names = "rx", "tx";
};
```

## Request and configure
```c
d->tx = dma_request_chan(dev, "tx");          /* release with dma_release_channel() in remove */
if (IS_ERR(d->tx)) return dev_err_probe(dev, PTR_ERR(d->tx), "tx dma\n");  /* may be -EPROBE_DEFER */

struct dma_slave_config cfg = {
    .direction      = DMA_MEM_TO_DEV,
    .dst_addr       = d->phys_base + REG_TXDR,     /* physical/bus address of the FIFO register */
    .dst_addr_width = DMA_SLAVE_BUSWIDTH_1_BYTE,
    .dst_maxburst   = 4,
};
dmaengine_slave_config(d->tx, &cfg);
```

## One transfer
```c
struct device *dma_dev = dmaengine_get_dma_device(d->tx);
dma_addr_t buf_dma = dma_map_single(dma_dev, buf, len, DMA_TO_DEVICE);
if (dma_mapping_error(dma_dev, buf_dma)) return -ENOMEM;

struct dma_async_tx_descriptor *desc =
    dmaengine_prep_slave_single(d->tx, buf_dma, len, DMA_MEM_TO_DEV, DMA_PREP_INTERRUPT | DMA_CTRL_ACK);
if (!desc) { ret = -EIO; goto unmap; }
desc->callback = mydrv_tx_done;               /* runs from the engine's tasklet, never interrupt context; do not sleep */
desc->callback_param = d;
dmaengine_submit(desc);
dma_async_issue_pending(d->tx);               /* nothing starts until this */
wait_for_completion_timeout(&d->tx_done, msecs_to_jiffies(100));
dma_unmap_single(dma_dev, buf_dma, len, DMA_TO_DEVICE);
```
Map with the **DMA controller's** `struct device` (`dmaengine_get_dma_device(chan)`), not the
peripheral's, since the controller does the bus mastering (matters with IOMMUs).

## Cyclic (audio, continuous ADC)
`dmaengine_prep_dma_cyclic(chan, buf_dma, buf_len, period_len, DMA_DEV_TO_MEM, DMA_PREP_INTERRUPT)`:
callback every period; read the current position with `dmaengine_tx_status()` residue.
Coherent buffers (`dma_alloc_coherent`) suit cyclic buffers the CPU reads continuously.

## Teardown and errors
- On timeout: `dmaengine_terminate_sync(chan)` (sleeps; `_async` + `dmaengine_synchronize` in
  atomic paths), then reset the peripheral.
- `dma_release_channel` in remove.
- Fall back to PIO when no DMA channel is available, if the hardware allows (check the error returned by `dma_request_chan`; `-EPROBE_DEFER` means retry later).

## Verify
- [ ] Large transfers complete with correct data; `CONFIG_DMA_API_DEBUG` reports no mapping misuse.
- [ ] Timeout path terminates and the next transfer succeeds.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/dmaengine/client.rst: dma_request_chan and dma_release_channel, dmaengine_slave_config with struct dma_slave_config, dmaengine_prep_dma_cyclic, dma_async_issue_pending (nothing starts until it is called), callbacks run from the engine tasklet and never from interrupt context, dmaengine_terminate_sync / _async (async usable from atomic context, dmaengine_terminate_all deprecated), and that mapping uses the DMA device from dmaengine_get_dma_device(chan) (the skill example now uses it instead of chan->device->dev). Not independently confirmed beyond the documented API names: the SPI DT cell values in the example, which are marked controller specific in the skill.

Method: documentation only; no commands were run.
