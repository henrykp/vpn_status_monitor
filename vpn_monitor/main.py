import os
import sys
import argparse
import threading
import winreg
import logging
import logging
from . import gui, tray, monitor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ALLOWED_COUNTRY = os.environ.get("ALLOWED_COUNTRY", "HU")
APP_NAME = "VPNMonitor"

def install_startup():
    """Registers the application to run at startup."""
    exe_path = sys.executable
    logging.info(f"Registering startup: {exe_path}")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print(f"Successfully registered {APP_NAME} for startup.")
    except Exception as e:
        print(f"Failed to register startup: {e}")

def remove_startup():
    """Removes the application from startup."""
    logging.info("Removing startup registration")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print(f"Successfully removed {APP_NAME} from startup.")
    except FileNotFoundError:
        print(f"{APP_NAME} was not registered for startup.")
    except Exception as e:
        print(f"Failed to remove startup: {e}")

def main():
    parser = argparse.ArgumentParser(description="VPN Monitor")
    parser.add_argument("--install-startup", action="store_true", help="Register to run at Windows startup")
    parser.add_argument("--remove-startup", action="store_true", help="Remove from Windows startup")
    args = parser.parse_args()

    if args.install_startup:
        install_startup()
        return
    if args.remove_startup:
        remove_startup()
        return
    # Start Tray (Blocking)
    logging.info(f"Starting VPN Monitor. Allowed Country: {ALLOWED_COUNTRY}")

    # Initialize Components
    warning_window = gui.WarningWindow()
    
    # State
    snooze_until = None

    # Callbacks
    def on_exit():
        logging.info("Exiting...")
        warning_window.stop()
        tray_icon.stop()
        sys.exit(0)

    def on_snooze(minutes):
        nonlocal snooze_until
        import datetime
        snooze_until = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        logging.info(f"Snoozed until: {snooze_until}")
        warning_window.hide() # Hide immediately if visible
        tray_icon.update_menu(is_snoozed=True)

    def on_unsnooze():
        nonlocal snooze_until
        snooze_until = None
        logging.info("Snooze cancelled")
        tray_icon.update_menu(is_snoozed=False)

    def on_set_country():
        global ALLOWED_COUNTRY
        new_country = gui.get_input("Set Allowed Country", "Enter 2-letter Country Code (e.g. US, DE):", ALLOWED_COUNTRY)
        if new_country:
            ALLOWED_COUNTRY = new_country.upper()
            logging.info(f"Allowed Country updated to: {ALLOWED_COUNTRY}")

    tray_icon = tray.TrayIcon(
        on_exit=on_exit, 
        on_snooze=on_snooze, 
        on_unsnooze=on_unsnooze, 
        on_set_country=on_set_country,
        show_set_country=not monitor.has_allowed_ips_file()
    )

    # Define Monitor Loop
    def monitor_loop():
        while True:
            # Check Snooze
            import datetime
            if snooze_until and datetime.datetime.now() < snooze_until:
                # Snoozed
                pass 
            else:
                is_safe = monitor.check_safety(ALLOWED_COUNTRY)
                if not is_safe:
                    warning_window.show()
                else:
                    warning_window.hide()
            
            # Sleep 5 seconds
            threading.Event().wait(5)

    # Start Monitor in separate thread
    monitor_thread = threading.Thread(target=monitor_loop)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Start Tray (Blocking)
    logging.info("App running. Check system tray.")
    tray_icon.run()

if __name__ == "__main__":
    main()
