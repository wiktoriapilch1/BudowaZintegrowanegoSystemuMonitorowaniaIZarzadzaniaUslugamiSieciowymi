from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Ścieżka do pliku dynamicznych targetów dla Prometheusa
TARGETS_FILE = "/etc/prometheus/targets.json"

# Funkcja pomocnicza do dodawania targetów
def add_target(targets, target, job):
    if target not in [t["targets"][0] for t in targets]:
        targets.append({"targets": [target], "labels": {"job": job}})
    return targets

@app.route('/register', methods=['POST'])
def register_vm():
    data = request.json
    vm_ip = data.get("ip")

    if not vm_ip:
        return jsonify({"error": "No IP provided"}), 400

    # Wczytaj istniejące targety
    if os.path.exists(TARGETS_FILE):
        with open(TARGETS_FILE, "r") as f:
            targets = json.load(f)
    else:
        targets = []

    # Dodaj target dla cadvisor (port 8080)
    targets = add_target(targets, f"{vm_ip}:8080", "cadvisor")

    # Dodaj target dla custom_exporter (port 9100)
    targets = add_target(targets, f"{vm_ip}:9100", "custom_exporter")

    # Zapisz zaktualizowane targety
    with open(TARGETS_FILE, "w") as f:
        json.dump(targets, f, indent=2)

    return jsonify({"status": "registered", "ip": vm_ip, "ports": ["8080", "9100"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
