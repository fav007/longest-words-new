# Environment

Another way of modifying the behavior of a Python script (other than command line arguments) is to use the **environment variables**.

## Getting started

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/03-Environment
code .
nosetests
pipenv run pylint flask_option.py
```

## Exercise

Open the `flask_option.py` file and implement the `start` method. It should return a `String` depending on the presence and value of the `FLASK_ENV` environment variable.

Here is the expected behavior:

```bash
FLASK_ENV=development pipenv run python flask_option.py
# => "Starting in development mode..."

FLASK_ENV=production pipenv run python flask_option.py
# => "Starting in production mode..."

pipenv run python flask_option.py
# => "Starting in production mode..."
```

:bulb: **Tip**: have a look at the [`os`](https://docs.python.org/3/library/os.html) module.

## (Optional) Environment variables in PowerShell

Let's write a third [Hello World program](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) with the following behavior:

```bash
THE_NAME=Boris powershell -ExecutionPolicy bypass ./hello_env.ps1
# => Hello Boris
```

You should be able to figure out from the [documentation](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables) how to implement this 2-lines script.

<details><summary markdown="span">View solution
</summary>

```powershell
$name = (Get-Item -Path Env:THE_NAME).value
Write-Output "Hello $name"
```

</details>
