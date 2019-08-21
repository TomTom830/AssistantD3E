def convert_siteid_to_adressknx(name_site, device_name):
    if name_site == "BureauR8R9":
        if device_name == "store":
            return '13/2/14'
        elif device_name == "lumiere":
            return '6/2/9'

    elif name_site == "BureauE11":
        if device_name == "store":
            return ''
        elif device_name == "lumiere":
            return ''
