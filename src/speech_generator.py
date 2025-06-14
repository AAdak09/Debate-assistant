from typing import List, Dict
from .tts_service import TTSService
import os

class SpeechGenerator:
    """
    Generates speech audio files from a debate script using a TTS service.
    """

    def __init__(self, tts_service: TTSService, output_directory: str = "audio_outputs"):
        """
        Initializes the SpeechGenerator.

        Args:
            tts_service: An instance of a TTSService implementation.
            output_directory: The directory to save the generated audio files.
        """
        self.tts_service = tts_service
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def generate_speeches_from_script(self, debate_script: List[Dict[str, str]]) -> List[str]:
        """
        Generates speech audio for each line in the debate script.

        Args:
            debate_script: A list of dictionaries, where each dictionary
                           represents a line of speech and should have
                           'speaker' and 'text' keys.

        Returns:
            A list of filenames for the generated audio files.
        """
        audio_files = []
        for i, speech_part in enumerate(debate_script):
            speaker = speech_part.get("speaker", f"speaker_{i+1}")
            text = speech_part.get("text")

            if not text:
                print(f"Warning: Skipping speech part {i+1} due to missing 'text'.")
                continue

            output_filename = os.path.join(self.output_directory, f"{speaker.lower().replace(' ', '_')}_{i+1}.mp3")

            try:
                self.tts_service.synthesize_speech(text, output_filename)
                audio_files.append(output_filename)
                print(f"Generated audio for {speaker}: {output_filename}")
            except Exception as e:
                print(f"Error generating speech for {speaker} (part {i+1}): {e}")

        return audio_files
