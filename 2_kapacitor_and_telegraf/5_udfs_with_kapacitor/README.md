# 3. User Defined Functions with Kapacitor
* Write a UDF in Python
* Configure a UDF with Kapacitor

## By the end of this section students will be able to...
* Describe what a User Defined Function (UDF) is and its role in Kapacitor
* Explain the interface that a UDF needs to implement
* Configure a UDF to work with Kapacitor

## Exercises

### Using a UDF

#### 1. Configure Kapacitor for the `outliers` UDF.

```
[udf]
[udf.functions]
    [udf.functions.outliers]
        # Should be the path to the outliers binary on your machine
        prog = "/Users/michaeldesa/go/src/github.com/influxdata/capital-one-slides/2_kapacitor_and_telegraf/5_udfs_with_kapacitor/udfs/osx/outliers"
        timeout = "10s"
```

#### 3. Read over the `python` implementation of the `outliers` UDF.


#### 3. Create and enable a task in Kapacitor with the following TICKscript

**cpu_outliers.tick**
```js
batch
    |query('''
        SELECT * FROM "telegraf"."autogen"."cpu" WHERE cpu='cpu-total'
    ''')
    @outliers()
      .field('user')
    |influxDBOut()
      .database('mydb')
      .retentionPolicy('autogen')
      .measurement('cpu_outliers')
```

**Hint**
```sh
$ kapacitor define -name cpu_outliers -type batch -tick cpu_outliers.tick -dbrp telegraf.default
$ kapacitor enable cpu_outliers
```


#### 4. Create a Graph in Grafana for the measurement `cpu_outliers` in the database `mydb`

#### 5. What types of UDFs would you like to see?

#### 6. Bonus: For those with `python` or `go` experience, try creating your own basic UDF.

