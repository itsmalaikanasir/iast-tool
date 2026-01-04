from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import run_iast_scan

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return {"status": "IAST Backend Running"}

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Target URL missing"}), 400

    target_url = data["url"]
    findings = run_iast_scan(target_url)

    return jsonify({
        "target": target_url,
        "total_findings": len(findings),
        "findings": findings
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

