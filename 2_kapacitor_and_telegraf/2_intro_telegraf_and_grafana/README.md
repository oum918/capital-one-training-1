# 4. Intro to Telegraf
* Install Telegraf and get it talking to your InfluxDB instance
* Install Grafana
* Use Grafana to visualize data in the Database

## By the end of this section students will be able to...
* Explain what Telegraf is and when to use it
* Install and Configure Telegraf
* Create Dashboards using Telegraf and Grafana data


## Exercises
### 1. Installing Telegraf

#### OSX

```sh
$ brew update
$ brew install telegraf
```

#### Debian/Ubuntu

```sh
wget http://get.influxdb.org/telegraf/telegraf_0.12.1-1_amd64.deb
sudo dpkg -i telegraf_0.12.1-1_amd64.deb
```

#### RedHat/CentOS

```sh
wget http://get.influxdb.org/telegraf/telegraf-0.12.1-1.x86_64.rpm
sudo yum localinstall telegraf-0.12.1-1.x86_64.rpm
```

### How to Use Telegraf

```sh
$ telegraf -help
Telegraf, The plugin-driven server agent for collecting and reporting metrics.

Usage:

  telegraf <flags>

The flags are:

  -config <file>     configuration file to load
  -test              gather metrics once, print them to stdout, and exit
  -sample-config     print out full sample configuration to stdout
  -config-directory  directory containing additional *.conf files
  -input-filter      filter the input plugins to enable, separator is :
  -output-filter     filter the output plugins to enable, separator is :
  -usage             print usage for a plugin, ie, 'telegraf -usage mysql'
  -debug             print metrics as they're generated to stdout
  -quiet             run in quiet mode
  -version           print the version to stdout
```

### Generate Config and Start Process

##### Generate a telegraf config file:
```sh
$ telegraf -sample-config > telegraf.conf
```

##### Run a single telegraf collection, outputing metrics to stdout
```sh
$ telegraf -config telegraf.conf -test
```

##### Run telegraf with all plugins defined in config file
```sh
$ telegraf -config telegraf.conf
```

### Check your InfluxDB Instance to be sure that it's writing out data

```sh
$ influx
> SHOW DATABASES
name: databases
---------------
name
_internal
air_data
telegraf

> USE telegraf
> SHOW SERIES
...
```

### 2. Create a Dashboard with some Grafana Data
#### Visualize the data in the `stocks` database.
Pick a couple different `ticker` values create a dashboard for them

**Hint**: You'll need to add a new data source for the `stocks` database.

#### Visualize the data in the `telegraf` database.
Create a dashboard with the free memory, disk used, and cpu user values in the `telegraf` database.

#### Bonus: Visualize the data in the `_internal` database.
Create a graph in Grafana that shows the current write throughput for you InfluxDB instance.
