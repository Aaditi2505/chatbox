# -*- coding: utf-8 -*-
"""add.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TdTpgBxneyMo4aXVZhqlvvqltnuYOXDJ
"""


import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# Set up the Streamlit page
st.set_page_config(page_title="Kamaraj College FAQ Chatbot", layout="centered")

# Load model and data (with caching)
@st.cache_resource
def load_model_and_data():
    # Load the dataset
    df = pd.read_csv("kamaraj_college_faq.csv")
    df.dropna(inplace=True)

    # Encode answers to numerical labels
    le = LabelEncoder()
    df["Answer_Label"] = le.fit_transform(df["Answer"])

    # Vectorize questions
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["Question"])
    y = df["Answer_Label"]

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X, y)

    return model, vectorizer, le

# Load model, vectorizer, and encoder
model, vectorizer, label_encoder = load_model_and_data()

# App title
st.title("🎓 Kamaraj College FAQ Chatbot")
st.markdown("Ask me anything related to **Kamaraj College of Engineering and Technology**! 🤖")

# User input
user_question = st.text_input("💬 Type your question here:")

# Button to get answer
if st.button("🔍 Get Answer"):
    if not user_question.strip():
        st.warning("⚠️ Please enter a valid question.")
    else:
        # Vectorize user input and predict answer
        user_vector = vectorizer.transform([user_question])
        predicted_label = model.predict(user_vector)[0]
        predicted_answer = label_encoder.inverse_transform([predicted_label])[0]
        
        # Display answer
        st.success(f"🟢 **Answer:** {predicted_answer}")
