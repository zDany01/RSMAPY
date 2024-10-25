## API settings
Before using the app you need to rename the `config.py.template` file to `config.py` and modify some settings in it:

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `DEBUG_LOGGING` | `boolean` | Include debug logs in the window output |
| `PROTECTED_CONTAINERS` | `list[str]` | List of IDs of containers that will be excluded from standard operation |
| `TOKEN_TIMEOUT` | `int` | Timeout for the API Token in minutes
| `AUTH_SECRET` | `string` | The server secret key used to generate JWT Token, if set to Random the server will generate a new one each boot
| `AUTH_USERNAME` | `string` | Login username
| `AUTH_PASSWORD_HASH` | `string` | Login password hash in bcrypt hash format
| `BACKUP_SCRIPT_PATH` | `string` |  Path to your bash backup script |
| `BACKUP_SCRIPT_ARGS` | `list[string]` |  Arguments for your backup script|
| `BACKUP_FLAG_PATH` | `string` | Path for backup updated file |
| `NGINX_DB_UPDATE_PATH` | `string` | Path to your nginx database update bash script |