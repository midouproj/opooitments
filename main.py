from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# تحميل مفتاح Firebase من المتغير البيئي
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials:
    raise ValueError("⚠️ لم يتم العثور على المتغير FIREBASE_CREDENTIALS في البيئة!")

cred = credentials.Certificate(json.loads(firebase_credentials))
firebase_admin.initialize_app(cred)

# إنشاء مرجع لقاعدة البيانات
db = firestore.client()
appointments_ref = db.collection("appointments")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book_appointment():
    try:
        data = request.json
        required_fields = ["first_name", "last_name", "phone", "email", "lawyer_name", "lawyer_code", "message"]

        if not all(k in data for k in required_fields):
            return jsonify({"error": "بيانات غير مكتملة"}), 400

        # حفظ البيانات في Firestore
        appointment = appointments_ref.add(data)

        return jsonify({"message": "تم حجز الموعد بنجاح!", "id": appointment[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
