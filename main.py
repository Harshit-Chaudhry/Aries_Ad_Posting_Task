import subprocess
import time


DEVICE_IP = "192.168.43.1"


ACTION_INTERVAL = 60*6


TEXT_TO_TYPE = "post_invite_card clan_SD8TM4"

# -----------------------------------------------------------------------
# *** CRITICAL: REPLACE THESE COORDINATES WITH YOUR DEVICE'S ACTUAL VALUES ***
# Use Android's 'Pointer location' tool in Developer Options to find them.
# -----------------------------------------------------------------------

# 1. Coordinates for the chat input field ("Enter the text...")
CHAT_INPUT_COORDS = (1600, 1000) #(1600, 1000)#

# 2. Coordinates for a safe spot to tap. This is an optional step 
# to dismiss the soft keyboard before hitting send (if needed).
OUT_CLICK_COORDS = (1555, 70) # Placeholder: Middle of the screen

# 3. Coordinates for the Send/Enter button (the blue arrow)
SEND_BUTTON_COORDS = (1846,1000)#(2340, 995)#


# ===========================
# 2. HELPER FUNCTIONS (ADB Commands)
# ===========================

def adb_connect(ip):
    """Connects to the device over Wi-Fi (ADB over TCP/IP)."""
    print(f"-> Attempting to connect to {ip}:5555...")
    # This command tries to connect to the ADB port on the specified IP
    subprocess.run(f"adb connect {ip}:5555", shell=True, check=True, capture_output=True, text=True)
    # List devices to confirm connection
    devices_output = subprocess.run("adb devices", shell=True, check=True, capture_output=True, text=True)
    print("-> Connected devices:\n" + devices_output.stdout)

def adb_tap(x, y):
    """Sends a tap event to the given coordinates (x, y)."""
    subprocess.run(f"adb shell input tap {x} {y}", shell=True)

def adb_type(text):
    """Types text safely using ADB input (escaping spaces & special chars)."""
    safe_text = text.replace(" ", "%s").replace("!", "%20").replace("'", "\\'")
    subprocess.run(f'adb shell input text "{safe_text}"', shell=True)


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
        adb_connect(DEVICE_IP)
    except Exception as e:
        print(f"!!! ERROR: Could not connect to device at {DEVICE_IP}. Ensure ADB over Wi-Fi is set up.")
        print(f"Details: {e}")
        return

    # Start the infinite loop for continuous operation
    while True:
        print("\n==================================")
        print(f"[*] Starting new cycle at {time.strftime('%H:%M:%S')}")
        
        # 1. Chat Click (Tap Input Field)
        print(f"[1/4] Tapping Chat Input at {CHAT_INPUT_COORDS}...")
        adb_tap(*CHAT_INPUT_COORDS)
        time.sleep(3)
        
        # 2. Writing Text
        print(f"[2/4] Typing text: '{TEXT_TO_TYPE}'")
        adb_type(TEXT_TO_TYPE)
        time.sleep(2)

        # 3. Out Click (Tap outside the keyboard/input field)
        # This is often necessary to dismiss the soft keyboard if it's blocking the Send button.
        print(f"[3/4] Tapping Out Click at {OUT_CLICK_COORDS} (Dismissing keyboard)...")
        adb_tap(*OUT_CLICK_COORDS)
        time.sleep(2)
        
        # 4. Enter Click (Tap Send Button)
        print(f"[4/4] Tapping Send Button at {SEND_BUTTON_COORDS}...")
        adb_tap(*SEND_BUTTON_COORDS)
        
        # Wait for the next loop cycle
        print(f"[*] Cycle finished. Waiting {ACTION_INTERVAL} seconds before restarting...")
        time.sleep(ACTION_INTERVAL)

if __name__ == "__main__":
    main()
