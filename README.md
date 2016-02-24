Export-CloudWatch-Metrics
=======

Export-CloudWatch-Metrics è uno scritp che permette di esportare direttamente le metriche di cloudwatch su S3

## Prerequisiti

* Python 3 o maggiore
* boto3
* AWS cli configured on machine

## Link Collegati

* **Download Python** [here](https://www.python.org/downloads/)
* **boto3** documentation [here](https://boto3.readthedocs.org/en/latest/)
* **Aws Namespaces** documentation [here](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/aws-namespaces.html)

### Run

I valori da passare allo scritps sono:
* name_space  => ovvero quale tipo di metrica di cloudwach vogliamo ottenere
* instance_id => id dell'istanza da ispezionare
* metric_name => il nome della metrica da ottenere
* statistic   => in che modo la statistica deve essere restituita
* unit        => in che tipo di unità voglio ricevere le informazioni
* period      => l'intervallo espresso in secondi
* start_time  => la data di inizio es YYYY-MM-DD hh:mm:ss
* end_time    => la data di fine es YYYY-MM-DD hh:mm:ss
* s3_bucket   => il Bucket s3 su salvare le metriche in formato .log

comando da eseguire 

```
$ python getCWMetrics.py -n 'nameSpace' -i 'istanceId' -m 'metric _name' -s 'statistic' -u 'unit' -p 'period' -S 'YYYY-MM-DD hh:mm:ss' -E 'YYYY-MM-DD hh:mm:ss' -b 'bucketName'
```

## Parameters

* **Aws Namespaces** documentation [here](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/aws-namespaces.html)

	Sono utilizzabili tutti i name space riportati.

	Nel caso si utilizzino delle metriche di Sistema [vedi qui](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/mon-scripts.html) potete utilizzare il nameSpace 
	"System/Linux"

* **Instance ID** 
	
	Inserire l'id della macchina da monitorare es: "i-abcdefghi"

* **Metric Name** documentation [here](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CW_Support_For_AWS.html)

* **Statistics** 
	Utilizzabile uno tra i seguenti valori : 'SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum'

* **Unit** 
	Utilizzabile uno tra i seguenti valori : 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'

* **Period** 
	Occorre passare un valore int che esprima l'intervallo (in secondi) da prendere in considerazione es: -p 3600 => intervallo di 1h

* **Start Time & End Time** 
	Occorre passare stringa con il seguente formato: "YYYY-MM-DD hh:mm:ss"
	NB Start Time deve essere minore di End Time

* **Bucket Name** 
	Occorre passare stringa nome del bucket nel quale si vogliono storare le metriche

### Result

Il risultato che andrete ad ottenere è il seguente: nel bucket di s3 che avete designato come ospitante delle metriche, verrà creato un oggetto con il seguente percorso "metrics-logs/20160210-20160220/i-91f55819_CPUUtilization.log". L'oggetto è formato dal periodo monitorato, l'id della macchina ec2 e il nome della metrica che richiedete.