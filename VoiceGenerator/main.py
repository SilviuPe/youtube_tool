from elevenlabs.client import ElevenLabs
from .logger import Logger

eb = ElevenLabs(
    api_key="sk_67b06ceb665785b7b749c0740d2efaebc936653140bb4fca"
)

audio_stream = eb.text_to_speech.stream(
    text="This is a test",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)

# Save the stream to a file
with open("../output.mp3", "wb") as f:
    for chunk in audio_stream:
        if isinstance(chunk, bytes):
            f.write(chunk)




class VoiceGenerator(object):
    
    """
    Class to generate voices from text 
    """

    def __init__(self, api_key: str, voice_id: str, model_id: str) -> None:
        
        self.lab = ElevenLabs(api_key)
        self.voice_id = voice_id
        self.model_id = model_id

        self.success_logger = Logger("")
        self.error_logger = Logger("")


    def genetate_voice(self, text :  str) -> list:

        """
        
        Method to generate the voice from text
        
        :param: text - the script for the voice

        """

        try:
            
            audio_stream = eb.text_to_speech.stream(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model_id
            )

            return [{"audio_object" : audio_stream
            }, 200]

        except Exception as error:
            
            print(str(error))

            return [{"error" : str(error)
            } , 400]



    def write_out_voice(self, binary_content : bytes) -> list:
        """
        
        Method to write out an .mp3 file

        """

        try:

            with open("../output.mp3", "wb") as f:
                
                for binary_data in binary_content:
                    if isinstance(binary_data, bytes):
                        f.write(binary_data)

                f.close()

            print("File")
        except Exception as error:

            print(str(error))

            return [{"error" : str(error)
            } , 400]