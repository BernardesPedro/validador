import os
import platform
import socket
import psutil
import speedtest
import distro
from colorama import init, Fore, Style
from tqdm import tqdm
import time
import requests

init(autoreset=True)

def print_header():
    for _ in tqdm(range(30), desc="Inicializando"):
        time.sleep(0.05)
    print(Style.BRIGHT + Fore.GREEN + "╔" + "═" * 48 + "╗")
    print(Style.BRIGHT + Fore.CYAN + "║" + " MAXIMA TECH - VALIDADOR DE AMBIENTE ".center(48) + "║")
    print(Style.BRIGHT + Fore.CYAN + "║" + " By Departamento de Tecnologia ".center(48) + "║")
    print(Style.BRIGHT + Fore.GREEN + "╚" + "═" * 48 + "╝")
    print()
    time.sleep(0.5)

def get_cpu_info():
    cpu_info = {}
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if ":" in line:
                key, value = [item.strip() for item in line.split(":", 1)]
                cpu_info[key] = value
    return cpu_info

def get_memory_info():
    mem_info = {}
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if ":" in line:
                key, value = [item.strip() for item in line.split(":", 1)]
                mem_info[key] = int(value.split()[0])  # Pega apenas o valor numérico e converte para int
    return mem_info

def convert_kb_to_gb(kb):
    return kb / 1024 / 1024

def convert_bytes_to_gb(bytes):
    return bytes / 1024 / 1024 / 1024

def get_os_info():
    os_info = {}
    os_info['system'] = platform.system()
    os_info['release'] = platform.release()
    os_info['version'] = platform.version()
    os_info['architecture'] = platform.machine()
    os_info['distro'] = distro.name()
    os_info['distro_version'] = distro.version()
    return os_info

def get_root_partition_info():
    root_partition = psutil.disk_usage('/')
    return {
        'total': convert_bytes_to_gb(root_partition.total),
        'used': convert_bytes_to_gb(root_partition.used),
        'free': convert_bytes_to_gb(root_partition.free),
        'percent': root_partition.percent
    }

def check_internal_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Erro ao verificar porta interna: {e}")
        return False

def check_external_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Erro ao verificar porta externa: {e}")
        return False

def test_internet_speed():
    try:
        st = speedtest.Speedtest()
        with tqdm(desc="Testando velocidade da internet", ncols=100, colour="green", total=2) as pbar:
            download_speed = st.download()
            pbar.update(1)
            upload_speed = st.upload()
            pbar.update(1)
        return {
            'download': download_speed / 1_000_000,  # Convert to Mbps
            'upload': upload_speed / 1_000_000,  # Convert to Mbps
            'ping': st.results.ping
        }
    except Exception as e:
        print(Fore.RED + f"Erro ao testar a velocidade da internet: {e}")
        return {
            'download': 0,
            'upload': 0,
            'ping': 0
        }

def print_section_header(title):
    print(Style.BRIGHT + Fore.YELLOW + "\n" + "═" * 50)
    print(Style.BRIGHT + Fore.YELLOW + f"★ {title} ★")
    print(Style.BRIGHT + Fore.YELLOW + "═" * 50)
    time.sleep(0.5)

def print_status_line(description, status, color, icon="■", requirement=None):
    if color == Fore.RED:
        print(f"  ▷ {description.ljust(20)}: {color}{icon} {status} (Requisito: {requirement})")
    else:
        print(f"  ▷ {description.ljust(20)}: {color}{icon} {status}")
    time.sleep(0.2)

def main():
    print_header()

    cpu_info = get_cpu_info()
    mem_info = get_memory_info()
    os_info = get_os_info()
    root_partition_info = get_root_partition_info()
    internet_speed = test_internet_speed()

    model_name = cpu_info.get("model name", "N/A")
    cpu_cores = int(cpu_info.get("cpu cores", 0))
    architecture = os_info['architecture']
    cpu_mhz = float(cpu_info.get("cpu MHz", 0.0))

    total_ram_kb = mem_info.get("MemTotal", 0)
    free_ram_kb = mem_info.get("MemFree", 0)
    total_swap_kb = mem_info.get("SwapTotal", 0)
    free_swap_kb = mem_info.get("SwapFree", 0)

    total_ram_gb = convert_kb_to_gb(total_ram_kb)
    free_ram_gb = convert_kb_to_gb(free_ram_kb)
    total_swap_gb = convert_kb_to_gb(total_swap_kb)
    free_swap_gb = convert_kb_to_gb(free_swap_kb)

    # Color coding for CPU information
    cpu_arch_color = Fore.GREEN if "64" in architecture else Fore.RED
    cpu_speed_color = Fore.GREEN if cpu_mhz >= 2000 else Fore.RED
    cpu_cores_color = Fore.GREEN if cpu_cores >= 2 else Fore.RED
    cpu_cores_status = "✔" if cpu_cores >= 2 else "✖"
    cpu_speed_status = "✔" if cpu_mhz >= 2000 else "✖"

    # Color coding for memory
    memory_color = Fore.GREEN if total_ram_gb >= 6 else Fore.RED
    memory_status = "✔" if total_ram_gb >= 6 else "✖"

    # Color coding for OS information
    os_dist_color = Fore.GREEN if "ubuntu" in os_info['distro'].lower() else Fore.RED
    os_arch_color = Fore.GREEN if "64" in os_info['architecture'] else Fore.RED
    os_dist_status = "✔" if "ubuntu" in os_info['distro'].lower() else "✖"
    os_arch_status = "✔" if "64" in os_info['architecture'] else "✖"

    # Check Ubuntu version
    required_version = "20.04"
    os_version_color = Fore.GREEN if os_info['distro'] == 'Ubuntu' and os_info['distro_version'] >= required_version else Fore.RED
    os_version_status = "✔" if os_info['distro'] == 'Ubuntu' and os_info['distro_version'] >= required_version else "✖"

    # Color coding for root partition total size and percent used
    disk_color = Fore.GREEN if root_partition_info['total'] >= 50 else Fore.RED
    disk_status = "✔" if root_partition_info['total'] >= 50 else "✖"
    percent_used_color = Fore.RED if root_partition_info['percent'] > 60 else Fore.RESET

    # Color coding for internet speed
    download_color = Fore.GREEN if internet_speed['download'] >= 10 else Fore.RED
    upload_color = Fore.GREEN if internet_speed['upload'] >= 10 else Fore.RED
    ping_color = Fore.GREEN if internet_speed['ping'] <= 100 else Fore.RED
    download_status = "✔" if internet_speed['download'] >= 10 else "✖"
    upload_status = "✔" if internet_speed['upload'] >= 10 else "✖"
    ping_status = "✔" if internet_speed['ping'] <= 100 else "✖"

    print_section_header("PROCESSADOR")
    print(f"  ▷ MODELO              : {model_name}")
    print_status_line("NÚCLEOS", f"{cpu_cores} {cpu_cores_status}", cpu_cores_color, requirement=">= 2")
    print_status_line("ARQUITETURA", architecture, cpu_arch_color, requirement="64-bit")
    print_status_line("VELOCIDADE", f"{cpu_mhz:.2f} GHz {cpu_speed_status}", cpu_speed_color, requirement=">= 2.0 GHz")

    print_section_header("MEMÓRIA")
    print_status_line("RAM", f"{total_ram_gb:.2f} GB {memory_status}", memory_color, requirement=">= 6 GB")
    print_status_line("SWAP", f"{total_swap_gb:.2f} GB", Fore.CYAN)

    print_section_header("SISTEMA OPERACIONAL")
    print_status_line("NOME", os_info['system'], Fore.CYAN)
    print_status_line("DISTRIBUIÇÃO", f"{os_info['distro']} {os_dist_status}", os_dist_color, requirement="Ubuntu")
    print_status_line("VERSÃO", f"{os_info['distro_version']} {os_version_status}", os_version_color, requirement=">= 20.04")
    print_status_line("ARQUITETURA", f"{os_info['architecture']} {os_arch_status}", os_arch_color, requirement="64-bit")

    print_section_header("DISCO")
    print_status_line("TAMANHO TOTAL", f"{root_partition_info['total']:.2f} GB {disk_status}", disk_color, requirement=">= 50 GB")
    print_status_line("USO", f"{root_partition_info['percent']}%", percent_used_color, requirement="<= 60%")

    print_section_header("INTERNET")
    print_status_line("DOWNLOAD", f"{internet_speed['download']:.2f} Mbps {download_status}", download_color, requirement=">= 10 Mbps")
    print_status_line("UPLOAD", f"{internet_speed['upload']:.2f} Mbps {upload_status}", upload_color, requirement=">= 10 Mbps")
    print_status_line("PING", f"{internet_speed['ping']} ms {ping_status}", ping_color, requirement="<= 100 ms")

    print_section_header("PORTAS")
    ports = [9000, 9001, 9002, 9003, 10050, 10051]
    external_ip = requests.get('https://api.ipify.org').text
    for port in ports:
        internal_access = check_internal_port(port)
        external_access = check_external_port(external_ip, port)

        internal_status = Fore.GREEN + "✔" if internal_access else Fore.RED + "✖"
        external_status = Fore.GREEN + "✔" if external_access else Fore.RED + "✖"

        print(f"  ▷ Porta {port} : Interno {internal_status} | Externo {external_status}")
        time.sleep(0.3)

if __name__ == "__main__":
    main()
