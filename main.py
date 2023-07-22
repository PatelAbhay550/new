from flask import Flask, request, jsonify, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    try:
        youtube_url = request.args.get('url')

        if not youtube_url:
            return jsonify({"error": "YouTube URL not provided."}), 400

        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Get the highest resolution stream (first progressive stream)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        if not video_stream:
            return jsonify({"error": "Video format not available."}), 400

        # Get the video title to use as the filename
        video_filename = f"{yt.title}.mp4"

        # Download the video
        video_path = video_stream.download(filename=video_filename)

        # Return the video file as the API response
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
