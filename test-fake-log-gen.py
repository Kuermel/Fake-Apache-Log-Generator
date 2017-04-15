#!/usr/bin/python
import time
import datetime
import random
import gzip
import sys
import argparse
from faker import Factory
fake = Factory.create('de_DE')
from tzlocal import get_localzone
local = get_localzone()


#todo:
# allow writing different patterns (Common Log, Apache Error log etc)
# log rotation


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT", choices=['LOG','GZ','CONSOLE'] )
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int, default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)
parser.add_argument("--sleep", "-s", help="Sleep this long between lines (in seconds)", default=0.0, type=float)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type


timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()

outFileName = 'access_log_'+timestr+'.log' if not file_prefix else file_prefix+'_access_log_'+timestr+'.log'

for case in switch(output_type):
	if case('LOG'):
		f = open(outFileName,'w')
		break
	if case('GZ'):
		f = gzip.open(outFileName+'.gz','w')
		break
	if case('CONSOLE'): pass
	if case():
		f = sys.stdout

flag = True
while (flag):
	if args.sleep:
		increment = datetime.timedelta(seconds=args.sleep)
	else:
		increment = datetime.timedelta(seconds=random.randint(30, 300))
	otime -= increment

	ipv4 = fake.ipv4()
	ipv6 = fake.ipv6()
	url = fake.url()
	uri = fake.uri()
	mac_address = fake.mac_address()
	user_agent = fake.user_agent()
	email = fake.email()
	user_name =fake.user_name()
	name = fake.name()
	int_number = fake.random_int(min=0, max=9999)
	color = fake.hex_color()
  
  
	dt = otime.strftime("%Y-%m-%dT%H:%M:%S")
	tz = datetime.datetime.now(local).strftime('%z')
  
	f.write(('time=%s|IPv4=%s|IPv6=%s|url=%s|uri=%s|mac_address=%s|user_agent=%s|email=%s|user_name=%s|name=%s|int=%s|color=%s\n' % (dt,ipv4,ipv6,url,uri,mac_address,user_agent,email,user_name,name,int_number,color)).encode('utf8'))

	log_lines = log_lines - 1
	flag = False if log_lines == 0 else True
	if args.sleep:
		time.sleep(args.sleep)
