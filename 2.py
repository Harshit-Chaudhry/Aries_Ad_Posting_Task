import subprocess
import time
import unicodedata

# ==================================================
# DEVICE CONFIGURATION
# ==================================================
DEVICE_IP = "192.168.43.1"

# Coordinates (update these based on your device)
CHAT_INPUT_COORDS = (1600, 1000)
OUT_CLICK_COORDS = (1555, 70)
SEND_BUTTON_COORDS = (2340, 995)

# ==================================================
# MESSAGE SETUP
# ==================================================
MESSAGES = {
        1: "post_invite_card clan_SD8TM4",

        2: "Hola"#"History is in motion.        Second Wave of Aries  has already advanced 1100 ranks in just a month.       The seas belong to those who dare to conquer.     Global Top 50 is the next target.       Join ARIES2 Clan id - SD8TM4",
    
       # 3: "The seas are shaking.Second Wave Of Aries has already torn through 1100 ranks.         Next target: Global Top 50.         We call all captains ready to rise and conquer.            Join the wave. ARIES2  Clan id - SD8TM4"
    
       # 4: "Aries Second Wave is rewriting the charts.           Climbed 1100 ranks in a month, now looking on Global Top 50.           We fight as one, we rise as one.Strong captains worldwide — join  us and make history.          ARIES2 Clan  id - SD8TM4",
    
       # 5: "Aries brings its Second Wave.         A clan that improved 1100 ranks in one month and now targets the Global Top 50.        We are calling warriors who want to dominate, not just play.                 Join ARIES and claim your place in history.         Clan id - SD8TM4",
    

}

# Send interval (1.2 minutes = 72 seconds)
MESSAGE_INTERVAL = 60 * 3  # 72 seconds


# ==================================================
# ADB FUNCTIONS
# ==================================================
def adb_connect(ip):
    """Connects to the device over Wi-Fi (ADB over TCP/IP)."""
    print(f"-> Attempting to connect to {ip}:5555...")
    subprocess.run(f"adb connect {ip}:5555", shell=True, check=True, capture_output=True, text=True)
    devices_output = subprocess.run("adb devices", shell=True, check=True, capture_output=True, text=True)
    print("-> Connected devices:\n" + devices_output.stdout)

def adb_tap(x, y):
    """Sends a tap event."""
    subprocess.run(f"adb shell input tap {x} {y}", shell=True)

def adb_type(text):
    """Types long/special text safely in chunks (prevents NullPointerException)."""
    # Normalize and clean up problematic Unicode characters
    text = text.replace("—", "-").replace("’", "'")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()

    # Break text into smaller parts to avoid adb buffer errors
    chunks = [text[i:i+120] for i in range(0, len(text), 120)]
    for chunk in chunks:
        safe_chunk = chunk.replace(" ", "%s").replace("'", "\\'")
        subprocess.run(f'adb shell input text "{safe_chunk}"', shell=True)
        time.sleep(0.3)  # slight delay between chunks


# ==================================================
# MAIN LOOP
# ==================================================
def main():
    print("--- ADB Chat Automation Started ---")
    try:
        adb_connect(DEVICE_IP)
    except Exception as e:
        print(f"!!! ERROR: Could not connect to {DEVICE_IP}")
        print(f"Details: {e}")
        return

    msg_keys = list(MESSAGES.keys())
    msg_index = -1

    while True:
        msg_index = (msg_index + 1) % len(msg_keys)
        msg_text = MESSAGES[msg_keys[msg_index]]
        
        print("\n==================================")
        print(f"[*] Sending Message #{msg_keys[msg_index]} at {time.strftime('%H:%M:%S')}")
        print(f"-> Text: {msg_text[:80]}...")  # show first 80 chars for preview

        # 1. Tap chat input
        adb_tap(*CHAT_INPUT_COORDS)
        time.sleep(2)

        # 2. Type text safely
        adb_type(msg_text)
        time.sleep(2)

        # 3. Dismiss keyboard
        adb_tap(*OUT_CLICK_COORDS)
        time.sleep(1)

        # 4. Tap send button
        adb_tap(*SEND_BUTTON_COORDS)

        print(f"[*] Message sent. Waiting {MESSAGE_INTERVAL} seconds before next one...")
        time.sleep(MESSAGE_INTERVAL)


if __name__ == "__main__":
    main()
