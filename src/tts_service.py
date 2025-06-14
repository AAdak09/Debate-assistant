from abc import ABC, abstractmethod

class TTSService(ABC):
    """
    Abstract base class for Text-to-Speech (TTS) services.
    """

    @abstractmethod
    def synthesize_speech(self, text: str, output_filename: str) -> None:
        """
        Synthesizes speech from the given text and saves it to an audio file.

        Args:
            text: The text to be synthesized.
            output_filename: The name of the file to save the audio to.
        """
        pass

class MockTTSService(TTSService):
    """
    A mock TTS service for testing purposes.
    It simulates speech synthesis by printing messages and creating an empty file.
    """

    def synthesize_speech(self, text: str, output_filename: str) -> None:
        """
        Simulates synthesizing speech from the given text.

        Args:
            text: The text to be synthesized.
            output_filename: The name of the file to save the audio to.
        """
        print(f"Synthesizing speech for: '{text}'")
        print(f"Saving audio to: '{output_filename}'")
        # Create an empty file to simulate audio output
        with open(output_filename, 'w') as f:
            pass
        print("Speech synthesized successfully (mocked).")
