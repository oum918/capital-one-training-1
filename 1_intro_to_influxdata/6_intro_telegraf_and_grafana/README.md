### 4. Intro to Telegraf (15-30 min) 1:30-2:00
* Install Telegraf and get it talking to your InfluxDB instance


## Installing Telegraf

### OSX

```sh
$ brew update
$ brew install telegraf
```

### Debian/Ubuntu

```sh
wget http://get.influxdb.org/telegraf/telegraf_0.12.1-1_amd64.deb
sudo dpkg -i telegraf_0.12.1-1_amd64.deb
```

### RedHat/CentOS

```sh
wget http://get.influxdb.org/telegraf/telegraf-0.12.1-1.x86_64.rpm
sudo yum localinstall telegraf-0.12.1-1.x86_64.rpm
```

## How to Use Telegraf

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

## Generate Config and Start Process

#### Generate a telegraf config file:
```sh
$ telegraf -sample-config > telegraf.conf
```

#### Run a single telegraf collection, outputing metrics to stdout
```sh
$ telegraf -config telegraf.conf -test
```

#### Run telegraf with all plugins defined in config file
```sh
$ telegraf -config telegraf.conf
```

## Check your InfluxDB Instance to be sure that it's writing out data

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
