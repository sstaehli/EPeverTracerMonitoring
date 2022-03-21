**UNDER RESTRUCTURING - not ready to be used**

Monitoring EPsolar Tracer devices via RS-485 with various logging options 
=========================================================================

**EPSolar Tracer** AN/BN devices have been around for a while so this is just another attempt to establish a good monitoring package.
**Supporting multiple controlers** via PAL-ADP Parallel Adapter (up to 6 controllers).

Main features:
* Data logging to DB, file, MQTT
* Grafana dashboard
* Error logs
* Device communication issues handling
* Multiple charge controllers supported
* Configuration options

## Requirements
- Linux - any distro - Debian, Ubuntu, Raspbian...
- Python 3 
- Influx DB and its Python modules
- Grafana
- Paho-MQTT 
- To communicate with the devices you will need [Minimal Modbus](https://minimalmodbus.readthedocs.io/en/stable/) module for Python
- CC-USB-RS485-150U cable
- PAL-ADP (optional)

Make sure you install the Linux driver for Exar USB UART first
--------------------------------------------------------------
The [xr_usb_serial_common](xr_usb_serial_common-1a/) directory contains the makefile and instructions that will compile properly on Liux. Before compiling be sure to install the linux headers.
Working with newest kernels (tested on 5.13)

* xr_serial stock kernel module is not suitable for communication with Epever devices

The resulting `xr_usb_serial_common.ko` file will need to be moved to `/lib/modules/YOUR_LINUX_VERSION/extra/`.
After building and moving the module, remove the xr_serial (cdc-acm on raspbian) that automatically installs for the usb-485 adapter.

You will also need to add the xr_serial (cdc-acm on raspbian) to the system blacklist:

If all goes well you should see `ttyXRUSB` when listing `ls /dev/tty*`

Device communications protocols
-------------------------------
* [Protocol for Epsolar Tracer] Check the pdf in folder: epsolars-docs

Python modules
--------------
Install minimalmodbus first:
`pip3 install minimalmodbus`

ToDO

Logging scripts
---------------
ToDo

Logging options
---------------
InfluxDB - used for Grafana visualization (for multiple devices, the watt data is agdregated)
File - separate file for each controller in dictionary structured format - to process or to integrate the data with other systems
MQTT - ToDo
Single registry check (volt, amp...) - mainly for testing

Grafana Dashboard
-----------------
Some very basic knowledge of InfluxDB and Grafana is assumed here.

![Img](grafana/screenshot.png)
The [grafana/](grafana/) folder contains the dashboard to monitor realtime and historical solar charging data.

## Grafana/InfluxDB installation

Use [this guide](https://simonhearne.com/2020/pi-influx-grafana/) to install InfluxDB and Grafana on Raspberry Pi

Run http://local.ip:3000 to configure the Grafana console

When you add InfluxDB as a Data Source. Influx DB should be set up with the following parameters:

- user = "grafana"
- pass = "solar"
- db   = "solar"
- host = "127.0.0.1"
- port = 8086

At this point you can also import SolarDashboard from [grafana/](grafana/) folder.

Use "solar" dataset to import the values from when setting up the console.


