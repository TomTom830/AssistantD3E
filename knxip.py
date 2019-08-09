"""Example for switching a light on and off."""
import asyncio

from xknx import XKNX
from xknx.devices import Cover, Light


async def controle_store_async(d_o):
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch of off again."""
    xknx = XKNX()
    await xknx.start()
    cover = Cover(xknx,
                  'Store_BureauR8R9',
                  group_address_position='13/2/14',
                  travel_time_down=50,
                  travel_time_up=60,
                  invert_position=True,
                  invert_angle=False)
    await cover.set_position(d_o)
    print (cover.current_position())
    await xknx.stop()


#Fonction pour controler les store KNX
def controle_store(deg_ouv):
    # pylint: disable=invalid-name
    loop = asyncio.new_event_loop()
    loop.run_until_complete(controle_store_async(deg_ouv))
    loop.close()

async def controle_lumiere_async(d_l):
    xknx = XKNX()
    await xknx.start()
    light = Light(xknx,
                  name='Lumiere_BureauR8R9',
                  group_address_brightness='6/2/9')

    # Set brightness
    await light.set_brightness(d_l)
    await xknx.stop()

def controle_lumiere(deg_lum):
    # pylint: disable=invalid-name
    loop = asyncio.new_event_loop()
    loop.run_until_complete(controle_lumiere_async(deg_lum))
    loop.close()