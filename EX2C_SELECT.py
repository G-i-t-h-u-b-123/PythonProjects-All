import random
import time

def send_frame(frame_number, data):
    print(f"Sender: Sending Frame {frame_number} with data: '{data}'")
    time.sleep(0.5)

def receive_frame(frame_number, data):
    # Simulate frame loss (20% chance)
    frame_received = random.choice([True] * 4 + [False])
    if frame_received:
        print(f"Receiver: Frame {frame_number} with data '{data}' received.")
        print(f"Receiver: Sending ACK {frame_number}")
        return True
    else:
        print(f"Receiver: Frame {frame_number} lost! No ACK sent.")
        return False

def selective_repeat_arq(frames, window_size):
    total_frames = len(frames)
    acked = [False] * total_frames
    base = 0

    while base < total_frames:
        # Send frames in window
        for i in range(base, min(base + window_size, total_frames)):
            if not acked[i]:
                send_frame(i + 1, frames[i])

        # Receive ACKs or simulate lost ACKs
        for i in range(base, min(base + window_size, total_frames)):
            if not acked[i]:
                time.sleep(0.5)
                acked[i] = receive_frame(i + 1, frames[i])

        # Slide window for acknowledged frames
        while base < total_frames and acked[base]:
            base += 1

        print(f"Sender: Sliding window. New base is Frame {base + 1}\n")
        time.sleep(1)

# Example usage
frames_to_send = ["A", "B", "C", "D", "E", "F"]
window_size = 3

print("=== Selective Repeat ARQ Simulation ===\n")
selective_repeat_arq(frames_to_send, window_size)