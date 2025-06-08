from flask import Flask, send_file, abort
import os

app = Flask(__name__)

@app.route('/watch/<int:file_id>/<filename>')
def serve_file(file_id, filename):
    path = f"./downloads/{file_id}/{filename}"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return abort(404)

if __name__ == "__main__":
    app.run()
