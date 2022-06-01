# EPever U-Power Monitoring with Docker

This project is about monitoring an EPever U-Power Solar Charger/Inverter connected via USB/RS485 Modbus RTU to a physical server where the interface is passed to docker. Data is aquired with a python module, sent to an Influx database and published on a Grafan dashboard.

## Setup & Usage - Minimal Instructions

- Build and install the Exar USB Serial converter driver found in `xr_usb_serial_common` on your target system.
- Edit [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml) to match your setup
- Use [Traefik](https://traefik.io/) or similar Proxy to expose Grafna. The traefik labels in the docker-compose file can be removed and ports might be exposed directly if traefik is not used.
- Run `docker-compose up -d` to start the services
- Configure the Influx database and Grafana's connection to that database accordingly. For Grafana, Query Language Flux and an Influx Token is recommended. The Influxdatabase is reachable under `http://db:8086', where the url name equals the the Influx database docker service name (see [docker-compose.yml](docker-compose.yml)).

## How to configure the Grafana Dashboard

- **Save** the dashboard when it's open by clicking the share icon and choose `Export > Save to File`

- **Load** the dashboard by hitting the `+ > Import...` sign in the left menu bar
- PAste the code from [grafana.json] to the JSON text field and click `Load`
