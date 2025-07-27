import psutil
import time
import os
import subprocess
import smtplib
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === CONFIGURATION ===
scan_keywords = ['malware', 'trojan', 'virus']
log_file = "usb_monitor_log.txt"
email_sender = "vishnthurvas@example.com"
email_password = "cgihebodcdxsoemi"
email_receiver = "tsvishcyber@example.com"

# === UTILITIES ===

def log_usb_event(event_type, message):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {event_type}: {message}\n")

def send_alert_email():
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = "🚨 Malware Alert - USB Intrusion"

    body = "A malicious USB device was detected and blocked."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, msg.as_string())
    server.quit()

def record_intruder_video(duration=10, filename="intruder.avi"):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Intruder Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def block_usb():
    os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f")
    os.system("sc stop USBSTOR")

def unblock_usb():
    os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f")
    os.system("sc start USBSTOR")

# === CORE FUNCTIONALITY ===

def get_usb_drive_letters():
    drive_letters = []
    for device in psutil.disk_partitions(all=False):
        if 'removable' in device.opts.lower():
            drive_letters.append(device.device)
        else:
            # Fallback to WMI for exact matching
            drive = device.device
            try:
                powershell_script = f'''
$drives = Get-WmiObject Win32_DiskDrive | Where-Object {{$_.InterfaceType -eq 'USB'}}
foreach ($drive in $drives) {{
    $partitions = Get-WmiObject -Query "ASSOCIATORS OF {{Win32_DiskDrive.DeviceID='$($drive.DeviceID)'}} WHERE AssocClass=Win32_DiskDriveToDiskPartition"
    foreach ($partition in $partitions) {{
        $logicalDisks = Get-WmiObject -Query "ASSOCIATORS OF {{Win32_DiskPartition.DeviceID='$($partition.DeviceID)'}} WHERE AssocClass=Win32_LogicalDiskToPartition"
        foreach ($logicalDisk in $logicalDisks) {{
            Write-Output $logicalDisk.DeviceID
        }}
    }}
}}
'''
                result = subprocess.run(["powershell", "-Command", powershell_script], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if line.strip() and line.strip() not in drive_letters:
                        drive_letters.append(line.strip() + "\\")
            except Exception as e:
                log_usb_event("Error", f"Drive detection error: {e}")
    return drive_letters

def scan_usb(drive):
    print(f"Scanning USB {drive}")
    record_intruder_video()

    
    try:
        for root, dirs, files in os.walk(drive):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read().lower()
                        for keyword in scan_keywords:
                            if keyword in content:
                                log_usb_event("Malware Found", f"{keyword} in {file_path}")
                                return True
                except Exception:
                    continue
    except Exception as e:
        log_usb_event("Error", f"Failed to scan USB: {e}")
    return False

# === MAIN LOOP ===

def monitor_usb():
    print("[INFO] USB monitoring started.")
    previous_drives = set(get_usb_drive_letters())

    while True:
        try:
            time.sleep(5)
            current_drives = set(get_usb_drive_letters())
            new_drives = current_drives - previous_drives

            if new_drives:
                for drive in new_drives:
                    log_usb_event("USB Inserted", f"Drive: {drive}")
                    print(f"[INFO] New USB detected: {drive}")
                    infected = scan_usb(drive)

                    if infected:
                        print("[ALERT] Malware found! Taking actions.")
                        send_alert_email()
                        block_usb()
                        log_usb_event("USB Blocked", f"Malware detected on drive {drive}")
                    else:
                        print("[OK] No malware found.")

            previous_drives = current_drives

        except Exception as e:
            log_usb_event("Error", f"Exception in monitor loop: {e}")
            print(f"[ERROR] Exception in monitor loop: {e}")

if __name__ == "__main__":
    unblock_usb()
    monitor_usb()
