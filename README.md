## Bot settings
Before using the app you need to rename the `config.py.template` file to `config.py` and modify some settings in it:

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `BACKUP_SCRIPT_PATH` | `string` |  Path to your bash backup script |
| `BACKUP_SCRIPT_ARGS` | `list[string]` |  Arguments for your backup script|
| `BACKUP_FLAG_PATH` | `string` | Path for backup updated file |
| `NGINX_DB_UPDATE_PATH` | `string` | Path to your nginx database update bash script |