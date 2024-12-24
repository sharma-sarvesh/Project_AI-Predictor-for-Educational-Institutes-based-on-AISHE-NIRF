import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

# Load data
@st.cache_data  # Cache data for improved performance
def load_data():
    return pd.read_csv("EngineeringRanking_Final.csv").fillna(0)

data = load_data()

# Function to display city list
def display_city_list(state):
    cities = sorted(data[data['State'] == state]['City'].unique())
    return cities

# Function to display institutes by city
def display_institutes_by_city(city):
    city_data = data[data['City'] == city]
    if len(city_data) == 0:
        st.write(f"No institutes found in {city}")
        return
    st.write(f"\nInstitutes in {city} from 2016 to 2021:")
    institute_df = city_data[['Institute Name', 'Rank_16', 'Rank_17', 'Rank_18', 'Rank_19', 'Rank_20', 'Rank_21']]
    # Convert ranks to int
    institute_df[['Rank_16', 'Rank_17', 'Rank_18', 'Rank_19', 'Rank_20', 'Rank_21']] = institute_df[
        ['Rank_16', 'Rank_17', 'Rank_18', 'Rank_19', 'Rank_20', 'Rank_21']].astype(int)
    st.table(institute_df)

# Function to make predictions for Rank_24
def make_predictions():
    predictions_df = pd.read_csv("Predictions of Rank_24.csv")
    return predictions_df

# Main function to run the Streamlit app
def main():
    st.title("AI Predictor for Educational Institutes using AISHE and NIRF")

    # Sidebar options
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Institute Predictor", "Rank Predictor for 2024"])

    # Display different pages based on selection
    if page == "Home":
        st.write("Welcome to the AI Predictor for Educational Institutes using AISHE and NIRF")
        st.write("This is the home page. You can find project-related information here.")
    elif page == "Institute Predictor":
        st.header("Institute Predictor")
        states = sorted(data['State'].unique())
        state = st.selectbox("Select state", states)
        cities = display_city_list(state)
        city = st.selectbox("Select city", cities)
        display_institutes_by_city(city)
    elif page == "Rank Predictor for 2024":
        st.header("Rank Predictor for 2024")
        predictions_df = make_predictions()
        st.write(predictions_df)

if __name__ == "__main__":
    main()
