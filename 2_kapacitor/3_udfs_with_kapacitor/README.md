# 3. User Defined Functions with Kapacitor
* Write a UDF in Python
* Configure a UDF with Kapacitor

## By the end of this section students will be able to...
* Describe what a User Defined Function (UDF) is and its role in Kapacitor
* Explain the interface that a UDF needs to implement
* Configure a UDF to work with Kapacitor

## Exercises

### Using a UDF

#### 1. Configure Kapacitor for the `moving_avg` UDF.

```
[udf]
[udf.functions]
    # Example python UDF.
    # Use in TICKscript like:
    #   stream.pyavg()
    #           .field('value')
    #           .size(10)
    #           .as('m_average')
    #
    # uncomment to enable
    [udf.functions.pyavg]
        prog = "/usr/bin/python2" # Should be the path to the python2 on your machine
        # Should be the path to https://github.com/influxdata/kapacitor/blob/master/udf/agent/examples/moving_avg/moving_avg.py locally on your computer
        args = ["-u", "/etc/kapacitor/udf/agent/examples/moving_avg/moving_avg.py"]
        timeout = "10s"
       [udf.functions.pyavg.env]
           # Should be path to https://github.com/influxdata/kapacitor/tree/master/udf/agent/py locally on your computer
           PYTHONPATH = "/etc/kapacitor/udf/agent/py"
```

#### 2. Start Kapacitor
**Note:** Before starting it, if you don't have python protocol buffers installed please run `sudo pip install googleapis-common-protos`.

#### 3. Create and enable a task in Kapacitor with the following TICKscript

**cpu_avg.tick**
```
stream
.from().measurement('cpu')
.where(lambda: "cpu" == 'cpu-total')
.pyavg()
  .field('usage_idle')
  .size(10)
  .as('cpu_avg')
.influxDBOut()
  .database('mydb')
  .retentionPolicy('default')
  .measurement('cpu_avg')
  .tag('kapacitor', 'true')
```

**Hint**
```sh
$ kapacitor define -name cpu_avg -type stream -tick cpu_avg.tick -dbrp telegraf.default
$ kapacitor enable cpu_avg
```


#### 4. Create a Graph in Grafana for the measurement `cpu_avg` in the database `mydb`


### Writing your own UDF

TODO

