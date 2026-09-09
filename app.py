######################################################################
# Patchip API
#
# REST API for the Patchip Tire Management System.
#
# Main responsibilities:
#   - Store tire readings
#   - Retrieve historical tire readings
#   - Retrieve the latest tire readings
#
# Application: Flask
# Database: MariaDB
# Server: Gunicorn
# Port: 5005
#
# SonarTech IoT
######################################################################

from flask import Flask, jsonify
from routes.tire_readings import tire_readings_bp

app = Flask(__name__)

app.register_blueprint(tire_readings_bp)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "service": "Patchip API"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005)