import minimalmodbus
import time

# on/off
ON = 1
OFF = 0

regs={
'pvvolt': 0x3100,
'pvamps': 0x3101,
'pvwattl': 0x3102,
'pvwatth': 0x3103,
'bavolt': 0x3104,
'baamps': 0x3105,
'bawattl': 0x3106,
'bawatth': 0x3107,
'batemp': 0x3110,
'baperc': 0x311A,
'bastat': 0x3200,
'eptemp1': 0x3111,
'eptemp2': 0x3112,
'epstat': 0x3201,
'dcvolt': 0x310C,
'dcamps': 0x310D,
'dcwattl': 0x310E,
'dcwatth': 0x310F,
'pvkwhtotal': 0x3312,
'dckwhtotal': 0x330A,
'pvkwhtoday': 0x330C,
'dckwhtoday': 0x3304
}

# Settings
#BatteryType=0x9000
#BatteryCapacity=0x9001
#TempCompensationCoeff=0x9002
#OverVoltageDisconnect=0x9003
#ChargingLimitVoltage=0x9004
#OverVoltageReconnect=0x9005
#EqualizationVoltage=0x9006
#BoostVoltage=0x9007
#FloatVoltage=0x9008
#BoostReconnectVoltage=0x9009
#LowVoltageReconnect=0x900A
#UnderVoltageRecover=0x900B
#UnderVoltageWarning=0x900C
#owVoltageDisconnect=0x900D
#DischargingLimitVoltage=0x900E

class SolarTracer:
	"""A member of SolarTracer communication class."""

	# connect to device
	def __init__(self, debug, logh, Logger, device = '/dev/ttyXRUSB0', serialid = 1):
		self.device = device
		self.id = serialid
		self.instrument = 0
		self.logh=logh
		self.Logger=Logger
		self.debug=debug

	def connect(self):
		try:
			self.instrument = minimalmodbus.Instrument(self.device, self.id)
		except minimalmodbus.serial.SerialException as e:
			self.logh(self.Logger(self.debug, 'MODBUS', str(e)))
			return -1

		self.instrument.serial.baudrate = 115200
		self.instrument.serial.bytesize = 8
		self.instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
		self.instrument.serial.stopbits = 1
		self.instrument.serial.timeout  = 1.2
		self.instrument.mode = minimalmodbus.MODE_RTU
		return 0
	
	def disconnect (self):
		self.instrument.serial.close()
		return 0;

	# read informational register
	def readReg(self,register):
		time.sleep(0.05) # dummy delay for sequence readings
		try:
			reading = self.instrument.read_register(register, 2, 4)
			return reading
		except IOError as e:
			self.logh(self.Logger(self.debug, 'TRACER', str(e)))
			return -2

	# read parameter
	def readParam(self,register,decimals=2,func=3):
		try:
			reading = self.instrument.read_register(register, decimals, func)
			return reading
		except IOError as e:
			self.logh(self.Logger(self.debug, 'TRACER', str(e)))
			return -2

	# write parameter
#	def writeParam(self,register,value,decimals=2,func=16):
#	    try:
#	            reading = self.instrument.write_register(register, value, decimals, func)
#	            return 0
#	    except IOError as err:
#	    		return -2
#	    except ValueError:
 #   			print ("Could not convert data!")
  #  			return -3



