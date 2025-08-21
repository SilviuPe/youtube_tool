# import asyncio
# import edge_tts
#
# async def main():
#     text = "Salut! Acesta este un test de redare audio."
#     voice = "en-US-EricNeural"  # Poți înlocui cu altă voce disponibilă
#     output_file = "output.mp3"  # Poți schimba extensia în ".wav" dacă dorești fișier WAV
#
#     communicate = edge_tts.Communicate(text, voice)
#     await communicate.save(output_file)
#     print(f"Audio salvat în {output_file}")
#
# if __name__ == "__main__":
#     asyncio.run(main())


import requests
api = 'http://109.176.199.63:5000/get-random-video'

jsond = {
    "category" : "hacking",
    "audio_script" : "Hacking-ul reprezintă procesul prin care se identifică și se exploatează vulnerabilitățile unui sistem informatic. Aceasta poate include accesarea neautorizată a rețelelor, aplicațiilor sau dispozitivelor, cu scopul de a obține informații sensibile sau de a perturba funcționarea acestora."
}

res = requests.post(api, json = jsond)