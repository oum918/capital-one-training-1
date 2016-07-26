# Day 1 Review

## 1. What is the difference between regular and irregular time series?

## 2. What are the names of the InfluxDB components on the graph on the screen? Additionally, please describe the roles of each of the components.

## 3. What types of values can be stored as tag values?

## 4. What types of values can be stored as field values?

## 5. What is the collection of all of the tags called?

## 6. What is the collection of all of the fields called?

## 7. What is the maximum number of tags that InfluxDB allows?

## 8. What is the maximum number of fields that InfluxDB allows?

## 9. What is a series? How is it different from a measurement?

## 10. Express a point in line protocol that has *measurement* `rainfall`, 3 *tags* `location=sf`, `meter_id=5a`, and `weather=sunny`, and 2 *fields* with keys `total` (float64), `is_raining` (bool).

## 11. Write some data into InfluxDB using the CLI

## 12. What would happen if I wrote the following points into InfluxDB? And why does it happen?
```
mem,location=us-west host="server1",value=0.5 1444234986000
mem,location=us-west host="server2",value=4 1444234982000
mem,location=us-west host="server2",value=1 1444234982000
```

## 13. What is the problem with having a large number of independent tags?

```
random,week=10,weekday=tues,meowmix=k,birthday=july,...,host=api0 value=2 144423498200
```
## 14. What is a retention policy?

## 15. What is the relationship between retention policies, databases, and series.

## 16. What is a continuous query? How are they used?

## 17. Design a schema

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

## 18A. Design a schema for the data above (e.g. What values should be tags, fields, etc).
Note that the measurement name is `polutants`.

## 18B. Create a 24 hour retention policy that is the `DEFAULT` retention policy for the database.
