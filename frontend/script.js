document.getElementById("predictionForm").addEventListener("submit", function(e) {
    e.preventDefault();

    // 1. Get values from the form
    // Note: Ensure your HTML IDs match these (e.g., id="Age")
    const age = document.getElementById("Age").value;
    const attendance = document.getElementById("AttendanceRate").value;
    const studyHours = document.getElementById("StudyHoursPerWeek").value;
    const gpa = document.getElementById("PreviousGPA").value;

    // 2. Validation
    if (!age || !gpa || !attendance || !studyHours) {
        alert("⚠️ Please fill all fields");
        return;
    }

    if (gpa < 0 || gpa > 10) {
        alert("⚠️ GPA must be between 0 and 10");
        return;
    }

    // 3. Prepare data for the 24-feature model
    // We send the 4 user inputs and fill the rest with defaults so the model doesn't crash
    const payload = {
        "Age": Number(age),
        "AttendanceRate": Number(attendance),
        "StudyHoursPerWeek": Number(studyHours),
        "PreviousGPA": Number(gpa),
        "Gender": "Female", 
        "Ethnicity": "Asian",
        "ParentEducation": "Graduate",
        "FamilyIncome": "30-60K",
        "Major": "Computer Science",
        "YearOfStudy": "Senior",
        "Absences": 5,
        "EntranceExamScore": 80,
        "AssignmentScore": 80,
        "MidtermScore": 80,
        "ProjectScore": 80,
        "ParticipationScore": 80,
        "TutoringSessionsAttended": 2,
        "PartTimeJob": "No",
        "PartTimeHours": 0,
        "FinancialAid": "Yes",
        "OnCampusHousing": "Yes",
        "ExtracurricularActivities": "Yes",
        "LateSubmissions": 1,
        "LibraryVisits": 10,
        "OnlinePlatformLogins": 50
    };

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "⏳ Processing...";

    // 4. Send to Flask Backend
    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Clear previous classes
        resultDiv.className = "result"; 

        // Match the key "Prediction" from your app.py
        const prediction = data.Prediction; 
        
        // Update styling based on result
        if (prediction === "Excellent" || prediction === "Yes") {
            resultDiv.classList.add("excellent");
        } else if (prediction === "Average") {
            resultDiv.classList.add("average");
        } else {
            resultDiv.classList.add("poor");
        }

        resultDiv.innerHTML = `📊 Prediction: <b>${prediction}</b> <br> <small>Accuracy: ${data.accuracy}%</small>`;
    })
    .catch(error => {
        resultDiv.innerHTML = "❌ Error connecting to server";
        resultDiv.className = "result poor";
        console.error(error);
    });
});