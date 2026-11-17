---
id: computing-software.firmware-embedded-development.device-driver-development.linux-uio-userspace-drivers
name: linux-uio-userspace-drivers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [uio, linux-driver-subsystem, uio-pdrv-genirq, mmap-registers, userspace-irq, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Drive FPGA or custom IP from userspace with Linux UIO: uio_pdrv_genirq in DT, mmap of registers, blocking reads for IRQs with re-enable writes, and its limits."
sources:
  - https://docs.kernel.org/driver-api/uio-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UIO userspace drivers

UIO (Userspace I/O) maps a device's registers into a process and delivers interrupts through a
file descriptor. Popular for FPGA soft IP on Zynq/Cyclone V/Agilex SoCs and custom peripherals
where a full kernel driver isn't justified.

## Device tree with the generic platform UIO driver
```dts
my_ip@43c00000 {
    compatible = "acme,my-ip";
    reg = <0x43c00000 0x10000>;
    interrupts = <0 29 IRQ_TYPE_LEVEL_HIGH>;
};
```
Bind it to `uio_pdrv_genirq` via the module parameter (or kernel command line):
```sh
modprobe uio_pdrv_genirq of_id=acme,my-ip
ls /sys/class/uio/uio0/maps/map0/          # addr, size
```

## Userspace access
```c
int fd = open("/dev/uio0", O_RDWR | O_SYNC);
volatile uint32_t *regs = mmap(NULL, 0x10000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0 * getpagesize()); /* map N: offset N*pagesize */
regs[CTRL] = 1;

for (;;) {
    uint32_t enable = 1;
    write(fd, &enable, 4);                 /* re-enable the IRQ (genirq disables it on each interrupt) */
    uint32_t count;
    read(fd, &count, 4);                   /* blocks until the next interrupt; count = total IRQs */
    handle(regs);                          /* clear the IP's interrupt status register here */
}
```
`uio_pdrv_genirq` masks the interrupt line in the kernel handler (level-triggered sources would
otherwise storm); userspace must clear the device's interrupt source and then write 1 to unmask.
Use `poll()`/`epoll` with a timeout instead of a blocking `read` if needed.

## Limits
- **No DMA mapping** API in userspace: you can't safely get bus addresses for user buffers. Use
  `uio_dmem_genirq` (it uses the dma-mapping API), reserved memory regions, or a proper kernel driver.
- Interrupt latency includes a context switch and scheduling, so it varies with system load.
- No integration with kernel subsystems (net, input, IIO); no power management.
- Security: any process with access to `/dev/uio0` controls the hardware; set udev permissions.
- Register access ordering: use `volatile` and add memory barriers where the IP requires ordering;
  match the access width the IP requires.

## Verify
- [ ] Register reads return the IP version/ID register; interrupt count increments once per event.
- [ ] No IRQ storm: interrupt status cleared before re-enable.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/uio-howto.rst: /dev/uioX read returns the total interrupt count (32-bit), write() of a 32-bit value (0 or 1) enables or disables the interrupt, uio_pdrv_genirq disables the line with disable_irq_nosync() in its handler, the of_id module parameter set to the DT compatible, mmap offset N * getpagesize() for map N, maps/mapN/addr and size attributes, and uio_dmem_genirq uses the dma-mapping API. Removed as unconfirmed: the tens-of-microseconds latency figure, udmabuf, the __sync_synchronize barrier advice, and the dead bindings/uio directory link.

Method: documentation only; no commands were run.
