from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

def run_pipeline():
    subprocess.run(["python", "main.py"])

@app.route('/start', methods=['POST'])
def start_pipeline():
    threading.Thread(target=run_pipeline).start()
    return jsonify({"status": "Pipeline started"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
