from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

location_data = {
    "lat": 0.0,
    "lon": 0.0,
    "timestamp": 0
}

@app.route("/", methods=["GET"])
def home():
    return "OwnTracks GPS Server is running.", 200

@app.route("/location", methods=["POST"])
def receive_location():
    try:
        data = request.get_json()
        if data is None or "_type" not in data:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

        if data["_type"] != "location":
            return jsonify({"status": "ignored", "message": "Not a location message"}), 200

        location_data["lat"] = data.get("lat", 0.0)
        location_data["lon"] = data.get("lon", 0.0)
        location_data["timestamp"] = data.get("tst", int(time.time()))

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/location", methods=["GET"])
def get_location():
    return jsonify(location_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
