# sim/server/api_server.py
from flask import Flask, request, jsonify
from sim.events.ghost_pedestrian import GhostPedestrianEvent
from sim.events.slow_congestion import SlowCongestionEvent

app = Flask(__name__)

@app.route("/trigger_event", methods=["POST"])
def trigger_event():
    data = request.get_json()
    event_name = data.get("event")
    params = data.get("params", {})

    if event_name == "ghost":
        event = GhostPedestrianEvent(params)
    elif event_name == "slow":
        event = SlowCongestionEvent(params)
    else:
        return jsonify({"status": "error", "message": "Unknown event"}), 400

    event.trigger()
    return jsonify({"status": "success", "event": event_name, "message": "Event triggered"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)