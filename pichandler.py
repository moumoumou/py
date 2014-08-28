#!/usr/local/bin/python2.7

import datetime, time
import pyinotify
import logging
import imghdr
import os.path
import os
import re
from pymongo import Connection
import gridfs


LOGDIR = '/var/log/pichdr'
LOGNAME = 'picSaveHdr.log'

COLL = 'pic'

def initFtpDir(rootDir):
	for root, dirs, filelist in os.walk(rootDir):
		for file in filelist:
			if not file.startswith('.') and imgRecognize(os.path.join(rootDir,file), file):
				sf = 0
				resvGridfs(file, os.path.join(rootDir,file), sf, file.split('_')[0])

def rmAll(path_file):
	if os.path.isdir(path_file):
		os.rmdir(path_file)
	elif os.path.isfile(path_file):
		os.remove(path_file)

def imgRecognize(path_file, _file):
	try:
		#time.sleep(0.01)
		imgtype = imghdr.what(path_file)
		pattern = re.compile(r'^\d+_\d+\.(jpg|jpeg|png|gif)$', re.I)
		if imgtype and pattern.match(_file):
			return 1
		else:
			#logg('warning', '%s file not matched' % _file)
			rmAll(path_file)
			return 0
	except BaseException, e:
		#logg('warning', e)
		rmAll(path_file)
		return 0


def resvGridfs(bn, fn, sf, uid):
    conn = Connection('127.0.0.1', 27017)
    db = conn.melotpic
    fs = gridfs.GridFS(db, collection=COLL)
    with open(fn, 'rb') as file:
        fs.put(file.read(), filename=bn, saveflag=sf, userid=uid)
	os.remove(fn)
	#logg('info', '%s img resaved' % bn)

def logg(level, content):
	global LOGDIR, LOGNAME
	logtime = datetime.datetime.now()

	if not os.path.exists(LOGDIR):
		os.mkdir(LOGDIR)
	logpath = os.path.join(LOGDIR, LOGNAME)
	logging.basicConfig(level=logging.INFO, filename=logpath)
	if level == 'info':
		logging.info('[%s] %s' % (logtime, content))
	if level == 'warning':
		logging.warning('[%s] %s' % (logtime, content)) 
	

class myEventHandler(pyinotify.ProcessEvent):

	#def process_IN_CREATE(self, event):
	def process_IN_CLOSE_WRITE(self, event):

		path_file = event.pathname
		_file = event.name
		nowtime = datetime.datetime.now()

		if imgRecognize(path_file, _file):
			#print path_file
			sflag = 0
			userid = _file.split('_')[0]

			resvGridfs(_file, path_file, sflag, userid)
		else:
			pass
			
def main():
	#LOGDIR = '/var/log/pichandler'
	#LOGNAME = 'picSaveHdr.log'

	initFtpDir('/ftphome/melot')
    # watch manager
	wm = pyinotify.WatchManager()
	wm.add_watch('/ftphome/melot', pyinotify.ALL_EVENTS, rec=True)
    # event handler
	eh = myEventHandler()
    # notifier
	notifier = pyinotify.Notifier(wm, eh)
	notifier.loop()

if __name__ == '__main__':
    
	main()
