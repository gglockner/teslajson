# teslajson
Simple Python class to access the Tesla JSON API.

Written by Greg Glockner

## Description
This is a simple Python interface to the [Tesla JSON
API](http://docs.timdorr.apiary.io/). With this, you can query your
vehicle, control charge settings, turn on the air conditioning, and
more.  You can also embed this into other programs to automate these
controls.

The class is designed to be simple.  You initialize a `Connection`
object, retrieve the list of `Vehicle` objects, then perform get/set
methods on a `Vehicle`.  There is a single get method
(`Vehicle.get_data()`) and a single set method (`Vehicle.command()`) so
that the class does not need to be updated when there are changes in the
underlying JSON API.

This has been tested with Python 2.7 and Python 3.2.  It has no dependencies
beyond the standard Python libraries.

## Installation
0. Download the repository zip file and uncompress it
0. Run the following command with your Python interpreter: `python setup.py install`

Alternately, add the teslajson.py code in your own program.

## Public API
`Connection(email, password, **kwargs)`:
Initialize the connection to the Tesla Motors website.

Required parameters:

- _email_: your login for teslamotors.com
- _password_: your password for teslamotors.com

Optional parameters:

- _url_: the base URL for the API
- _api_: API string
- _client\_id_: API identifier
- _client\_secret_: Secret API identifier

`Connection.vehicles`: A list of Vehicle objects, corresponding to the
vehicles associated with your account on teslamotors.com.

`Vehicle`: The vehicle class is a subclass of a Python dictionary
(`dict`).  A `Vehicle` object contains fields that identify your
vehicle, such as the Vehicle Identification Number (`Vehicle['vin']`). 
All standard dictionary methods are supported.

`Vehicle.wake()`: Wake the vehicle.

`Vehicle.get_data(name)`: Retrieve data values specified by `name`.
Returns a dictionary (`dict`).  Examples for `name`: `charge_state`,
`climate_state`, `vehicle_state`.  For a full list of name values, see
the `GET` commands in the [Tesla JSON API](http://docs.timdorr.apiary.io/).

`Vehicle.command(name)`: Execute the command specified by `name`.
Returns a dictionary (`dict`).  Examples for `name`:
`charge_port_door_open`, `charge_max_range`. For a full list of names,
see the `POST` commands in the [Tesla JSON API](http://docs.timdorr.apiary.io/).

## Example
	import teslajson
	c = teslajson.Connection('youremail', 'yourpassword')
	v = c.vehicles[0]
	v.wake()
	v.get_data('charge_state')
	v.command('charge_start')

## Credits
Many thanks to [Tim Dorr](http://timdorr.com) for documenting the Tesla JSON API.
This would not be possible without his work.

## Disclaimer
This software is provided as-is.  This software is not supported by or
endorsed by Tesla Motors.  Tesla Motors does not publicly support the
underlying JSON API, so this software may stop working at any time.  The
author makes no guarantee to release an updated version to fix any
incompatibilities.
