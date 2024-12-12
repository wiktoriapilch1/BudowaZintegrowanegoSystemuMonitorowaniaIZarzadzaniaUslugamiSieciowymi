from prometheus_client import start_http_server, Gauge
import psutil
import time

# Definiowanie metryk
cpu_usage = Gauge('system_cpu_usage', 'CPU usage percentage')
memory_usage = Gauge('system_memory_usage', 'Memory usage in percentage')
disk_usage = Gauge('system_disk_usage', 'Disk usage in percentage')
load_1m = Gauge('system_load_1m', 'System load average over 1 minute')
load_5m = Gauge('system_load_5m', 'System load average over 5 minutes')
load_15m = Gauge('system_load_15m', 'System load average over 15 minutes')
disk_read_bytes = Gauge('system_disk_read_bytes', 'Total number of bytes read from disk')
network_bytes_sent = Gauge('system_network_bytes_sent', 'Total number of bytes sent over the network')
network_bytes_recv = Gauge('system_network_bytes_recv', 'Total number of bytes received over the network')

def collect_metrics():
    while True:
        # Zbieranie metryk
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        load1, load5, load15 = psutil.getloadavg()
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()

        # Aktualizacja metryk
        cpu_usage.set(cpu)
        memory_usage.set(memory)
        disk_usage.set(disk)
        load_1m.set(load1)
        load_5m.set(load5)
        load_15m.set(load15)
        disk_read_bytes.set(disk_io.read_bytes)
        network_bytes_sent.set(net_io.bytes_sent)
        network_bytes_recv.set(net_io.bytes_recv)

        # Odczekaj chwilę przed kolejnym zbiorem
        time.sleep(5)

if __name__ == '__main__':
    # Uruchomienie serwera HTTP na porcie 9100
    start_http_server(9100)
    # Zbieranie metryk
    collect_metrics()
