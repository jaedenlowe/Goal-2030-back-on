import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model

# Load the PyCaret model (make sure to replace 'model_name' with your actual model name)
model1 = load_model('model_y1_tradkeeper')
model2 = load_model('model_y2_sweeperkeeper')
model3 = load_model('model_y3_ballplayingdefender')
model4 = load_model('model_y4_nononsensedefender')
model5 = load_model('model_y5_fullback')
model6 = load_model('model_y6_allactionmidfielder')
model7 = load_model('model_y7_midfieldplaymaker')
model8 = load_model('model_y8_traditionalwinger')
model9 = load_model('model_y9_invertedwinger')
model10 = load_model('model_y10_goalpoacher')
model11 = load_model('model_y11_targetman')

model_map = {
    'target1': model1,
    'target2': model2,
    'target3': model3,
    'target4': model4,
    'target5': model5,
    'target6': model6,
    'target7': model7,
    'target8': model8,
    'target9': model9,
    'target10': model10,
    'target11': model11,
}

# Streamlit app
st.title("Player Attribute Prediction")

# File uploader widget
uploaded_file = st.file_uploader("Upload a CSV file with player attributes", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("Uploaded DataFrame:")
    st.write(df.head())
    
    # Make predictions
    predictions = predict_model(model, data=df)
    
    # Display predictions
    st.write("Predictions:")
    st.write(predictions)
    
    # Optionally, you can display just the prediction column
    st.write("Predicted Labels:")
    st.write(predictions['Label'])