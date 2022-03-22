#!/bin/bash
BASEDIR="/var/www/energy"
EPOCH=`/bin/date +%s`
STARTEPOCH=`expr $EPOCH - 10800`
URL="http://local.ip:3000"

bacharge="$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to="$EPOCH"000&panelId=4&width=430&height=200&tz=Europe%2FSofia";
bavolt="$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to="$EPOCH"000&panelId=22&width=430&height=200&tz=Europe%2FSofia";
pvwatt="$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to="$EPOCH"000&panelId=20&width=430&height=200&tz=Europe%2FSofia";
totalwatt="$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to="$EPOCH"000&panelId=33&width=430&height=200&tz=Europe%2FSofia";
pvva="$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to="$EPOCH"000&panelId=30&width=1720&height=200&tz=Europe%2FSofia";
bavolt1="$URL/render/d-solo/000000001/solar?orgId=1&refresh=30s&from="$STARTEPOCH"000&to=&"$EPOCH"000&panelId=14&width=1720&height=200&tz=Europe%2FSofia";

`/usr/bin/wget -q --output-document=$BASEDIR/bacharge_tmp.png $bacharge`
`/usr/bin/wget -q --output-document=$BASEDIR/bavolt_tmp.png $bavolt`
`/usr/bin/wget -q --output-document=$BASEDIR/pvwatt_tmp.png $pvwatt`
`/usr/bin/wget -q --output-document=$BASEDIR/totalwatt_tmp.png $totalwatt`
`/usr/bin/wget -q --output-document=$BASEDIR/pvva_tmp.png $pvva`
`/usr/bin/wget -q --output-document=$BASEDIR/bavolt1_tmp.png $bavolt1`

mv -f $BASEDIR/bacharge_tmp.png $BASEDIR/bacharge.png
mv -f $BASEDIR/bavolt_tmp.png $BASEDIR/bavolt.png
mv -f $BASEDIR/pvwatt_tmp.png $BASEDIR/pvwatt.png
mv -f $BASEDIR/totalwatt_tmp.png $BASEDIR/totalwatt.png
mv -f $BASEDIR/pvva_tmp.png $BASEDIR/pvva.png
mv -f $BASEDIR/bavolt1_tmp.png $BASEDIR/bavolt1.png
