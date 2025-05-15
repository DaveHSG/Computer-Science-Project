# NexTrip: A personalized getaway destination app 

## _Overview_

- [Objectives](#objectives)
- [Features](#features)
- [Limitations](#limitations)
- [Disclosures](#disclosures)

## _Objectives_

Our website answer the need for spontaneous trip destination ideas. 
It provides a selection of different destination based on the following criteria:

- Vacation style
- Budget preference (taken into account for the machine learnin algorithm)
- Travel constrains (distance and travelin duration, as well as weather for the recommended cities)
- Previous travel patterns, using Machine Learning

## _Features_

Our website includes the following:
### 1. **Data Sources and APIs**

- Wikipedia API: Retrieves a brief description and image of suggested cities.
- Open-Meteo API: Provides current temperature for each destination.
- Google Maps Directions API**: Calculates train times in real time.
- Nominatim (Geopy): Geocodes user-entered city names into coordinates.

### 2. **Machine learning**

The pre-trained K-Nearest Neighbors (KNN) model predicts ideal destinations based on :

- Budget type
- Type of holydays (deduced from quiz answers)
- Preferred means of transport

  ###  Core functions

#### `wikipedia_description(city)`
- Retrieves a summary and image of the city, using Wikipedia's API.
- Results are cached for 24 hours, to avoid crashes.

#### `get_temperature_from_meteo(lat, lon)`
- Queries the Open-Meteo API to obtain current weather conditions for the suggested destination coordinates.
- Lightweight, cached for 36 seconds, to avoid crashes.

#### `haversine(lat1, lon1, lat2, lon2)`
- Implements Haversine's formula for calculating geographic distance (used in filtering destinations for the users selecting plane as a means of travel).

#### `get_train_travel_time_seconds(origin, destination)`
- Uses the Google Maps Directions API to calculate train travel time in seconds.
- The API takes into account transit stops marked as “TRAIN”.

#### `geocode_city(city)`
- Converts the name of input city into geographic coordinates using Nominatim.

#### `machine_learning()`
- Loads the pre-trained model and associated label encoders:
  - Budget
  - Vacation type
  - Mode of transport
  - Destination city
 
## User experience

The application consists of three main windows:

### 1. **User information page**
- The user inputs :
  - Name
  - Budget ( multiple selection)
  - Current position (geocoded in coordinates)

### 2. **Preferences page**
- A quiz determines the user's vacation personality in 4 categories:
  
- Nature & Outdoor Adventure
  - Cultural & Historical Exploration
  - Relaxation & Wellness
  - Urban Entertainment & Nightlife

- A pie chart displays the activity breakdown.
- Users select their mode of transport (plane or train).
- Based on the selected departure coordinates, the nearest departure cities are identified automatically.

### 3. **Results page**
- City filtering logic differs according to mode of transport:

#### Plane :
- Calculates maximum distance using flight speed (~600 km/h) minus check-in time (2h).
- Uses Haversine formula to match destinations.

#### Train:
- Uses real-time timetables via Google Maps API.
- Includes only destinations reachable within the selected time range.


- For each corresponding city:
- Displays temperature, image and summary.
- Displays pertinent activities according to the user's vacation preferences (the number of activities is distributed proportionally to the user's preferences).
 
### Machine learning predictions

- Additional cities are recommended using KNN predictions.
- These are based on how similar users ( from whom we have generated the data) have previously rated the destinations.
- Avoids overlap with cities already displayed.
- The user can select a favorite suggestion, which is saved in a file csv file

---

## Database design

The application uses a SQLite database (.db) with the following tables:

- entities (id, name, latitude and longitude)
- activities (id, name of the activity)
- activities_city (city id, activitiy id and description)

This data is loaded into Pandas DataFrames for fast access at runtime.

## _Limitations_
- Although we explored various options, we were unable to identify any free and reliable API providing accurate real-time flight times. Consequently, air travel times are estimated on the basis of average flight speeds and adjusted for airport waiting times.
  
- The KNN recommendation model proposes destinations based on the user's past preferences. However, due to its high dimensionality (number of cities and variability of user parameters), its accuracy is limited. That said, it still offers useful inspiration based on user profiles.
  
- We didn't find an API capable of identifying nearby train stations or airports based on the user's location, so we implemented a workaround: select the nearest main departure city using geospatial distance. This design choice was made following a suggestion from ChatGPT.
  
- The application currently includes a database of 60 European cities (~34% of our initial scope). Given this constraint, the diversity of potential user personas is not fully represented, which may have an impact on the model's clustering performance.
  
- We generated user profiles in a programmatic way to feed our dataset and simulate realistic travel preferences. This approach improves aggregation reliability, but may not perfectly reflect the diversity of "the real world".

## Disclosures

- ChatGPT was used to generate the initial dataset of past user choices "useer_choices.csv" in order to save time on data collection and simulate realistic travel behaviour.
  
- City-specific activities were compiled using a combination of Wikipedia, Trivago, and ChatGPT to ensure relevance to different travel styles.
  
- Due to the large number of cities and different possibilites, we created several dozens of fictitious personas to recreate common patterns in preferences that can be observed in real life.
  
- ChatGPT also provided advice on the UI/UX structure, especially the use of multi-page navigation and interactive buttons in the Streamlit application.

- Finally, as a rule, if a certain idea required a specific tool, we used the following order of priority to understand how to implement the tool: lecture slides and assignments/ coaching sessions/ web research and tutorials/ Chat GPT. For full transparency, if ChatGPT was used to understand the implementation of a tool, the comments of the block mention it.
