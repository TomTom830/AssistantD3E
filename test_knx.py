"""Example for switching a light on and off."""
import asyncio

from xknx import XKNX
from xknx.devices import Light, Cover


async def la_fonction_async():
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch of off again."""
    xknx = XKNX()
    await xknx.start()
    #light = Light(xknx,
    #              name='TestLight',
    #             group_address_switch='13/0/14')
    #await light.set_on()
    #await asyncio.sleep(2)
    #await light.set_off()

    cover = Cover(xknx,
                  'TestCover',
                  group_address_position='13/2/14',
                  travel_time_down=50,
                  travel_time_up=60,
                  invert_position=True,
                  invert_angle=False)

    await cover.set_position(70)
    #await asyncio.sleep(15)
    #await cover.set_position(60)


    await xknx.stop()


def function():
    # pylint: disable=invalid-name
    loop = asyncio.get_event_loop()
    loop.run_until_complete(la_fonction_async())
    loop.close()

