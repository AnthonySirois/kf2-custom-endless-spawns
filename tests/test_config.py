import pytest

from config import ConfigValidator, ConfigHandler

class TestConfigValidator:
    
    def test_given_valid_property_validate_property_returns_true(x):
        properties = { "property": "value" }

        ConfigValidator._validate_property("property", str, properties)


    def test_given_missing_property_validate_property_raises_key_error(x):
        properties = { }

        with pytest.raises(KeyError):
            ConfigValidator._validate_property("property", str, properties)


    def test_given_wrong_type_validate_property_raises_type_error(x):
        properties = { "property": "value" }

        with pytest.raises(TypeError):
            ConfigValidator._validate_property("property", int, properties)


    def test_given_valid_property_set_default_attr_changes_nothing(x):
        properties = { "property": "value" }

        ConfigValidator._set_default_attr("property", str, "default", properties)

        assert properties["property"] == "value"


    def test_given_missing_property_set_default_attr_sets_default_value(x):
        properties = { }

        ConfigValidator._set_default_attr("property", str, "default", properties)

        assert properties["property"] == "default"


    def test_given_wrong_type_property_set_default_attr_raises_type_error(x):
        properties = { "property": 1 }

        with pytest.raises(TypeError):
            ConfigValidator._set_default_attr("property", str, "default", properties)


class TestConfigHandler:
    def _get_spawn_attr() -> dict:
        return {
            'probability': 1.0, 
            'spawn_delay': 10.0, 
            'spawn_at_once': 2, 
            'n_generators': 1
        }

    def test_given_undefined_attribute_propagate_sets_value(x):
        dest = { }
        source = { "property": "value" }

        ConfigHandler._propagate_undefined_attributes(dest, source, ['property'])

        assert dest['property'] == 'value'

    def test_given_defined_attritube_propagate_changes_nothing(x):
        dest = { "property": 'start' }
        source = { 'property': 'value' }

        ConfigHandler._propagate_undefined_attributes(dest, source, ['property'])

        assert dest["property"] == 'start'
        
    def test_given_only_main_attr_propagate_sets_subvalues(x):
        properties = TestConfigHandler._get_spawn_attr()
        properties['zeds_register'] = [ {'zeds': [{'zed': "Test"}] } ]
        
        ConfigHandler._propagate_spawn_attributes(properties)

        assert properties["zeds_register"][0]['probability'] == 1.0


    def test_given_defined_attr_propagate_changes_nothing(x):
        properties = TestConfigHandler._get_spawn_attr()
        properties['zeds_register'] = [ {
            'probability': 2.0,
            'zeds': [{
                'zed': "Test",
                'probability': 3.0
                }] 
            } ]
        
        ConfigHandler._propagate_spawn_attributes(properties)
        assert properties["zeds_register"][0]['probability'] == 2.0
        assert properties["zeds_register"][0]['zeds'][0]['probability'] == 3.0
