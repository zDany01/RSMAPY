# RSMAPY
A Python-written API to manage your server remotely

## Requirements
This application requires some installed software before being used
- Python
  - python3
  - python3-pip
  - python3-virtualenv
  - python3-wheel (optional)
- Docker

## Installation
You must execute the `install` file to install this bot as a system service.
```bash
sudo ./install
```
This will create a virtual environment in your folder where the script will automatically install all the dependencies.

If you want to uninstall the service you need to execute the `uninstall` script
```bash
sudo ./uninstall
```

If you want to execute the software without installing it as a service you can create a virtual environment called RSMAPY and then install the requirements.txt file
```bash
virtualenv RSMAPY 
source ./RSMAPY/bin/activate
pip3 install -r requirements.txt
```
From here you can either start manually the python script by accessing first to the virtual environment every time or you can deactivate it and just use the `pystart` file
> Remember to run the Python API with privileges

## API settings
Before using the app you need to rename the `config.py.template` file to `config.py` and modify some settings in it:

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `DEBUG_LOGGING` | `boolean` | Include debug logs in the window output |
| `PROTECTED_CONTAINERS` | `list[str]` | List of IDs of containers that will be excluded from standard operation |
| `TOKEN_TIMEOUT` | `int` | Timeout for the API Token in minutes
| `AUTH_SECRET` | `string` | The server secret key used to generate the JWT Token.<br>Setting it to `Random` will let the server generate a new one on each boot
| `AUTH_USERNAME` | `string` | Login username
| `AUTH_PASSWORD_HASH` | `string` | Login password hash in bcrypt hash format
| `BACKUP_SCRIPT_PATH` | `string` |  Path to your bash backup script |
| `BACKUP_SCRIPT_ARGS` | `list[string]` |  Arguments for your backup script|
| `BACKUP_FLAG_PATH` | `string` | Path for backup updated file |
| `NGINX_DB_UPDATE_PATH` | `string` | Path to your nginx database update bash script |

## Documentation
Since this API uses FastAPI as a backend, you can see the auto-generated docs by appending `/docs` or `/redoc`. \
If you only want a basic understanding of responses you can check the value of the "result" key with the following table

For HTTP response code check [here](CONTRIBUTING.md#http-codes)

#### API Standard response
| Response Literal | Meaning |
| :--------------- | :------ |
| Ok               | The action has been executed correctly and (if applicable) for all elements of the requests |
| Valid            | The action for all existing elements has been executed correctly. This response will include a list of invalid elements found in the requests |
| Partial          | The action for some elements of the requests has been executed correctly. This type of response obligatory includes other data |
| None             | The specified action hasn't been executed for any of the elements |
| Invalid          | None of the specified elements exists |
| Received         | The specified action has been received by the server but no response is to be expected |

## Usage
### Manual
To start the bot manually use the `pystart` file
```bash
sudo ./pystart
```
### Service
Service status
```bash
sudo systemctl status RSMAPY
```
Start the service
```bash
sudo systemctl start RSMAPY
```
Stop the service
```bash
sudo systemctl stop RSMAPY
```
Disable the service (stop and prevent it from running automatically)
```bash
sudo systemctl disable RSMAPY
sudo systemctl stop RSMAPY
```
Enable the service
```bash
sudo systemctl enable RSMAPY
sudo systemctl start RSMAPY
```

# Contributing
See `CONTRIBUTING.md` for more information

## License
Distributed under the MIT License. See `LICENSE` for more information.