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
    institute_df.insert(0, 'Sr. No.', range(1, 1 + len(institute_df)))  # Add serial number column
    st.table(institute_df.set_index('Sr. No.'))

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
        st.write("Welcome to the AI Predictor for Educational Institutes using AISHE and NIRF, this is the home page. You can find project-related information here.")
        # Project Information
        st.header("Project Information")
        st.write("This project develops a predictive analytics system that forecasts the annual rankings of academic institutes across India. This predictive capability enables stakeholders to make informed decisions regarding institute selection proactively. Complementing the ranking prediction, the system incorporates a user-friendly interface allowing users to specify their preferred state and city. It then retrieves and presents the top five highest-ranked institutes within that region. By combining predictive analytics with location-based filtering, users can effortlessly identify the most suitable academic institutions aligning with their geographical preferences. Through this comprehensive solution, the project streamlines the process of evaluating and selecting institutes, contributing to the education sector's advancement. It empowers informed decision-making, promotes accessibility to quality education, and fosters an environment conducive to academic excellence.")

        # Contact Information
        st.header("Contact Information")
        st.write("1. Ishika Sharma - 45 AI&DS - 8433654540 - sishika650@gmail.com")
        st.write("2. Sarvesh Sharma - 46 AI&DS - 7248940124 - Sarvesh9075@gmail.com")
        st.write("3. Tanishq Suryawanshi - 53 AI&DS - 9769600735 - suryawanshitanishq@gmail.com")
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
