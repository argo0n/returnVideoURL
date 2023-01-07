import time

from flask import Flask, redirect, render_template, request, abort, jsonify
import os

app = Flask(__name__)

@app.route('/video')
def video():
    video_url = request.args.get('url')
    text = request.args.get('text')
    if video_url:
        # Parse the video name and file format
        video_name, file_format = os.path.splitext(os.path.basename(video_url))
        # Set the title and description
        if text:
            title = text
        else:
            title = video_name
        description = file_format
        # If the name or format could not be parsed, use a fallback value
        if not title:
            title = "Video"
        if not description:
            description = "Video file"
        return render_template('video.html', video_url=video_url, title=title, description=description)
    else:
        abort(400, "Missing url parameter")

@app.route('/')
def index():
    redirect("https://discord.com/oauth2/authorize?client_id=844489130822074390&permissions=313344&scope=bot")

@app.route('/status')
def get_status():
    current_time = time.time()
    start_time = app.config['START_TIME']

    # Calculate the uptime in seconds, minutes, and hours
    uptime_seconds = int(current_time - start_time)
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)

    # Create the JSON object with the status information
    status = {
        "status": "OK",
        "uptime": f"{uptime_hours} hours, {uptime_minutes} minutes, {uptime_seconds} seconds",
        "last_restart": app.config['START_TIME']
    }

    # Return the JSON object as the response
    return jsonify(status)


if __name__ == '__main__':
    # from waitress import serve
    app.config['START_TIME'] = time.time()
    app.run(host="0.0.0.0", port=8080)