import aiohttp
import asyncio
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_NAME, CONF_UNIT_OF_MEASUREMENT
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

CONF_BASE_ID = "base_id"
CONF_TABLE_ID = "table_id"
CONF_FIELD_NAME = "field_name"
CONF_FIELD_ID = "field_id"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_BASE_ID): cv.string,
        # Note: table_id can also be the table's name
        vol.Required(CONF_TABLE_ID): cv.string,
        vol.Optional(CONF_FIELD_NAME): cv.string,
        vol.Optional(CONF_FIELD_ID): cv.string,
        vol.Optional(CONF_NAME, default="Airtable Cell Value"): cv.string,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=""): cv.string,
    }
).extend(
    {
        vol.Exclusive(CONF_FIELD_NAME, "field"): cv.string,
        vol.Exclusive(CONF_FIELD_ID, "field"): cv.string,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api_key = config[CONF_API_KEY]
    base_id = config[CONF_BASE_ID]
    table_id = config[CONF_TABLE_ID]
    field_name = config.get(CONF_FIELD_NAME)
    field_id = config.get(CONF_FIELD_ID)
    name = config[CONF_NAME]
    unit_of_measurement = config[CONF_UNIT_OF_MEASUREMENT]
    
    async_add_entities(
        [AirtableReadCellSensor(api_key, base_id, table_id, field_name, field_id, name, unit_of_measurement)]
    )


class AirtableReadCellSensor(Entity):
    def __init__(self, api_key, base_id, table_id, field_name, field_id, name, unit_of_measurement):
        self._state = None
        self._api_key = api_key
        self._base_id = base_id
        self._table_id = table_id
        self._field_name = field_name
        self._field_id = field_id
        self._name = name
        self._unique_id = f"{base_id}_{table_id}_{field_name or field_id}"
        self._unit_of_measurement = unit_of_measurement

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    async def async_update(self):
        field = await self.async_get_cell(
            self._api_key, self._base_id, self._table_id, self._field_name, self._field_id
        )
        if field is not None:
            self._state = field

    async def async_get_cell(self, api_key, base_id, table_id, field_name, field_id):
        if field_id:
            url = f"https://api.airtable.com/v0/{base_id}/{table_id}?returnFieldsByFieldId=true"
        else:
            url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

        headers = {"Authorization": f"Bearer {api_key}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()

                for record in data["records"]:
                    if field_id and field_id in record["fields"]:
                        return record["fields"][field_id]
                    if field_name and field_name in record["fields"]:
                        return record["fields"][field_name]
        return None
