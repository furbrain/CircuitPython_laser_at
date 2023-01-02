# SPDX-FileCopyrightText: 2022 Phil Underwood
#
# SPDX-License-Identifier: Unlicense
"""
example that reads from the cdc data serial port in groups of four and prints
to the console. The USB CDC data serial port will need enabling. This can be done
by copying examples/usb_cdc_boot.py to boot.py in the CIRCUITPY directory

Meanwhile a simple counter counts up every second and also prints
to the console.
"""


import asyncio
import board
import laser_at


async def laser_client():

    uart = board.UART()
    uart.baudrate = 19200
    laser = laser_at.Laser(uart)
    while True:
        try:
            distance = await laser.async_read()
            print(f"LASER: {distance}")
        except laser_at.LaserError as error:
            print(f"LASER ERROR: {error}")


async def counter():
    i = 0
    while True:
        print(f"COUNTER: {i}")
        i += 1
        await asyncio.sleep(1)


async def main():
    clients = [asyncio.create_task(counter())]
    clients.append(asyncio.create_task(laser_client()))
    await asyncio.gather(*clients)


asyncio.run(main())
