# Home Assistant Airtable Sensor

This custom component for Home Assistant allows you to read values from an Airtable base and use them as sensor values in Home Assistant.

## Installation

Clone this repo into the `custom_components/airtable_read_cell/` directory in your Home Assistant configuration directory.

## Configuration

To use this component, add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: airtable_read_cell
    api_key: YOUR_AIRTABLE_API_KEY
    base_id: YOUR_AIRTABLE_BASE_ID
    table_id: YOUR_AIRTABLE_TABLE_NAME # Can be either the table's ID or table's name
    field_name: YOUR_FIELD_NAME        # Optional, required if field_id is not used
    field_id: YOUR_FIELD_ID            # Optional, required if field_name is not used
    name: "Airtable Sensor Name"       # Optional, default is "Airtable Cell Value"
    unit_of_measurement: "Unit"        # Optional, default is ""
```

Parameters

	•	api_key (required): Your Airtable API key.
	•	base_id (required): The ID of your Airtable base.
	•	table_id (required): The ID or name of the table in your Airtable base.
	•	field_name (optional): The name of the field to read the value from. Required if field_id is not used.
	•	field_id (optional): The ID of the field to read the value from. Required if field_name is not used.
	•	name (optional): The name of the sensor. Default is “Airtable Cell Value”.
	•	unit_of_measurement (optional): The unit of measurement of the sensor. Default is “”.

## Example Configuration

```
sensor:
  - platform: airtable_read_cell
    api_key: "keyXXXXXXXXXXXXXX"
    base_id: "appXXXXXXXXXXXXXX"
    table_name: "Counts"
    field_name: "Orders Total"
    name: "Orders Received"
    unit_of_measurement: "orders"
```

## Usage

Once configured, the sensor will appear in Home Assistant with the specified name and will update with the value from the specified Airtable field or record.

## License

This project is licensed under the MIT License.
