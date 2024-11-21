import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load the trained model
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

# Initialize the standard scaler
standard_to = StandardScaler()

# Title of the application
st.title("CarCadabra")

# Sidebar inputs
st.sidebar.header("User Input Parameters")

def user_input_features():
    Year = st.sidebar.number_input('Year of Buying the Car', 1990, 2024, step=1, key='year')
    Present_Price = st.sidebar.number_input('What was the Cost Price of the Car? (In lakhs)', min_value=0.0, key='present_price')
    Kms_Driven = st.sidebar.number_input('How Many Kilometers Driven?', min_value=0.0, key='kms_driven')
    Owner = st.sidebar.selectbox('How many owners previously had the car?', [0, 1, 2, 3], key='owner')
    Fuel_Type = st.sidebar.selectbox('What is the Fuel Type?', ['Petrol', 'Diesel', 'CNG'], key='fuel_type')
    Seller_Type = st.sidebar.selectbox('Are you a Dealer or Individual?', ['Dealer', 'Individual'], key='seller_type')
    Transmission = st.sidebar.selectbox('Transmission Type', ['Manual', 'Automatic'], key='transmission')

    return {
        'Year': Year,
        'Present_Price': Present_Price,
        'Kms_Driven': Kms_Driven,
        'Owner': Owner,
        'Fuel_Type': Fuel_Type,
        'Seller_Type': Seller_Type,
        'Transmission': Transmission
    }

input_data = user_input_features()

# Preprocess inputs
Year = 2024 - input_data['Year']
Present_Price = input_data['Present_Price']
Kms_Driven = np.log(input_data['Kms_Driven'] + 1)  # To avoid log(0)
Owner = input_data['Owner']

Fuel_Type_Petrol = 1 if input_data['Fuel_Type'] == 'Petrol' else 0
Fuel_Type_Diesel = 1 if input_data['Fuel_Type'] == 'Diesel' else 0

Seller_Type_Individual = 1 if input_data['Seller_Type'] == 'Individual' else 0
Transmission_Mannual = 1 if input_data['Transmission'] == 'Manual' else 0

# Prediction
prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
output = round(prediction[0], 2)

# Display the prediction
if output < 0:
    st.error("Sorry, you cannot sell this car")
else:
    st.success(f"You can sell the car at {output} lakhs")
