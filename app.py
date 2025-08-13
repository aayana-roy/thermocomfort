from flask import Flask, render_template, abort, request, jsonify
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import uuid
from datetime import datetime, timedelta, timezone

# Load environment variables from .env
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Fetch Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialising Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Location Dict with all details
locations = {
    "college-library-1": [
        "static/images/cl1.jpg",
        "https://docs.google.com/forms/d/e/1FAIpQLSeurE3m8ZLLfBH4TqBIsdQXjDqmfpIYrYlW9dnJOf7W2gLw3g/viewform?usp=header", 
        "College Library First Floor"
    ],
    "college-library-2": [
        "static/images/cl2.jpg", 
        "https://docs.google.com/forms/d/e/1FAIpQLSeurE3m8ZLLfBH4TqBIsdQXjDqmfpIYrYlW9dnJOf7W2gLw3g/viewform?usp=header", 
        "College Library Second Floor"
    ],
    "college-library-3": [
        "static/images/cl3.jpg", 
        "https://docs.google.com/forms/d/e/1FAIpQLSeurE3m8ZLLfBH4TqBIsdQXjDqmfpIYrYlW9dnJOf7W2gLw3g/viewform?usp=header", 
        "College Library Third Floor"
    ],
}

# Room_ID with coordinates as polygons
def rect_to_poly(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return [
        [x1, y1],  # Top-left
        [x1, y2],  # Bottom-left
        [x2, y2],  # Bottom-right
        [x2, y1]   # Top-right
    ]

rooms_data = {
    "college-library-1": [
        {"id": "1191B", "polygon": rect_to_poly([282,764], [203,688])},
        {"id": "1191D", "polygon": rect_to_poly([202,570], [283,686])},
        {"id": "1191A", "polygon": rect_to_poly([201,481], [282,569])},
        {"id": "1191 Main Collection", "polygon": [
            [104,325],[282,325],[285,485],[203,483],[204,762],[66,761],[67,676],
            [105,675],[103,567],[66,568],[64,479],[101,475],[101,393],[104,389]
        ]},
        {"id": "1191E", "polygon": rect_to_poly([63, 389], [99, 477])},
        {"id": "1193D Instruction Classroom", "polygon": rect_to_poly([104, 183], [191, 319])},
        {"id": "1193C", "polygon": rect_to_poly([64, 202], [99, 226])},
        {"id": "1193B", "polygon": rect_to_poly([65, 228], [99, 252])},
        {"id": "1193A", "polygon": rect_to_poly([63, 254], [100, 281])},
        {"id": "1193 Ethnic Studies Collection", "polygon": rect_to_poly([192, 181], [326, 319])},
        {"id": "1201 Security Office", "polygon": rect_to_poly([332, 180], [380, 268])},
        {"id": "1209 First Floor Center", "polygon": [
            [654,280],[654,179],[385,181],[384,280],[428,282],[431,338],
            [416,332],[400,329],[350,329],[339,329],[339,361],[376,361],
            [380,381],[653,381],[653,359],[711,361],[710,332],[657,331],
            [625,332],[607,338],[605,279]
        ]},
        {"id": "West Stairwell", "polygon": rect_to_poly([379, 384], [470, 466])},
        {"id": "East Stairwell", "polygon": rect_to_poly([568, 384], [654, 466])},
        {"id": "1250 Open Book Cafe", "polygon": rect_to_poly([710, 180], [842, 283])},
        {"id": "1250 Open Book Collection", "polygon": [
            [840,200],[893,201],[893,553],[702,551],[698,361],
            [712,361],[712,333],[712,283],[842,284]
        ]},
        {"id": "1250A Vending", "polygon": [
            [893,554],[893,657],[807,657],[703,552]
        ]},
        {"id": "Entrance/Exit", "polygon": rect_to_poly([474, 383], [562, 465])},
        {"id": "Elevator", "polygon": rect_to_poly([284, 323], [338, 422])}
    ]
}

# Testing supabase integration
@app.route("/test-supabase")
def test_supabase():
    response = supabase.table("markers").select("*").order("timestamp", desc=True).limit(10).execute()
    print(response.data)
    return jsonify(response.data)

# Route to submit markers to supabase in the "markers" table
@app.route("/submit-markers", methods=["POST"])
def submit_markers():
    try:
        data = request.json
        print("Received data:", data)
        
        user_id = data.get("user_id")
        location = data.get("location")
        markers = data.get("markers", [])

        for marker in markers:
            print("Inserting marker:", marker)
            
            supabase.table("markers").insert({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "location": location,
                "room_id": marker.get("room_id"),
                "x": marker.get("x"),
                "y": marker.get("y"),
                "type": marker.get("type"),
                "timestamp": datetime.fromtimestamp(marker.get("timestamp") / 1000).isoformat()
            }).execute()
        print("Markers saved.")
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print("Error in /submit-markers:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/get-markers/<location>/<user_id>")
def get_markers(location, user_id):
    try:
        # 3 hours ago in ISO format (UTC)
        three_hours_ago = (datetime.utcnow() - timedelta(hours=3)).isoformat()
        
        response = supabase.table("markers") \
            .select("room_id, x, y, type") \
            .eq("location", location) \
            .eq("user_id", user_id) \
            .gte("timestamp", three_hours_ago) \
            .execute()
            
        markers = response.data or []
        print("Markers fetched (last 3 hours):", markers)
        
        return jsonify(markers)
        
    except Exception as e:
        print("Error in /get-markers:", e)
        return jsonify({"error": str(e)}), 500

# This is an experiment for the dashboard. May change!!!
@app.route("/<location>/dashboard")
def dashboard(location):
    if location not in locations:
        abort(404)
    print(f"Dashboard requested for location: {location}")

    response = supabase.table("markers") \
        .select("room_id, type, timestamp") \
        .eq("location", location) \
        .gte("timestamp", (datetime.utcnow() - timedelta(hours=3)).isoformat()) \
        .execute()

    data = response.data or []

    # Aggregate by room
    from collections import defaultdict, Counter
    room_stats = defaultdict(lambda: Counter())

    for entry in data:
        room = entry["room_id"]
        marker_type = entry["type"]
        room_stats[room][marker_type] += 1
        room_stats[room]["total"] += 1

    # Compute comfort index
    def compute_comfort_index(c):
        w = {
            "hot": -1,
            "warm": -0.5,
            "ideal": 0,
            "cool": 0.5,
            "cold": 1
        }
        total = c["total"]
        if total == 0:
            return {"index": 0, "label": "No Data"}
        index = sum(w.get(k, 0) * c[k] for k in w) / total
        if index <= -0.75:
            label = "Too Hot"
        elif index <= -0.25:
            label = "Warm"
        elif index <= 0.25:
            label = "Ideal"
        elif index <= 0.75:
            label = "Cool"
        else:
            label = "Too Cold"
        return {"index": round(index, 2), "label": label}

    comfort_data = {
        room: {
            "stats": dict(c),
            **compute_comfort_index(c)
        }
        for room, c in room_stats.items()
    }
    
    rooms = rooms_data.get(location, [])

    return render_template("dashboard.html", comfort_data=comfort_data, location=location, rooms=rooms,image=locations[location][0],title=locations[location][2])

#THIS CAN BE DELETED, is some API for the dasboard
@app.route("/api/<location>/comfort-data")
def api_comfort_data(location):
    if location not in locations:
        return jsonify({"error": "Invalid location"}), 404

    try:
        # Get 'hours' parameter from query string, default to 3
        hours = int(request.args.get("hours", 3))
    except ValueError:
        hours = 3

    # Calculate cutoff time
    cutoff = datetime.utcnow() - timedelta(hours=hours)

    # Query supabase for markers in that time range
    response = supabase.table("markers") \
        .select("room_id, type, timestamp") \
        .eq("location", location) \
        .gte("timestamp", cutoff.isoformat()) \
        .execute()

    data = response.data or []

    from collections import defaultdict, Counter
    room_stats = defaultdict(lambda: Counter())
    total_counts = Counter()

    # Accumulate stats per room and overall
    for entry in data:
        room = entry["room_id"]
        marker_type = entry["type"]
        room_stats[room][marker_type] += 1
        room_stats[room]["total"] += 1

        total_counts[marker_type] += 1
        total_counts["total"] += 1

    # Compute comfort index helper
    def compute_comfort_index(c):
        weights = {
            "hot": -1,
            "warm": -0.5,
            "ideal": 0,
            "cool": 0.5,
            "cold": 1
        }
        total = c.get("total", 0)
        if total == 0:
            return 0
        index = sum(weights.get(k, 0) * c.get(k, 0) for k in weights) / total
        return index

    # Compute overall average comfort index
    avg_comfort = compute_comfort_index(total_counts)

    # Percent too hot and too cold overall
    def percent(count):
        return round((count / total_counts["total"]) * 100, 1) if total_counts["total"] > 0 else 0

    too_hot_percent = percent(total_counts.get("hot", 0) + total_counts.get("warm", 0))
    too_cold_percent = percent(total_counts.get("cold", 0) + total_counts.get("cool", 0))
    total_submissions = total_counts["total"]

    # Build trend data (e.g., averages per hour in the time window)
    # For simplicity, create hourly buckets with average comfort score
    from collections import defaultdict
    buckets = defaultdict(lambda: {"sum": 0, "count": 0})

    weights = {
        "hot": -1,
        "warm": -0.5,
        "ideal": 0,
        "cool": 0.5,
        "cold": 1
    }

    for entry in data:
        # Parse timestamp string to datetime
        ts = datetime.fromisoformat(entry["timestamp"])
        # Bucket by hour relative to now (or absolute hour)
        bucket_hour = ts.replace(minute=0, second=0, microsecond=0)
        score = weights.get(entry["type"], 0)
        buckets[bucket_hour]["sum"] += score
        buckets[bucket_hour]["count"] += 1

    # Sort buckets by time ascending
    sorted_buckets = sorted(buckets.items())
    trend_labels = [b[0].strftime("%H:%M") for b in sorted_buckets]
    trend_values = [
        (b[1]["sum"] / b[1]["count"]) if b[1]["count"] > 0 else 0
        for b in sorted_buckets
    ]

    trend = {"labels": trend_labels, "values": trend_values}

    # Prepare room colors and notes for map visualization
    # Map comfort index to color and label
    def comfort_color_label(index):
        if index == 0:
            return {"color": "#e5e7eb", "note": "No Data"}  # gray-200
        elif index <= -0.75:
            return {"color": "#ef4444", "note": "Too Hot"}  # red-500
        elif index <= -0.25:
            return {"color": "#fca5a5", "note": "Warm"}    # red-300
        elif index <= 0.25:
            return {"color": "#34d399", "note": "Ideal"}   # green-400
        elif index <= 0.75:
            return {"color": "#a5b4fc", "note": "Cool"}    # indigo-300
        else:
            return {"color": "#3b82f6", "note": "Too Cold"} # blue-500

    rooms = {}
    for room_id, counts in room_stats.items():
        idx = compute_comfort_index(counts)
        color_label = comfort_color_label(idx)
        rooms[room_id] = color_label

    # Build JSON response
    result = {
        "avgComfort": avg_comfort,
        "tooHot": too_hot_percent,
        "tooCold": too_cold_percent,
        "totalSubmissions": total_submissions,
        "trend": trend,
        "rooms": rooms
    }

    return jsonify(result)

#This is also an experiment for dashboard
@app.route("/<location>/newdashboard")
def new_dashboard(location):
    if location not in locations:
        abort(404)
    print(f"Dashboard requested for location: {location}")

    response = supabase.table("markers") \
        .select("room_id, type, timestamp") \
        .eq("location", location) \
        .gte("timestamp", (datetime.utcnow() - timedelta(hours=3)).isoformat()) \
        .execute()

    data = response.data or []

    # Aggregate by room
    from collections import defaultdict, Counter
    room_stats = defaultdict(lambda: Counter())

    for entry in data:
        room = entry["room_id"]
        marker_type = entry["type"]
        room_stats[room][marker_type] += 1
        room_stats[room]["total"] += 1

    # Compute comfort index
    def compute_comfort_index(c):
        w = {
            "hot": -1,
            "warm": -0.5,
            "ideal": 0,
            "cool": 0.5,
            "cold": 1
        }
        total = c["total"]
        if total == 0:
            return {"index": 0, "label": "No Data"}
        index = sum(w.get(k, 0) * c[k] for k in w) / total
        if index <= -0.75:
            label = "Too Hot"
        elif index <= -0.25:
            label = "Warm"
        elif index <= 0.25:
            label = "Ideal"
        elif index <= 0.75:
            label = "Cool"
        else:
            label = "Too Cold"
        return {"index": round(index, 2), "label": label}

    comfort_data = {
        room: {
            "stats": dict(c),
            **compute_comfort_index(c)
        }
        for room, c in room_stats.items()
    }
    
    rooms = rooms_data.get(location, [])

    return render_template("newdashboard.html", comfort_data=comfort_data, location=location, rooms=rooms,image=locations[location][0],title=locations[location][2])



@app.route('/<location>')

def show_floor_map(location):
    if location not in locations:
        abort(404)
    image, form_url, title = locations[location]
    rooms = rooms_data.get(location, [])
    return render_template(
        "floor_map.html",
        image=image,
        form_url=form_url,
        title=title,
        location=location,
        rooms=rooms
    )