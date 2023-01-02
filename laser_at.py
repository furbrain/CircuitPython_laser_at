# SPDX-FileCopyrightText: Copyright (c) 2022 Phil Underwood for Underwood Underground
#
# SPDX-License-Identifier: MIT
"""
`laser_at`
================================================================================

Driver for an inexpensive laser rangefinder module, made by Hi-AT, available on aliexpress.


* Author(s): Phil Underwood

Implementation Notes
--------------------

**Hardware:**

  * `Hi-AT laser range finder <https://www.aliexpress.com/item/32792768667.html>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""
import re
import time

try:
    from typing import Optional
except ImportError:
    pass

import busio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/furbrain/CircuitPython_laser_at.git"


class LaserError(Exception):
    """
    An error while reading from the laser
    """


class LaserTimeoutError(LaserError):
    """
    Laser read has timed out
    """


class Laser:
    """
    Driver for low cost laser range finder by Hi-AT.

    :param ~busio.UART uart: The I2C bus the LSM6DS3 is connected to.
    :param speed: The speed at which to take a measurement. Choices are ``Laser.FAST``,
      ``Laser.MEDIUM``, and ``Laser.SLOW``
    """

    FAST = b"F"
    MEDIUM = b"D"
    SLOW = b"M"

    DEFAULT_SPEEDS = {FAST: 1000, MEDIUM: 3000, SLOW: 6000}

    def __init__(self, uart: busio.UART, speed: bytes = MEDIUM):
        self.uart: busio.UART = uart
        self.speed = speed
        self._on = False

    def _clear_buffer(self):
        self.uart.reset_input_buffer()

    def start_measurement(self):
        """
        Start a measurement with the laser
        """
        self._clear_buffer()
        self.uart.write(self.speed)
        self._on = True

    def read_measurement(self, timeout: Optional[int] = None) -> float:
        """
        Retrieve a reading form the laser

        :param int timeout: How long to wait for a reading in millisecond. Default depends on
          ``speed``: 1000 for FAST, 3000 for MEDIUM, 6000 for SLOW.
        :raises: `LaserError` if a bad reading is done, `LaserTimeoutError` if the reading times out
        :return: Distance in metres
        """
        self._on = False
        if timeout is None:
            timeout = self.DEFAULT_SPEEDS[self.speed]
        expired = time.monotonic() + timeout / 1000.0
        while self.uart.in_waiting < 9:
            time.sleep(0.01)
            if time.monotonic() > expired:
                raise LaserTimeoutError(
                    f"Timed out: {self.uart.read(self.uart.in_waiting)}"
                )
        output = self.uart.read(self.uart.in_waiting)
        match = re.search(rb"\d+\.\d+", output)
        if match is None:
            raise LaserError(f"Laser read failed: {output}")
        return float(match.group(0))

    @property
    def distance(self):
        """
        Distance as measured by the device

        :raises: `LaserError` if a bad reading is done, `LaserTimeoutError` if the reading times out
        :return: Distance in cm
        """
        self.start_measurement()
        return self.read_measurement() * 100.0

    # pylint: disable=invalid-name
    @property
    def on(self):
        """
        Whether the laser is currently on or not. You can turn the laser on or off by assigning to
        this property
        """
        return self._on

    # pylint: disable=invalid-name
    @on.setter
    def on(self, value: bool):
        self._on = value
        if value:
            self.uart.write(b"O")
        else:
            self.uart.write(b"C")

    async def async_read(self, timeout=None):
        """
        Make an asynchronous laser reading

        :param int timeout: How long to wait for a reading in millisecond. Default depends on
          ``speed``: 1000 for FAST, 3000 for MEDIUM, 6000 for SLOW.
        :raises: `LaserError` if a bad reading is done, `LaserTimeoutError` if the reading times out
        :return: Distance in metres
        """
        # pylint: disable=import-outside-toplevel
        import asyncio

        self.start_measurement()
        old_timeout = self.uart.timeout
        self.uart.timeout = 0
        stream = asyncio.StreamReader(self.uart)
        if timeout is None:
            timeout = self.DEFAULT_SPEEDS[self.speed]

        try:
            # pylint: disable=no-member
            output = await asyncio.wait_for_ms(stream.readexactly(9), timeout)
        except asyncio.TimeoutError as exc:
            raise LaserTimeoutError("Timed out") from exc
        finally:
            self.uart.timeout = old_timeout
        match = re.search(rb"\d+\.\d+", output)
        if match is None:
            raise LaserError(f"Laser read failed: {output}")
        return float(match.group(0))
