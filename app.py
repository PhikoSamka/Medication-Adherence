from flask import Flask, request, render_template
import pickle
import os

# --- Load model and DictVectorizer ---
model_path = os.path.join("models", "adherence_model-v1.0.bin")
with open(model_path, "rb") as f_in:
    dv, model = pickle.load(f_in)

# --- Initialize Flask App ---
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # --- Extract form data ---
        age = int(request.form['age'])
        gender = 1 if request.form['gender'] == 'Male' else 0
        prescription_period = int(request.form['prescription_period'])
        diabetes = 1 if request.form.get('diabetes') else 0
        alcoholism = 1 if request.form.get('alcoholism') else 0
        hypertension = 1 if request.form.get('hypertension') else 0
        smokes = 1 if request.form.get('smokes') else 0
        tuberculosis = 1 if request.form.get('tuberculosis') else 0
        smsReminder = 1 if request.form.get('smsReminder') else 0  # Optional intervention

        # --- Build input dictionary ---
        input_dict = {
            "age": age,
            "gender": gender,
            "prescription_period": prescription_period,
            "diabetes": diabetes,
            "alcoholism": alcoholism,
            "hypertension": hypertension,
            "smokes": smokes,
            "tuberculosis": tuberculosis,
            "smsReminder": smsReminder  # optional feature
        }

        # --- Vectorize ---
        input_vector = dv.transform([input_dict])

        # --- Predict ---
        prob = model.predict_proba(input_vector)[0, 1]  # probability for adherence

        # --- Determine adherence status ---
        threshold = 0.69
        adherence_status = "adhere" if prob >= threshold else "be non-adherent"
        confidence = round(prob * 100, 1)

        # --- Render template with result ---
        return render_template(
            'index.html',
            prediction_text=f"The patient is likely to {adherence_status}",
            confidence=confidence
        )

    except Exception as e:
        # Handle errors gracefully
        return render_template(
            'index.html',
            prediction_text=f"Error: {e}"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
