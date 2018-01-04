import logging
import asyncio
import datetime

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

DEPENDENCIES = ['sector_alarm']

import custom_components.sector_alarm as sector_alarm

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass,
                               config,
                               async_add_entities,
                               discovery_info=None):

    sector_hub = hass.data[sector_alarm.DATA_SA]

    temometers = await sector_hub.get_termometers()

    async_add_entities(
        SectorAlarmTemperatureSensor(sector_hub, temometer)
        for temometer in temometers)


class SectorAlarmTemperatureSensor(Entity):
    """Representation of a Sector Alarm Temperature Sensor."""

    def __init__(self, hub, name):
        """Initialize the sensor."""
        self._hub = hub
        self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @asyncio.coroutine
    def async_update(self):
        """ Update temperature """
        update = self._hub.update()
        if update:
            yield from update

    @property
    def state(self):
        """Return the state of the sensor."""
        temp = self._hub.temperatures(self._name)
        if temp is None:
            _LOGGER.info('Failed to fetch temperature for %s', self._name)
        return temp
