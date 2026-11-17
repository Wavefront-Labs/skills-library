---
id: computing-software.firmware-embedded-development.device-driver-development.linux-character-device-driver
name: linux-character-device-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-kernel-module, char-device, misc-device, file-operations, copy-to-user, ioctl, poll-wait, wait-queue, udev-node, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write a Linux character device driver: misc device vs cdev registration, file_operations, safe copy_to/from_user, blocking reads with wait queues, poll and ioctl design."
sources:
  - https://docs.kernel.org/driver-api/misc_devices.html
  - https://docs.kernel.org/userspace-api/ioctl/ioctl-number.html
  - https://docs.kernel.org/driver-api/ioctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux character device driver

**Goal:** a `/dev/mydev` node that user space can open, read, write, poll and configure,
implemented safely against concurrent users and bad pointers.

## Registration: use miscdevice unless you need many minors
```c
static const struct file_operations mydev_fops = {
    .owner = THIS_MODULE,
    .open = mydev_open, .release = mydev_release,
    .read = mydev_read, .write = mydev_write,
    .poll = mydev_poll, .unlocked_ioctl = mydev_ioctl,
};  /* non-seekable stream: call stream_open(inode, file) in open() */
static struct miscdevice mydev_misc = {
    .minor = MISC_DYNAMIC_MINOR, .name = "mydev", .fops = &mydev_fops, .mode = 0660,
};
/* probe: */ ret = misc_register(&mydev_misc);   /* udev creates /dev/mydev */
```
For many instances, `alloc_chrdev_region` + `cdev_add` + `device_create` with a class.

## Blocking read with a wait queue
```c
static ssize_t mydev_read(struct file *f, char __user *buf, size_t len, loff_t *off) {
    struct mydev *d = f->private_data;
    if (wait_event_interruptible(d->wq, kfifo_len(&d->fifo) > 0))
        return -ERESTARTSYS;                         /* signal: let the syscall restart */
    unsigned int copied;
    if (kfifo_to_user(&d->fifo, buf, len, &copied)) return -EFAULT;
    return copied;
}
/* IRQ/bottom half: kfifo_in(...); wake_up_interruptible(&d->wq); */
```
Honour `O_NONBLOCK` (`f->f_flags & O_NONBLOCK` -> return `-EAGAIN`).

## poll
```c
static __poll_t mydev_poll(struct file *f, poll_table *pt) {
    struct mydev *d = f->private_data;
    poll_wait(f, &d->wq, pt);
    return kfifo_is_empty(&d->fifo) ? 0 : (EPOLLIN | EPOLLRDNORM);
}
```

## User pointers
Never dereference `__user` pointers directly; always `copy_from_user`/`copy_to_user`/
`get_user`/`put_user`, check return values (bytes **not** copied), and validate lengths
against your buffer sizes before copying.

## ioctl design
- Define numbers with `_IO/_IOR/_IOW/_IOWR` (do not pass `sizeof(type)` to them) and a unique
  magic registered in `ioctl-number.rst`; use fixed-size structs with explicit-width types
  (`__u32`) and avoid pointers inside structs if possible (32/64-bit compat).
- Prefer sysfs attributes for simple settings, ioctl for operations with structured arguments.

## Concurrency and lifetime
Multiple processes can open the device: protect shared state with a mutex (sleeping context)
or spinlock (shared with IRQ). Device removal while open: use reference counting or
`devm`-managed data plus a "disconnected" flag checked in fops.

## Verify
- [ ] `cat /dev/mydev` blocks and returns data when the IRQ fires; Ctrl-C interrupts cleanly.
- [ ] `poll`/`select` based test program works; O_NONBLOCK returns EAGAIN.
- [ ] Passing a bad pointer (e.g. 0x1) to read returns EFAULT, no oops.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/miscdevice.h: MISC_DYNAMIC_MINOR (255), struct miscdevice mode field, misc_register. Confirmed in include/linux/fs.h: unlocked_ioctl member and stream_open(). Confirmed in include/linux/kfifo.h: kfifo_to_user. Confirmed in Documentation/driver-api/ioctl.rst: _IO/_IOR/_IOW/_IOWR for new commands, do not pass sizeof(type) into them. Confirmed in Documentation/userspace-api/ioctl/ioctl-number.rst: numbers should be globally unique. The LDD3 link was removed (not kernel documentation and covers an old API).

Method: documentation only; no commands were run.
