**Built with:** Python · Streamlit · Pandas

# NYU AV Operations Portal

![Dashboard](screenshots/dashboard.png)
## Overview
This project is a [Streamlit](streamlit.io)-based dashboard, developed as a sample application for the NYU Cloud and API Automation Developer position.

The application combines AV equipment inventory and staff schedules into a unified interface with Role-Based Access Control (RBAC), simulated device commands, and JSON payload generation.

## Features

- User authentication

- Role-Based Access Control (RBAC)

- AV equipment inventory dashboard

- Staff schedule dashboard

- Search and sort table data

- Device command simulation

- JSON payload generation

- JSON download

- Audit logging

## Project Structure
```text
app.py                  -> Main application

av_inventory.csv        -> Mock AV inventory

staff_schedules.csv     -> Mock staff schedules

audit_log.csv           -> Execution history

requirements.txt

README.md
```

## Installation
Install the required packages.

```bash
pip install -r requirements.txt
```

## Usage
1. Create `.streamlit/secrets.toml` with the following structure:

```toml
[usrs.your user name here]
psw = "your password here"
is_admin = true

[usrs.your user name here]
psw = "your password here"
is_admin = false

```
A template is named `secrets.example.toml` and is provided in the repository.

2. Run the application.

```bash
streamlit run app.py
```

## How to Test
### Manager

1. Login with Manager username & password.
2. Open **Control Center**.
3. Select one or more devices.
    1. To select multiple devices, enable **Batch Selection**.
    2. You can also enter device IDs manually.

![Device Selection](screenshots/control_center_1.png)
![Command Excecution](screenshots/control_center_2.png)
4. Choose a command.
5. Click **Generate & Preview**.
6. Confirm execution.
![Execution Confirm](screenshots/execution_confirm.png)
7. View the generated JSON payload.
8. Check the Audit Logs.
![Audit Log](screenshots/audit_log.png)

The generated JSON payload is displayed before command execution and can be downloaded after confirmation.

### Technician

1. Login with a Technician account.
2. View Inventory and Staff Schedules.
![Staff Schedules](screenshots/staff_schedule.png)
3. Device Control is restricted.
![Access Denied](screenshots/access_denied.png)

## Notes

This application is intended for demonstration purposes only.

No real AV hardware is controlled.
No real staff names are used.

Sample data is included for demonstration purposes.