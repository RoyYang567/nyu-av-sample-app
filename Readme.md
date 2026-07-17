# NYU AV Operations Portal

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](#)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-FF4B4B?logo=streamlit&logoColor=white)](https://nyu-av-sample-app.streamlit.app/)

> A Streamlit-based sample application demonstrating spreadsheet integration,
> role-based access control (RBAC), and JSON-based AV device command simulation.

<img src="screenshots/dashboard.png" width="850">

---

## 🚀 Live Demo

**Demo Website:**  https://nyu-av-sample-app.streamlit.app/

**Demo Accounts**

| Role | Username | Password |
| :--- | :------: | :------: |
| Manager | `admin` | `123123` |
| Technician | `tec` | `123123` |

---

## Overview

This project was developed as a sample application for the **NYU Cloud and API Automation Developer** position.

The application integrates AV equipment inventory and staff schedules into a unified dashboard with Role-Based Access Control (RBAC), simulated AV device commands, JSON payload generation, and audit logging.

## Features

- 🔐 User Authentication
- 👥 Role-Based Access Control (RBAC)
- 📦 AV Equipment Inventory Dashboard
- 📅 Staff Schedule Dashboard
- 🔍 Search & Sort Data
- 🎛 Device Command Simulation
- 📄 JSON Payload Generation
- ⬇ JSON Payload Download
- 📝 Audit Logging

## Project Structure
```text
.
├── app.py
├── requirements.txt
├── README.md
├── av_inventory.csv
├── staff_schedules.csv
├── audit_log.csv
├── screenshots/
└── .streamlit/
    ├── config.toml
    └── secrets.example.toml
```

## Installation
Install all required packages for this project with the following command:

```bash
pip install -r requirements.txt
```

## Configuration
Create `.streamlit/secrets.toml` with the following structure:

```toml
[usrs.MANAGER username here]
psw = "your password here"
is_admin = true

[usrs.TECHNICIAN username here]
psw = "your password here"
is_admin = false

```
A template is named `secrets.example.toml` and is provided in the repository.

`config.toml` sets the Theme color for this project.

## Run
Run the application:

```bash
streamlit run app.py
```

## How to Test
### Manager

1. Login with Manager username & password.
2. Open **Control Center**.
3. Select one or more devices.
    1. To select multiple devices, enable **Batch Selection**.
    <img src="screenshots/control_center_1.png" width="450">
    
    2. You can also enter device IDs manually.
    <img src="screenshots/control_center_2.png" width="450">

4. Choose a command.
5. Click **Generate & Preview**.
6. Confirm execution.
<img src="screenshots/execution_confirm.png" width="450">

7. View the generated JSON payload.

8. Check the Audit Logs.
![Audit Log](screenshots/audit_log.png)

#### JSON Payload Example
The generated JSON payload is displayed before command execution and can be downloaded after confirmation.

Sample downloaded JSON File:
```JSON
{
  "request_id": "REQ-20260717-1b14454c",
  "timestamp": "2026-07-17T07:21:23.428799Z",
  "user": "admin",
  "command": "power_on",
  "device": "display_037",
  "status": "queued"
}
```

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