from flask import Flask, jsonify
from database.db import get_connection

app = Flask(__name__)


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


@app.route("/api/tire-readings", methods=["GET"])
def get_tire_readings():
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM t_tire_readings
                ORDER BY reading_time DESC
            """)

            readings = cursor.fetchall()

        return jsonify(readings), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005)