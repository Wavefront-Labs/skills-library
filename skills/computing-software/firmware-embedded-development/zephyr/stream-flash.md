---
id: computing-software.firmware-embedded-development.zephyr.stream-flash
name: stream-flash
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [stream-flash, stream-flash-init, stream-flash-buffered-write, flash-img, dfu-image-write, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write a byte stream (firmware download, log upload) to flash in Zephyr with stream_flash: buffering to write-block size, erase-on-the-fly, progress callbacks, and resume."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/storage/stream_flash.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/storage/stream/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dfu/flash_img.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dfu/img_util/flash_img.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dfu/mcuboot.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream flash

`stream_flash` accepts arbitrary-sized chunks (from HTTP, BLE, UART), buffers them to the flash write-block
size and writes them to flash; with `CONFIG_STREAM_FLASH_ERASE` it also performs the erase operations. `flash_img`
(the DFU image writer) is built on it.

```
CONFIG_STREAM_FLASH=y
CONFIG_STREAM_FLASH_ERASE=y       # perform erase operations (depends on FLASH_HAS_EXPLICIT_ERASE)
```

```c
#include <zephyr/storage/stream_flash.h>
#include <zephyr/storage/flash_map.h>

static struct stream_flash_ctx sf;
static uint8_t sf_buf[CONFIG_IMG_BLOCK_BUF_SIZE] __aligned(4);   /* multiple of write-block size, at most one page */

int dl_begin(void)
{
    const struct flash_area *fa;
    flash_area_open(PARTITION_ID(slot1_partition), &fa);
    return stream_flash_init(&sf, fa->fa_dev, sf_buf, sizeof sf_buf,
                             fa->fa_off, fa->fa_size, NULL /*callback*/);
}

int dl_chunk(const uint8_t *data, size_t len, bool last)
{
    return stream_flash_buffered_write(&sf, data, len, last);   /* last=true flushes padding */
}

size_t dl_written(void) { return stream_flash_bytes_written(&sf); }
```

## Higher level for firmware: flash_img
```c
#include <zephyr/dfu/flash_img.h>
struct flash_img_context img;
flash_img_init(&img);                          /* upload slot: slot1_partition when slot0 is the running image */
/* flash_img_init_id(&img, area_id) targets an explicit flash area */
flash_img_buffered_write(&img, data, len, last);
/* then: boot_request_upgrade(BOOT_UPGRADE_TEST); sys_reboot(SYS_REBOOT_COLD); */
```
`CONFIG_IMG_ENABLE_IMAGE_CHECK=y` enables `flash_img_check()`, which verifies the written image against a
SHA-256 (the only algorithm the header lists).

## Resume after interruption
With `CONFIG_STREAM_FLASH_PROGRESS=y` and the settings subsystem:
```c
stream_flash_progress_save(&sf, "dl/progress");
/* after reboot: call directly after stream_flash_init(), before writing any data */
stream_flash_progress_load(&sf, "dl/progress");    /* restores bytes_written; ignored if it has fewer bytes than ctx */
stream_flash_progress_clear(&sf, "dl/progress");   /* when done */
```
Ask the server for a range starting at `stream_flash_bytes_written()`.

## Callback
The optional callback `int cb(uint8_t *buf, size_t len, size_t offset)` is invoked on completed flash writes and
is supported only when `CONFIG_STREAM_FLASH_POST_WRITE_CALLBACK` is enabled; use it for read-back verification
or progress reporting.

## Gotchas
- Buffer size must be a multiple of the write-block size and cannot be larger than the flash page size.
- The final call must pass `flush = true`, or the last partial block stays in RAM; after a flushed write, do not
  write again until the context is re-initialised.
- With erase enabled the old content of the target area is destroyed; never target the running image's partition.

## Verify
- [ ] Interrupted download resumes and the final image hash matches.
- [ ] Last chunk flushed (`bytes_written` equals image size).

## Checked

Checked 2026-10-26 against Zephyr main on GitHub: `stream_flash_init()` parameters and buffer limits (multiple of write-block
size, not larger than a page), `stream_flash_buffered_write()` flush rules, `stream_flash_bytes_written()`, the progress
save/load/clear functions and when to call load, `CONFIG_STREAM_FLASH_ERASE`, `_PROGRESS`, `_POST_WRITE_CALLBACK`,
`flash_img_init()`/`flash_img_init_id()`/`flash_img_buffered_write()`/`flash_img_check()` (SHA-256), `CONFIG_IMG_BLOCK_BUF_SIZE`,
`CONFIG_IMG_ENABLE_IMAGE_CHECK`, `boot_request_upgrade()` and `BOOT_UPGRADE_TEST`, and that `flash_img.c` uses stream_flash.
`FIXED_PARTITION_ID` replaced with `PARTITION_ID`, which `flash_map.h` marks as the current name. Removed the
unconfirmed CPU-stall remark.

Method: documentation only; no commands were run.
