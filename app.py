from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask backend is working!", 200


# Read DB credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    sslmode="require"
)

@app.route('/save_transcript', methods=['POST'])
def save_transcript():
    data = request.json
    filename = data.get('filename')
    transcript = data.get('transcript')

    if not filename or not transcript:
        return jsonify({'error': 'Missing data'}), 400

    cur = conn.cursor()
    cur.execute("INSERT INTO session_transcripts (filename, transcript) VALUES (%s, %s)", (filename, transcript))
    conn.commit()
    cur.close()

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
