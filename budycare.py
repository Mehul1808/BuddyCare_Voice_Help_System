import speech_recognition as sr
import pyttsx3
from geopy.geocoders import Nominatim
import pywhatkit
import datetime
import geocoder


phone = "+1547124587" #Enter your Modile Number



engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input and return the recognized text."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Error with the speech recognition service.")
        return ""
    except sr.WaitTimeoutError:
        print("Timeout reached while waiting for input.")
        return ""

def get_current_coordinates():
    """Get the current latitude and longitude."""
    try:
        g = geocoder.ip('me')  
        if g.ok:
            return g.latlng
        else:
            print("Could not fetch coordinates.")
            return None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None

def get_location():
    """Get the user's current location using geopy."""
    geolocator = Nominatim(user_agent="buddy-care")
    try:
        coords = get_current_coordinates()
        if coords:
            location = geolocator.reverse(coords, timeout=10)
            if location:
                return f"{location.address} (Lat: {coords[0]}, Lon: {coords[1]})"
        return "Location not available"
    except Exception as e:
        print(f"Error fetching location: {e}")
        return "Location not available"

def send_sms(ph, msg):
    """Send an SMS using pywhatkit."""
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 2 
    
    
    if minute >= 60:
        minute -= 60
        hour += 1
    
    try:
        pywhatkit.sendwhatmsg(ph, msg, hour, minute, 15, True)
    except Exception as e:
        print(f"Failed to send message: {e}")
        speak("Failed to send the message.")

def main():
    """Main program to activate and respond."""
    speak("Buddy Care is ready. Say 'Buddy Care help' to activate me.")
    activation_phrase = "help me"
    response_phrase = "help"
    exit_phrase = "exit"
    retry_count = 0

    while True:
        command = listen()
        if activation_phrase in command:
            speak("How can I help you?")
            print("How can I help you?")

            while retry_count < 3:
                command = listen()
                if response_phrase in command:
                    retry_count += 1
                    speak(f"Help acknowledged {retry_count} time(s).")
                    print(f"Help acknowledged {retry_count} time(s).")
                elif exit_phrase in command:
                    speak("Goodbye!")
                    print("Goodbye!")
                    return
                else:
                    speak("I didn't catch that. Please say 'help' or 'exit'.")

                if retry_count == 1:
                   
                    location = get_location()

                   
                    emergency_message = (
                        f"Emergency Alert! The user needs help. "
                        f"Location: {location}. Calling police (100)."
                    )

                   
                    send_sms(phone, emergency_message)

                   
                    print("Calling police at 100...")
                    speak("Help message sent, and the police have been notified.")

                    return

if __name__ == "__main__":
    main()
