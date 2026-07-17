import streamlit as st
import pandas as pd
import os
import json
import uuid
from datetime import datetime

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(page_title="NYU AV Operations Portal", page_icon="🎓", layout="wide")

# --------------------------------------------------
# Data Access Layer
# --------------------------------------------------
@st.cache_data
def load_data():
    """Loads and sanitizes CSV data."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def safe_load(filename):
        try:
            filepath = os.path.join(current_dir, filename)
            df = pd.read_csv(filepath, encoding="utf-8-sig")
            
            # Recover malformed CSV
            if len(df.columns) == 1 and "," in df.columns[0]:
                header = df.columns[0]
                df = df[header].str.split(',', expand=True)
                df.columns = [c.strip() for c in header.split(',')]
            return df
        except Exception:
            return None

    return safe_load("av_inventory.csv"), safe_load("staff_schedules.csv")

def update_inventory_status(device_list, command):
    """Updates the status of target devices and saves back to the CSV."""
    av_inv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "av_inventory.csv")
    try:
        df_inv = pd.read_csv(av_inv_path, encoding="utf-8-sig")
        status_changed = False
        
        for dev_id in device_list:
            # Locate target device
            row_mask = df_inv.iloc[:, 0].astype(str) == dev_id
            if row_mask.any():
                row_idx = df_inv.index[row_mask].tolist()[0]
                current_status = str(df_inv.iloc[row_idx, 3]).lower()
                
                # Update device status
                if command == "power_off" and "online" in current_status:
                    df_inv.iat[row_idx, 3] = "Offline"
                    status_changed = True
                elif command == "power_on" and "offline" in current_status:
                    df_inv.iat[row_idx, 3] = "Online"
                    status_changed = True
                    
        if status_changed:
            df_inv.to_csv(av_inv_path, index=False, encoding="utf-8-sig")
            st.cache_data.clear() # Refresh cached data
            
        return True
    except Exception as e:
        st.error(f"Database update failed: {e}")
        return False

def log_audit_action(user, device_list, command, result):
    """Appends administrative actions to the local audit log."""
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_log.csv")
    new_record = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": user,
        "Command": command,
        "Target Count": len(device_list),
        "Device IDs": ", ".join(device_list),
        "Status": result
    }])
    
    if os.path.exists(log_file):
        new_record.to_csv(log_file, mode='a', header=False, index=False, encoding="utf-8-sig")
    else:
        new_record.to_csv(log_file, index=False, encoding="utf-8-sig")

# --------------------------------------------------
# Execution Dialog
# --------------------------------------------------
@st.dialog("Execution Confirmation")
def confirm_execution_dialog(api_payload, device_list, action_cmd):
    """Execution confirmation dialog"""
    st.warning("You are about to execute a network command.")
    st.markdown(f"**Command:** `{action_cmd}`  \n**Target:** {len(device_list)} device(s)")
    st.json(api_payload)
    
    col1, col2 = st.columns(2)
    if col1.button("Cancel", use_container_width=True):
        st.rerun()
    if col2.button("Proceed", type="primary", use_container_width=True):
        if update_inventory_status(device_list, action_cmd):
            log_audit_action(st.session_state["usrname"], device_list, action_cmd, "Success")
            
            # Save execution state
            st.session_state["last_payload"] = api_payload
            st.session_state["last_command"] = f"{action_cmd} ({len(device_list)} devices)"
            st.session_state["last_time"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.update({"logged_in": False, "usrname": "", "is_admin": False})
if "last_payload" not in st.session_state:
    st.session_state.update({"last_payload": None, "last_command": None, "last_time": None})

# --------------------------------------------------
# Authentication UI
# --------------------------------------------------
if not st.session_state["logged_in"]:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.write("<br><br>", unsafe_allow_html=True)
        st.title("NYU AV Operations")
        with st.form("login"):
            usr = st.text_input("NetID")
            psw = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In", use_container_width=True):
                # Retrieve credentials securely from secrets
                if usr in st.secrets.get("usrs", {}) and psw == st.secrets["usrs"][usr]["psw"]:
                    st.session_state.update({
                        "logged_in": True, 
                        "usrname": usr, 
                        "is_admin": st.secrets["usrs"][usr]["is_admin"]
                    })
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    st.stop()

# --------------------------------------------------
# Main Dashboard
# --------------------------------------------------
df_inventory, df_schedules = load_data()
if df_inventory is None or df_schedules is None:
    st.error("Data Loading Error: Missing CSV files.")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    # NYU logo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
        with logo_col2:
            st.image(os.path.join(current_dir, "nyu_logo.png"), use_container_width=True)
    except Exception:
        st.markdown("<h3 style='text-align: center;'>NYU AV Ops</h3>", unsafe_allow_html=True)
        
    st.markdown("---")
    role = "Manager" if st.session_state["is_admin"] else "Technician"
    st.write(f"**User:** {st.session_state['usrname']}  \n**Role:** {role}")
    
    st.markdown("---")
    st.write("**Recent Activity**")
    if st.session_state["last_command"]:
        st.success(f"{st.session_state['last_command']}  \n{st.session_state['last_time']}")
    else:
        st.caption("No operations yet.")
        
    st.markdown("---")
    if st.button("Sign Out", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- Main Tabs ---
st.title("System Dashboard")
tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Staff Schedules", "Control Center", "Audit Logs"])

# Tab 1: Equipment Inventory with Status Indicators
with tab1:    
    # Helper to inject status lights
    def add_status_indicator(val):
        # Normalizing string to catch 'online', 'Online', ' ONLINE '
        status = str(val).strip().lower()
        if "online" in status:
            return "🟢 Online"
        elif "offline" in status:
            return "🔴 Offline"
        else:
            return f"⚪ {val}"

    # Apply the visual indicator
    df_display = df_inventory.copy()
    status_col = df_display.columns[3] # Assuming Status is index 3
    df_display[status_col] = df_display[status_col].apply(add_status_indicator)
    
    # Display
    df_display.index = range(1, len(df_display) + 1)
    st.dataframe(df_display, use_container_width=True, height=400)

# Tab 2: Shift Schedules
with tab2:
    st.subheader("Shift Management")
    
    # # Detect key columns
    name_col = df_schedules.columns[0]
    date_col = None
    for col in df_schedules.columns:
        if "name" in col.lower() or "staff" in col.lower():
            name_col = col
        if "date" in col.lower():
            date_col = col
            
    # Filters
    with st.form("schedule_filter"):
        search_staff = st.text_input("Search Staff", placeholder="Enter staff name...")
        show_today = st.checkbox("Today's Shifts")

        col1, col2 = st.columns([5, 1])

        with col2:
            apply = st.form_submit_button("Apply Filters", use_container_width=True)
  
    df_sch_disp = df_schedules.copy()

    if apply:
        if search_staff:
            df_sch_disp = df_sch_disp[df_sch_disp[name_col].astype(str).str.contains(search_staff, case=False, na=False)]

        if show_today and date_col:
            today_str = datetime.now().strftime("%Y-%m-%d")
            df_sch_disp = df_sch_disp[pd.to_datetime(df_sch_disp[date_col], errors="coerce").dt.strftime("%Y-%m-%d") == today_str]

    df_sch_disp.index = range(1, len(df_sch_disp) + 1)
    st.dataframe(df_sch_disp, use_container_width=True, height=400)

# Tab 3: Control Center
with tab3:
    if not st.session_state["is_admin"]:
        st.warning("Manager privileges required.")
    else:
        st.markdown("#### Step 1: Select Targets")
        enable_batch = st.checkbox("Enable Batch Selection")
        sel_mode = "multi-row" if enable_batch else "single-row"
        
        # ---Visual DataFrame---
        df_display = df_inventory.copy()
        def add_light(val):
            status = str(val).strip().lower()
            if "online" in status:
                return "🟢 Online"
            if "offline" in status:
                return "🔴 Offline"
            return val
        df_display.iloc[:, 3] = df_display.iloc[:, 3].apply(add_light)
        
        # Keep selection mapped to the original data
        sel_event = st.dataframe(df_display, use_container_width=True, hide_index=True, on_select="rerun", selection_mode=sel_mode)
        
        sel_rows = sel_event.selection.rows
        sel_ids = df_inventory.iloc[sel_rows].iloc[:, 0].tolist() if sel_rows else []
        
        st.markdown("---")
        st.markdown("#### Step 2: Dispatch Command")
        c1, c2 = st.columns(2)
        with c1:
            with st.form("cmd_form"):
                targets = st.text_input("Targets (Comma separated):", value=", ".join(sel_ids))
                action = st.selectbox("Action:", ["power_on", "power_off", "mute_audio", "unmute_audio", "reboot"])
                preview_btn = st.form_submit_button("Generate & Preview", use_container_width=True)
                
        with c2:
            if preview_btn:
                if not targets.strip():
                    st.error("Provide at least one Device ID.")
                else:
                    dev_list = [d.strip() for d in targets.split(",") if d.strip()]
                    payload = {
                        "request_id": f"REQ-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "user": st.session_state["usrname"],
                        "command": action,
                        **({"device": dev_list[0]} if len(dev_list) == 1 else {"devices": dev_list}),
                        "status": "queued"
                    }
                    confirm_execution_dialog(payload, dev_list, action)
                    
            elif st.session_state.get("last_payload"):
                st.success("Command successfully dispatched.")
                st.download_button(
                    "Download JSON Payload", 
                    json.dumps(st.session_state["last_payload"], indent=2), 
                    f"payload_{datetime.now().strftime('%H%M%S')}.json", 
                    "application/json",
                    use_container_width=True
                )

# Tab 4: Audit Logs
with tab4:
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_log.csv")
    if os.path.exists(log_path):
        df_audit = pd.read_csv(log_path)
        df_audit = df_audit.sort_values(by="Timestamp", ascending=False).reset_index(drop=True)
        df_audit.index = range(1, len(df_audit) + 1)
        st.dataframe(df_audit, use_container_width=True)
    else:
        st.info("No audit logs found. Logs will appear here once commands are executed.")