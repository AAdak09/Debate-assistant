# Debate Speech Generation Tool

This tool generates a short debate speech based on a given topic and stance,
and then uses a Text-to-Speech (TTS) engine to convert the speech into an
audio file.

Currently, speech content is generated using basic templates. The focus has
been on setting up the pipeline for speech generation and TTS conversion.

## Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   For Linux users, `pyttsx3` (the TTS engine used) requires certain system
    libraries. You can install them using:
    ```bash
    sudo apt-get update
    sudo apt-get install espeak ffmpeg
    ```
    (`espeak` is a speech synthesis engine, `ffmpeg` is used for MP3 conversion).
    For other operating systems, please refer to `pyttsx3` documentation for
    platform-specific dependencies if audio output does not work.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <repository-url>
    # cd debate-speech-tool
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main script to generate a debate speech is `scripts/generate_debate.py`.

You can run it from the root directory of the project:

```bash
python scripts/generate_debate.py [OPTIONS]
```

### Command-line Options:

*   `--topic TEXT`: The topic of the debate (default: "The Future of Work").
*   `--stance TEXT`: The stance on the topic. Choices: `pro`, `con`, `neutral` (default: "con").
*   `--speaker TEXT`: The name of the speaker (default: "Narrator").
*   `--points INTEGER`: Number of main points for the speech (default: 2).
*   `--tts TEXT`: TTS engine to use. Choices: `pyttsx3`, `mock` (default: "pyttsx3").
*   `--output_format TEXT`: Desired audio output format. Choices: `mp3`, `wav` (default: "mp3").
                     (Note: `SpeechGenerator` currently defaults to `.mp3` internally for `pyttsx3` if not WAV).
*   `--help`: Show the help message and exit.

### Example:

To generate a speech in favor of "AI in Healthcare" as "Dr. Smith", outputting an MP3:

```bash
python scripts/generate_debate.py --topic "AI in Healthcare" --stance "pro" --speaker "DrSmith" --output_format mp3
```

Generated audio files will be saved in the `audio_outputs/` directory.

## Current Limitations

*   **Speech Content:** Argumentation is very basic and template-driven. It does not yet possess a "humanly argumentative tone" or sophisticated reasoning.
*   **Error Handling:** While some error handling is in place, it can be further improved.
*   **Voice Customization:** Limited options for voice selection or fine-tuning TTS output beyond basic rate control in `Pyttsx3TTSService`.

Further development will focus on improving these areas.
