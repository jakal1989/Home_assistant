import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN  # Erstelle eine Datei const.py, die "DOMAIN = 'vzug'" enthält

@config_entries.HANDLERS.register(DOMAIN)
class VZugConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for V-ZUG Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="V-ZUG Geräte", data=user_input)

        data_schema = vol.Schema({
            vol.Required("dishwasher_ip"): str,
            vol.Required("oven_ip"): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)