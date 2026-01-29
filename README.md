# Automated Hardware-in-the-Loop (HIL) Verification Framework

**Project Role:** Validation & QA Automation   
**Domain:** Embedded Systems, Automated Testing, Python Scripting

This repository contains an **Automated Validation Suite** engineered to verify the robustness, latency, and data integrity of the Edge-to-Gateway communication link (STM32 Microcontroller to Python Host). It is designed to act as a "Hardware-in-the-Loop" (HIL) tester, stimulating inputs via UART and validating outputs against strict timing and integrity requirements.

---

## 🧪 Architecture Overview

The framework validates the embedded device as a black box system. It employs a suite of Python scripts to stress-test the serial interface, ensuring the system meets hard real-time constraints before deployment.



### Key Capabilities
* **Stress Testing:** Floods the serial interface with high-frequency telemetry packets (10KB payloads) to detect buffer overflows, race conditions, and packet loss thresholds.
* **Precision Timing Analysis:** Validates the host's ability to maintain real-time control loops (e.g., 100Hz) with sub-millisecond jitter, ensuring the setup is capable of accurate HIL simulation.
* **Protocol Handshaking:** Automates connection establishment and health monitoring, allowing for unattended long-duration stability testing.

---

## 📂 Module Breakdown

### 1. Stress Test Module (`uart_stress_test.py`)
This script performs a high-load integrity test to verify the physical link stability and driver performance.
* **Mechanism:** Generates a 10KB payload of cryptographically random bytes using `os.urandom`.
* **The Blast:** Transmits the full payload in a continuous stream to saturate the TX buffer.
* **The Autopsy:** Compares the received echo against the transmitted data byte-by-byte to detect bit flips or packet loss.
* **Metrics:** Calculates effective throughput (kbps) and Packet Loss Rate (PLR).

### 2. Timing Validator (`timing_validator.py`)
Before running HIL simulations, it is critical to ensure the Host PC's scheduler is stable enough to act as a real-time controller.
* **Target:** Simulates a 100Hz control loop (`INTERVAL = 0.01s`) for 10 seconds.
* **Precision:** Uses `time.perf_counter()` and a busy-wait loop to achieve higher precision than standard `time.sleep()`.
* **Analysis:** Calculates Mean Interval, Standard Deviation, and Max Jitter. If standard deviation exceeds 1.0ms, it flags the host as unsuitable for HIL simulation.

### 3. Connection Handshake (`handshake.py`)
A utility script to automate the initial "hello" sequence between the PC and the Microcontroller.
* **Protocol:** Clears input/output buffers, sends a test pattern ('ABCD'), and verifies the echo response.
* **Hardware Check:** Prompts the user to verify physical connections (TX connected to RX) if the echo fails.

### 4. Basic Functional Unit Test (`uart_test.py`)
A lightweight script for quick "sanity checks" during hardware setup.
* **Tests:** Validates single character transmission ('A'), string transmission ('HELLO'), and termination character handling (`\r\n`).
* **Troubleshooting:** Provides specific debugging steps if the port fails to open.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* STM32 Nucleo Board (programmed with Echo Firmware)
* Required Python libraries:
    ```bash
    pip install pyserial numpy
    ```

### Configuration
Edit the `SERIAL_PORT` variable in the scripts to match your system configuration:
* **Windows:** `COM3`, `COM4`, etc.
* **Linux/Mac:** `/dev/ttyUSB0`, `/dev/ttyACM0`

### Running the Suite

**1. Validate Host Timing**
Ensure your PC is not too busy to run the test.
```bash
python timing_validator.py
