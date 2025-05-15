# this block imports relevant libraries
import streamlit as st
import sqlite3
import pandas as pd
import requests
import math
import joblib
import time
import matplotlib.pyplot as plt
from pathlib import Path
from config import GOOGLE_MAPS_API_KEY
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
from collections import Counter


# The functions used throughout the code have been grouped below.

# Wikipedia Description Fetching Function 
# We use a cache results for 24 hours to reduce API calls, and make our app run smoother.
@st.cache_data(ttl=864) #the 24 hours time frame was chosen, as wikipedia pictures and captions are not often updated
def wikipedia_description(city: str):
    title = city.replace(" ", "_")
    url_wikipedia = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(url_wikipedia, headers={"Accept": "application/json"})
    data = response.json()
    if "thumbnail" in data and "source" in data["thumbnail"]:
        image_url = data["thumbnail"]["source"]
    elif "originalimage" in data and "source" in data["originalimage"]:
        image_url = data["originalimage"]["source"]
    else:
        image_url = None
    description = data.get("extract", "")
    return image_url, description

# This block loads the Machine Learning components and the pre-trained KNN model and label encoders for inputs. 
# Finally, it models once globally the algorithm to avoid repeated loading
# we used ChatGPT to ensure the correctness of the approach using joblib
def machine_learning():
    knn = joblib.load("knn_dest_model.pkl")
    le_budget = joblib.load("le_budget.pkl")
    le_vacation = joblib.load("le_vacation.pkl")
    le_mode = joblib.load("le_mode.pkl")
    le_destination = joblib.load("le_destination.pkl")
    return knn, le_budget, le_vacation, le_mode, le_destination
knn, le_budget, le_vacation, le_mode, le_destination = machine_learning()


# This block uses the Haversine Formula for Calculating Distance Between Two Coordinates
# The Haversine formula uses the radius of Earth in kilometers, and converts latitude/longitude difference to radians
# ChatGPT recommended the implementation of the haversine formula, to get the distance between to points on the planet.
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    d_lat = radians(lat2 - lat1) 
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c 

# This part gets real-time temperature using the open meteo API (cached briefly for a smoother user experience)
@st.cache_data(ttl=36) #the function is cached in a short period of time, to ensure an updated weather
def get_temperature_from_meteo(lat, lon):
    url_meteo = "https://api.open-meteo.com/v1/forecast"
    params = {}
    params['latitude'] = lat
    params['longitude'] = lon
    params['current_weather'] = True
    r = requests.get(url_meteo, params=params)
    data = r.json()
    temperature = data["current_weather"]["temperature"]
    return f"{temperature}\u00b0C"

# This part gets travel time using Google Maps Directions API (only for train)
def get_train_travel_time_seconds(origin_city, destination_city):
    url_maps = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {}
    params['origin'] = origin_city
    params['destination'] = destination_city
    params['mode'] = 'transit'
    params['transit_mode'] = 'train'
    params['departure_time'] = int(time.time())
    params['key'] = GOOGLE_MAPS_API_KEY
    resp = requests.get(url_maps, params=params)
    data = resp.json()
    routes = data.get('routes')
    if not routes or not routes[0].get('legs'):
        return None
 # This block sums up the total duration of the travel, including transits       
    total_secs = 0
    for leg in routes[0]['legs']:
        for step in leg.get('steps', []):
            if step.get('travel_mode') == 'TRANSIT':
                total_secs += step['duration']['value']
    return total_secs
    
# The geocoder is used to determine the latiture and longitude of the users'location inputs
# this approach was recommended with ChatGPT
def geocode_city(city):
    geolocator = Nominatim(user_agent="vacation_type_app")
    return geolocator.geocode(city)

def closest_city(lat, lon):
    distances = cities_df.apply(
        lambda row: haversine(lat, lon, row["latitude"], row["longitude"]),
        axis=1
    )
    return cities_df.loc[distances.idxmin(), "name"]

# the below line represents the name and the logo, shown as a window on the users' browsers
st.set_page_config(page_title="NexTrip", page_icon="logo.jpg")
# The following block is calling our database to fetch the data from cities (activities, location, name)
DB_FILE = Path("database.db")
DB = sqlite3.connect(DB_FILE)
cities_df = pd.read_sql("SELECT id, name, latitude, longitude FROM cities;", DB)
acts_df = pd.read_sql("SELECT id, name FROM activities;", DB)
ca_df = pd.read_sql("SELECT city_id, activity_id, description FROM city_activities;", DB)
city_names = cities_df["name"]
activity_names = acts_df["name"]

# The following parts represent the visible layout for the user (logo, inputs: name, budget type, current location) 
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=700) 
if "page" not in st.session_state:
    st.session_state.page = "user_info"
# this is the navigation function
def goto(page_name):
    st.session_state.page = page_name
if st.session_state.page == "user_info":
    st.title("Welcome to NexTrip")
    st.write("_Define your preferred criteria and find the perfect destination!_")
# explanation of our business case (on a sidebar)
    st.sidebar.markdown(""" 
    Planning a weekend trip can be daunting and time-consuming. 
    With countless destinations, transportation options and personal preferences, finding the PERFECT travel spot is often stressful and time-consuming.
    
    ---
    
    How NexTrip helps you?
    We are happy to help you plan your trip by suggesting THE BEST weekend destinations in Europe, tailored to your needs.
    
    NexTrip suggests travel destinations to suit your :  
    - Vacation preferences 
    - Preferred mode of transportation  
    - Current location
    
    *Our app combines real-time data, past travel experiences paired with machine learning, to give you personalized travel suggestions that match your style.*
    ---
    """)

    st.subheader("What's your name?")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("", placeholder="Enter your name")
        st.session_state.name = name
        
    st.subheader("What budget do you have?")
    budget_types = st.multiselect("", options=["Cheap", "Medium", "Expensive"])
    st.session_state.budget_types = budget_types
    
    st.subheader("Where are you currently located?")
    user_location = st.text_input("", placeholder="Enter your current city")
    if user_location:
        geo_result = geocode_city(user_location)
        if geo_result:
            st.session_state.user_lat = geo_result.latitude
            st.session_state.user_lon = geo_result.longitude
            st.session_state.user_city = user_location
            st.success(f"Location set to: {user_location} ({geo_result.latitude:.2f}, {geo_result.longitude:.2f})")
        else:
            st.error("Could not determine your location. Please check your spelling.")
  
# this function enables to navigate from the first page (the string enables to create spacing)
    st.write("") 
    if st.button("Go to Preferences →"):
        goto("preferences")

# preferences page which helps to determine the vacation type
elif st.session_state.page == "preferences":
    st.title("Vacation Type")
    st.write(f"_{st.session_state.name}, answer the following questions to help us determine your ideal vacation style._")

    vacation_categories = {
        "Nature & Outdoor Adventure": [
            "Why relax when you can fall off a cliff? I enjoy extreme sports like hiking, rafting, or rock climbing",
            "Luxury is overrated: give me a tent and a fire pit. I don’t mind basic or rustic accommodations",
        ],
        "Cultural & Historical Exploration": [
            "Learning about local history and culture is important to me",
            "Museums are my nightclubs. I get a thrill from visiting museums and cultural sites",
        ],
        "Relaxation & Wellness": [
            "Work hard, spa harder. I take wellness and self-care very seriously, even while traveling",
            "A vacation without a beach is like a margarita without tequila",
        ],
        "Urban Entertainment & Nightlife": [
            "I didn’t come all this way to sleep at 9. I love cities with buzzing nightlife",
            "The real culture is in the shopping bags. I experience new cities best through their shops and markets.​",
        ]}
    
    #this block analyses the vacation type, with a slider from 0 to 4
    vacation_scores = {}
    
    st.caption("**Scale**: 0 = Highly Disagree, 4 = Highly Agree")
    
    for category, questions in vacation_categories.items():
        st.subheader(category)
        score = 0
        for i, question in enumerate(questions, start=1):
            response = st.slider(question, 0, 4, value=2, key=f"{category}_{i}")
            score += response
        vacation_scores[category] = score
        
    scores = pd.Series(vacation_scores)

# we find the preferred category and the vacation percentage
    vacation_percentages = ((scores / scores.sum()) * 100)
    st.session_state.vacation_percentages = vacation_percentages
    preferred_category = max(vacation_scores, key=vacation_scores.get)
    st.session_state.vacation_type = preferred_category

# we plot the percentages as a pie chart (to visualize the data), as the user will get an easy overview of his vacation preferences 
    labels = vacation_percentages.index.tolist()
    sizes = vacation_percentages.values.tolist()
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    ax.set_title("Your Vacation Type Profile")
    ax.axis("equal") 
    st.pyplot(fig)

# we determine and save the means of transport the users want to use
    travel_mode = st.selectbox("_Select your preferred mode of transportation:_", ["Plane", "Train"])
    st.session_state.travel_mode = travel_mode
    
# logic for airplane mode: we determine the nearest city of the database, define the user's maximum acceptable flight time
    if travel_mode == "Plane":
        if "user_lat" in st.session_state and "user_lon" in st.session_state:
            user_lat = st.session_state.user_lat
            user_lon = st.session_state.user_lon
            origin = closest_city(user_lat, user_lon)
            st.write(f"Based on your current location, your departure city is: **{origin}**")
# lets the user select his departure city manually, if it couldn't be fetched previously      
        else:
            origin = st.selectbox("Departure city:", city_names)
# this stores both origin and time constraints in session for downstream processing   
        duration = st.slider("Max flight time (h):", min_value=2.5, max_value=10.0, value=5.0, step=0.5)
        st.write("_Your travel time must exceed 2 hours to account for check-in time._")
        st.session_state.plane_inputs = (origin, duration)
# (we use the same functions as above)
    else:
        if "user_lat" in st.session_state and "user_lon" in st.session_state:
            user_lat = st.session_state.user_lat
            user_lon = st.session_state.user_lon
            origin = closest_city(user_lat, user_lon)
            st.write(f"_Based on your current location, your departure city is: **{origin}**_")
            
        else:
            origin = st.selectbox("Departure city:", city_names)
    
        duration = st.slider("Max train time (h):", 1, 12)
        st.session_state.train_inputs = (origin, duration)

# This navigation button enables to move to the third (results) page
    st.write("") 
    if st.button("← Back to User Info"):
        goto("user_info")
    st.write("")  
    if st.button("Go to Results →"):
        st.session_state.show_recommendations = True
        goto("results")
# The below is the third page: results  
# This part retrieves the vacation preference breakdown (percentages) stored earlier, and retrieve the chosen travel mode
elif st.session_state.page == "results":
    vacation_percentages = st.session_state.vacation_percentages
    if st.session_state.travel_mode == "Plane":
        origin, dur = st.session_state.plane_inputs
    else:
        origin, dur = st.session_state.train_inputs

# this is the allocation block of activity slots for the vacation type of the user
    row = cities_df.loc[cities_df["name"] == origin, ["latitude", "longitude"]]
    if row.empty:
        st.write("Origin not found.")
        st.stop()
    lat1, lon1 = row.iloc[0]
    TOTAL = 8
    ideal = {cat: pct/100 * TOTAL for cat, pct in vacation_percentages.items()}
    alloc = {cat: math.floor(v) for cat, v in ideal.items()}
    rem = {cat: ideal[cat] - alloc[cat] for cat in alloc}
    leftover = TOTAL - sum(alloc.values())
# The below function distributes remaining slots based on highest leftover decimal values. This approach was recommended by ChatGPT.
    for cat, _ in sorted(rem.items(), key=lambda x: x[1], reverse=True)[:leftover]:
        alloc[cat] += 1

    st.header("Your criteria-based recommendations:")
    st.write("_Each city recommends a certain number of activities based on your personalized activity profile._")
            
    city_matches = []
# The following block uses the geolocation to determine the transporation time (by plane), with a 2h buffer for check-in (at an average speed of 600km/h) 
    if st.session_state.travel_mode == "Plane":
        effective = dur - 2
        max_distance = effective * 600
        def travel_time(d): return d / 600 + 2

        for _, city_row in cities_df[cities_df["name"] != origin].iterrows():
            city_id, city_name, lat2, lon2 = city_row["id"], city_row["name"], city_row["latitude"], city_row["longitude"]
            
            d = haversine(lat1, lon1, lat2, lon2)
            if d <= max_distance:
                t_h = travel_time(d)
                hours = int(t_h)
                mins = int((t_h - hours) * 60)
                tneed = f"{hours}h{mins}m"
                city_matches.append((city_id, city_name, lat2, lon2, tneed))
# The following block uses the geolocation to determine the transporation time (by train), using the googlemaps API.
    else:  
        max_hours = dur
        for _, city_row in cities_df[cities_df["name"] != origin].iterrows():
            city_id = city_row["id"]
            city_name = city_row["name"]
            lat2, lon2 = city_row["latitude"], city_row["longitude"]

 # this function uses Google Maps API to get real travel time by train
            origin_coordinates = f"{lat1},{lon1}"
            destination_coordinates = f"{lat2},{lon2}"
            sec = get_train_travel_time_seconds(origin_coordinates, destination_coordinates)
            if sec is None:
                continue
            if (sec / 3600) > max_hours:
                continue

# the following blocl makes the formatting of time in hours and minutes
            duration_hours = sec / 3600
            hours = int(duration_hours)
            minutes = int((duration_hours - hours) * 60)
            tneed = f"{hours}h{minutes}m"
    
            city_matches.append((city_id, city_name, lat2, lon2, tneed))
    
# This displays the matching cities (with current meteo, image and summmary retrieved from above), with activites tailored to users' vacation type.
    for city_id, city_name, lat2, lon2, tneed in city_matches:
        temperature = get_temperature_from_meteo(lat2, lon2)
        image, description = wikipedia_description(city_name)
        st.subheader(f"{city_name} — {tneed} — {temperature}")
        
        if image:
            st.image(image, width=400)  
        if description:
            st.write(description)
# this shows N recommendations based on the vacation type percentages of the user 
# example: the more a user likes a certain type of activity, the more recommendations he will get for the prefered activity
        for cat in vacation_percentages.index:
            n = alloc[cat]
            if n <= 0:
                continue
            act_id = acts_df.loc[acts_df["name"] == cat, "id"].item()
            mask = (ca_df["city_id"] == city_id) & (ca_df["activity_id"] == act_id)
            descs = ca_df.loc[mask, "description"].tolist()
            if not descs:
                continue

            st.markdown(f"**{cat}**")
            for d in descs[:n]:
                st.write(f"- {d}")

        st.markdown("---")
        
# This text introduces the machine learning-based suggestions
    if st.session_state.get("show_recommendations", False):
        st.title(f"{st.session_state.name}, if you don’t mind traveling a bit further... ")
        st.write("_Other users with the same preferences absolutely loved these places_")

# this block uses a trained KNN model to recommend destinations by encoding the user's preferences and retrieving the top 3 matching destinations per budget type.
        suggestions = []
        for budget in st.session_state.budget_types:
            feat = pd.DataFrame([{
                "budget_enc": le_budget.transform([budget])[0],
                "vacation_enc": le_vacation.transform([st.session_state.vacation_type])[0],
                "mode_enc": le_mode.transform([st.session_state.travel_mode])[0]}])
# the following function gets top 3 destination predictions from KNN model, using probabilities if available.
# approach recommended by ChatGPT
            if hasattr(knn, "predict_proba"):
                probs = knn.predict_proba(feat)[0]
                idxs = probs.argsort()[-3:][::-1]
            else:
                idxs = knn.kneighbors(feat, n_neighbors=3, return_distance=False)[0]
            suggestions.extend(le_destination.inverse_transform(idxs))

        frequency = Counter(suggestions)
        ml_recommendations = [city for city,_ in frequency.most_common(5)]

# The following function collects the city names, filters out the cities that already appeared and displays the ML recommended cities.
# approach recommended by ChatGPT (only for the append function, asking AI how to add cities for the user matches)       
        basic_cities = []
        for city_id, city_name, lat2, lon2, tneed in city_matches:
            basic_cities.append(city_name)
        
        filtered_ml = []
        for rec in ml_recommendations:
            if rec not in basic_cities:
                filtered_ml.append(rec)
        ml_recommendations = filtered_ml
        combined = basic_cities + ml_recommendations

        for city in ml_recommendations:
            st.subheader(city)
            image, description = wikipedia_description(city)
            if image:
                st.image(image, width=400)  
            if description:
                st.write(description)
            st.markdown("---")
        
        basic_cities = [city_name for (_, city_name, _, _, _) in city_matches]
        combined = basic_cities + [city for city in ml_recommendations if city not in basic_cities]
        chosen = st.radio("_Which appeals to you most?_",combined)

# this section saves the final user choice to CSV file
# we asked ChatGPT how to collect user choices into the CSV file (to get more data for our algorithm)
        if st.button("Save my preferences"):
            new = {
                "budget_type": ",".join(st.session_state.budget_types),
                "vacation_type": st.session_state.vacation_type,
                "travel_mode": st.session_state.travel_mode,
                "destination_chosen": chosen}
            pd.DataFrame([new]).to_csv(
                "user_choices.csv",
                mode="a",
                header=False,
                index=False)
            st.success(f"_We saved your preferences!_")

# the navigation buttons enables to go back to the second page, or to start the process over again
        st.write("")  
        if st.button("← Back to Preferences"):
            goto("preferences")
        st.write("")  
        if st.button("Start Over"):
            goto("user_info")
