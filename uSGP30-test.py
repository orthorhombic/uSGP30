""" uSGP30-test.py
Tests the uSGP30 library. Uses test values for temperature and humidity for
triggering humidity compensation.
Does not check < 7 day validity of stored baseline, nor does it enforce
12 hour early operation phase if no baseline is found (just a warning is
displayed).
"""

import uSGP30
import machine
import ujson
import utime

BASELINE_FILE = "sgp30_iaq_baseline.txt"
I2C_SCL_GPIO = const(18)
I2C_SDA_GPIO = const(19)
I2C_FREQ = const(400000)
MEASURE_INTERVAL_MS = const(1000)
BASELINE_INTERVAL_MS = const(60000)
SGP30_INIT_TIME_MS = const(15000)
# Made-up test values
TEST_TEMP_C = const(25)
TEST_R_HUMIDITY_PERC = const(50)

def main():
    """ Runs main application """
    i2c = machine.I2C(
        scl=machine.Pin(I2C_SCL_GPIO, machine.Pin.OUT),
        sda=machine.Pin(I2C_SDA_GPIO, machine.Pin.OUT),
        freq=I2C_FREQ
    )
    sgp30 = uSGP30.SGP30(i2c)
    # Sensor initialisation time
    utime.sleep_ms(SGP30_INIT_TIME_MS)
    try:
        with open(BASELINE_FILE, "r") as file:
            current_baseline = ujson.loads(file.read())
    except OSError as exception:
        print(exception)
        print("No valid baseline found. You should wait 12 hours for calibration before use.")
    else:
        print("Baseline found:", current_baseline)
        sgp30.set_iaq_baseline(current_baseline)
    finally:
        # Set absolute humidity
        a_humidity_perc = uSGP30.convert_r_to_a_humidity(TEST_TEMP_C, TEST_R_HUMIDITY_PERC)
        sgp30.set_absolute_humidity(a_humidity_perc)
    # Main application loop
    last_baseline_commit_ms = utime.ticks_ms()
    while True:
        last_iaq_check_ms = utime.ticks_ms()
        co2eq_ppm, tvoc_ppb = sgp30.measure_iaq()
        print(
            "Carbon Dioxide Equivalent (ppm): " + str(co2eq_ppm) + "\n" +
            "Total Volatile Organic Compound (ppb): " + str(tvoc_ppb)
            )
        # Set absolute humidity
        a_humidity_perc = uSGP30.convert_r_to_a_humidity(TEST_TEMP_C, TEST_R_HUMIDITY_PERC)
        sgp30.set_absolute_humidity(a_humidity_perc)
        if utime.ticks_ms() - last_baseline_commit_ms > BASELINE_INTERVAL_MS:
            # Get current baseline and store on flash
            current_baseline = sgp30.get_iaq_baseline()
            with open(BASELINE_FILE, "w") as file:
                file.write(str(current_baseline))
            print("Baseline commited")
            last_baseline_commit_ms = utime.ticks_ms()
        utime.sleep_ms(MEASURE_INTERVAL_MS - utime.ticks_ms() - last_iaq_check_ms)

if __name__ == "__main__":
    main()
