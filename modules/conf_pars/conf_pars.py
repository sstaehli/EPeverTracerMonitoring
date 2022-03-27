import configparser
import socket
import sys

cnfp_req_version = (3,2)
cnfp_cur_version = sys.version_info

class Config_Parser (object):
    def __init__(self, conffile):
        self.conffile=conffile
    
    # ToDo miningful validataion    
    def validate(self):
        config = configparser.ConfigParser()
        a=config.read(self.conffile)
        if len(a)==0:
            return False
        if cnfp_cur_version == cnfp_req_version: # COnfig parser don't work in the same way in Python 3.1 and 3.2
            for c in config['DEFAULT']:
                if 'ip' in c:
                    if not self.valid_ip(config['DEFAULT'][c]):
                        return False
                elif 'port' in c:
                    if not self.valid_port(int(config['DEFAULT'][c])):
                        return False
        return config
    
    # ToDo miningful validataion
    def dbvalidate(self):
        config = configparser.ConfigParser()
        a=config.read(self.conffile)
        if len(a)==0:
            return False
        if cnfp_cur_version == cnfp_req_version: # COnfig parser don't work in the same way in Python 3.1 and 3.2
            for c in config['INFLUXDB']:
                if 'ip' in c:
                    if not self.valid_ip(config['INFLUXDB'][c]):
                        return False
        return config
    
    def valid_ip(self, ip):
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return True
            
    def valid_port(self, port):
        return isinstance(port, int)