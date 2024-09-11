from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from .const import DOMAIN
import requests

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the V-ZUG sensors based on a config entry."""
    dishwasher_ip = entry.data["dishwasher_ip"]
    oven_ip = entry.data["oven_ip"]

    sensors = [
        VZugSensor(
            name="V-ZUG Dishwasher",
            resource=f"http://{dishwasher_ip}/ai?command=getDeviceStatus",
            icon="mdi:dishwasher",
            attributes=["DeviceName", "Serial", "Inactive", "Program", "Status", "ProgramEnd", "End", "EndType", "deviceUuid"]
        ),
        VZugSensor(
            name="V-ZUG Oven",
            resource=f"http://{oven_ip}/ai?command=getDeviceStatus",
            icon="mdi:stove",
            attributes=["DeviceName", "Serial", "Inactive", "Program", "Status", "ProgramEnd", "End", "EndType", "deviceUuid"]
        )
    ]
    async_add_entities(sensors, True)

class VZugSensor(SensorEntity):
    """Representation of a V-ZUG sensor."""

    def __init__(self, name, resource, icon, attributes):
        self._name = name
        self._resource = resource
        self._icon = icon
        self._attributes = attributes
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(self._resource)
            data = response.json()
            self._state = data.get("result")
            for attr in self._attributes:
                self._attr_extra_state_attributes[attr] = data.get(attr)
        except Exception as e:
            self._state = None
            self._attr_extra_state_attributes = {}
            _LOGGER.error(f"Error fetching data from {self._resource}: {e}")