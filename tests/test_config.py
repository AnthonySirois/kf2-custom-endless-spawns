import pytest

from config import ConfigValidator

class TestConfig:
    
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

        