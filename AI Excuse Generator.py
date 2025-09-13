import random
import datetime
from faker import Faker
import pyttsx3
import json
import os
import threading
import pygame
from gtts import gTTS
import tempfile
from PIL import Image, ImageDraw, ImageFont

fake = Faker()
excuse_history = []
favorites = []
voice_engine = pyttsx3.init()
pygame.mixer.init()  
def load_data():
    try:
        with open('excuse_history.json', 'r') as f:
            global excuse_history
            excuse_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        excuse_history = []  

    try:
        with open('favorites.json', 'r') as f:
            global favorites
            favorites = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        favorites = []
def save_data():
    with open('excuse_history.json', 'w') as f:
        json.dump(excuse_history, f)
    
    with open('favorites.json', 'w') as f:
        json.dump(favorites, f)
def generate_excuse():
    excuses = {
        'work': {
            'low': [
                "Feeling kinda off today, need to rest",
                "Got a family thing I can’t move"
            ],
            'medium': [
                "Internet’s down, total chaos",
                "Forgot about a doctor’s appointment"
            ],
            'high': [
                "Family emergency, gotta run",
                "Tested positive for COVID, quarantining"
            ]
        },
        'school': {
            'low': [
                "Need more time to nail this assignment",
                "Got confused by the instructions"
            ],
            'medium': [
                "Computer died, lost my work",
                "Been dealing with some personal stuff"
            ],
            'high': [
                "Lost someone close, need time",
                "Having some serious health issues"
            ]
        },
        'social': {
            'low': [
                "Totally forgot we had plans",
                "Not really up for going out"
            ],
            'medium': [
                "Car’s in the shop, bad timing",
                "Work’s keeping me late"
            ],
            'high': [
                "Going through a rough patch, need space",
                "Was around someone with COVID"
            ]
        },
        'family': {
            'low': [
                "Got something else that day",
                "Feeling under the weather"
            ],
            'medium': [
                "Work schedule got crazy",
                "Car’s acting up, can’t drive"
            ],
            'high': [
                "Emergency came up, gotta handle it",
                "Dealing with some health problems"
            ]
        }
    }

    print("\nCategories: work, school, social, family")
    category = input("What’s it for? ").lower()
    print("Urgency levels: low, medium, high")
    urgency = input("How urgent is it? ").lower()

    if category in excuses and urgency in excuses[category]:
        excuse = random.choice(excuses[category][urgency])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        excuse_data = {
            'excuse': excuse,
            'category': category,
            'urgency': urgency,
            'timestamp': timestamp
        }
        excuse_history.append(excuse_data)
        save_data()
        print(f"\nYour excuse: {excuse}")
        return excuse
    else:
        print("Doh! Bad category or urgency. Try again.")
        return None
def generate_proof():
    proof_types = ["document", "chat screenshot", "location log", "image proof"]
    print("\nProof types:", ", ".join(proof_types))
    proof_type = input("What kind of proof do you need? ").lower()

    if proof_type == 'document':
        proof = f"Generated Document: {fake.file_name(extension='pdf')}"
    elif proof_type == 'chat screenshot':
        proof = f"Chat Screenshot: {fake.file_name(extension='png')}"
    elif proof_type == 'location log':
        proof = f"Location Log: {fake.address()}"
    elif proof_type == 'image proof':
        proof = "Image Proof: Generated (saved as proof_image.png)"
        generate_proof_image()
    else:
        proof = "No proof generated, pick a valid type next time!"
    
    print(proof)
def generate_proof_image():
    try:
        img = Image.new('RGB', (400, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()  # Fallback, not ideal but works
        
        d.rectangle([50, 50, 350, 250], outline=(9, 132, 227), width=2)
        d.text((60, 60), "Official Proof Document", fill=(45, 52, 54), font=font)
        d.text((60, 90), f"Date: {datetime.date.today()}", fill=(45, 52, 54), font=font)
        d.text((60, 120), "Status: Verified", fill=(9, 132, 227), font=font)
        d.text((60, 150), f"Ref: {fake.uuid4()}", fill=(45, 52, 54), font=font)
        d.text((60, 180), "Signed: Dr. Smith", fill=(45, 52, 54), font=font)
        
        img.save('proof_image.png')  # Save it since no UI
        print("Image saved as proof_image.png")
    except ImportError:
        print("Bummer, need Pillow for images. Install it!")
def generate_emergency():
    emergencies = [
        "Family crisis, gotta go now",
        "Medical emergency, heading to hospital",
        "House flooded, dealing with it",
        "Car crash, sorting it out"
    ]
    emergency = random.choice(emergencies)
    print(f"\nEmergency message: {emergency} (Sent to whoever needs to know)")
def generate_apology():
    style = input("\nWant a professional apology? (yes/no): ").lower()
    if style == 'yes':
        apology = "So sorry for the inconvenience. I value our relationship and I’ll make sure this doesn’t happen again."
    else:
        apology = "I’m super sorry, I messed up big time! Please forgive me, I’ll make it right."
    
    print(f"\nApology: {apology}")
def speak_excuse(excuse):
    if not excuse:
        print("Nothing to say, generate an excuse first!")
        return
    
    voice = input("\nUse Google TTS? (yes/no, no means system voice): ").lower()
    if voice == 'yes':
        speak_with_gtts(excuse)
    else:
        speak_with_pyttsx3(excuse)

def speak_with_pyttsx3(text):
    def _speak():
        voice_engine.say(text)
        voice_engine.runAndWait()
    
    threading.Thread(target=_speak, daemon=True).start()

def speak_with_gtts(text):
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        
        tts = gTTS(text=text, lang='en')
        tts.save(temp_path)
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        os.unlink(temp_path)
    except Exception as e:
        print(f"Speech failed: {str(e)}")
def add_to_favorites(excuse):
    if not excuse:
        print("No excuse to save!")
        return
    
    for item in excuse_history:
        if item['excuse'] == excuse:
            if item not in favorites:
                favorites.append(item)
                save_data()
                print("Added to favorites!")
            else:
                print("Already in favorites!")
            return
    
    print("Can’t find that excuse in history.")
def show_history():
    if not excuse_history:
        print("\nNo excuses yet!")
        return
    
    print("\nYour Excuse History:")
    for i, item in enumerate(excuse_history):
        print(f"{i+1}. {item['timestamp']} | {item['category'].capitalize()} | {item['urgency'].capitalize()} | {item['excuse']}")
    
    choice = input("\nEnter number to speak or favorite (0 to skip): ")
    if choice.isdigit() and 0 < int(choice) <= len(excuse_history):
        item = excuse_history[int(choice) - 1]
        action = input("Speak or favorite? (s/f): ").lower()
        if action == 's':
            speak_excuse(item['excuse'])
        elif action == 'f':
            add_to_favorites(item['excuse'])
def show_favorites():
    if not favorites:
        print("\nNo favorites yet!")
        return
    
    print("\nYour Favorite Excuses:")
    for i, item in enumerate(favorites):
        print(f"{i+1}. {item['timestamp']} | {item['category'].capitalize()} | {item['urgency'].capitalize()} | {item['excuse']}")
    
    choice = input("\nEnter number to speak or remove (0 to skip): ")
    if choice.isdigit() and 0 < int(choice) <= len(favorites):
        item = favorites[int(choice) - 1]
        action = input("Speak or remove? (s/r): ").lower()
        if action == 's':
            speak_excuse(item['excuse'])
        elif action == 'r':
            favorites.remove(item)
            save_data()
            print("Removed from favorites!")
def get_prediction():
    if len(excuse_history) > 3:
        print("\nYo, my gut says you’ll need an excuse tomorrow afternoon. You’ve been slacking a lot!")
    else:
        print("\nNot enough excuses to predict yet, keep at it!")
def generate_multilang():
    langs = ["english", "spanish", "french", "german"]
    print("\nLanguages:", ", ".join(langs))
    lang = input("Pick a language: ").lower()
    
    excuses = {
        'english': "Sorry, can’t make it today",
        'spanish': "Lo siento, hoy no puedo",
        'french': "Désolé, je ne peux pas venir aujourd’hui",
        'german': "Tut mir leid, ich kann heute nicht"
    }
    
    excuse = excuses.get(lang, "No clue how to say it in that language")
    print(f"\nExcuse: {excuse}")
def get_ranking():
    if not excuse_history:
        print("\nNo excuses to rank yet!")
        return
    
    ranked = sorted(excuse_history, 
                    key=lambda x: 3 if x['urgency'] == 'high' else 
                                 2 if x['urgency'] == 'medium' else 1, 
                    reverse=True)
    
    print("\nYour Best Excuses:")
    for i, item in enumerate(ranked[:3]):
        print(f"{i+1}. {item['excuse']} (Vibe: {item['urgency'].capitalize()})")
def main():
    load_data()
    while True:
        print("\n Excuse Generator ")
        print("1. Generate Excuse")
        print("2. Generate Proof")
        print("3. Emergency Message")
        print("4. Apology")
        print("5. Show History")
        print("6. Show Favorites")
        print("7. Predict Next Excuse")
        print("8. Multi-language Excuse")
        print("9. Rank Excuses")
        print("0. Quit")
        
        choice = input("What is your choice: ")
        
        if choice == '1':
            excuse = generate_excuse()
            if excuse:
                speak = input("Speak this excuse? (yes/no): ").lower()
                if speak == 'yes':
                    speak_excuse(excuse)
                fav = input("Add to favorites? (yes/no): ").lower()
                if fav == 'yes':
                    add_to_favorites(excuse)
        elif choice == '2':
            generate_proof()
        elif choice == '3':
            generate_emergency()
        elif choice == '4':
            generate_apology()
        elif choice == '5':
            show_history()
        elif choice == '6':
            show_favorites()
        elif choice == '7':
            get_prediction()
        elif choice == '8':
            generate_multilang()
        elif choice == '9':
            get_ranking()
        elif choice == '0':
            print("Peace out!")
            break
        else:
            print("Pick a valid option, dude!")
if __name__ == "__main__":
                main()
