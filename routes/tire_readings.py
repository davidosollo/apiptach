######################################################################
# Tire Readings API
#
# Endpoints for managing tire pressure, temperature, tread,
# sensor status, GPS and other tire reading information.
#
# Routes:
#   GET  /api/tire-readings
#   POST /api/tire-readings
#
# SonarTech IoT
######################################################################
    
from flask import Blueprint, jsonify, request
from database.db import get_connection

tire_readings_bp = Blueprint("tire_readings", __name__)


@tire_readings_bp.route("/api/tire-readings", methods=["GET"])
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


@tire_readings_bp.route("/api/tire-readings", methods=["POST"])
def create_tire_reading():
    conn = None

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        required_fields = [
            "trailer_id",
            "axle_number",
            "position",
            "reading_time"
        ]

        missing_fields = [
            field for field in required_fields
            if field not in data
        ]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "fields": missing_fields
            }), 400

        conn = get_connection()

        sql = """
            INSERT INTO t_tire_readings (
                trailer_id,
                axle_number,
                position,
                tag_id,
                pressure,
                pressure_unit,
                temperature,
                temperature_unit,
                tread_depth,
                tread_unit,
                original_tread_depth,
                minimum_tread_depth,
                wear_percent,
                tread_remaining_percent,
                pressure_status,
                temperature_status,
                tread_status,
                overall_status,
                sensor_battery,
                odometer,
                latitude,
                longitude,
                reading_time
            )
            VALUES (
                %(trailer_id)s,
                %(axle_number)s,
                %(position)s,
                %(tag_id)s,
                %(pressure)s,
                %(pressure_unit)s,
                %(temperature)s,
                %(temperature_unit)s,
                %(tread_depth)s,
                %(tread_unit)s,
                %(original_tread_depth)s,
                %(minimum_tread_depth)s,
                %(wear_percent)s,
                %(tread_remaining_percent)s,
                %(pressure_status)s,
                %(temperature_status)s,
                %(tread_status)s,
                %(overall_status)s,
                %(sensor_battery)s,
                %(odometer)s,
                %(latitude)s,
                %(longitude)s,
                %(reading_time)s
            )
        """

        cursor_data = {
            "trailer_id": data.get("trailer_id"),
            "axle_number": data.get("axle_number"),
            "position": data.get("position"),
            "tag_id": data.get("tag_id"),
            "pressure": data.get("pressure"),
            "pressure_unit": data.get("pressure_unit", "PSI"),
            "temperature": data.get("temperature"),
            "temperature_unit": data.get("temperature_unit", "C"),
            "tread_depth": data.get("tread_depth"),
            "tread_unit": data.get("tread_unit", "mm"),
            "original_tread_depth": data.get("original_tread_depth"),
            "minimum_tread_depth": data.get("minimum_tread_depth"),
            "wear_percent": data.get("wear_percent"),
            "tread_remaining_percent": data.get("tread_remaining_percent"),
            "pressure_status": data.get("pressure_status"),
            "temperature_status": data.get("temperature_status"),
            "tread_status": data.get("tread_status"),
            "overall_status": data.get("overall_status"),
            "sensor_battery": data.get("sensor_battery"),
            "odometer": data.get("odometer"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "reading_time": data.get("reading_time")
        }

        with conn.cursor() as cursor:
            cursor.execute(sql, cursor_data)
            new_id = cursor.lastrowid

        return jsonify({
            "status": "ok",
            "message": "Tire reading created",
            "id": new_id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    finally:
        if conn:
            conn.close()