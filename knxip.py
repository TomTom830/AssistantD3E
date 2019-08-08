"""Example for switching a light on and off."""
import asyncio

from xknx import XKNX
from xknx.devices import Cover


async def controle_store_async(d_o):
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch of off again."""
    xknx = XKNX()
    await xknx.start()
    cover = Cover(xknx,
                  'TestCover',
                  group_address_position='13/2/14',
                  travel_time_down=50,
                  travel_time_up=60,
                  invert_position=True,
                  invert_angle=False)

    await cover.set_position(d_o)
    await xknx.stop()


def controle_store(deg_ouv):
    # pylint: disable=invalid-name
    loop = asyncio.new_event_loop()
    loop.run_until_complete(controle_store_async(deg_ouv))
    loop.close()

