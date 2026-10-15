import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

# Small demonstration dataset: 0 = Fail, 1 = Pass.
data = {
    "study_hours": [1,2,2,3,3,4,4,5,5,6,1,2,3,4,6,7,8,8,9,10],
    "attendance": [30,40,50,45,60,55,70,65,75,80,20,35,40,50,85,90,80,95,90,100],
    "internal_marks": [10,15,20,18,25,22,30,28,35,38,5,12,15,20,35,40,38,45,42,48],
    "result": [0,0,0,0,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1]
}

df = pd.DataFrame(data)
X = df[["study_hours", "attendance", "internal_marks"]]
y = df["result"]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)
joblib.dump(model, "student_model.joblib")
print("Model trained and saved as student_model.joblib")
