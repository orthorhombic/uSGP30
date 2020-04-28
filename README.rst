
Introduction
============

This is a MicroPython fork of the Adafruit CircuitPython SGP30 library (https://github.com/adafruit/Adafruit_CircuitPython_SGP30). The library is designed to interface with a SGP30 module / breakout board over I2C, and retrieve Total Volatile Organic Compounds (TVOC) and Equivalent Carbon Dioxide (CO2eq) readings.

This driver has removed the original Adafruit library's dependency on the adafruit_bus_device.i2c_device module, and supports MicroPython's native i2c implementation directly. It has also widened support for SGP30 commands not present in the original library.

So far, it has been tested only with ESP32 MicroPython firmware.

.. image:: docs/pimoroni_sgp30.JPG

Usage Notes
=============

.. code-block:: python

	import uSGP30
	import machine

	I2C_SCL_GPIO = const(18)
	I2C_SDA_GPIO = const(19)

	i2c = I2C(scl=Pin(I2C_SCL_GPIO, Pin.OUT), sda=Pin(I2C_SDA_GPIO, Pin.OUT), freq=400000)
	sgp30 = uSGP30.SGP30(i2c)

Reading from the Sensor
------------------------

To read from the sensor:

.. code-block:: python

    co2eq_ppm, tvoc_ppb = sgp30.measure_iaq()

Note the various calibration / initialisation parameters documented in the Sensirion SGP30 Driver Integration Guide. Specifically, there is a 15-second device initialisation period, and a recommended 12-hour early operation phase. In order to prevent the reinitialisation of the SGP30 algorithm / baseline after each microprocessor deepsleep, instantiate the uSGP30 class with the :code:`init_algo` set to :code:`False`. If initialising the sensor, cater for the 15 second initialisation period.

.. code-block:: python

	SGP30_INIT_MS = const(15000)
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        initialise_sgp30_algo = False
    else:
        initialise_sgp30_algo = True
    sgp30 = uSGP30.SGP30(i2c, init_algo=initialise_sgp30_algo)
    if initialise_sgp30_algo:
        sleep_ms(SGP30_INIT_MS)

Documentation
=========================

* `Sensirion SGP30 Datasheet <docs/Sensirion_Gas_Sensors_SGP30_Datasheet.pdf>`_
* `Sensirion SGP30 Driver Integration Guide <docs/Sensirion_Gas_Sensors_SGP30_Driver-Integration-Guide_SW_I2C.pdf>`_