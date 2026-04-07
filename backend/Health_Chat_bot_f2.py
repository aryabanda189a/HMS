import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
import csv

# -----------------------------
# Load datasets (UNCHANGED)
# -----------------------------
training = pd.read_csv('Training.csv')
testing  = pd.read_csv('Testing.csv')

cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

# Encode labels
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

# Train model
clf = DecisionTreeClassifier()
clf.fit(x, y)

# Reduced data
reduced_data = training.groupby(training['prognosis']).max()

# -----------------------------------------
# SESSION STORAGE FOR TREE TRAVERSAL
# -----------------------------------------
tree_state = {
    "node": 0,
    "symptoms_present": []
}

# -----------------------------------------
# Utility Functions (UNCHANGED)
# -----------------------------------------
def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return disease


# -----------------------------------------
# Start Conversation
# -----------------------------------------
def start_chat():
    tree_state["node"] = 0
    tree_state["symptoms_present"] = []
    return ask_next_question()


# -----------------------------------------
# Continue Tree Based on User Answer
# -----------------------------------------
def answer_question(user_answer):
    tree_ = clf.tree_
    node = tree_state["node"]

    feature = tree_.feature[node]
    threshold = tree_.threshold[node]

    if feature != _tree.TREE_UNDEFINED:
        if user_answer.lower() == "yes":
            val = 1
        else:
            val = 0

        if val <= threshold:
            tree_state["node"] = tree_.children_left[node]
        else:
            symptom_name = cols[feature]
            tree_state["symptoms_present"].append(symptom_name)
            tree_state["node"] = tree_.children_right[node]

        return ask_next_question()
    else:
        return get_result()


# -----------------------------------------
# Ask Next Question
# -----------------------------------------
def ask_next_question():
    tree_ = clf.tree_
    node = tree_state["node"]

    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        symptom = cols[tree_.feature[node]]
        return {
            "type": "question",
            "question": f"Do you have {symptom.replace('_',' ')} ?"
        }
    else:
        return get_result()


# -----------------------------------------
# Final Result
# -----------------------------------------
def get_result():
    tree_ = clf.tree_
    node = tree_state["node"]

    present_disease = print_disease(tree_.value[node])
    disease = present_disease[0]

    red_cols = reduced_data.columns
    symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]

    # Doctor consultation risk
    consult = {}
    with open('doc_consult.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            consult[row[0]] = int(row[1])

    consult_msg = "You may consult a doctor"
    if disease in consult and consult[disease] > 50:
        consult_msg = "You should consult a doctor as soon as possible"

    return {
        "type": "result",
        "disease": disease,
        "symptoms_present": tree_state["symptoms_present"],
        "other_symptoms": list(symptoms_given),
        "advice": consult_msg
    }
