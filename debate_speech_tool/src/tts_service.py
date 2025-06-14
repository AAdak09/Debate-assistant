from abc import ABC, abstractmethod
import os
import pyttsx3 # Main TTS engine library
import subprocess # For running ffmpeg more robustly

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
    A mock TTS service for testing purposes. Creates a dummy file.
    """
    def synthesize_speech(self, text: str, output_filename: str) -> None:
        print(f"--- MockTTSService: Synthesizing speech for: '{text[:50]}...' ---")
        print(f"--- MockTTSService: Saving audio to: '{output_filename}' ---")

        output_dir = os.path.dirname(output_filename)
        if not output_dir: output_dir = "." # Handle cases where output_filename might not have a dir part
        os.makedirs(output_dir, exist_ok=True)

        with open(output_filename, 'w') as f:
            f.write(f"Mock audio data for: {text}")
        print(f"--- MockTTSService: Mock audio file created at {output_filename} ---")

class Pyttsx3TTSService(TTSService):
    """
    A TTS service implementation using the pyttsx3 library.
    Saves speech as WAV, then optionally converts to MP3 using ffmpeg.
    """
    def __init__(self, rate: int = 150):
        self.engine = None
        self.ffmpeg_path = "ffmpeg" # Assumes ffmpeg is in PATH
        try:
            print("--- Pyttsx3TTSService: Initializing pyttsx3 engine... ---")
            self.engine = pyttsx3.init()

            voices = self.engine.getProperty('voices')
            if voices:
                print(f"--- Pyttsx3TTSService: Found {len(voices)} voices. Using default. ---")
                # Example: self.engine.setProperty('voice', voices[0].id)
            else:
                print("--- Pyttsx3TTSService: Warning: No voices found for pyttsx3. Speech may use a default system voice or fail. ---")

            self.engine.setProperty('rate', rate)
            print(f"--- Pyttsx3TTSService: Engine initialized successfully. Speech rate set to {rate}. ---")

        except Exception as e:
            print(f"--- Pyttsx3TTSService: CRITICAL: Error initializing pyttsx3 engine: {e} ---")
            self.engine = None # Ensure engine is None if init fails

    def _check_ffmpeg(self) -> bool:
        """Checks if ffmpeg is available."""
        try:
            subprocess.run([self.ffmpeg_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print(f"--- Pyttsx3TTSService: ffmpeg found at '{self.ffmpeg_path}'. ---")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"--- Pyttsx3TTSService: WARNING: ffmpeg not found or not executable at '{self.ffmpeg_path}'. MP3 conversion will be skipped. ---")
            return False

    def synthesize_speech(self, text: str, output_filename: str) -> None:
        if not self.engine:
            print("--- Pyttsx3TTSService: Engine not initialized. Cannot synthesize speech. ---")
            # Optionally, raise an error or handle gracefully
            raise RuntimeError("Pyttsx3 engine was not initialized successfully or failed during init.")

        print(f"--- Pyttsx3TTSService: Preparing to synthesize: '{text[:50]}...' to {output_filename} ---")

        absolute_output_filename = os.path.abspath(output_filename)
        output_dir = os.path.dirname(absolute_output_filename)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"--- Pyttsx3TTSService: Created output directory: {output_dir} ---")

        base_name = os.path.splitext(os.path.basename(absolute_output_filename))[0]
        temp_wav_filename = os.path.join(output_dir, f"{base_name}_temp_{os.getpid()}.wav")

        try:
            print(f"--- Pyttsx3TTSService: Saving speech to temporary WAV: {temp_wav_filename} ---")
            self.engine.save_to_file(text, temp_wav_filename)
            self.engine.runAndWait()

            if not os.path.exists(temp_wav_filename) or os.path.getsize(temp_wav_filename) == 0:
                print(f"--- Pyttsx3TTSService: ERROR: Temporary WAV file {temp_wav_filename} was not created or is empty after save_to_file. ---")
                raise FileNotFoundError(f"Temporary WAV file {temp_wav_filename} failed to be created by pyttsx3.")
            print(f"--- Pyttsx3TTSService: Successfully saved to temporary WAV: {temp_wav_filename} (Size: {os.path.getsize(temp_wav_filename)}) ---")

            # Conversion or rename logic
            if absolute_output_filename.lower().endswith(".mp3"):
                if self._check_ffmpeg():
                    print(f"--- Pyttsx3TTSService: Attempting to convert {temp_wav_filename} to MP3: {absolute_output_filename} ---")
                    convert_command = [
                        self.ffmpeg_path, "-i", temp_wav_filename,
                        "-acodec", "libmp3lame", "-q:a", "2", # Standard MP3 quality
                        "-y", absolute_output_filename # Overwrite output file if it exists
                    ]
                    process = subprocess.run(convert_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if process.returncode == 0 and os.path.exists(absolute_output_filename):
                        print(f"--- Pyttsx3TTSService: Successfully converted WAV to MP3: {absolute_output_filename} ---")
                    else:
                        print(f"--- Pyttsx3TTSService: WARNING: ffmpeg conversion failed (code {process.returncode}). MP3 not created. ---")
                        print(f"--- ffmpeg stdout: {process.stdout.decode(errors='ignore')} ---")
                        print(f"--- ffmpeg stderr: {process.stderr.decode(errors='ignore')} ---")
                        # Save the original WAV as a fallback
                        fallback_wav_name = os.path.splitext(absolute_output_filename)[0] + "_conversion_failed.wav"
                        if os.path.exists(fallback_wav_name): os.remove(fallback_wav_name) # remove if exists
                        os.rename(temp_wav_filename, fallback_wav_name)
                        print(f"--- Pyttsx3TTSService: Original WAV saved as {fallback_wav_name} ---")
                        temp_wav_filename = None # WAV has been handled
                else: # ffmpeg not found
                    fallback_wav_name = os.path.splitext(absolute_output_filename)[0] + "_ffmpeg_not_found.wav"
                    if os.path.exists(fallback_wav_name): os.remove(fallback_wav_name) # remove if exists
                    os.rename(temp_wav_filename, fallback_wav_name)
                    print(f"--- Pyttsx3TTSService: Original WAV saved as {fallback_wav_name} ---")
                    temp_wav_filename = None # WAV has been handled
            else: # Output is not MP3, assume WAV or other format pyttsx3 handles directly (though it's usually WAV)
                if os.path.exists(absolute_output_filename): os.remove(absolute_output_filename) # remove if exists
                os.rename(temp_wav_filename, absolute_output_filename)
                print(f"--- Pyttsx3TTSService: Output saved as (non-MP3): {absolute_output_filename} ---")
                temp_wav_filename = None # WAV has been handled

        except Exception as e:
            print(f"--- Pyttsx3TTSService: CRITICAL: Error during speech synthesis or conversion: {e} ---")
            # Attempt to save temp WAV if it exists and an error occurred after its creation
            if temp_wav_filename and os.path.exists(temp_wav_filename) and os.path.getsize(temp_wav_filename) > 0:
                error_wav_name = os.path.splitext(absolute_output_filename)[0] + "_error_processing.wav"
                if os.path.exists(error_wav_name): os.remove(error_wav_name)
                try:
                    os.rename(temp_wav_filename, error_wav_name)
                    print(f"--- Pyttsx3TTSService: Temp WAV saved as {error_wav_name} due to error. ---")
                except OSError as ose_rename: # Catch potential error during rename itself
                    print(f"--- Pyttsx3TTSService: Could not rename problematic temp WAV {temp_wav_filename} to {error_wav_name}: {ose_rename} ---")
            raise
        finally:
            # Clean up the temporary WAV file if it still exists (i.e., wasn't renamed)
            if temp_wav_filename and os.path.exists(temp_wav_filename):
                print(f"--- Pyttsx3TTSService: Cleaning up leftover temporary WAV file: {temp_wav_filename} ---")
                os.remove(temp_wav_filename)
