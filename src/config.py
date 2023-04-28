def _get_main_attributes() -> dict:
        return {
            "mutator_name": { "type": str, "default": "ZedCustom.ZedCustomMut" },
            "n_players": { "type": int },
            "difficulty": { "type": str },
            "zed_multiplier": { "type": float, "default": 1.0 },
            "modded": { "type": bool, "default": False },
            "boss_wave_probability": { "type": float, "default": 1.0 },
            "custom_zeds_ratio_policy": { "type": str, 'default': 'constant' },
            "custom_zeds_ratio_policy_params": { "type" : object, 'default': [1] },
            "probability": { "type": float, "default": 1.0 },
            "spawn_delay": { "type": float, "default": 1.0 },
            "spawn_at_once": { "type": int, "default": 1 },
            "n_generators": { "type": int, "default": 1 },
            "zeds_register": { "type" : list }
        }

def _get_wave_attributes() -> dict:
    return { 
        "num_wave": { "type": int },
        "name": { "type": str, "default": "Unnamed" },
        "zeds": { "type": list },
        }

def _get_zed_attributes() -> dict:
    return {
        "zed": { "type": str },
        "number": { "type": int, "default": 0 },
        "ratio": { "type": float, "default": 0.0 }
    }

def _get_shared_attributes() -> list:
    return ['probability', 'spawn_delay', 'spawn_at_once', 'n_generators']


# Ratio policies
def make_line_interp(x0, y0, x1, y1):
    assert x1 != x0
    def f(x):
        return (y1 - y0) * (x - x0) / (x1 - x0) + y0
    return f


def make_line_const_interp(x0, y0, x1, y1):
    """Same as `make_line_interp`, but extrapolated constantly beyond [x0; x1]."""
    min_val = min(x0, x1)
    max_val = max(x0, x1)
    def f(x):
        if(x > max_val): 
            x = max_val
        elif(x < min_val):
            x = min_val

        return make_line_interp(x0, y0, x1, y1)(x)
    return f

def constant(x0):
    def f(x):
        return x0
    
    return f

class ValidationError(Exception):
    pass

class ConfigValidator():
    @staticmethod
    def _validate_property(name: str, type: type, properties: dict):
         if(name not in properties):
            raise KeyError
         if(not isinstance(properties[name], type)):
            raise TypeError
         
         
    @staticmethod
    def _set_default_attr(name: str, type: type, default, properties: dict):
        if(name not in properties):
            properties[name] = default
        elif(not isinstance(properties[name], type)):   
            raise TypeError


    @staticmethod
    def validate_attributes(properties: dict, attributes: dict):
        is_valid = True

        for name, values in attributes.items():
            try:
                if("default" in values):
                    ConfigValidator._set_default_attr(name, values["type"], values["default"], properties)
                else:
                    ConfigValidator._validate_property(name, values["type"], properties)

            except KeyError:
                is_valid = False
                print('ERROR: "{name}" key is missing from configuration'.format(name=name))
            except TypeError:
                is_valid = False
                print('ERROR: "{name}" value type is invalid; expected {expected} but received {actual}'.format(name=name, expected=values["type"], actual=type(properties[name])))


        if(not is_valid):
            raise ValidationError
    
    
    @staticmethod
    def validate_config(properties: dict):
        ConfigValidator.validate_attributes(properties, _get_main_attributes())

        for wave in properties['zeds_register']:
            ConfigValidator.validate_attributes(wave, _get_wave_attributes())

            for zed in wave['zeds']:
                ConfigValidator.validate_attributes(zed, _get_zed_attributes())


class ConfigHandler():
    @staticmethod
    def __propagate_undefined_attributes(dest: dict, source: dict, attributes: list):
        for attr in attributes:
            dest.setdefault(attr, source[attr])


    @staticmethod
    def __propagate_spawn_attributes(properties: dict):
        for wave in properties['zeds_register']:
            ConfigHandler.__propagate_undefined_attributes(wave, properties, _get_shared_attributes())

            for zed in wave['zeds']:
                ConfigHandler.__propagate_undefined_attributes(zed, wave, _get_shared_attributes())


    @staticmethod
    def __set_ratio_policy(properties: dict):
        ratio_policy = globals()[properties['custom_zeds_ratio_policy']]
        properties['custom_zeds_ratio_policy'] = ratio_policy(*properties['custom_zeds_ratio_policy_params'])


    @staticmethod
    def init_config(properties: dict):
        ConfigValidator.validate_config(properties)

        ConfigHandler.__set_ratio_policy(properties)

        ConfigHandler.__propagate_spawn_attributes(properties)
    
