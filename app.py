from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# ✅ Replace with your API Gateway URL
API_GATEWAY_URL = "https://9tvi4xz43g.execute-api.us-east-1.amazonaws.com/prod/fraud-detection"

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None

    if request.method == "POST":
        try:
            # ✅ Get form inputs
            features = [
                float(request.form["amt"]),
                int(request.form["gender"]),
                int(request.form["category_entertainment"]),
                int(request.form["category_food_dining"]),
                int(request.form["category_gas_transport"]),
                int(request.form["category_grocery_net"]),
                int(request.form["category_health_fitness"]),
                int(request.form["category_home"]),
                int(request.form["category_travel"]),
            ]

            # ✅ Send request to API Gateway
            response = requests.post(API_GATEWAY_URL, json={"features": features})
            data = response.json()  # API response

            # ✅ Determine fraud status
            if data["is_fraud"]:
                prediction_result = "❌ Fraud Detected!"
            else:
                prediction_result = "✅ Legitimate Transaction"

        except Exception as e:
            prediction_result = f"⚠️ Error: {str(e)}"

    return render_template("index.html", result=prediction_result)

if __name__ == "__main__":
    app.run(debug=True)
