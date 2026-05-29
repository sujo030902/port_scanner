#!/usr/bin/env python3

import os
import threading
import uuid
import datetime
from flask import Flask, render_template, request, jsonify, send_file
from recon_scanner import run_scan, save_results, resolve_target, COMMON_PORTS, read_report

app = Flask(__name__)
scans = {}
scans_lock = threading.Lock()
scan_order = []


def scan_worker(scan_id, target, start_port, end_port):
    def progress(scanned, total, results):
        with scans_lock:
            if scan_id in scans:
                scans[scan_id]["scanned"] = scanned
                scans[scan_id]["total"] = total
                scans[scan_id]["results"] = results

    def stop_check():
        with scans_lock:
            return scan_id in scans and scans[scan_id]["stopped"]

    with scans_lock:
        now = datetime.datetime.now().isoformat()
        scans[scan_id] = {
            "status": "running",
            "target": target,
            "ip": "",
            "start_port": start_port,
            "end_port": end_port,
            "scanned": 0,
            "total": end_port - start_port + 1,
            "results": [],
            "elapsed": 0,
            "stopped": False,
            "report_path": None,
            "created_at": now
        }
        scan_order.insert(0, scan_id)

    result = run_scan(target, start_port, end_port, progress, stop_check)

    with scans_lock:
        if scan_id in scans:
            if result:
                scans[scan_id]["status"] = "complete"
                scans[scan_id]["ip"] = result["ip"]
                scans[scan_id]["elapsed"] = result["elapsed"]
                scans[scan_id]["results"] = result["results"]
                scans[scan_id]["scanned"] = result["scanned"]
                scans[scan_id]["total"] = result["total"]
                report_path = save_results(target, result["results"], result["elapsed"])
                scans[scan_id]["report_path"] = report_path
            else:
                scans[scan_id]["status"] = "error"
                scans[scan_id]["error"] = f"Could not resolve target: {target}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/resolve", methods=["POST"])
def api_resolve():
    data = request.get_json()
    target = data.get("target", "").strip()
    if not target:
        return jsonify({"error": "Target is required"}), 400
    ip = resolve_target(target)
    if ip:
        return jsonify({"ip": ip})
    return jsonify({"error": "Could not resolve"}), 400


@app.route("/api/scan", methods=["POST"])
def api_scan():
    data = request.get_json()
    target = data.get("target", "").strip()
    scan_type = data.get("type", "quick")

    if not target:
        return jsonify({"error": "Target is required"}), 400

    if scan_type == "quick":
        start_port, end_port = 1, 30
    elif scan_type == "common":
        ports = sorted(COMMON_PORTS.keys())
        start_port, end_port = ports[0], max(ports)
    elif scan_type == "full":
        start_port, end_port = 1, 10000
    elif scan_type == "custom":
        try:
            p_range = data.get("range", "")
            parts = p_range.split("-")
            if len(parts) == 2:
                start_port = max(1, int(parts[0]))
                end_port = min(65535, int(parts[1]))
                if start_port > end_port:
                    start_port, end_port = end_port, start_port
            else:
                start_port = end_port = int(parts[0])
        except:
            return jsonify({"error": "Invalid port range"}), 400
    else:
        return jsonify({"error": "Invalid scan type"}), 400

    scan_id = uuid.uuid4().hex[:12]
    thread = threading.Thread(target=scan_worker, args=(scan_id, target, start_port, end_port), daemon=True)
    thread.start()

    return jsonify({"scan_id": scan_id})


@app.route("/api/scan/<scan_id>", methods=["GET"])
def api_scan_status(scan_id):
    with scans_lock:
        if scan_id not in scans:
            return jsonify({"error": "Scan not found"}), 404
        return jsonify(scans[scan_id])


@app.route("/api/scan/<scan_id>/stop", methods=["POST"])
def api_scan_stop(scan_id):
    with scans_lock:
        if scan_id in scans:
            scans[scan_id]["stopped"] = True
            return jsonify({"status": "stopped"})
    return jsonify({"error": "Scan not found"}), 404


@app.route("/api/scan/<scan_id>/report")
def api_scan_report(scan_id):
    with scans_lock:
        if scan_id not in scans:
            return jsonify({"error": "Scan not found"}), 404
        report_path = scans[scan_id].get("report_path")
        if not report_path or not os.path.exists(report_path):
            return jsonify({"error": "Report not found"}), 404

    return send_file(report_path, as_attachment=True)


@app.route("/api/scans")
def api_scans_list():
    with scans_lock:
        history = []
        for sid in scan_order[:20]:
            s = scans.get(sid)
            if s:
                history.append({
                    "scan_id": sid,
                    "target": s["target"],
                    "status": s["status"],
                    "open_ports": len(s.get("results", [])),
                    "created_at": s.get("created_at", ""),
                    "elapsed": s.get("elapsed", 0)
                })
        return jsonify(history)


@app.route("/results/<scan_id>")
def results_page(scan_id):
    with scans_lock:
        scan = scans.get(scan_id)
        if not scan:
            return render_template("results.html", scan=None, error="Scan not found.")
        report_content = ""
        report_path = scan.get("report_path")
        if report_path and os.path.exists(report_path):
            report_content = read_report(report_path)
        history = []
        for sid in scan_order[:20]:
            s = scans.get(sid)
            if s:
                history.append({
                    "scan_id": sid,
                    "target": s["target"],
                    "status": s["status"],
                    "open_ports": len(s.get("results", [])),
                    "created_at": s.get("created_at", ""),
                    "elapsed": s.get("elapsed", 0)
                })
    return render_template("results.html", scan=dict(scan), scan_id=scan_id, report_content=report_content, history=history, error=None)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"  [*] Recon Scanner Web UI starting on http://127.0.0.1:{port}")
    print(f"  [*] Open your browser and navigate to http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
