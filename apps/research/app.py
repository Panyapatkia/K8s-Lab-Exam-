from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "research.json")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

DEFAULT_DATA = {
    "title": "การศึกษาเปรียบเทียบประสิทธิภาพของระบบ Object Storage (MinIO, SeaweedFS และ RustFS) ภายใต้รูปแบบการจัดการพื้นที่จัดเก็บข้อมูลแบบ JBOD และ LVM Striped บนสภาพแวดล้อมเสมือน",
    "summary": """การจัดเก็บข้อมูลในรูปแบบ Object Storage เป็นเทคโนโลยีที่มีบทบาทสำคัญต่อระบบ Cloud Infrastructure เนื่องจากรองรับการจัดเก็บข้อมูลจำนวนมาก การเข้าถึงข้อมูลผ่าน S3-compatible API และการขยายระบบให้รองรับปริมาณข้อมูลที่เพิ่มขึ้น อย่างไรก็ตาม ประสิทธิภาพของระบบ Object Storage ไม่ได้ขึ้นอยู่กับซอฟต์แวร์เพียงอย่างเดียว แต่ยังได้รับผลกระทบจากรูปแบบการจัดการพื้นที่จัดเก็บข้อมูลและโครงสร้างพื้นฐานที่ใช้ให้บริการด้วย

งานวิจัยนี้มีวัตถุประสงค์เพื่อศึกษาและเปรียบเทียบประสิทธิภาพของระบบ Object Storage จำนวน 3 ระบบ ได้แก่ MinIO, SeaweedFS และ RustFS ภายใต้รูปแบบการจัดการพื้นที่จัดเก็บข้อมูล 2 รูปแบบ คือ Separate Disk หรือ JBOD ซึ่งเป็นการใช้งานดิสก์แยกจากกัน และ LVM Striped Pool ซึ่งเป็นการกระจายข้อมูลไปยังอุปกรณ์จัดเก็บข้อมูลหลายชุดผ่าน Logical Volume Manager โดยดำเนินการทดลองบนสภาพแวดล้อมเสมือนที่ทำงานบน VMware ESXi

การออกแบบสภาพแวดล้อมการทดลองกำหนดให้แต่ละระบบมีโครงสร้างการทำงาน 4 Nodes และแยกการทดสอบตามรูปแบบ Storage ทั้งสองประเภท รวมเป็นเครื่องเสมือนทั้งหมด 24 VM โดยใช้ HAProxy เป็นตัวกลางในการกระจายคำขอไปยังระบบ Object Storage และใช้ MinIO WARP เป็นเครื่องมือสำหรับสร้างภาระงานทดสอบผ่าน S3 API เพื่อให้สามารถประเมินประสิทธิภาพภายใต้รูปแบบการใช้งานที่กำหนดได้อย่างเป็นระบบ

การทดสอบแบ่งออกเป็นการเขียนข้อมูล (PUT) และการอ่านข้อมูล (GET) โดยกำหนดขนาด Object ได้แก่ 4 KiB, 16 MiB และ 256 MiB ใช้ค่า Concurrency เท่ากับ 4 ระยะเวลาการทดสอบ 5 นาทีต่อชุด และทำการทดสอบซ้ำ 5 ครั้งต่อเงื่อนไข รวมทั้งสิ้น 180 ชุดทดสอบ เพื่อให้สามารถนำข้อมูลที่ได้มาเปรียบเทียบระหว่างระบบและรูปแบบ Storage ได้ภายใต้เงื่อนไขเดียวกัน

ตัวชี้วัดที่ใช้ในการวิเคราะห์ประกอบด้วย Throughput, Latency, จำนวน Objects ต่อวินาที และจำนวน Operations ต่อวินาที รวมถึงการตรวจสอบข้อผิดพลาดที่เกิดขึ้นระหว่างการทดสอบ ข้อมูลที่ได้จะถูกนำมาวิเคราะห์เปรียบเทียบเพื่อศึกษาความแตกต่างของประสิทธิภาพระหว่างระบบ Object Storage และรูปแบบการจัดการพื้นที่จัดเก็บข้อมูลแต่ละประเภท ผลการศึกษาจะช่วยให้เข้าใจผลกระทบของรูปแบบ Storage ต่อการทำงานของระบบ Object Storage และสามารถใช้เป็นข้อมูลประกอบการพิจารณาเลือกใช้สถาปัตยกรรมจัดเก็บข้อมูลในสภาพแวดล้อมเสมือนได้""",
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

@app.route("/research", methods=["GET"])
def research():
    return render_template("research.html", data=load_data())

@app.route("/research/edit", methods=["GET", "POST"])
def edit():
    data = load_data()
    if request.method == "POST":
        data["title"] = request.form.get("title", "").strip()
        data["summary"] = request.form.get("summary", "").strip()

        photo = request.files.get("photo")
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            if not photo.mimetype.startswith("image/"):
                return "กรุณาเลือกไฟล์รูปภาพ", 400
            photo.save(os.path.join(UPLOAD_DIR, filename))
            data["image"] = filename

        save_data(data)
        return redirect(url_for("research"))

    return render_template("edit.html", data=data)

@app.route("/research/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/health")
def health():
    return {"status": "ok", "application": "app-research"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
