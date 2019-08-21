"""Example for switching a light on and off."""
import asyncio

from xknx import XKNX
from xknx.devices import Cover, Light


async def controle_store_async(d_o, adr_store, name_site):
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch of off again."""
    xknx = XKNX()
    await xknx.start()
    cover = Cover(xknx,
                  'Store_'+name_site,
                  group_address_position=adr_store,
                  travel_time_down=50,
                  travel_time_up=60,
                  invert_position=True,
                  invert_angle=False)
    await cover.set_position(d_o)
    print (cover.current_position())
    await xknx.stop()


#Fonction pour controler les store KNX
def controle_store(deg_ouv, adr_store, name_site):
    # pylint: disable=invalid-name
    loop = asyncio.new_event_loop()
    loop.run_until_complete(controle_store_async(deg_ouv, adr_store, name_site))
    loop.close()

async def controle_lumiere_async(d_l, adr_lum, name_site):
    xknx = XKNX()
    await xknx.start()
    light = Light(xknx,
                  name='Lumiere_'+name_site,
                  group_address_brightness=adr_lum)

    # Set brightness
    await light.set_brightness(d_l)
    await xknx.stop()

def controle_lumiere(deg_lum, adr_lum, name_site):
    # pylint: disable=invalid-name
    loop = asyncio.new_event_loop()
    loop.run_until_complete(controle_lumiere_async(deg_lum, adr_lum, name_site))
    loop.close()