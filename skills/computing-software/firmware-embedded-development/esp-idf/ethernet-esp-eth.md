---
id: computing-software.firmware-embedded-development.esp-idf.ethernet-esp-eth
name: ethernet-esp-eth
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-protocols, esp-eth, ethernet-phy, rmii, spi-ethernet, w5500, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Add wired Ethernet to ESP32 with esp_eth: internal EMAC with RMII PHYs (LAN8720, IP101) or SPI modules (W5500, DM9051), clocking, netif glue and link events."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/network/esp_eth.html
  - https://github.com/espressif/esp-eth-drivers
  - https://github.com/espressif/esp-idf/tree/master/examples/ethernet/basic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ethernet with esp_eth

## Internal EMAC (ESP32, ESP32-P4) + RMII PHY
```c
eth_mac_config_t mac_cfg = ETH_MAC_DEFAULT_CONFIG();
eth_esp32_emac_config_t emac = ETH_ESP32_EMAC_DEFAULT_CONFIG();
emac.smi_gpio.mdc_num = 23; emac.smi_gpio.mdio_num = 18;
emac.clock_config.rmii.clock_mode = EMAC_CLK_EXT_IN;        /* 50 MHz REF_CLK from PHY/oscillator; default on ESP32 */
emac.clock_config.rmii.clock_gpio = 0;                      /* GPIO0 is the only input pin on ESP32 */
esp_eth_mac_t *mac = esp_eth_mac_new_esp32(&emac, &mac_cfg);

eth_phy_config_t phy_cfg = ETH_PHY_DEFAULT_CONFIG();
phy_cfg.phy_addr = 1; phy_cfg.reset_gpio_num = 5;
esp_eth_phy_t *phy = esp_eth_phy_new_lan87xx(&phy_cfg);

esp_eth_config_t cfg = ETH_DEFAULT_CONFIG(mac, phy);
esp_eth_handle_t eth; ESP_ERROR_CHECK(esp_eth_driver_install(&cfg, &eth));
esp_netif_config_t ncfg = ESP_NETIF_DEFAULT_ETH();
esp_netif_t *netif = esp_netif_new(&ncfg);
esp_netif_attach(netif, esp_eth_new_netif_glue(eth));
esp_event_handler_register(ETH_EVENT, ESP_EVENT_ANY_ID, on_eth_event, NULL);
esp_event_handler_register(IP_EVENT, IP_EVENT_ETH_GOT_IP, on_got_ip, NULL);
esp_eth_start(eth);
```
In ESP-IDF v6.1 the built-in PHY driver is `esp_eth_phy_new_generic()` (any IEEE 802.3 PHY). Drivers
for specific PHYs (LAN87xx, IP101, ...) and SPI modules (W5500, DM9051) are components from the
esp-eth-drivers repository, added with `idf.py add-dependency`; check each component's
`idf_component.yml` for its supported targets and minimum IDF version (lan87xx and w5500 require IDF 6.0 or newer).

## RMII clock: the main pitfall
On ESP32 the 50 MHz REF_CLK must enter on GPIO0 (`EMAC_CLK_EXT_IN`) or be output by the ESP32 (APLL
source) on GPIO0, GPIO16 or GPIO17 (`EMAC_CLK_OUT`; the GPIO16/17 outputs are only available if PSRAM is
not used). GPIO0 is a strapping pin: if it samples low at power-up the chip enters download mode,
so disable the REF_CLK in hardware (for example hold the oscillator or PHY in reset) until the driver
is installed.

## SPI Ethernet (any chip with an SPI host, via an esp-eth-drivers component)
```c
spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO);
spi_device_interface_config_t dev = { .mode = 0, .clock_speed_hz = 20 * 1000 * 1000, .queue_size = 20, .spics_io_num = CS };
eth_w5500_config_t w = ETH_W5500_DEFAULT_CONFIG(SPI2_HOST, &dev);
w.base.int_gpio_num = INT_PIN;             /* or w.base.poll_period_ms if there is no INT line */
esp_eth_mac_t *mac = esp_eth_mac_new_w5500(&w, &mac_cfg);
esp_eth_phy_t *phy = esp_eth_phy_new_w5500(&phy_cfg);
```
A MAC address can be read or set with `esp_eth_ioctl(eth, ETH_CMD_G_MAC_ADDR / ETH_CMD_S_MAC_ADDR, mac_addr)`.

## Link events
`ETHERNET_EVENT_CONNECTED` and `ETHERNET_EVENT_DISCONNECTED` report the link state; IP assignment arrives separately as `IP_EVENT_ETH_GOT_IP`.

## Verify
- [ ] Link up at the expected speed (`esp_eth_ioctl(eth, ETH_CMD_G_SPEED, &speed)`).
- [ ] Board boots reliably with the RMII oscillator present (100 power cycles).
- [ ] iperf throughput meets requirement.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/network/esp_eth.rst, components/esp_eth headers) and the esp-eth-drivers repository (master).
Confirmed: ETH_ESP32_EMAC_DEFAULT_CONFIG (smi_gpio MDC 23 / MDIO 18, EMAC_CLK_EXT_IN, clock_gpio 0 on ESP32), no `EMAC_CLK_IN_GPIO` symbol exists (removed); REF_CLK input only on GPIO0 for ESP32, output on GPIO0/16/17, GPIO16/17 only without PSRAM, GPIO0 strapping warning; generic PHY driver in IDF with LAN87xx, IP101, W5500 and DM9051 drivers distributed as components (lan87xx and w5500 declare idf >=6.0); `eth_w5500_config_t` nests `int_gpio_num` and `poll_period_ms` under `.base`; ETH_CMD_G_MAC_ADDR, ETH_CMD_S_MAC_ADDR, ETH_CMD_G_SPEED in esp_eth_driver.h; ETHERNET_EVENT_CONNECTED/DISCONNECTED; esp_netif glue calls. Removed unconfirmed claims: the IDF 5.4 move date, the W5500 having no MAC address, DHCP restart behaviour, and the 100 Mbit full duplex expectation.

Method: documentation only; no commands were run.
