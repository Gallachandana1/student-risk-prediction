import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_csv("student_data.csv")
data.columns = data.columns.str.strip()

# -----------------------------
# Features & Target
# -----------------------------
feature_columns = [
    "Age", "Gender", "Ethnicity", "ParentEducation", "FamilyIncome",
    "Major", "YearOfStudy", "PreviousGPA", "EntranceExamScore",
    "AttendanceRate", "Absences", "StudyHoursPerWeek",
    "AssignmentScore", "MidtermScore", "ProjectScore",
    "ParticipationScore", "TutoringSessionsAttended",
    "PartTimeJob", "FinancialAid", "OnCampusHousing",
    "LateSubmissions", "LibraryVisits", "OnlinePlatformLogins"
]

target_column = "AtRisk"

X = data[feature_columns].copy()
y = data[target_column]

# -----------------------------
# Encode categorical columns
# -----------------------------
categorical_cols = [
    "Gender", "Ethnicity", "ParentEducation",
    "FamilyIncome", "Major", "YearOfStudy",
    "PartTimeJob", "FinancialAid", "OnCampusHousing"
]

label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# -----------------------------
# Train model
# -----------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
accuracy = accuracy_score(y_test, model.predict(X_test))

# -----------------------------
# Save model
# -----------------------------
os.makedirs("model", exist_ok=True)

pickle.dump(model, open("model/student_model.pkl", "wb"))
pickle.dump(label_encoders, open("model/feature_encoders.pkl", "wb"))
pickle.dump(target_encoder, open("model/target_encoder.pkl", "wb"))

print("✅ Model training completed")
print(f"✅ Accuracy: {accuracy * 100:.2f} %")
