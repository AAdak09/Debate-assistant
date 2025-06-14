# Main script to generate debate speech
import sys
import os
import argparse

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from speech_generator import SpeechGenerator
# Import the real TTS service
from tts_service import Pyttsx3TTSService, MockTTSService # Keep Mock for easy switching if needed

def main():
    print("--- generate_debate.py: main() called ---")

    parser = argparse.ArgumentParser(description="Generate a debate speech.")
    parser.add_argument("--topic", type=str, default="The Future of Work", help="The topic of the debate.")
    parser.add_argument("--stance", type=str, default="con", choices=["pro", "con", "neutral"], help="The stance on the topic.")
    parser.add_argument("--speaker", type=str, default="Narrator", help="The name of the speaker.")
    parser.add_argument("--points", type=int, default=2, help="Number of main points.")
    parser.add_argument("--tts", type=str, default="pyttsx3", choices=["pyttsx3", "mock"], help="TTS engine to use.")
    parser.add_argument("--output_format", type=str, default="mp3", choices=["mp3", "wav"], help="Desired audio output format.")

    args = parser.parse_args()

    print(f"--- generate_debate.py: Args: Topic='{args.topic}', Stance='{args.stance}', Speaker='{args.speaker}', Points={args.points}, TTS='{args.tts}', Format='{args.output_format}' ---")

    if args.tts == "pyttsx3":
        print("--- generate_debate.py: Initializing Pyttsx3TTSService ---")
        tts_service = Pyttsx3TTSService()
    else:
        print("--- generate_debate.py: Initializing MockTTSService ---")
        tts_service = MockTTSService()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_output_dir = os.path.join(project_root, "audio_outputs")
    # Ensure audio_output_dir is absolute for SpeechGenerator path handling
    absolute_audio_output_dir = os.path.abspath(audio_output_dir)
    print(f"--- generate_debate.py: Audio output directory set to: {absolute_audio_output_dir} ---")

    speech_gen = SpeechGenerator(tts_service=tts_service, output_directory=absolute_audio_output_dir)
    print("--- generate_debate.py: SpeechGenerator initialized ---")

    # Construct a dynamic output filename based on choices - this is what the script *would* want
    # output_filename_base = f"{args.speaker.lower()}_{args.topic.replace(' ', '_').lower()}_{args.stance.lower()}_main_speech"
    # output_filename_with_ext = f"{output_filename_base}.{args.output_format}"
    # However, SpeechGenerator.generate_debate_speech creates its own filename and determines format (currently hardcoded to .mp3).
    # The --output_format arg is therefore not fully honored by SpeechGenerator yet.
    # Pyttsx3TTSService *can* handle different formats if SpeechGenerator requests them.

    print(f"Starting single debate speech generation for topic '{args.topic}' ({args.stance}). SpeechGenerator will use its internal naming. ---")

    generated_file_path = speech_gen.generate_debate_speech(
        topic=args.topic,
        stance=args.stance,
        speaker_name=args.speaker,
        num_points=args.points
        # output_filename=output_filename_with_ext # This argument doesn't exist in current SpeechGenerator
    )

    if generated_file_path and os.path.exists(generated_file_path):
        print(f"\nSuccessfully generated audio file: {os.path.abspath(generated_file_path)}")
        print(f"File size: {os.path.getsize(generated_file_path)} bytes")
    elif generated_file_path: # Path returned but file doesn't exist
        print(f"\nTTS service reported generation of {os.path.abspath(generated_file_path)}, but the file was not found.")
    else: # No path returned
        print("\nNo audio file path was returned by the speech generator. Check logs for errors.")

    print("--- generate_debate.py: main() finished ---")

if __name__ == "__main__":
    print("--- generate_debate.py: script started ---")
    main()
    print("--- generate_debate.py: script finished ---")
