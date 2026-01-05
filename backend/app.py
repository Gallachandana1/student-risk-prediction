from unittest import result
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load model and encoders
model = pickle.load(open("model/student_model.pkl", "rb"))
feature_encoders = pickle.load(open("model/feature_encoders.pkl", "rb"))
target_encoder = pickle.load(open("model/target_encoder.pkl", "rb"))

feature_columns = [
    "Age", "Gender", "Ethnicity", "ParentEducation", "FamilyIncome",
    "Major", "YearOfStudy", "PreviousGPA", "EntranceExamScore",
    "AttendanceRate", "Absences", "StudyHoursPerWeek",
    "AssignmentScore", "MidtermScore", "ProjectScore",
    "ParticipationScore", "TutoringSessionsAttended",
    "PartTimeJob", "FinancialAid", "OnCampusHousing",
    "LateSubmissions", "LibraryVisits", "OnlinePlatformLogins"
]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])

        # ✅ SAFE ENCODING (handles unseen labels)
        for col, encoder in feature_encoders.items():
            df[col] = df[col].astype(str)
            df[col] = df[col].apply(
                lambda x: x if x in encoder.classes_ else encoder.classes_[0]
            )
            df[col] = encoder.transform(df[col])

        # Ensure correct column order
        df = df[feature_columns]
        prob = model.predict_proba(df)[0]
        risk_percent = round(prob[1]*100,2)

        return jsonify({
            "predicton": result,
            "risk_percentage": risk_percent
        })
    
        prediction = model.predict(df)
        result = target_encoder.inverse_transform(prediction)[0]

        return jsonify({"prediction": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
