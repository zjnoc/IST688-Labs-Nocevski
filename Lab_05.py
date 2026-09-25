import streamlit as st
from openai import OpenAI
import requests
import json

# location can be a city, a zip code, an airport code ('SYR'), 
# or a landmark ('Eiffel+Tower') 
# note: hard codes units to degrees Fahrenheit 
def get_current_weather(location): 
    url = f'https://wttr.in/{location}?format=j1' 
    response = requests.get(url, timeout=10) 
    if response.status_code != 200: 
        raise Exception(f'wttr.in error: status {response.status_code}') 
    try: 
        data = response.json() 
    except ValueError: 
        # unknown locations come back as plain text, not JSON 
        raise Exception(f'Could not find a location named {location}') 
    # j1 has three top-level sections: 
    #   current_condition -- one entry, conditions right now 
    #   weather           -- three entries, one per day, each with 
    #                        min/max, astronomy, and hourly forecasts 
    #   nearest_area      -- the location wttr.in actually matched 
    current = data['current_condition'][0] 
    # two examples; note that some values are nested one level deeper 
    return {
        'location': location,
        'temperature': float(current['temp_F']),
        'feels_like': float(current['FeelsLikeF']),
        'description': current['weatherDesc'][0]['value'],
        'wind_mph': float(current['windspeedMiles']),
        'chance_of_rain': float(data['weather'][0]['hourly'][4]['chanceofrain'])
    }

st.title("What to Wear Bot")
st.write("Enter a city and I'll tell you what to wear and suggest an outdoor activity.")

OPENAI_API_KEY = st.secrets.OPEN_AI_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-5-mini"

city = st.text_input("Enter a city:", placeholder="e.g., Syracuse, NY")

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Gets today's weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name, e.g. Syracuse, NY"}
            },
            "required": ["location"]
        }
    }
}

if st.button("Get Advice"):
    effective_city = city if city.strip() else "Syracuse, NY"
    question = f"What should I wear today in {effective_city} and what outdoor activities do you suggest?"
    messages = [{"role": "user", "content": question}]

    # First call - model decides if it needs the weather tool
    first = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[weather_tool],
        tool_choice="auto"
    )
    reply = first.choices[0].message

    if reply.tool_calls:
        call = reply.tool_calls[0]
        args = json.loads(call.function.arguments)
        location = args.get("location", "Syracuse, NY")
        weather = get_current_weather(location)

        # Second call - give model the real weather data
        messages.append(reply)
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(weather)})
        second = client.chat.completions.create(model=model, messages=messages)

        st.write(second.choices[0].message.content)
    else:
        st.write(reply.content)



