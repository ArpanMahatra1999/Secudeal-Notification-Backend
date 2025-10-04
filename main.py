from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

@app.route("/send-notification", methods=["POST"])
def send_notification():
    data = request.get_json()
    fcm_token = data.get("fcmToken")
    title = data.get("title", "New Message")
    body = data.get("body", "")

    if not fcm_token:
        return jsonify({"error": "fcmToken is required"}), 400

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=fcm_token
    )

    try:
        response = messaging.send(message)
        return jsonify({"success": True, "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
