import sys
import os
import minimalmodbus
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from math import nan

registers={
    # addres | decimals | 32-bit 
    'util_volt': [ 0x3500, 2, False ],
    'util_charge_volt' : [ 0x3505, 2, False ],
    'util_charge_cur': [ 0x3506, 2, False ],
    'util_pwr': [ 0x3507, 2, True ],
    'util_energy': [ 0x350F, 2, True ],

    'pv_volt': [ 0x3519, 2, False ],
    'pv_cur': [ 0x351A, 2, False ],
    'pv_pwr': [ 0x351B, 2, True ],
    'pv_charge_volt': [ 0x351D, 2, False ],
    'pv_charge_cur': [ 0x351E, 2, False ],
    'pv_charge_pwr' : [ 0x351F, 2, True ],

    'inv_volt' : [ 0x3533, 2, False ],
    'inv_cur' : [ 0x3534, 2, False ],
    'inv_pwr' : [ 0x3536, 2, True ],
    'inv_freq' : [ 0x353B, 2, False ],

    'batt_volt' : [ 0x354C, 2, False ],
    'batt_temp' : [ 0x354F, 2, False ],
    'batt_soc' : [ 0x3550, 0, False ],
    
    'bypass_volt' : [ 0x3558, 2, False ],
    'bypass_cur' : [ 0x3559, 2, False ],
    'bypass_pwr' : [ 0x355A, 2, True ],
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

    def readReg(self, register, decimals, func, reg32 = False) -> float:
        try:
            if reg32:
                retval = (self.instrument.read_long(register, func, False, byteorder = minimalmodbus.BYTEORDER_LITTLE_SWAP)) / pow(10.0, decimals)
            else:            
                retval = self.instrument.read_register(register, decimals, func, False)
        except:
            retval = nan
        return retval

# connect to inverter
up = EPCom("/dev/ttyXRUSB0",10)
up.connect();

# connect to db
try:
    # You can generate a Token from the "Tokens Tab" in the UI
    token = "Y4R3mStnYYjiO8cKLb8RWLxRsOKlgIVT-b_UAQb-_p-HrGf-AROH_o2kaIvfV-HIFgNAOEHnEa6LI8q8cXQz-g=="
    org = "org"
    bucket = "solardata"
    dbclient = InfluxDBClient(url="http://db:8086", token=token)
except:
    print("DB Problem!")

write_api = dbclient.write_api(batch_size=len(registers), flush_interval=30_000, jitter_interval=2_000, retry_interval=5_000)

# endless
while True:
    # collect dataset
    t = datetime.utcnow()
    for i, (reg, adr) in enumerate(registers.items()):
        record = Point("solards")\
            .tag("inverter", "Upower3222-10")\
            .field(reg, float(up.readReg(adr[0], adr[1], 0x04, adr[2])))\
            .time(t, WritePrecision.S)
        try:
            write_api.write(bucket, org, record)
        except:
            errortime = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            print("Could not write record %s (%s)" % (reg, errortime))
        time.sleep(0.5)

    # pause
    time.sleep(30)
    
