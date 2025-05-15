import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("user_choices.csv")

le_budget = LabelEncoder().fit(df['budget_type'])
le_vacation = LabelEncoder().fit(df['vacation_type'])
le_mode = LabelEncoder().fit(df['travel_mode'])
le_destination = LabelEncoder().fit(df['destination_chosen'])

X = pd.DataFrame({
    'budget_enc': le_budget.transform(df['budget_type']),
    'vacation_enc': le_vacation.transform(df['vacation_type']),
    'mode_enc': le_mode.transform(df['travel_mode'])})

y = le_destination.transform(df['destination_chosen'])

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=42, stratify=df["destination_chosen"], shuffle=True,)

knn = KNeighborsClassifier(n_neighbors=100)
knn.fit(X_train, y_train)

print(classification_report(y_test,knn.predict(X_test),target_names=le_destination.classes_))

joblib.dump(knn, "knn_dest_model.pkl")
joblib.dump(le_budget, "le_budget.pkl")
joblib.dump(le_vacation, "le_vacation.pkl")
joblib.dump(le_mode, "le_mode.pkl")
joblib.dump(le_destination, "le_destination.pkl")
print("Saved: knn_dest_model.pkl, le_budget.pkl, le_vacation.pkl, le_mode.pkl, le_destination.pkl")
