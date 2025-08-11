import os
import shutil
import json
import platform
import time
import sys
import socket
import requests

# --- Fungsi Utility ---
def clear():
    os.system("clear")

def box(title, content):
    width = shutil.get_terminal_size().columns
    border = "╭" + "─" * (width - 2) + "╮"
    footer = "╰" + "─" * (width - 2) + "╯"
    middle_lines = content.split('\n')

    formatted_lines = []
    for i, line in enumerate(middle_lines):
        if i == 0:
            formatted_lines.append(f"│ {title}: {line}".ljust(width - 1) + "│")
        else:
            formatted_lines.append(f"│ {line}".ljust(width - 1) + "│")

    return f"{border}\n" + "\n".join(formatted_lines) + f"\n{footer}"

# --- Fungsi Pengambilan Data ---
def count_running_apps():
    """Menghitung jumlah proses yang sedang berjalan."""
    try:
        output = os.popen("ps -A").read().strip()
        return len(output.split('\n')) - 1
    except:
        return "N/A"

def get_ram():
    try:
        with open("/proc/meminfo") as f:
            meminfo = f.readlines()
        total = int(meminfo[0].split()[1]) // 1024
        available = int(meminfo[2].split()[1]) // 1024
        used = total - available
        apps = count_running_apps()
        return f"{used}MB / {total}MB | Aplikasi: {apps}"
    except:
        return "Tidak terdeteksi"

def get_cpu():
    try:
        cpu_name = os.popen("getprop ro.soc.model").read().strip() or os.popen("getprop ro.hardware").read().strip()
        if not cpu_name:
            with open("/proc/cpuinfo") as f:
                for line in f.readlines():
                    if "model name" in line:
                        cpu_name = line.split(":", 1)[1].strip()
                        break
        core_count = os.cpu_count() or "?"
        arch = platform.machine()
        return f"{cpu_name or 'Tidak terdeteksi'} ({core_count} cores, {arch})"
    except:
        return "Tidak terdeteksi"

def get_storage(path="/storage/emulated/0"):
    try:
        total, used, free = shutil.disk_usage(path)
        total_gb = total // (2**30)
        used_gb = used // (2**30)
        return f"{used_gb}GB / {total_gb}GB"
    except:
        return "Tidak terdeteksi"

def get_battery(short=True):
    try:
        status = os.popen("termux-battery-status").read()
        data = json.loads(status)
        if short:
            return f"{data['percentage']}% | {data['temperature']}°C"
        else:
            lines = [
                f"Battery: {data['percentage']}% ({data['status'].capitalize()})",
                f"Health: {data['health'].capitalize()}",
                f"Technology: {data['technology']}",
                f"Temperature: {data['temperature']}°C",
                f"Voltage: {data['voltage'] / 1000:.2f} V",
                f"Current: {data['current'] / 1000:.0f} mA",
            ]
            return "\n".join(lines)
    except:
        return "Termux API belum diinstal"

def get_sim_provider():
    """Mendapatkan nama provider seluler."""
    try:
        provider = os.popen("getprop gsm.operator.alpha").read().strip()
        return provider if provider else "Tidak terdeteksi"
    except:
        return "Tidak terdeteksi"

def get_wifi_details():
    """Mendapatkan detail Wi-Fi menggunakan Termux API."""
    try:
        wifi_info = os.popen("termux-wifi-connectioninfo").read().strip()
        if wifi_info:
            data = json.loads(wifi_info)
            if data['supplicant_state'] == 'COMPLETED':
                ssid = data.get("ssid", "Tidak diketahui").replace('"', '')
                bssid = data.get("bssid", "Tidak terdeteksi")
                return f"SSID: {ssid}\nBSSID (MAC Address): {bssid}"
            else:
                return "Wi-Fi tidak terhubung"
        return "Termux API untuk Wi-Fi tidak berfungsi"
    except Exception as e:
        return f"Error: {e}"

def get_network_info_summary():
    """Mendapatkan informasi jaringan (ringkas) untuk tampilan awal."""
    try:
        # Cek koneksi dengan socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            ping_status = "Tersambung"
        except socket.error:
            ping_status = "Terputus"
            
        # Dapatkan IP Publik dengan requests
        public_ip = "Tidak terdeteksi"
        if ping_status == "Tersambung":
            try:
                response = requests.get("https://ifconfig.me", timeout=5)
                if response.status_code == 200:
                    public_ip = response.text.strip()
            except requests.exceptions.RequestException:
                pass
        
        return f"Status: {ping_status}\nIP Publik: {public_ip or 'Tidak terdeteksi'}"
    except:
        return "Tidak terdeteksi"

def get_network_info_detail():
    """Mendapatkan informasi jaringan yang lebih lengkap."""
    try:
        output_lines = []
        
        # Cek koneksi dengan socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            ping_status = "Tersambung"
        except socket.error:
            ping_status = "Terputus"
            
        output_lines.append(f"Status: {ping_status}")
        
        # Dapatkan IP Publik dengan requests
        public_ip = "Tidak terdeteksi"
        if ping_status == "Tersambung":
            try:
                response = requests.get("https://ifconfig.me", timeout=5)
                if response.status_code == 200:
                    public_ip = response.text.strip()
            except requests.exceptions.RequestException:
                pass
        
        output_lines.append(f"IP Publik: {public_ip or 'Tidak terdeteksi'}")
        
        output_lines.append("\n--- Wi-Fi ---")
        output_lines.append(get_wifi_details())
        
        output_lines.append("\n--- Seluler ---")
        provider = get_sim_provider()
        output_lines.append(f"Provider: {provider}")
        output_lines.append("MAC Address: Tidak dapat diakses tanpa root")

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: {e}"

def get_termux_api_status():
    """Memeriksa apakah termux-api terinstal."""
    return os.system("command -v termux-sensor > /dev/null") == 0

def check_sensors():
    """Mendapatkan daftar sensor dan statusnya."""
    if not get_termux_api_status():
        return "ERROR: termux-api belum diinstal. Jalankan 'pkg install termux-api'."
    try:
        sensor_list_output = os.popen("termux-sensor -l").read().strip()
        if not sensor_list_output or "sensors" not in sensor_list_output:
            return "Tidak ada sensor yang terdeteksi."
        data = json.loads(sensor_list_output)
        sensors = data.get("sensors", [])
        output_lines = [
            f"Jumlah sensor terdeteksi: {len(sensors)}",
            "Daftar Sensor:"
        ]
        for sensor in sensors:
            output_lines.append(f"- {sensor}")
        if "Accelerometer" in sensor_list_output:
            output_lines.append("\n--- Pengecekan Akselerometer ---")
            accel_data_raw = os.popen("termux-sensor -s Accelerometer -d 1 -c 1").read().strip()
            if accel_data_raw:
                accel_data = json.loads(accel_data_raw)
                latest_data = accel_data['sensors']['Accelerometer'][0]
                output_lines.append(f"Akselerasi X: {latest_data['values'][0]:.2f} G")
                output_lines.append(f"Akselerasi Y: {latest_data['values'][1]:.2f} G")
                output_lines.append(f"Akselerasi Z: {latest_data['values'][2]:.2f} G")
            else:
                output_lines.append("Gagal mengambil data akselerometer.")
        return "\n".join(output_lines)
    except Exception as e:
        return f"ERROR: Terjadi kesalahan saat mengambil data sensor.\nDetail: {e}"

def real_time_monitor():
    """Menampilkan informasi sistem secara real-time"""
    try:
        while True:
            clear()
            print(box("CPU", get_cpu()))
            print(box("RAM", get_ram()))
            print(box("Storage", get_storage()))
            print(box("Battery", get_battery(short=True)))
            print(box("Jaringan", get_network_info_summary()))
            print("\nProses Teratas:")
            os.system("ps -o pid,pcpu,pmem,user,cmd --sort=-pcpu | head -n 6")
            print("\nTekan Ctrl+C untuk kembali ke menu utama...")
            time.sleep(2)
    except KeyboardInterrupt:
        pass

# --- Menu Utama ---
def main_menu():
    while True:
        clear()
        print(box("CPU", get_cpu()))
        print(box("RAM", get_ram()))
        print(box("Storage", get_storage()))
        print(box("Battery", get_battery(short=True)))
        print(box("Jaringan", get_network_info_summary()))

        print("\nPilih menu:")
        print("1. Monitoring real-time")
        print("2. Pengecekan Sensor")
        print("3. baterai")
        print("4. jaringan")
        print("0. Keluar")

        choice = input("Masukkan pilihan: ")
        if choice == "1":
            real_time_monitor()
        elif choice == "2":
            clear()
            print(box("Pengecekan Sensor", check_sensors()))
            input("\nTekan Enter untuk kembali...")
        elif choice == "3":
            clear()
            print(box("Detail Baterai", get_battery(short=False)))
            input("\nTekan Enter untuk kembali...")
        elif choice == "4":
            clear()
            print(box("Detail Jaringan", get_network_info_detail()))
            input("\nTekan Enter untuk kembali...")
        elif choice == "0":
            break

if __name__ == "__main__":
    main_menu()

