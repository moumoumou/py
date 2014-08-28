#!/usr/local/bin/python2.7

from pymongo import Connection
from bson.objectid import ObjectId
import gridfs
import datetime, time
import re

conn = Connection('127.0.0.1', 27017)

db = conn.melotpic
srccoll = db.pic.files
srcfs = gridfs.GridFS(db, collection='pic')

dbbak = conn.bakpic
bak_coll = 'bak%s' % str(datetime.datetime.now().month)
dstfs = gridfs.GridFS(dbbak, collection=bak_coll)

indexcoll = db.samplingInterval

def selectInterval(userid):
	interval = indexcoll.find_one({'userid':userid})
	if not interval:
		interval = 5
		d = {'userid':userid, 'interval':interval}
		indexcoll.insert(d)
	else:
		interval = int(indexcoll.find_one({'userid':userid})['interval'])
	return interval

def getUserIdList(srcfsFind):
	userIdList = []
	for grid_out in srcfsFind:
		#print grid_out.userid
		if grid_out.userid not in userIdList:
			userIdList.append(grid_out.userid)
	return userIdList

def findRecordOfOne(userid, timestamp):
	'''
	    get all record(fmt:GridOut) of a userid
		return a list of record
	'''
	recordOfOne = []
	for grid_out in srcfs.find({'userid':userid}, timeout=False).sort('uploadDate'):
		tsp = int(re.split(r'_|\.', grid_out.filename)[1])
		if grid_out.userid == userid and tsp < timestamp:
			recordOfOne.append(grid_out)
	return recordOfOne

def getTimeStampHoursAgo(now, nhour):
	hourAgo = now - datetime.timedelta(hours=nhour)
	timeStamp = int(time.mktime(hourAgo.timetuple()))
	return timeStamp
	
	
	
def main():
    
	srcfsFind = srcfs.find(timeout=False)
	allUserIdList = getUserIdList(srcfsFind)
	#print allUserIdList

	_now = datetime.datetime.now()

	for userid in allUserIdList:
		recordOfOne = findRecordOfOne(userid, getTimeStampHoursAgo(_now, 1))	
		interval = selectInterval(userid)
		#print interval

		counter = 0
		for record in recordOfOne:
			counter += 1

			if counter%interval == 0 or record.saveflag == -1:
				#print record.filename

				dstfs.put(record, filename=record.filename, saveflag=record.saveflag, userid=record.userid)
				srcfs.delete(record._id)
			else:
				srcfs.delete(record._id)

if __name__ == "__main__":
    
    main()