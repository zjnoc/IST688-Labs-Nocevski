import os
import streamlit as st
import requests
from langchain.agents import create_agent

os.environ["OPENAI_API_KEY"] = st.secrets["OPEN_AI_KEY"]


# location can be a city, a zip code, an airport code ('SYR'), 
# or a landmark ('Eiffel+Tower') 
# note: hard codes units to degrees Fahrenheit 
def get_current_weather(location: str = "Syracuse, NY") -> dict: 
    """Gets the current weather in Fahrenheit for a location.
    Accepts a city, zip code, airport code, or landmark."""

    url = f'https://wttr.in/{location}?format=j1' 
    response = requests.get(url, timeout=10) 
    if response.status_code != 200: 
        raise Exception(f'wttr.in error: status {response.status_code}') 
    try: 
        data = response.json() 
    except ValueError: 
        # unknown locations come back as plain text, not JSON 
        raise Exception(f'Could not find a location named {location}') 
    
    current = data['current_condition'][0] 
    return {
        'location': location,
        'temperature': float(current['temp_F']),
        'feels_like': float(current['FeelsLikeF']),
        'description': current['weatherDesc'][0]['value'],
        'wind_mph': float(current['windspeedMiles']),
        'chance_of_rain': float(data['weather'][0]['hourly'][4]['chanceofrain'])
    }

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[get_current_weather],
    system_prompt="Use real weather data to recommend what to wear and suggest outdoor activities",
)

st.title("What to Wear Bot")
st.write("Enter a city and I'll tell you what to wear and suggest an outdoor activity.")

city = st.text_input("Enter a city:", placeholder="e.g., Syracuse, NY")

if st.button("Get Advice"):
    effective_city = city if city.strip() else "Syracuse, NY"
    question = f"What should I wear today in {effective_city} and what outdoor activities do you suggest?"
    
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})   

    with st.chat_message("assistant"):
        st.write(result["messages"][-1].content)

    with st.expander("Behind the scenes"):
        for message in result["messages"]:
            st.write(f"**{message.type}**")
            st.write(message.content)
            if message.type == "ai" and message.tool_calls:
                st.write(message.tool_calls)



# Part D #12

# A 
# How many messages are there, and what is each one?
# There are 4 messages:
# 1. human: my question
# 2. ai: the model asking to use the weather tool
# 3. tool: the weather data that came back
# 4. ai: the final answer

# B 
# Which message asks for the weather tool? (Its content is empty. Where is the request?)
# Message 2. Its text is empty because the model is not answering yet.
# The request is in the tool_calls part, not in the text.

# C
# In Lab 5, which lines of your code created each of those messages?
# 1. messages = [{"role": "user", "content": question}]
# 2. messages.append(reply)
# 3. messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(weather)})
# 4. second = client.chat.completions.create(model=model, messages=messages)