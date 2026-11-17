---
id: computing-software.systems-network-administration.linux.kdump-and-crash-analysis
name: kdump-and-crash-analysis
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kdump, vmcore, crash-utility, kexec, crashkernel, kernel-panic, sysrq, makedumpfile, kdumpctl, kernel-debuginfo, troubleshooting, sysadmin]
level: advanced
status: docs-checked
description: "Capture and analyse Linux kernel crashes: crashkernel reservation, kdump service and targets, testing with sysrq, makedumpfile filtering, and first-pass vmcore analysis with the crash utility."
sources:
  - https://docs.kernel.org/admin-guide/kdump/kdump.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_monitoring_and_updating_the_kernel/configuring-kdump-on-the-command-line_managing-monitoring-and-updating-the-kernel
  - https://crash-utility.github.io/
  - https://docs.kernel.org/admin-guide/kdump/kdump.html
  - https://github.com/rhkdump/kdump-utils/blob/main/kdump.conf.5
  - https://github.com/rhkdump/kdump-utils/blob/main/kdumpctl.8
  - https://github.com/makedumpfile/makedumpfile/blob/master/makedumpfile.8.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kdump and crash analysis

**Goal:** when the kernel panics or hangs, a vmcore is saved automatically, and you can
extract the panic reason and stack to hand to the vendor or fix the driver.

## 1. Reserve memory and enable
```bash
dnf install kexec-tools          # Fedora/RHEL family; kdumpctl comes from the kdump-utils project
kdumpctl reset-crashkernel --kernel=ALL     # reset crashkernel= to the default recommended by kdump-utils
# or by hand: grubby --update-kernel=ALL --args="crashkernel=512M"
reboot
cat /proc/cmdline | grep -o 'crashkernel=[^ ]*'; cat /sys/kernel/kexec/crash_size   # non-zero = reserved (older kernels: /sys/kernel/kexec_crash_size, deprecated)
systemctl enable --now kdump; kdumpctl status       # non-zero exit if kdump is not operational
```

## 2. Where dumps go — `/etc/kdump.conf`
```
path /var/crash
core_collector makedumpfile -l --message-level 7 -d 31     # -l = lzo compression; -d <level> chooses which page types to exclude (see makedumpfile(8))
# nfs nfs01.corp.example:/export/crash
# ssh kdump@crash01.corp.example + sshkey /root/.ssh/kdump_id_rsa
failure_action reboot
```
Ensure the dump target has enough free space for the filtered vmcore. After changes: `kdumpctl restart` (stop then start), or `kdumpctl rebuild` to rebuild the kdump initramfs.

## 3. Test (on a maintenance window — this crashes the host)
```bash
echo 1 > /proc/sys/kernel/sysrq
echo c > /proc/sysrq-trigger
# after reboot:
ls /var/crash/*/                  # vmcore, vmcore-dmesg.txt
```
Hangs without panic: enable `kernel.hung_task_panic=1`, `kernel.softlockup_panic=1`, or `kernel.unknown_nmi_panic=1`
(an unknown NMI then panics the kernel) so they produce a dump.

## 4. First-pass analysis
Start with the text log — often enough:
```bash
less /var/crash/*/vmcore-dmesg.txt     # look for "BUG:", "Oops", "Kernel panic - not syncing", the RIP and Call Trace
```
Then `crash` (needs debuginfo for the **exact** kernel):
```bash
dnf debuginfo-install kernel-$(uname -r)    # or the kernel version that crashed
crash /usr/lib/debug/lib/modules/<ver>/vmlinux /var/crash/<dir>/vmcore
crash> sys          # kernel, panic string, uptime
crash> log          # dmesg ring buffer
crash> bt           # backtrace of the panicking task
crash> ps | grep UN # tasks in D state (hangs)
crash> kmem -i      # memory summary
crash> sys -t       # kernel taint information
```
Report to the vendor: panic string, RIP function, call trace, taint flags, kernel version, vmcore location.

## Gotchas
- If the `crashkernel` reservation is too small the capture kernel may run out of memory and write no dump; watch the console during the test.
- Encrypted/remote root: dumping to local disk needs the dump target accessible from the kdump initramfs — test.

## Verify
- [ ] `kdumpctl status` reports operational and `/sys/kernel/kexec/crash_size` is non-zero.
- [ ] A sysrq-triggered test produced a vmcore that `crash` opens and shows `PANIC: "sysrq triggered crash"`.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (admin-guide/kdump, ABI testing/obsolete kexec sysfs, sysctl/kernel, drivers/tty/sysrq.c), the kdump-utils `kdump.conf(5)` and `kdumpctl(8)` sources, makedumpfile `makedumpfile.8.in` and the crash utility help text on 2026-10-26. Confirmed: `crashkernel=` boot parameter, `kexec -p` loads the capture kernel, `echo c > /proc/sysrq-trigger` crashes the system with panic text `sysrq triggered crash`, `kdump.conf` keys `path`, `core_collector`, `nfs`, `ssh`, `sshkey` and `failure_action` (default reboot), `kdumpctl reset-crashkernel --kernel=ALL`, `status` non-zero when not operational, `restart` = start; stop, `rebuild`, makedumpfile `-l` = lzo, `unknown_nmi_panic`. Stale: `/sys/kernel/kexec_crash_size` is in the obsolete ABI list; the current path is `/sys/kernel/kexec/crash_size`. Removed: Debian tooling, default crashkernel example values, dump-size ratio, `mod -t`, Secure Boot claim.

Method: documentation only; no commands were run.
