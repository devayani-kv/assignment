import openai
from openai import OpenAI
import os
import requests
import json

from lxml import html
from bs4 import BeautifulSoup
from extract_country import qa_rag_chain
from wikipedia import get_location_description
from weather import get_current_weather
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

def extract_place():
    '''Extracts the name of the place from the transcribed text
        Call is made to the function that extracts data from a vector database'''

    query = '''Can you pick out the names of any cities from the paragraph, not people from cities, only cities
            Return only the name of the city
            Return the answer as a json file with the key as the word "city" and the value as the extracted city'''
    ans = qa_rag_chain(query)
    with open('city.json','w') as f:
        json.dump(ans,f)
    return ans["city"]

def return_answer(messages):

    '''This function uses function calling
        The tools used are the weather API and the wikipedia API
        Inputs to both functions are the place that's extracted above
    
    Args:
        messages: list of messages containing conversation history'''
    
    tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather parameters GIVEN a location, like temperature, wind speed etc in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The place, can be a city, state or a country",
                            },
                            #"unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_location_description",
                    "description": "Get the info of a location from wikipedia, like its history, the culture and traditions of the people there etc",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The place, can be a city, state or a country",
                            },
                            #"unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
    
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

    assistant_message = response.choices[0].message
    #messages.append(assistant_message)
    try:
        funcName = assistant_message.to_dict()['tool_calls'][0]['function']['name']
        funcArg = assistant_message.to_dict()['tool_calls'][0]['function']['arguments']
        funcArg = json.loads(funcArg)['location']

        print('Function being called: ',funcName)
        print('Arguments being sent to above function :',funcArg)

        function_to_call = globals()[funcName]
        result = function_to_call(funcArg)
    except:
        result = assistant_message.content
    #print(result)
    return result

city = extract_place()
print('CITY = ', city)
messages = []
q1 = '''What can you tell me about the place {}? Tell me about it's history, the culture of the people there, their lifestyle, etc'''
q1 = q1.format(city)
messages.append({"role": "user", "content": q1})

#print(return_answer(messages))
text = return_answer(messages)
with open('description.txt','w', encoding="utf-8") as f:
    f.write(text)

q2 = '''What is the weather/climate in {} like right now?'''
q2 = q2.format(city)
messages = []
messages.append({"role": "user", "content": q2})

#print(return_answer(messages))
weather_info = return_answer(messages)
with open('weather_info.json','w') as f:
    json.dump(weather_info,f)


with open('weather_info.json','r') as f:
    data = json.load(f)

temp = data['current']['temp_c']
print(temp)
q3 = '''Follow the below instructions:
        You will be given the temperature in a city in degree celsius, if the temperature is greater than 25 degree celsius
        it's a hot day, if it's less than 25 degree celsius, its a warm day
        The city does not matter, only focus on the instructions mentioned above. 
        Since there is not location mentioned, do not hallucinate a location
        There are only two options, hot or warm. Return only the answer
        Temperature: {}
        
        Based on the above instructions and the temperature, return whether its a hot day or a warm day'''

q3 = q3.format(temp)

messages = []
messages.append({"role":"system", "content":"You are a smart assistant with some tools at hand that you will use only if you deem them necessary. You have 2 tools at hand, one to get the exact weather conditions in a place and one to get the description of a place. If you are asked a question that is not related to either of these tools, use your general knowledge to answer it"})
messages.append({"role": "user", "content": q3})

#print(return_answer(messages))
temp_info = return_answer(messages)
print(temp_info)