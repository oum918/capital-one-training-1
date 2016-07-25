# 5. Schema design
* A little bit deeper with the InfluxDB Data Model (RP's and Databases)
* Continuous Queries and Retention policies
* Schema Design (Project)

## By the end of this section students will be able to...

* Identify poorly designed schemas
* Design a basic schema for a common use case and query it efficiently.
* Explain what a continuous query is and why they are used.
* Create their own continuous queries.
* Describe what a retention policy is and its relations to databases and series.
* Create a retention policy.
* Combine retention policies and continuous queries in novel ways to manage their data's lifecycle.
* Use `influx_stress` to test generate load on your InfluxDB instance to generate load for your system.

## Quiz (20 min)

* Design a schema

# 1. What would happen if I wrote the following points into InfluxDB? And why does it happen?
```
mem,location=us-west host="server1",value=0.5 1444234986000
mem,location=us-west host="server2",value=4 1444234982000
mem,location=us-west host="server2",value=1 1444234982000
```

# 2. What is the problem with having a large number of independent tags?

```
random,week=10,weekday=tues,meowmix=k,birthday=july,...,host=api0 value=2 144423498200
```
# 3. What is a retention policy?

# 4. What is the relationship between retention policies, databases, and series.

# 5. What is a continuous query? How are they used?

# 6. Design a schema

In the CLI, create and use a database called `air_data`.

The following information is emitted to InfluxDB every 10 seconds from 10,000 unique devices.

* `zipcode`
* `city`
* `latitude`
* `longitude`
* `device_id`
* `smog_level`
* `co2_ppm`
* `lead`
* `so2_level`

The most important queries I have are:

```sql
SELECT median(lead) FROM polutants WHERE time > now() - 5m GROUP BY city

SELECT mean(co2_ppm) FROM polutants WHERE time > now() - 5m AND city='sf' GROUP BY device_id

SELECT max(smog_level) FROM polutants WHERE time > now() - 5m AND city='nyc' GROUP BY zipcode

SELECT min(so2_level) FROM polutants WHERE time > now() - 5m AND city='nyc' GROUP BY zipcode
```

## 6A. Design a schema for the data above (e.g. What values should be tags, fields, etc).
Note that the measurement name is `polutants`.

## 6B. Create a 24 hour retention policy that is the `DEFAULT` retention policy for the database.

## 6C. Create a continuous query that moves data from the 24 hour rentention policy to the `"default"` retention policy.

## 7. Create an `influx_stress` script that will generate load data for your system.
See the documentation on `influx_stress` for more information on how to generate load.
