"""
Name:   Blake Babikian
Data:   UFO
add list comp**********

This program has 5 pages all have same heading and same page select in sidebar each page has a touching story
home page - displays image shows map of all sightings as well as country selector in sidebar
general data - displays charts for shape duration and country
IDK you tell me - looks at the 10 most frequent sighting datetimes you can control the date, state as well as display map
or two pie charts
4th of july - tries to answer how much of an impact the 4th has on submissions
Combined days - uses the 10 frequent names above and then combines if a date appears more than once at different times


"""
import random
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly-express as px
from PIL import Image


def get_data(filename):
    df = pd.read_csv(filename, on_bad_lines='skip', low_memory=False)
    return df.rename(columns={"longitude ": "longitude"})

def map(location_data, view_state):

    layer1 = pdk.Layer('ScatterplotLayer',
                      data = location_data[["datetime","longitude", "latitude"]],
                      get_position = ["longitude", "latitude"],
                      get_radius = 15000,
                      get_color = [57,255,20],
                      pickable = True)
    tool_tip = {"html": "Sighting Date:<br/> <b>{datetime}</b> ",
            "style": { "backgroundColor": "lime",
                        "color": "black"}}
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v8',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip= tool_tip
    )
    return st.pydeck_chart(map)

def world_map(ufo_data):
    return st.map(ufo_data[["longitude", "latitude"]])

def country_bar(top_countries):
    fig = px.bar(top_countries,color_discrete_sequence =['green']*len(top_countries),title="Most Frequent Country for Sightings", labels={'index':'Countries','value':'Frequency'})
    return st.write(fig)

def country_pie(top_countries):
    fig = px.pie(top_countries, values= list(top_countries[0:]), names = list(top_countries.keys()), color_discrete_sequence=px.colors.sequential.Greens, title = "Most Frequent Country for Sightings")
    return st.write(fig)

def popular_shapes_pie(shape_data):
    shape_data = shape_data[:10]
    fig = px.pie(shape_data, values= list(shape_data[0:]), names = list(shape_data.keys()), color_discrete_sequence=px.colors.sequential.Greens, title = "Most Frequent Shapes of Sightings")
    return st.write(fig)

def popular_duration_pie(duration_data):
    duration_data = duration_data[:10]
    fig = px.pie(duration_data, values= list(duration_data[0:]), names = list(duration_data.keys()), color_discrete_sequence=px.colors.sequential.Greens)
    return st.write(fig)

def random_story(ufo_data):
    number = random.randint(1,80000)
    quote = tuple((ufo_data.iloc[number, 7],ufo_data.iloc[number+10, 7]))
    return quote

def date_with_most_sighting(ufo_data):
    data = ufo_data["datetime"].value_counts()
    return data[:10]

def date_of_interest_data(date_of_interst, ufo_data):
    data = ufo_data[ufo_data['datetime'] == date_of_interst]
    return data

def same_location_as_well(dates):
    data = dates['state'].value_counts()
    return data[:5]

def loaction_of_interest_data(location_of_interest,dates):
    data = dates[dates['state']==location_of_interest]
    return data

def states_location_map(states_location):
    view_state = pdk.ViewState(
        latitude=states_location["latitude"].mean(),
        longitude=states_location["longitude"].mean(),
        zoom = 6,
        pitch = 30)
    layer1 = pdk.Layer('ScatterplotLayer',
                      data = states_location[["shape","longitude", "latitude"]],
                      get_position = ["longitude", "latitude"],
                      get_radius = 5000,
                      get_color = [57,255,20],
                      pickable = True)
    tool_tip = {"html": "Sighting Shape:<br/> <b>{shape}</b> ",
            "style": { "backgroundColor": "lime",
                        "color": "black"}}
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v8',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip= tool_tip
    )
    return st.pydeck_chart(map)

def day_dec_map(day_dec_coord):
    view_state = pdk.ViewState(
        latitude=day_dec_coord["latitude"].mean(),
        longitude=day_dec_coord["longitude"].mean(),
        zoom = 3,
        pitch = 20)
    layer1 = pdk.Layer('ScatterplotLayer',
                      data = day_dec_coord[["datetime","longitude", "latitude"]],
                      get_position = ["longitude", "latitude"],
                      get_radius = 10000,
                      get_color = [57,255,20],
                      pickable = True)
    tool_tip = {"html": "Sighting Date:<br/> <b>{datetime}</b> ",
            "style": { "backgroundColor": "lime",
                        "color": "black"}}
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v8',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip= tool_tip
    )
    return st.pydeck_chart(map)

def state_shape_pie(states_shape):
    fig = px.pie(states_shape, values= list(states_shape[0:]), names = list(states_shape.keys()), color_discrete_sequence=px.colors.sequential.Greens, title = "Most Frequent Shapes of Sightings")
    return st.write(fig)

def state_duration_pie(states_duration):
    fig = px.pie(states_duration, values= list(states_duration[0:]), names = list(states_duration.keys()), color_discrete_sequence=px.colors.sequential.Greens, title = "Most Frequent Duration of Sightings (in Seconds)")
    return st.write(fig)

ufo_data = get_data("scrubbed.csv") # back-end set variable
st.set_option('deprecation.showPyplotGlobalUse', False) # back-end fix data
location_data = ufo_data[["datetime","longitude","latitude"]] # back-end set variable

st.sidebar.title('Inputs:') # Front-end sidebar title
pages = ("Home", "Map","General Data", "IDK you tell me", "Combined Days", "July Fourth") # Page options
page_select = st.sidebar.selectbox("Page Select:",pages) # Page selector

if page_select == "Home": # back-end if statement, loads home page
    st.title("UFO Sightings: a Python Project") # front-end home page title
    img = Image.open("ufo.jpg")
    st.image(img)
    st.caption("Blake Babikian - Bentley University - CS 230") # front-end home page caption
    st.text(f"With {len(ufo_data)} entries, not only is there data, it's overwhelming! I hope this program\n can convert everyone into UFO believers!")
    st.write("\n \n") # front-end spacing
    st.subheader("A Touching Story:") # front-end story heading
    quote = random_story(ufo_data)
    st.markdown(f"One story reads '{quote[0]}' another, '{quote[1]}' Wicked!.") # front-end call and display random story
elif page_select == "Map":
    st.title("UFO Sightings: a Python Project") # front-end home page title
    st.caption("Blake Babikian - Bentley University - CS 230") # front-end home page caption
    st.sidebar.header("Map:") # front-end sidebar map heading
    countries = ("US","Canada","Australia","Europe","World") # back-end set variable
    selected = st.sidebar.radio('Country for sightings:', countries) # front-end sidebar country selector
    if selected == "US": # back-end if country selector was US
        view_state = pdk.ViewState( # back-end set map
            latitude = 37.0902,
            longitude = -95.7129,
            zoom = 3,
            pitch = 40)
    elif selected == "Canada": # back-end if country selector was Canada
        view_state = pdk.ViewState( # back-end set map
            latitude= 56.1304,
            longitude= -106.3468,
            zoom = 2,
            pitch = 0)
    elif selected == "Australia": # back-end if country selector was Australia
        view_state = pdk.ViewState( # back-end set map
            latitude = -25.2744,
            longitude = 133.7751,
            zoom = 3,
            pitch = 40)
    elif selected == "Europe": # back-end if country selector was Europe
        view_state = pdk.ViewState( # back-end set map
            latitude = 54.5260,
            longitude = 15.2551,
            zoom = 2,
            pitch = 40)
    else:  # back-end if country selector was World
        view_state = pdk.ViewState( # back-end set map
            latitude = 0,
            longitude = 0,
            zoom = 0,
            pitch = 0)
    st.header("Map of Sightings:") # front-end map heading
    map(location_data,view_state) # front-end call and display map
elif page_select == "General Data": # back-end if statement, loads general data page
    st.title("UFO Sightings: a Python Project") # front-end general data page title
    st.caption("Blake Babikian - Bentley University - CS 230") # front-end general data page caption
    st.write("\n \n") # front-end spacing
    st.header("Chart Statistics:") # front-end chart stats heading
    choices = ["Bar","Pie"] # back-end set variables
    st.sidebar.header("Chart:") # front-end sidebar chart stats heading 
    bar_or_pie = st.sidebar.radio('What type of graph would you like?', choices) # front-end sidebar graph type check box
    top_countries = ufo_data["country"].value_counts() # back-end set variable
    st.subheader(f"A {bar_or_pie} chart for countries with most sightings:") # front-end chart sub heading
    if bar_or_pie == "Bar": # back-end if bar chart enter
        country_bar(top_countries) # front-end
    else: # back-end if pie enter
        country_pie(top_countries) # front-end
    shape_data = ufo_data["shape"].value_counts() # back-end set variable
    st.subheader("Pie Chart of Top 15 Sighting Shapes:") # front-end chart heading
    popular_shapes_pie(shape_data) # front-end call and siplay shape pie chart
    duration_data = ufo_data["duration (seconds)"].value_counts() # back-end set variable
    st.subheader("Pie Chart of Top 15 Durations in Seconds:") # front-end chart heading
    popular_duration_pie(duration_data) # front-end call and siplay shape pie chart
elif page_select == "IDK you tell me": # back-end if statement, loads idk page
    st.title("UFO Sightings: a Python Project") # front-end general data page title
    st.caption("Blake Babikian - Bentley University - CS 230") # front-end general data page caption
    st.write("\n \n") # front-end spacing
    pop_dates = date_with_most_sighting(ufo_data) # back-end set variabl
    st.sidebar.header("Date Time:") # front-end sidebar heading
    date_of_interest = st.sidebar.selectbox('What date would you like to explore more?', pop_dates.keys()) # front-end sidebar select date
    dates = date_of_interest_data(date_of_interest,ufo_data)  # back-end *useful* set variable
    st.subheader("Popular DateTime:") # front-end story heading
    st.write(f"There were {len(dates)} sightings at {date_of_interest} here are the States and frequencies in which the sightings occurred:")
    locations = same_location_as_well(dates) # back-end set variable
    st.table(locations) # front-end table
    st.sidebar.header("States:") # front-end sidebar heading
    locations_of_interest = st.sidebar.selectbox('What date would you like to explore more?', locations.keys()) # front-end sidebar select date
    states = loaction_of_interest_data(locations_of_interest,dates) # back-end *useful* set variable
    states_location = states[["shape","longitude","latitude"]] # back-end set variable
    states_shape = states["shape"].value_counts() # back-end set variable
    states_duration = states["duration (seconds)"].value_counts() # back-end set variable
    st.sidebar.header("Display:") # front-end sidebar heading
    map = st.sidebar.checkbox("Map", False) # front-end sidebar checkbox
    shape = st.sidebar.checkbox("Shape Data", False) # front-end sidebar checkbox
    duration = st.sidebar.checkbox("Duration Data", False) # front-end sidebar checkbox

    if map and shape and duration:
        st.subheader("Map:") # front-end sub heading
        states_location_map(states_location) # front-end call and display function
        st.subheader("Pie Chart of Top Shapes:") # front-end sub heading
        state_shape_pie(states_shape) # front-end call and display function
        st.subheader("Pie Chart of Top Duration:") # front-end sub heading
        state_duration_pie(states_duration) # front-end call and display function
    elif map and shape:
        st.subheader("Map:") # front-end sub heading
        states_location_map(states_location) # front-end call and display function
        st.subheader("Pie Chart of Top Shapes:") # front-end sub heading
        state_shape_pie(states_shape) # front-end call and display function
    elif map and duration:
        st.subheader("Map:") # front-end sub heading
        states_location_map(states_location) # front-end call and display function
        st.subheader("Pie Chart of Top Duration:") # front-end sub heading
        state_duration_pie(states_duration) # front-end call and display function
    elif shape and duration:
        st.subheader("Pie Chart of Top Shapes:") # front-end sub heading
        state_shape_pie(states_shape) # front-end call and display function
        st.subheader("Pie Chart of Top Duration:") # front-end sub heading
        state_duration_pie(states_duration) # front-end call and display function
    elif map:
        st.subheader("Map:") # front-end sub heading
        states_location_map(states_location) # front-end call and display function
    elif shape:
        st.subheader("Pie Chart of Top Shapes:") # front-end sub heading
        state_shape_pie(states_shape) # front-end call and display function
    elif duration:
        st.subheader("Pie Chart of Top Duration:") # front-end sub heading
        state_duration_pie(states_duration) # front-end call and display function
elif page_select == "Combined Days":
    st.title("UFO Sightings: a Python Project") # front-end general data page title
    st.caption("Blake Babikian - Bentley University - CS 230") # front-end general data page caption
    st.write("\n \n") # front-end spacing
    choices = ["11/16/1999","10/31/2004","9/19/2009","7/4/2010","7/4/2011","7/4/2012","7/4/2013"] # back-end set variable 
    st.sidebar.header("Map:") # front-end sidebar heading
    day_dec = st.sidebar.radio("Which High activity day do you want to map out?",choices) # front end sidebar date selector
    st.header(f"All of the Sightings on {day_dec}:") # front-end map heading
    if day_dec == "11/16/1999": # back-end
        st.caption(f"{day_dec} was an interesting day, as all the sightings seem to be regional, interesting!")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("11/16/1999")][["datetime","longitude","latitude"]] # back-end look through data set variable
    elif day_dec == "10/31/2004": # back-end
        st.caption(f"{day_dec} was an interesting day, as there were 21 sightings all in Chicago!")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("10/31/2004")][["datetime","longitude","latitude"]] # back-end
    elif day_dec == "9/19/2009": # back-end
        st.caption(f"{day_dec} was an interesting day, as all the sightings seem to be regional, interesting!")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("9/19/2009")][["datetime","longitude","latitude"]] # back-end
    elif day_dec == "7/4/2010": # back-end
        st.caption(f"{day_dec} in my opinion wasn't an interesting day. Well, what could people see in the sky on July fourth?")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("7/4/2010")][["datetime","longitude","latitude"]] # back-end
    elif day_dec == "7/4/2011": # back-end
        st.caption(f"{day_dec} in my opinion wasn't an interesting day. Well, what could people see in the sky on July fourth?")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("7/4/2011")][["datetime","longitude","latitude"]] # back-end
    elif day_dec == "7/4/2012": # back-end
        st.caption(f"{day_dec} in my opinion wasn't an interesting day. Well, what could people see in the sky on July fourth?")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("7/4/2012")][["datetime","longitude","latitude"]] # back-end
    else: # back-end
        st.caption(f"{day_dec}.....Well maybe the aliens just like to party! Who knows")
        day_dec_coord = ufo_data[ufo_data["datetime"].str.startswith("7/4/2013")][["datetime","longitude","latitude"]] # back-end
    st.text(f"There was {len(day_dec_coord)} sightings on {day_dec}")
    day_dec_map(day_dec_coord) # front-end
else:
    st.title("UFO Sightings: a Python Project") # front-end general data page title
    st.caption("Blake Babikian - Bentley University - CS 230") # front-end general data page caption
    st.write("\n \n") # front-end spacing
    st.header("Sightings on July Fourth:")
    not_july_fourth = ufo_data[ufo_data["datetime"].str.startswith("7/4")]
    st.text(f"{len(not_july_fourth)} of the, {len(ufo_data)} reported sightings happen on July 4th.")
    st.text(f"That's only {(len(not_july_fourth)/len(ufo_data)*100):<0.2f}% of the sightings.")
    st.text(f"Although July 4th is a popular day, its not THE reason for so many sightings.")
    st.subheader("Map of Sightings on July Fourth:")
    view_state = pdk.ViewState( # back-end set map
            latitude = 37.0902,
            longitude = -95.7129,
            zoom = 3,
            pitch = 40)
    map(not_july_fourth, view_state)
    st.subheader("Table of Sightings on July Fourth:")
    st.sidebar.subheader("Display:")
    options = ["Ascending","Descending"]
    descide = st.sidebar.radio("Display Data in Ascending or Descending:",options)
    if descide == "Ascending":
        ascending = True
    else:
        ascending = False
    df = pd.DataFrame(not_july_fourth[["state","city","shape","comments"]])
    df = df.sort_values("state",ascending=ascending)
    st.write(df)
