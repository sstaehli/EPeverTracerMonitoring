#!/bin/bash
# Get Epever Tracer data from filesnap 
######################################################
GREP=/usr/bin/grep
CAT=/usr/bin/cat
CUT=/usr/bin/cut
WC="/usr/bin/wc -l"
####
DUMP="/tmp/ep_tracer_$1.log"
######################################################

function show_usage  {
echo "#######################################################"
echo "# Get Epever Tracer data from filesnap                #"
echo "#######################################################"
echo ""
echo "Usage: ./get_tracer.sh <id> <check>"
echo ""
}	

function show_error  {
echo "#######################################################"
echo "# Get Epever Tracer data from filesnap                #"
echo "#######################################################"
echo ""
echo $1
echo ""
}

if test "${1+set}" != set ; then
	show_usage
	exit -1
fi

if test "${2+set}" != set ; then
        show_usage
        exit -1
fi

if [ ! -f $DUMP ]; then
	show_error "ERROR: $DUMP not found. Check the ID or logtracer.py (filesnap) never executed"
	exit -1
fi

if [ `$CAT $DUMP | $GREP $2 | $CUT -d':' -f2 | $WC` == "0" ]; then
	show_error "ERROR: Data not found. Verify the seeking check"
	exit -1
fi

$CAT $DUMP | $GREP $2 | $CUT -d':' -f2
exit 0
