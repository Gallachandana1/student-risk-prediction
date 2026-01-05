import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "PreviousGPA": 3.2,
    "AttendanceRate": 88,
    "StudyHoursPerWeek": 12,
    "AssignmentScore": 80,
    "MidtermScore": 75,
    "ProjectScore": 85,
    "ParticipationScore": 90,
    "Absences": 2,
    "LateSubmissions": 1,
    "LibraryVisits": 15,
    "OnlinePlatformLogins": 40,
    "Gender": "Male",
    "FamilyIncome": "Medium",
    "ParentEducation": "Graduate",
    "PartTimeJob": "No"
}

response = requests.post(url, json=data)
print(response.json())
