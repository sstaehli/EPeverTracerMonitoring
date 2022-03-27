#!/bin/sh
GRAFANA_HOST='grafana'
GRAFANA_PORT=8086
GRAFANA_USER='grafana'
GRAFANA_PASS='solar'

influx -host $GRAFANA_HOST -port $GRAFANA_PORT -username $GRAFANA_USER -password $GRAFANA_PASS -execute 'drop measurement solar_backup' -database solar
influx -host $GRAFANA_HOST -port $GRAFANA_PORT -username $GRAFANA_USER -password $GRAFANA_PASS -execute 'SELECT * INTO solar_backup from solar GROUP BY *' -database solar
influx -host $GRAFANA_HOST -port $GRAFANA_PORT -username $GRAFANA_USER -password $GRAFANA_PASS -execute 'SELECT * INTO solar_clean from solar WHERE PVwatt>-1 and DCwatt>-1 GROUP BY *' -database solar
influx -host $GRAFANA_HOST -port $GRAFANA_PORT -username $GRAFANA_USER -password $GRAFANA_PASS -execute 'drop measurement solar' -database solar
influx -host $GRAFANA_HOST -port $GRAFANA_PORT -username $GRAFANA_USER -password $GRAFANA_PASS -execute 'SELECT * INTO solar from solar_clean GROUP BY *' -database solar
influx -host $GRAFANA_HOST -port $GRAFANA_PORT -username $GRAFANA_USER -password $GRAFANA_PASS -execute 'drop measurement solar_clean' -database solar
