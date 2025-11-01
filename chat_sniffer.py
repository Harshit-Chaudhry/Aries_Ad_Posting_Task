import subprocess
import time

# ===========================
# 1. CONFIGURABLE SETTINGS
# ===========================

# Replace with your phone's IP address (check your phone's Wi-Fi settings)
DEVICE_IP = "192.168.43.1"

# The time delay (in seconds) between each action (tap, type, send)
ACTION_INTERVAL = 2

# The message you want the script to automatically type (Updated by user)
TEXT_TO_TYPE = "Hello from the DefQuant's bot! Ignoring, just a test."

# -----------------------------------------------------------------------
# *** CRITICAL: REPLACE THESE COORDINATES WITH YOUR DEVICE'S ACTUAL VALUES ***
# Use Android's 'Pointer location' tool in Developer Options to find them.
# -----------------------------------------------------------------------

# 1. Coordinates for the chat input field ("Enter the text...") (Updated by user)
# IMPORTANT: Find the exact X, Y where you tap to start typing.
CHAT_INPUT_COORDS = (1600, 1000) 

# 2. Coordinates for the Send/Enter button (the blue arrow) (Updated by user)
# IMPORTANT: Find the exact X, Y for the Send button.
SEND_BUTTON_COORDS = (2340, 995)

# OUT_CLICK_COORDS is no longer needed, as we use the reliable adb_back_key()


# ===========================
# 2. HELPER FUNCTIONS (ADB Commands)
# ===========================

def adb_connect(ip):
    """Connects to the device over Wi-Fi (ADB over TCP/IP)."""
    print(f"-> Attempting to connect to {ip}:5555...")
    # This command tries to connect to the ADB port on the specified IP
    # Adding a timeout for robustness
    subprocess.run(f"adb connect {ip}:5555", shell=True, check=True, capture_output=True, text=True, timeout=5)
    # List devices to confirm connection
    devices_output = subprocess.run("adb devices", shell=True, check=True, capture_output=True, text=True)
    print("-> Connected devices:\n" + devices_output.stdout)

def adb_tap(x, y):
    """Sends a tap event to the given coordinates (x, y)."""
    subprocess.run(f"adb shell input tap {x} {y}", shell=True)

def adb_type(text):
    """Types the given string of text."""
    # Note: Text must be enclosed in double quotes for ADB shell input
    subprocess.run(f'adb shell input text "{text}"', shell=True)

def adb_back_key():
    """Simulates pressing the physical Android Back button (keyevent 4)."""
    subprocess.run(f'adb shell input keyevent 4', shell=True)
    
def adb_swipe(x1, y1, x2, y2, duration=300):
    """Performs a swipe action (not used in this specific task, but kept)."""
    subprocess.run(f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}", shell=True)


# ===========================
# 3. MAIN AUTOMATION LOOP
# ===========================

def main():
    """Executes the sequence of tap, type, and send actions."""
    print("--- ADB Chat Automation Started ---")
    try:
        # Added robust error handling back
        adb_connect(DEVICE_IP)
    except subprocess.CalledProcessError:
        print(f"!!! ERROR: Failed to connect to device at {DEVICE_IP}. Check IP and ADB setup.")
        return
    except subprocess.TimeoutExpired:
        print(f"!!! ERROR: Connection attempt to {DEVICE_IP} timed out.")
        return
    except Exception as e:
        print(f"!!! An unexpected error occurred during connection: {e}")
        return

    # Start the infinite loop for continuous operation
    while True:
        print("\n==================================")
        print(f"[*] Starting new cycle at {time.strftime('%H:%M:%S')}")
        
        # 1. Chat Click (Tap Input Field)
        # This tap must correctly open the soft keyboard.
        print(f"[1/4] Tapping Chat Input at {CHAT_INPUT_COORDS}...")
        adb_tap(*CHAT_INPUT_COORDS)
        time.sleep(ACTION_INTERVAL)
        
        # 2. Writing Text
        # This will only work if the keyboard is up and the input field is active.
        print(f"[2/4] Typing text: '{TEXT_TO_TYPE}'")
        adb_type(TEXT_TO_TYPE)
        time.sleep(ACTION_INTERVAL)

        # 3. Dismiss Keyboard (Use Back Key for reliability)
        # This reliably hides the soft keyboard, making sure it doesn't block the Send button.
        print(f"[3/4] Dismissing keyboard using Back Key...")
        adb_back_key()
        time.sleep(ACTION_INTERVAL)
        
        # 4. Enter Click (Tap Send Button)
        print(f"[4/4] Tapping Send Button at {SEND_BUTTON_COORDS}...")
        adb_tap(*SEND_BUTTON_COORDS)
        
        # Wait for the next loop cycle
        print(f"[*] Cycle finished. Waiting {ACTION_INTERVAL} seconds before restarting...")
        time.sleep(ACTION_INTERVAL)

if __name__ == "__main__":
    main()
