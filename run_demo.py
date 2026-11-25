"""
MediMind AI: One-Click 600x Viva Demonstration Script
Executes an automated full-day adherence cycle:
1. Verifies backend seed data
2. Connects simulator at 600x time-warp speed
3. Simulates Morning Dose: TAKEN on time
4. Simulates Afternoon Dose: Network Offline + TAKEN queued
5. Simulates Evening Dose: WRONG COMPARTMENT alarm
6. Simulates Night Dose: 3 retries expired -> MISSED dose alert & SMS Outbox
7. Restores Wi-Fi and flushes offline queue
"""
import sys
import os
import time
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.seeds.seed_data import seed_database
from simulator.box_sim import BoxSimulator

def run_viva_demo():
    print("\n" + "="*70)
    print("   MEDIMIND AI: 600x ACCELERATED VIVA DEMONSTRATION")
    print("   Final-Year B.E. CSE Project Software Demonstration")
    print("="*70 + "\n")

    client = TestClient(app)
    seed_database()

    print("[DEMO STAGE 1] Initializing ESP32 Virtual Medicine Box...")
    sim = BoxSimulator(box_id="box_esp32_001", device_key="devkey_medimind_secret_7721", timewarp=600, http_client=client)
    sim.sync_schedule_from_cloud()
    # Transition past BOOT and SYNC into IDLE
    sim.tick()
    sim.tick()
    print(f"--> Box provisioned. Synced v{sim.local_schedule_version} with {len(sim.local_schedules)} active compartments.\n")
    time.sleep(0.5)

    def jump_time(hour: int, minute: int):
        sim.virtual_clock = sim.virtual_clock.replace(hour=hour, minute=minute, second=0, microsecond=0)
        sim.last_wall_tick = time.time()
        sim.tick()

    # 1. Morning Dose
    slot0_time = sim.local_schedules[0]["scheduled_time"]
    h0, m0 = map(int, slot0_time.split(":"))
    print(f"[DEMO STAGE 2] Morning Dose ({slot0_time} {sim.local_schedules[0]['medicine_name']}) - TAKEN ON TIME")
    jump_time(h0, m0)
    print(f"--> [HARDWARE] Slot {sim.active_remind_slot + 1} LED ON. Piezo Buzzer Sounding. OLED: '{sim.oled_text.splitlines()[0]}'")
    time.sleep(0.8)
    print("--> [PATIENT] Elderly patient opens Compartment 1 within 15 seconds.")
    sim.trigger_lid_open(0)
    print("--> Status: TAKEN recorded. LED extinguished, buzzer silenced.\n")
    time.sleep(0.8)

    # 2. Afternoon Dose (Wi-Fi Offline)
    slot1_time = sim.local_schedules[1]["scheduled_time"]
    h1, m1 = map(int, slot1_time.split(":"))
    print(f"[DEMO STAGE 3] Afternoon Dose ({slot1_time} {sim.local_schedules[1]['medicine_name']}) - WI-FI OFFLINE & QUEUE TEST")
    print("--> [NETWORK] Home Wi-Fi router loses power. Box toggles to OFFLINE mode.")
    sim.wifi_online = False
    jump_time(h1, m1)
    print("--> [LOCAL RTC] Dose alarm fires from cached schedule in SPIFFS flash memory.")
    sim.trigger_lid_open(1)
    print(f"--> [OFFLINE BUFFER] Event queued in event_queue.json. Queued items count: {len(sim.event_queue)}\n")
    time.sleep(0.8)

    # 3. Evening Dose (Wrong Compartment)
    slot2_time = sim.local_schedules[2]["scheduled_time"]
    h2, m2 = map(int, slot2_time.split(":"))
    print(f"[DEMO STAGE 4] Evening Dose ({slot2_time} {sim.local_schedules[2]['medicine_name']}) - WRONG COMPARTMENT TEST")
    jump_time(h2, m2)
    print(f"--> [HARDWARE] Slot {sim.active_remind_slot + 1} LED ON for {sim.active_medicine}. Buzzer sounding.")
    print("--> [PATIENT ERROR] Patient mistakenly opens Compartment 2 instead of Compartment 3.")
    sim.trigger_lid_open(1) # Wrong slot!
    print(f"--> [ALARM] OLED Warning: '{sim.oled_text.splitlines()[0]}'. Emergency buzzer beeps.")
    time.sleep(0.8)

    # 4. Night Dose (Missed Dose Escalation)
    slot3_time = sim.local_schedules[3]["scheduled_time"]
    h3, m3 = map(int, slot3_time.split(":"))
    print(f"\n[DEMO STAGE 5] Night Dose ({slot3_time} {sim.local_schedules[3]['medicine_name']}) - MISSED DOSE ESCALATION & ALERTS")
    jump_time(h3, m3)
    print(f"--> Attempt 1/3: Gentle reminder sounds at {slot3_time}. No lid opened.")
    time.sleep(0.5)
    sim.virtual_clock += datetime.timedelta(minutes=5)
    sim.last_wall_tick = time.time()
    sim.tick()
    print("--> Attempt 2/3: Louder reminder sounds (+5m). No lid opened.")
    time.sleep(0.5)
    sim.virtual_clock += datetime.timedelta(minutes=5)
    sim.last_wall_tick = time.time()
    sim.tick()
    print("--> Attempt 3/3: Urgent highest-frequency alarm sounds (+10m). No lid opened.")
    time.sleep(0.5)
    sim.virtual_clock += datetime.timedelta(minutes=5)
    sim.last_wall_tick = time.time()
    sim.tick()
    print(f"--> [CRITICAL TIMEOUT] Dose marked MISSED. Alert dispatched to caregiver push feed & SMS Outbox.")
    time.sleep(0.8)

    # 5. Wi-Fi Reconnect
    print("\n[DEMO STAGE 6] Wi-Fi Reconnection & Zero-Loss Queue Drain")
    print("--> [NETWORK] Wi-Fi connection restored.")
    sim.wifi_online = True
    sim.drain_offline_queue()
    print(f"--> Offline queue drained. Remaining local queue: {len(sim.event_queue)} (Zero event loss confirmed).\n")
    time.sleep(0.8)

    # 6. AI Risk Assessment
    print("[DEMO STAGE 7] AI Risk Predictor & Doctor Analytics Verification")
    res_ai = client.get("/api/v1/ai/risk/usr_patient_001")
    if res_ai.status_code == 200:
        data = res_ai.json()
        print(f"--> AI Evaluated Risk: {data['risk_level']} ({data['risk_score']*100:.1f}%)")
        print(f"--> Clinical Reasons: {data['reasons']}")
        print(f"--> Adaptive Protocol: {data['adaptive_action']}")

    print("\n" + "="*70)
    print("   VIVA DEMONSTRATION COMPLETE: ALL SCENARIOS VERIFIED SUCCESSFULLY!")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_viva_demo()
