    Code for reading modbus data and populate to database

0 : Motor_Status - Bool
1 : DG_Status - Bool
2 : Solar_Inverter_Status - Bool
3 : Fire_Alarm_Status - Bool
4 : Lights_Status - Bool
'''

import os
import sys
import time
import django
import datetime

sys.path.append("path_to_find_the_required_files")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

from pyModbusTCP.client import ModbusClient 
django.setup()
from api import models

from daemonize import Daemonize

def fetchValues():
    ModbusBMS = ModbusClient(host="modbus_master_address", port=502, unit_id=100, auto_open=True, auto_close=True) 
    data = ModbusBMS.read_input_registers(0,5)
    return data

def dbInsStatus(status):
    row = models.status(
        Motor_Status = status[0],
        DG_Status = status[1],
        Solar_Inverter_Status = status[2],
        Fire_Alarm_Status = status[3],
        Lights_Status = status[4],
    )
    row.save()

def main():
    while True:
        data = fetchValues()
        lights = data[:5]
        dbInsStatus(status)

        with open('/tmp/mbcli_db.log','a') as fh:
            now = datetime.datetime.now()
            print(now,file=fh)
        
        time.sleep(60)


if __name__ == '__main__':
    pidfile = '/tmp/mbcli_db.pid'
    daemon = Daemonize(app='mbcli_db', pid=pidfile, action=main)
    daemon.start()
