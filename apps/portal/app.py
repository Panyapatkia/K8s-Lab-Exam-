from flask import Flask, render_template, request, redirect, url_for
import json
import os
import tempfile

app = Flask(__name__)

DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "portal.json")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

DEFAULT_DATA = {
    "name": "Panyapat Sungrung",
    "student_id": "68130589",
    "image": ""
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DATA.copy()

def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=DATA_DIR)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, DATA_FILE)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route("/")
def index():
    return render_template("index.html", data=load_data())

@app.route("/edit", methods=["GET", "POST"])
def edit():
    data = load_data()

    if request.method == "POST":
        data["name"] = request.form.get("name", "").strip()
        data["student_id"] = request.form.get("student_id", "").strip()

        photo = request.files.get("photo")
        if photo and photo.filename:
            if not photo.mimetype.startswith("image/"):
                return "กรุณาเลือกไฟล์รูปภาพ", 400

            filename = "profile" + os.path.splitext(photo.filename)[1].lower()
            photo.save(os.path.join(UPLOAD_DIR, filename))
            data["image"] = filename

        save_data(data)
        return redirect(url_for("index"))

    return render_template("edit.html", data=data)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/health")
def health():
    return {"status": "ok", "application": "portal-589"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
