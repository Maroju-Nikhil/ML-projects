import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
nltk.download('punkt')
nltk.download('stopwords')

def transform_text(text):
  text = text.lower()
  text = nltk.word_tokenize(text)
  modified = []
  for i in text:
    if i.isalnum():
      modified.append(i)

  text = modified[:]
  modified.clear()
  
  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      modified.append(i)

  text = modified[:]
  modified.clear()
  
  for i in text:
    modified.append(ps.stem(i))

  return " ".join(modified)


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title('Email/SMS Spam Classifier')
input_text = st.text_input("Enter Message:")

if st.button("Predict"):
  if input_text:
    # 1. preprocess
    transformed_text = transform_text(input_text)

    # 2. vectorize
    vector_input = tfidf.transform([transformed_text])

    # 3. predict
    result = model.predict(vector_input)[0]

    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")

