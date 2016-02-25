import boto3
from datetime import datetime
import json
import sys, getopt
from optparse import OptionParser



def prepareDate(date):
	result = date.replace(' ','-')
	result = result.replace(':','-')
	return result.split('-')

def getMetrics(instanceId, name_space, metricName, statistics, unit, startTime, endTime, period):
	cloud_watch = boto3.client('cloudwatch')

	response = cloud_watch.get_metric_statistics(
		Namespace=name_space,
	    MetricName=metricName,
	    Dimensions=[
        	{
            	'Name': 'InstanceId',
            	'Value': instanceId
        	},
    	],
	    StartTime=startTime,
	    EndTime=endTime,
	    Period=period,
	    Statistics=[
	        statistics
	    ],
	    Unit=unit
	)

	for i in response["Datapoints"]:
		Timestamp = str(i["Timestamp"])
		i["Timestamp"] = Timestamp

	return response


def pushToS3(bucket, key, json):
	s3 = boto3.client('s3')
	response = s3.put_object(
		Body=bytes(str(json), encoding="UTF-8"),
	    Bucket=bucket,
	    Key=key,
	)

def createObjectName(dateStart, dateEnd, Namespace, MetricName, Statistics, instanceID):
	start_time = datetime(int(dateStart[0]),int(dateStart[1]),int(dateStart[2])).strftime("%Y%m%d")
	end_time = datetime(int(dateEnd[0]),int(dateEnd[1]),int(dateEnd[2])).strftime("%Y%m%d")

	return 'metrics-logs/'+start_time+'-'+end_time+'/'+Namespace+'_'+instanceID+'_'+MetricName+'_'+Statistics+'.log'

	
def main():
	usage = "usage: %prog [options] arg"
	parser = OptionParser()
	parser.add_option("-n", "--name_space", dest="name_space", help="set the AWS namespace", metavar="NAMESPACE")
	parser.add_option("-i", "--instance_id", metavar="INSTANCE_ID" , dest="instance_id", help="set the EC2 instance id")
	parser.add_option("-m", "--metric_name", metavar="METRIC_NAME" , dest="metric_name", help="set the EC2 instance id")
	parser.add_option("-s", "--statistic", metavar="STATISTIC" , dest="statistic", help="set the name of Statistics")
	parser.add_option("-u", "--unit", metavar="UNIT" , dest="unit", help="set the unit Value")
	parser.add_option("-p", "--period", metavar="PERIOD" , dest="period", help="set the period es 300")
	parser.add_option("-S", "--start_time", metavar="START_TIME" , dest="start_time", help="set the Start Time es: YYYY-MM-DD hh:mm:ss")
	parser.add_option("-E", "--end_time", metavar="END_TIME" , dest="end_time", help="set the EC2 End Time es: YYYY-MM-DD hh:mm:ss")
	parser.add_option("-b", "--bucket_name", metavar="BUCKET_NAME" , dest="bucket_name", help="set the s3 Bucket Name")

	(options, args) = parser.parse_args()
	if not options.name_space:   # if filename is not given
		parser.error('Namespace not given')
	if not options.instance_id:   # if filename is not given
		parser.error('Instance Id not given')
	if not options.metric_name:   # if filename is not given
		parser.error('Metric Name not given')		
	if not options.statistic:   # if filename is not given
		parser.error('Statistic not given')
	if not options.unit:   # if filename is not given
		parser.error('Unit not given')
	if not options.start_time:   # if filename is not given
		parser.error('Start Time not given')
	if not options.end_time:   # if filename is not given
		parser.error('End Time not given')	
	if not options.period:   # if filename is not given
		parser.error('End Time not given')
	if not options.bucket_name:   # if filename is not given
		parser.error('BUCKET_NAME not given')

	options.start_time = prepareDate(options.start_time)
	options.end_time = prepareDate(options.end_time)
	name_space = options.name_space
	instance_id = options.instance_id
	metric_name = options.metric_name
	statistic = options.statistic
	unit = options.unit
	bucket_name = options.bucket_name
	period = int(options.period)
	startTime = datetime(int(options.start_time[0]),int(options.start_time[1]),int(options.start_time[2]),int(options.start_time[3]),int(options.start_time[4]),int(options.start_time[5])).isoformat('T')+'Z'
	endTime = datetime(int(options.end_time[0]),int(options.end_time[1]),int(options.end_time[2]),int(options.end_time[3]),int(options.end_time[4]),int(options.end_time[5])).isoformat('T')+'Z'
	


	response = getMetrics(instance_id,name_space,metric_name,statistic,unit,startTime,endTime,period)
	pushToS3(bucket_name, createObjectName(options.start_time,options.end_time,name_space,metric_name,statistic,instance_id), response)		
	


if __name__ == "__main__":
    main()