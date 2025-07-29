# 🔒 USB Physical Drive Security System

A Python-based system to **detect, block, and log malicious USB drive insertions** on a Windows machine. It enhances physical device security by logging USB events, scanning file contents, recording intruders via webcam, and sending email alerts when suspicious devices are detected.

---

## 🚀 Features

- **USB Insertion Detection**
- **Malware Keyword Scan** in USB files (e.g., `virus`, `trojan`, `malware`)
- **USB Blocking** via registry edits when threat is found
- **Webcam Intruder Recording** on detection
- **Email Alert** to system admin with incident log
- **User-friendly GUI** with quick access buttons
- **Log and Video Storage** for evidence

---

## 📂 Project Structure

| File/Folder         | Description |
|---------------------|-------------|
| `main.py`           | Main runner: initializes monitoring and GUI |
| `usb_monitor.py`    | Core USB detection and malware scan logic |
| `intruder.py`       | Handles webcam-based intruder video recording |
| `usb_gui.py`        | GUI interface using `Tkinter` |
| `Login.py`          | Admin login window (future use/expansion) |
| `intruder_logs/`    | Saved intruder videos (auto-generated) |
| `usb_monitor_log.txt` | Event logs with timestamps (auto-generated) |

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/usb-security-system.git
cd usb-security-system
```

### 2. Install Requirements
```bash
pip install opencv-python psutil
```

---

## 🧪 Usage

### Run the system:
```bash
python main.py
```

The program starts monitoring USB drives. If a new USB is inserted:
- It scans for malware keywords.
- If infected, it blocks USB ports, logs the event, sends an alert email, and records the intruder.

---

## 📸 Sample Output

- Intruder videos: can be saved in `intruder_logs/`
- Logs: saved in `usb_monitor_log.txt`

---

## 📚 Technologies Used

- Python 3.x
- OpenCV
- psutil
- Tkinter
- Windows Registry Commands
- SMTP (Email Notifications)

---

## 👨‍💻 Author

**Vishnu Thurvas**  
[LinkedIn Profile](https://www.linkedin.com/in/tsvishnu/)  
Cybersecurity Professional | Developer | Problem Solver

---
