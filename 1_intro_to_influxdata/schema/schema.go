// This file generates data for the exercise section of the data admin course
package main

import (
	"fmt"
	"log"
	"math/rand"
	"time"

	crypto "crypto/rand"

	influx "github.com/influxdata/influxdb/client/v2"
)

func randStr(n int) string {
	b := make([]byte, n/2)

	_, _ = crypto.Read(b)

	return fmt.Sprintf("%x", b)
}

func newZipCodes() []string {
	return []string{randStr(5), randStr(5)}
}

func newDevices() []string {
	devs := make([]string, 1000)

	for i := 0; i < 1000; i++ {
		devs[i] = randStr(20)
	}

	return devs
}

func writePoints(c influx.Client, city string, zips []string, devices map[string][]string, t time.Time) {
	bp, err := influx.NewBatchPoints(influx.BatchPointsConfig{
		Database:  "air_data",
		Precision: "s",
	})
	if err != nil {
		log.Fatalln("Error: ", err)
	}

	for _, zip := range zips {
		for _, dev := range devices[zip] {
			tags := map[string]string{
				"zipcode":   zip,
				"city":      city,
				"device_id": dev,
			}
			fields := map[string]interface{}{
				"lead":      rand.Intn(100),
				"co2_ppm":   rand.Intn(100),
				"smog":      rand.Intn(100),
				"so2_level": rand.Intn(100),
			}

			pt, err := influx.NewPoint("polutants", tags, fields, time.Now())
			if err != nil {
				log.Fatalln("Error: ", err)
			}

			bp.AddPoint(pt)
		}

		c.Write(bp)
	}
}

func main() {
	cities := map[string][]string{
		"sf":     newZipCodes(),
		"nyc":    newZipCodes(),
		"london": newZipCodes(),
		"paris":  newZipCodes(),
		"la":     newZipCodes(),
	}

	devices := map[string][]string{}
	for _, zips := range cities {
		for _, zip := range zips {
			devices[zip] = newDevices()
		}
	}

	// Make client
	c, err := influx.NewHTTPClient(influx.HTTPConfig{
		Addr: "http://localhost:8086",
	})
	if err != nil {
		log.Fatalln("Error: ", err)
	}

	ch := time.Tick(10 * time.Second)
	for now := range ch {
		for city, zips := range cities {
			writePoints(c, city, zips, devices, now)
		}
	}

}
