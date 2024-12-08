import requests
import geocoder
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from transformers import pipeline
from flask import Flask, request, jsonify
# import torch
import abc

# Initialize the Translate API client
# translate_client = translate.Client()


# API Configuration
# api_key = "AIzaSyCb5qh7aXAqy2E2gPh8CK6638U5XBTuZmY"
api_key = "AIzaSyAl649RLgf6JCi71Y0CS1JXSS9iAOjG0ME"
# weather_api_key = "e78103da0ad2ef8ca49f6697fd92aa25"
weather_api_key = "2b2974487c3e211a19781fe2ef39cf1b"

import google.generativeai as genai

# Configure the PaLM API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

 

app = Flask(__name__)




def detect_language(text):
    """Detect the language of the input text."""
    try:
        lang = detect(text)
        if lang == "en":
            return "English"
        elif lang == "gu":
            return "Gujarati"
        elif lang == "hi":
            return "Hindi"
        else:
            return "Unknown"
    except LangDetectException:
        return "Unknown"
# def main():
#     text_translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", max_length=400)
    
# text_translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", max_length=400)

    
# def abc.translate_text(text, src_lang="hin", tgt_lang="eng_Latn", max_length=400):
#     # Translate the text using NLLB-200
#     translated = abc.text_translator(text, src_lang=src_lang, tgt_lang=tgt_lang, max_length=max_length)
#     return translated[0]['translation_text']

def get_location_from_ip():
    """Automatically get location from user's IP address."""
    g = geocoder.ip('me')  # Detect location from user's IP address
    # print(g.city)
    return g.city if g.city else "your area"
    # return g.latlng if g.latlng else [0, 0]


def get_weather(location, language="en"):
    """Fetch weather conditions for the specified location and translate based on language."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        # url = f"https://api.openweathermap.org/data/2.5/weather?lat={location[0]}&lon={location[1]}&appid={weather_api_key}&units=metric"
        # url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        # print(response.json())
        
        # Check if the response status is OK (200)
        if response.status_code == 200:
            data = response.json()
            # print(data)

            # Check if the necessary data exists in the response
            if 'weather' in data and 'main' in data:
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                # print(weather)
                # Translate location and weather information into the detected language


                if language == "Hindi":
                    translated_location = abc.translate_text(location, src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)
                    translated_weather = abc.translate_text(weather, src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)

                    return f"{translated_location} में वर्तमान मौसम {translated_weather} है और तापमान {temperature}°C है।"
                elif language == "Gujarati":
                    translated_location = abc.translate_text(location, src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)
                    translated_weather = abc.translate_text(weather, src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)
                    return f"{translated_location}માં વર્તમાન હવામાન {translated_weather} છે અને તાપમાન {temperature}°C છે."
                else:
                    return f"The current weather in {location} is {weather} with a temperature of {temperature}°C."
            else:
                return "Weather data is missing from the response. Please try again later."
        else:
            return f"Failed to fetch weather data for {location}. Status Code: {response.status_code}"
    except Exception as e:
        return f"An error occurred while fetching the weather: {e}"


def get_nearest_apmc_prices(crop_name, language="en"):
    """
    Fetch real-time crop prices for the nearest APMC.
    """
    try:
        # API request to fetch APMC prices
        g = geocoder.ip('me')
        city = g.city
        state = g.state
        # print(city)
        # print(state)
        


        
        # print(en_crop_name)
        

        if city == "Vadodara":
            city = "Vadodara(Baroda)"
        
        # print(crop_name)
        # print(state)
        # print(city)
        

        url = f"https://didactic-barnacle-pvw9qr4xjrgf544-3000.app.github.dev/api/get-market-data?commodity={crop_name}&state={state}&district={city}&market=0"
        response = requests.get(url)
        # response.raise_for_status()
        # data = response.json()
        # print(response.json())



        if response.status_code == 200:
            data = response.json()

            if language == "Hindi":
                crop_name = abc.translate_text(crop_name, src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)
            elif language == "Gujarati":
                crop_name = abc.translate_text(crop_name, src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)
            else:
                crop_name = crop_name
            
            if data.get("isEmpty") or not data.get("data") or data["data"] == [{}]:

                if language == "Hindi":
                    return f"{city}, {state} में {crop_name} के लिए कोई बाजार मूल्य डेटा उपलब्ध नहीं है।"
                elif language == "Gujarati":
                    return f"{city}, {state} માં {crop_name} માટે કોઈ બજાર ભાવ ડેટા ઉપલબ્ધ નથી."
                else:
                    message = f"No market price data available for {crop_name} in {city}, {state} at the moment."
                return message
            

            min_price = data["data"][-1]["minPrice"]
            max_price = data["data"][-1]["maxPrice"]
            # print(data)
            apmc_name = data["data"][-1]["marketName"]

            if language == "Hindi":
                apmc_name = abc.translate_text(apmc_name, src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)
                city = abc.translate_text(city, src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)
                min_price = abc.translate_text(str(min_price), src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)
                max_price = abc.translate_text(str(max_price), src_lang="eng_Latn", tgt_lang="hin_Deva", max_length=100)

            elif language == "Gujarati":
                apmc_name = abc.translate_text(apmc_name, src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)
                city = abc.translate_text(city, src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)
                min_price = abc.translate_text(str(min_price), src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)
                max_price = abc.translate_text(str(max_price), src_lang="eng_Latn", tgt_lang="guj_Gujr", max_length=100)    

            if language == "Hindi":
               return (
                    f"{crop_name} के लिए {apmc_name}, {city} में वर्तमान मूल्य है:\n"
                    f"न्यूनतम मूल्य: ₹{min_price}\n"
                    f"अधिकतम मूल्य: ₹{max_price}"
                )
            elif language == "Gujarati":
                return (
                    f"{crop_name} માટે {apmc_name}, {city} માં વર્તમાન ભાવ છે:\n"
                    f"ન્યૂનતમ ભાવ: ₹{min_price}\n"
                    f"ઉચ્ચતમ ભાવ: ₹{max_price}"
                )
            
            
            # Formulate the response
            message = (
                f"The current price for {crop_name} in {apmc_name}, {city} is:\n"
                f"Minimum Price: ₹{min_price}\n"
                f"Maximum Price: ₹{max_price}"
            )

            return message
        else:
            if language == "Hindi":
                return f"एपीएमसी मूल्य प्राप्त करने में विफल। कृपया बाद में पुनः प्रयास करें।"
            elif language == "Gujarati":
                return f"એપીએમસી કિંમતો મેળવવામાં નિષ્ફળ. કૃપા કરીને પછીથી ફરી પ્રયાસ કરો."
            else:
                return f"Failed to fetch APMC prices. Please try again later."

        
        
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching APMC prices: {e}"
    

def summarize_response(response_text):
    """Summarize the generated response for conciseness and clarity."""
    try:
        # Use a summarization prompt to refine the response
        model = genai.GenerativeModel("gemini-1.5-flash")
        summarization_prompt = (
            f"Summarize the following text into a concise and accurate response:\n\n{response_text}"
        )
        summary_response = model.generate_content(f"'{summarization_prompt}'")
        return summary_response.text.strip()
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return response_text
    






DetectorFactory.seed = 0

@app.route('/')
def home():
    return "Server is running!"

@app.route('/chat', methods=['POST'])
def chat():
    """Interactive chatbot loop."""
    print("Welcome to the Contract Farming Chatbot!")
    print("Type 'exit' to end the chat.\n")

    while True:
        data = request.get_json()
        user_input = data.get('user_input')
        if not user_input:
            return jsonify({'error': 'User input is required'}), 400

        if user_input.lower() == "exit":
            # print("Chatbot: Thank you for using the chatbot. Goodbye!")
            return "Chatbot: Thank you for using the our Sarthi chatbot. Goodbye!"
            # break

        # Detect the language of user input
        detected_language = detect_language(user_input)
        # print(f"Detected Language: {detected_language}")

        # Generate a response using the chatbot model
        try:



            # If the user input is not in English, translate it to English
            # Set up the prompt for the detected language
            if detected_language == "English":
                prompt = f"You are a contract farming assistant. Respond to the user's query in English: '{user_input}'"
            elif detected_language == "Gujarati":
                prompt = f"You are a contract farming assistant. Respond to the user's query in Gujarati: '{user_input}'"
            elif detected_language == "Hindi":
                prompt = f"You are a contract farming assistant. Respond to the user's query in Hindi: '{user_input}'"
            else:
                prompt = f"You are a contract farming assistant. Respond to the user's query in English: '{user_input}' (Default to English)"


            # Check if the user wants weather information
            if any(weather_keyword in user_input.lower() for weather_keyword in ['weather', 'मौसम', 'હવામાન']):
                 # Automatically detect location from IP address if not specified
                if "in" in user_input.lower():
                    location = user_input.split("in")[-1].strip()
                else:
                    location = get_location_from_ip()  # Fallback to IP-based location if not provided
                    # print(f"Chatbot: I detected your location as {location}.")
                weather_info = get_weather(location, detected_language)
                # print(f"Chatbot: {weather_info}")
                return weather_info
                

            # Translate the user input to English for the chatbot model
            if detected_language == "English":
                price_crop = user_input
            elif detected_language == "Hindi":
                price_crop = abc.translate_text(user_input, src_lang="hin", tgt_lang="eng_Latn")
                # print(price_crop)
            elif detected_language == "Gujarati":
                price_crop = abc.translate_text(user_input, src_lang="guj", tgt_lang="eng_Latn")
            
            # print(price_crop)

            # Check if the user wants APMC prices
            if any(keyword in price_crop.lower() for keyword in ["price"]):
                price_detected_language = "English"
                # Extract crop name from user input
                if price_detected_language == "English":
                    crop_name = price_crop.split("price of")[-1].split()[0]
                # elif price_detected_language == "Hindi":
                #     crop_name = price_crop.split("कीमत की")[-1].split()[0]
                # elif detected_language == "Gujarati":
                #     crop_name = price_crop.split("ભાવ")[-1].split()[0]
                    
                    # print(crop_name)
                else:
                    # print(crop_name)
                    crop_name = user_input  # Fallback
                
                # Fetch APMC prices for the specified crop
                apmc_prices = get_nearest_apmc_prices(crop_name, detected_language)
                # print(f"Chatbot: {apmc_prices}")
                return apmc_prices
                # continue

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"You are a contract farming assistant. Respond to the user's query in normal language: '{prompt}'"
            )
            chatbot_reply = response.text
            
            # Summarize the response for clarity
            summarized_reply = summarize_response(chatbot_reply)
            # print(f"Chatbot: {summarized_reply}")
            return summarized_reply
        except Exception as e:
            # print(f"An error occurred: {e}")
            return f"An error occurred: {e}"

# Run the chatbot
if __name__ == "__main__":
    # text_translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", max_length=400)

    app.run(debug=True, port=5000)