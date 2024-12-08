import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for headless environments
from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import io
import numpy as np

app = Flask(__name__)

# Utility function to generate a chart
def generate_chart(data, labels, colors, title, xlabel, ylabel, crash_time=None):
    time = np.arange(0, len(data[0]) * 0.1, 0.1)  # Time in 0.1-second intervals

    fig, ax = plt.subplots()
    for i, series in enumerate(data):
        ax.plot(time, series, label=labels[i], color=colors[i])

    # Add vertical line for crash time
    if crash_time is not None:
        ax.axvline(x=crash_time, color='red', linestyle='--', label="Crash Trigger")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    plt.title(title)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

@app.route('/charts/plot/accelerometer', methods=['POST'])
def plot_accelerometer():
    data = request.json
    if not data or 'accelerometer_data' not in data:
        return jsonify({"error": "Invalid input, 'accelerometer_data' required"}), 400

    accelerometer_data = data['accelerometer_data']

    if not all(len(point) == 4 for point in accelerometer_data):  # Expecting [x, y, z, resultant]
        return jsonify({"error": "Each accelerometer data point must be an array of [x, y, z, resultant]"}), 400

    crash_time = data.get('crash_time')  # Optional crash time in seconds

    x_data = [point[0] for point in accelerometer_data]
    y_data = [point[1] for point in accelerometer_data]
    z_data = [point[2] for point in accelerometer_data]
    resultant_data = [point[3] for point in accelerometer_data]

    buf = generate_chart(
        [x_data, y_data, z_data, resultant_data],
        ["X-axis", "Y-axis", "Z-axis", "Resultant Acceleration"],
        ["blue", "green", "orange", "red"],
        "Accelerometer Data",
        "Time (seconds)",
        "Acceleration (m/s²)",
        crash_time=crash_time
    )
    return send_file(buf, mimetype='image/png')

@app.route('/charts/plot/gyroscope', methods=['POST'])
def plot_gyroscope():
    data = request.json
    if not data or 'gyroscope_data' not in data:
        return jsonify({"error": "Invalid input, 'gyroscope_data' required"}), 400

    gyroscope_data = data['gyroscope_data']

    if not all(len(point) == 4 for point in gyroscope_data):  # Expecting [x, y, z, rotationMagnitude]
        return jsonify({"error": "Each gyroscope data point must be an array of [x, y, z, rotationMagnitude]"}), 400

    crash_time = data.get('crash_time')  # Optional crash time in seconds

    x_data = [point[0] for point in gyroscope_data]
    y_data = [point[1] for point in gyroscope_data]
    z_data = [point[2] for point in gyroscope_data]
    rotation_magnitude = [point[3] for point in gyroscope_data]

    buf = generate_chart(
        [x_data, y_data, z_data, rotation_magnitude],
        ["X-axis", "Y-axis", "Z-axis", "Rotation Magnitude"],
        ["blue", "green", "orange", "purple"],
        "Gyroscope Data",
        "Time (seconds)",
        "Rotation (rad/s)",
        crash_time=crash_time
    )
    return send_file(buf, mimetype='image/png')

@app.route('/charts/plot/speed', methods=['POST'])
def plot_speed():
    data = request.json
    if not data or 'speed_data' not in data:
        return jsonify({"error": "Invalid input, 'speed_data' required"}), 400

    speed_data = data['speed_data']
    crash_time = data.get('crash_time')  # Optional crash time in seconds

    buf = generate_chart(
        [speed_data],
        ["Speed"],
        ["blue"],
        "Speed Over Time",
        "Time (seconds)",
        "Speed (m/s)",
        crash_time=crash_time
    )
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    