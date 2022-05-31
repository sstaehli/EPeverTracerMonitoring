import sys
import os
import minimalmodbus
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

registers={
    'util_volt': [ 0x3500, 2 ],
    'util_charge_volt' : [ 0x3505, 2 ],
    'util_charge_cur': [ 0x3506, 2 ],
    'util_pwr': [ 0x3507, 2 ],
    'util_energy': [ 0x350F, 2 ],

    'pv_volt': [ 0x3519, 2 ],
    'pv_cur': [ 0x351A, 2 ],
    'pv_pwr': [ 0x351B, 2 ],
    'pv_charge_volt': [ 0x351D, 2 ],
    'pv_charge_cur': [ 0x351E, 2 ],
    'pv_charge_power' : [ 0x351F, 2 ],

    'inv_volt' : [ 0x3533, 2 ],
    'inv_cur' : [ 0x3534, 2 ],
    'inv_pwr' : [ 0x3536, 2 ],
    'inv_freq' : [ 0x353B, 2 ],

    'batt_volt' : [ 0x354C, 2 ],
    'batt_temp' : [ 0x354F, 2 ],
    'batt_soc' : [ 0x3550, 0 ],
    'bypass_volt' : [ 0x3558, 2 ],
    'bypass_cur' : [ 0x3559, 2 ],
    'bypass_pwr' : [ 0x3559, 2 ],
}

class EPCom:

    def __init__(self, device, id):
        self.device = device
        self.id = id

    def connect(self):
        try:
            self.instrument = minimalmodbus.Instrument(self.device, self.id)
        except minimalmodbus.serial.SerialException as e:
            print("Not ideal... %s" % str(e))

        self.instrument.serial.baudrate = 115200
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 1.2
        self.instrument.mode = minimalmodbus.MODE_RTU

    def readReg(self, register, decimals, func) -> float:
        try:
            retval = self.instrument.read_register(register, decimals, func)
        except:
            retval = -1.0
        return retval

# connect to inverter
up = EPCom("/dev/ttyXRUSB0",10)
up.connect();

# connect to db
try:
    # You can generate a Token from the "Tokens Tab" in the UI
    token = "pcq_p2IPBEI7lxXfks9WX9Sh709wrIBteLuUQOVvruaB8pVcFPOQQTsAu66zeH0n00YtkXYF6IabcSmKL3aaPg=="
    org = "org"
    bucket = "solardata"
    dbclient = InfluxDBClient(url="http://db:8086", token=token)
except:
    print("DB Problem!")

write_api = dbclient.write_api(batch_size=len(registers), flush_interval=30_000, jitter_interval=2_000, retry_interval=5_000)

# endless
while True:
    #print("---")
    # collect dataset
    t = datetime.utcnow()
    for i, (reg, adr) in enumerate(registers.items()):
        record = Point("solards")\
            .tag("inverter", "Upower3222-10")\
            .field(reg, float(up.readReg(adr[0], adr[1], 0x04)))\
            .time(t, WritePrecision.S)
        try:
            write_api.write(bucket, org, record)
        except:
            errortime = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            print("Could not write record %s (%s)" % (reg, errortime))
        time.sleep(0.5)

    # pause
    time.sleep(30)
    
