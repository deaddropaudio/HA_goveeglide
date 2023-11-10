"""Platform for light integration."""
from __future__ import annotations

import logging

import voluptuous as vol
from .govee import Wandlicht

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_RGB_COLOR,
    PLATFORM_SCHEMA,
    LightEntity,
    ColorMode,
)
from homeassistant.const import (
    CONF_IP_ADDRESS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import homeassistant.util.color as color_util

logger = logging.getLogger("govee")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    # Add devices
    ip = config.get("ip_address")
    add_entities([GoveeLight(Wandlicht(ip))])


class GoveeLight(LightEntity):
    """Representation of an Godox Light."""

    def __init__(self, licht) -> None:
        """Initialize an GoveeLight."""

        self._attr_unique_id = "Govee Glide"
        self._light = licht
        self._name = "Glide"
        self._state = None
        self._brightness = None

        self._attr_supported_color_modes: set[ColorMode] = set()

        self._attr_supported_color_modes.add(ColorMode.BRIGHTNESS)
        self._attr_supported_color_modes.add(ColorMode.RGB)

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on."""
        logger.info(kwargs)
        if ATTR_BRIGHTNESS in kwargs:
            value = kwargs.get(ATTR_BRIGHTNESS)
            await self._light.set_brightness(value)
            self._brightness = value

        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs.get(ATTR_RGB_COLOR)
            await self._light.set_color(rgb)
            self._color = rgb
        await self._light.set_on_off(1)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        await self._light.set_on_off(0)

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._light._is_on
        self._brightness = self._light._brightness
