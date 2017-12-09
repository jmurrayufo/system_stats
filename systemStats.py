#!/usr/bin/env python3

import json
import logging
import logstash
import platform
import psutil
import subprocess, re
import sys
import uptime

host = '192.168.1.2'
test_logger = logging.getLogger('systemStats.py')
test_logger.setLevel(logging.DEBUG)
test_logger.addHandler(logstash.LogstashHandler(host, 5002, version=1))
formatter = logging.Formatter('%(asctime)s %(process)d %(levelname)s %(filename)s %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
test_logger.addHandler(ch)

report_dict = {
   "metric": True,
   "app.name":"systemStats",
   "app.version":"1.2.0",
   "env.domain":"home",
   "env.infrastructure":"prod",
   "env.name":"isbe",
   "env.platform":platform.platform(),
   }


test_logger.info('Log Stats')

cpus = psutil.cpu_percent(interval=1, percpu=True)

cpu_total = 0.0

for idx,val in enumerate(cpus):
   cpu_total += val
   t_dict = report_dict.copy()
   t_dict['percent'] = val/100
   t_dict['name'] = 'CPU{}'.format(idx)
   test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['percent'] = cpu_total/4/100
t_dict['name'] = 'CPU_all'
test_logger.info(json.dumps(t_dict))


memory = psutil.virtual_memory()
#svmem(total=972369920, available=876040192, percent=9.9, used=35721216, free=497659904, active=176173056, inactive=262606848, buffers=25124864, cached=413863936, shared=6434816)
t_dict = report_dict.copy()
t_dict['bytes'] = memory.total
t_dict['name'] = 'Memory Total'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = memory.available
t_dict['name'] = 'Memory Available'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['percent'] = memory.percent/100
t_dict['name'] = 'Memory Utlization'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = memory.used
t_dict['name'] = 'Memory Used'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = memory.free
t_dict['name'] = 'Memory Free'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = memory.active
t_dict['name'] = 'Memory Active'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = memory.inactive
t_dict['name'] = 'Memory Inactive'
test_logger.info(json.dumps(t_dict))

disk = psutil.disk_usage('/')

t_dict = report_dict.copy()
t_dict['bytes'] = disk.total
t_dict['name'] = 'Disk Total'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = disk.used
t_dict['name'] = 'Disk Used'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['bytes'] = disk.free
t_dict['name'] = 'Disk Free'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
t_dict['percent'] = disk.percent/100
t_dict['name'] = 'Disk Percent'
test_logger.info(json.dumps(t_dict))

home = psutil.disk_usage('/home/jmurray')

t_dict = report_dict.copy()
t_dict['bytes'] = home.used
t_dict['name'] = 'Home Used'
test_logger.info(json.dumps(t_dict))

t_dict = report_dict.copy()
up_time = uptime.uptime()
t_dict['generic_float'] = up_time
t_dict['name'] = 'Uptime'
test_logger.info(json.dumps(t_dict))

test_logger.info('Finished logging stats')
