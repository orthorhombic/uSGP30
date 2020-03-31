
Introduction
============

This is a MicroPython fork of the Adafruit CircuitPython SGP30 library (https://github.com/adafruit/Adafruit_CircuitPython_SGP30). The library is designed to interface with a SGP30 module / breakout board over I2C, and retrieve Total Volatile Organic Compounds (TVOC) and Equivalent Carbon Dioxide (CO2eq) readings.

So far, it has been tested only with ESP32 MicroPython firmware.

.. image:: docs/pimoroni_sgp30.JPG

Usage Notes
=============

.. code-block:: python

	import uSGP30

	I2C_SCL_GPIO = const(18)
	I2C_SDA_GPIO = const(19)

	i2c = I2C(scl=Pin(I2C_SCL_GPIO, Pin.OUT), sda=Pin(I2C_SDA_GPIO, Pin.OUT), freq=400000)
	sgp30 = uSGP30.SGP30(i2c)

Reading from the Sensor
------------------------

To read from the sensor:

.. code-block:: python

    co2eq_ppm, tvoc_ppb = sgp30.measure_iaq()
