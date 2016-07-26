# 2. Introduction to Kapacitor
* Install and configure Kapacitor
* Process data with Kapacitor
* Alert on data with Kapacitor

## By the end of this section students will be able to...
* Describe what Kapacitor is and when to use it
* Install and Configure Kapacitor
* Explain the Kapacitor computational model
* Understand the TICKscript Syntax
* Process data with Kapacitor.
* Alert on data with Kapacitor.


## Exercises

# 1. Create tasks for the TICKscripts in the `scripts` folder.

### 2A. Convert the following CQ into a Kapacitor batch task.
```sql
CREATE CONTINUOUS QUERY mycq ON air_data RESAMPLE EVERY 1m
BEGIN
  SELECT
   median(lead) as lead,
   mean(co2_ppm) as co2_ppm,
   max(smog_level) as smog_level,
   min(so2_level) as so2_level
  INTO "air_data"."default"."new_polutants"
  FROM "air_data"."24_hour"."polutants"
  GROUP BY time(60m), *
END
```
### 2B. Convert the following CQ into a Kapacitor stream task.
```sql
CREATE CONTINUOUS QUERY mycq ON air_data RESAMPLE EVERY 1m
BEGIN
  SELECT
   median(lead) as lead,
   mean(co2_ppm) as co2_ppm,
   max(smog_level) as smog_level,
   min(so2_level) as so2_level
  INTO "air_data"."default"."new_polutants"
  FROM "air_data"."24_hour"."polutants"
  GROUP BY time(60m), *
END
```

### 3. Create a task
Using the data from the [`schema`](https://github.com/influxdata/capital-one-training/tree/master/1_intro_to_influxdata/5_schema_design/linux) binary from the schema design section.

### 3A. Create a streaming TICKscript that does the following:

1. Issue an `info` alert when the average `lead` level for a 1 minute interval is greater than `50`.
2. Issue an `warn` alert when the average `lead` level for a 1 minute interval is greater than `70`.
3. Issue an `crit` alert when the average `lead` level for a 1 minute interval is greater than `90`.

### 3B. Create a streaming TICKscript that does the following:

1. Computes the ratio of the averave `smog_level` and `so2_level` for a 2 minute interval that emits to the pipeline every minute.
