import asyncio
from collections import deque
from bleak import BleakScanner, BleakClient

SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHAR_UUID = "abcdefab-1234-1234-1234-abcdefabcdef"
DEVICE_NAME = "SmartWear_ESP32"

# ===== Tuning parameters =====
CALIBRATION_SAMPLES = 30
GOOD_THRESHOLD_ROLL = 15.0
GOOD_THRESHOLD_PITCH = 15.0

ROLL_THRESHOLD = 18.0
PITCH_THRESHOLD = 18.0

# If your sensor direction is reversed, change 1 to -1
ROLL_SIGN = 1
PITCH_SIGN = 1

# ===== Global state =====
baseline_roll = None
baseline_pitch = None

calibration_buffer = []
recent_roll = deque(maxlen=5)
recent_pitch = deque(maxlen=5)


def avg(values):
    return sum(values) / len(values) if values else 0.0


def classify_posture(roll: float, pitch: float) -> str:
    global baseline_roll, baseline_pitch, calibration_buffer

    # Fix sign if sensor is mounted in reverse
    roll = ROLL_SIGN * roll
    pitch = PITCH_SIGN * pitch

    # ----- Calibration phase -----
    if baseline_roll is None or baseline_pitch is None:
        calibration_buffer.append((roll, pitch))

        if len(calibration_buffer) < CALIBRATION_SAMPLES:
            return f"Calibrating... {len(calibration_buffer)}/{CALIBRATION_SAMPLES}"

        baseline_roll = avg([x[0] for x in calibration_buffer])
        baseline_pitch = avg([x[1] for x in calibration_buffer])
        calibration_buffer.clear()

        return "Baseline set"

    # ----- Smooth live data -----
    recent_roll.append(roll)
    recent_pitch.append(pitch)

    smooth_roll = avg(recent_roll)
    smooth_pitch = avg(recent_pitch)

    roll_diff = smooth_roll - baseline_roll
    pitch_diff = smooth_pitch - baseline_pitch

    # ----- Good posture -----
    if abs(roll_diff) < GOOD_THRESHOLD_ROLL and abs(pitch_diff) < GOOD_THRESHOLD_PITCH:
        return "Good posture"

    posture_flags = []

    # Left / Right
    if roll_diff > ROLL_THRESHOLD:
        posture_flags.append("Leaning right")
    elif roll_diff < -ROLL_THRESHOLD:
        posture_flags.append("Leaning left")

    # Forward / Backward
    if pitch_diff > PITCH_THRESHOLD:
        posture_flags.append("Leaning backward")
    elif pitch_diff < -PITCH_THRESHOLD:
        posture_flags.append("Slouching forward")

    if posture_flags:
        return " | ".join(posture_flags)

    return "Uncertain posture"


def notification_handler(sender, data):
    try:
        msg = data.decode("utf-8").strip()
        heading, roll, pitch = map(float, msg.split(","))

        posture = classify_posture(roll, pitch)

        print(
            f"Heading={heading:.2f}, Roll={roll:.2f}, Pitch={pitch:.2f} --> {posture}"
        )

    except Exception as e:
        print("Parse error:", e)


async def main():
    print("Scanning for BLE device...")
    devices = await BleakScanner.discover(timeout=5.0)

    target = None
    for d in devices:
        if d.name == DEVICE_NAME:
            target = d
            break

    if target is None:
        print("ESP32 device not found.")
        return

    print(f"Connecting to {target.name} ({target.address})")

    async with BleakClient(target.address) as client:
        print("Connected!")
        await client.start_notify(CHAR_UUID, notification_handler)

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())