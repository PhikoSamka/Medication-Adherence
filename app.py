from flask import Flask, request, render_template
import pickle

# Load the pickled model and DictVectorizer
with open('models/adherence_model-v1.0.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input data from form
        age = int(request.form['age'])
        gender = 1 if request.form['gender'] == 'Male' else 0
        prescription_period = int(request.form['prescription_period'])
        diabetes = 1 if request.form.get('diabetes') else 0
        alcoholism = 1 if request.form.get('alcoholism') else 0
        hypertension = 1 if request.form.get('hypertension') else 0
        smokes = 1 if request.form.get('smokes') else 0
        tuberculosis = 1 if request.form.get('tuberculosis') else 0

        # Create dictionary input
        input_dict = {
            "age": age,
            "gender": gender,
            "prescription_period": prescription_period,
            "diabetes": diabetes,
            "alcoholism": alcoholism,
            "hypertension": hypertension,
            "smokes": smokes,
            "tuberculosis": tuberculosis,
        }

        # Vectorize input
        input_data = dv.transform([input_dict])

        # Predict adherence
        prediction = model.predict_proba(input_data)[0, 1]  # Probability for class 1 (Adherent)

        # Format response
        adherence = "adhere" if prediction >= 0.69 else "be non-adherent"
        return render_template(
            'index.html',
            prediction_text=f"The patient is likey to {adherence}"
        )

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)


