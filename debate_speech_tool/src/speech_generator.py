# Python script for Speech Generation
from typing import List, Dict, Union
from tts_service import TTSService
import os
import random

# --- Phrase Lists for Argumentative Tone (with refinements) ---
PRO_INTRO_OPENERS = [
    "Let me be unequivocally clear:",
    "It is my firm conviction that",
    "Today, I will compellingly argue that",
    "There should be no doubt in anyone's mind that",
    "It is imperative that we recognize the value of", # New opener
]
CON_INTRO_OPENERS = [ # Unchanged
    "I stand before you today to issue a stark warning:",
    "It is with a great sense of urgency that I must state:",
    "We must critically examine the dangerous path presented by",
    "I am here to vigorously oppose the notion of",
]
PRO_ARGUMENT_LEADS = [ # Unchanged
    "Firstly, the undeniable positive impact of {topic} on {aspect} cannot be overstated.",
    "A crucial piece of evidence supporting {topic} is its profound effect on {aspect}.",
    "Consider, for a moment, the significant advancements {topic} brings to {aspect}.",
    "Furthermore, it's essential to recognize how {topic} revolutionizes {aspect}.",
]
CON_ARGUMENT_LEADS = [ # Unchanged
    "The most glaring issue is the devastating consequence {topic} will have on {aspect}.",
    "We cannot ignore the severe risks {topic} poses to {aspect}.",
    "A primary concern must be the detrimental effect of {topic} upon {aspect}.",
    "Moreover, the inherent dangers of {topic} for {aspect} are simply unacceptable.",
]
REBUTTAL_PREVIEWS_PRO = [ # Unchanged
    "Opponents may raise concerns, perhaps focusing on perceived drawbacks. However, these arguments crumble under scrutiny, as I will demonstrate.",
    "Some might attempt to discredit {topic} by pointing to hypothetical issues. This perspective, however, is fundamentally flawed.",
]
REBUTTAL_PREVIEWS_CON = [ # Unchanged
    "Proponents will undoubtedly sing praises of {topic}, citing supposed benefits. Yet, they conveniently ignore the fundamental flaws, which I will expose.",
    "Advocates for {topic} often highlight potential upsides. What they fail to address, however, are the critical failures.",
]
PRO_CONCLUSIONS = [
    "Therefore, to embrace progress and secure a better future, we must champion {topic}. The case is clear, the time to act is now.",
    "In conclusion, the evidence overwhelmingly supports {topic}. Let us move forward with conviction.",
    "The path forward is clear: {topic} offers an unparalleled opportunity we must seize.",
    "To deny the importance of {topic} is to deny progress itself; let us choose wisely.", # New conclusion
]
CON_CONCLUSIONS = [ # Unchanged
    "In light of these grave concerns, it is our moral imperative to resist {topic}. To proceed would be an act of profound irresponsibility.",
    "The risks associated with {topic} are simply too great to ignore. We must choose a safer, more responsible path.",
    "Thus, for the sake of prudence and safety, we are compelled to reject {topic} outright.",
]
# --- Thematic Aspect Lists for Arguments (with refinements) ---
PRO_ASPECT_EXAMPLES = [ # Unchanged
    "its undeniable contribution to innovation",
    "the significant improvement in efficiency it provides",
    "its positive impact on societal well-being",
    "the advancement of knowledge it fosters",
    "the economic benefits it unlocks",
    "its role in solving complex global challenges",
    "the enhancement of human potential it offers",
]
CON_ASPECT_EXAMPLES = [
    "the inherent risk of misuse and malicious exploitation", # Refined
    "the potential for societal disruption and inequality",
    "its detrimental effect on individual liberties and privacy",
    "the ethical dilemmas and moral hazards it creates",
    "the unforeseen negative consequences that could arise",
    "its capacity to exacerbate existing societal problems",
    "the erosion of human autonomy it might lead to",
]

class SpeechGenerator:
    """
    Generates a structured debate speech and synthesizes it to audio.
    """

    def __init__(self, tts_service: TTSService, output_directory: str = "audio_outputs"):
        self.tts_service = tts_service
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        print(f"--- SpeechGenerator: Initialized. Output directory: {os.path.abspath(self.output_directory)} ---")

    def generate_speech_structure(self, topic: str, stance: str, num_points: int = 3) -> Dict[str, Union[str, List[str]]]:
        structure = {}
        if stance.lower() == "pro":
            actual_num_points = min(num_points, len(PRO_ASPECT_EXAMPLES))
            available_aspects = random.sample(PRO_ASPECT_EXAMPLES, actual_num_points)
            structure["introduction"] = f"{random.choice(PRO_INTRO_OPENERS)} {topic} is not just beneficial, it is essential, and I will lay out precisely why."
            structure["arguments"] = [
                random.choice(PRO_ARGUMENT_LEADS).format(topic=topic, aspect=available_aspects[i])
                for i in range(len(available_aspects))
            ]
            structure["rebuttal_preview"] = random.choice(REBUTTAL_PREVIEWS_PRO).format(topic=topic)
            structure["conclusion"] = random.choice(PRO_CONCLUSIONS).format(topic=topic)
        elif stance.lower() == "con":
            actual_num_points = min(num_points, len(CON_ASPECT_EXAMPLES))
            available_aspects = random.sample(CON_ASPECT_EXAMPLES, actual_num_points)
            structure["introduction"] = f"{random.choice(CON_INTRO_OPENERS)} the notion of {topic} is fraught with peril, and I will meticulously outline the dangers."
            structure["arguments"] = [
                random.choice(CON_ARGUMENT_LEADS).format(topic=topic, aspect=available_aspects[i])
                for i in range(len(available_aspects))
            ]
            structure["rebuttal_preview"] = random.choice(REBUTTAL_PREVIEWS_CON).format(topic=topic)
            structure["conclusion"] = random.choice(CON_CONCLUSIONS).format(topic=topic)
        else:
            structure["introduction"] = f'The subject of {topic} presents a complex tapestry of viewpoints.'
            structure["arguments"] = [f'One perspective on {topic} relates to aspect {i+1}.' for i in range(num_points)]
            structure["conclusion"] = f'Ultimately, understanding {topic} requires careful consideration of these varied facets.'
        return structure

    def format_speech_text(self, speech_structure: Dict[str, Union[str, List[str]]]) -> str:
        text_parts = []
        if "introduction" in speech_structure: text_parts.append(speech_structure["introduction"])
        if "arguments" in speech_structure and isinstance(speech_structure["arguments"], list):
            for point in speech_structure["arguments"]: text_parts.append(point)
        if "rebuttal_preview" in speech_structure: text_parts.append(speech_structure["rebuttal_preview"])
        if "conclusion" in speech_structure: text_parts.append(speech_structure["conclusion"])
        return " ".join(text_parts)

    def generate_debate_speech(self, topic: str, stance: str, speaker_name: str = "Debater", num_points: int = 3) -> str:
        print(f"--- SpeechGenerator: Generating single debate speech. Topic: {topic}, Stance: {stance} ---")
        speech_structure = self.generate_speech_structure(topic, stance, num_points)
        speech_text = self.format_speech_text(speech_structure)
        if not speech_text:
            print(f"--- SpeechGenerator: Error: Generated speech text is empty for topic '{topic}'. ---")
            return ""
        safe_topic = "".join(c if c.isalnum() else "_" for c in topic)
        safe_speaker_name = "".join(c if c.isalnum() else "_" for c in speaker_name)
        filename = f"{safe_speaker_name.lower()}_{safe_topic.lower()}_{stance.lower()}.mp3"
        output_filename = os.path.join(os.path.abspath(self.output_directory), filename)
        print(f"--- SpeechGenerator: Synthesizing speech for {speaker_name} on '{topic}' ({stance}). Output: {output_filename} ---")
        print(f"--- SpeechGenerator: Speech Text (first 300 chars): {speech_text[:300]}... ---")
        try:
            self.tts_service.synthesize_speech(speech_text, output_filename)
            print(f"--- SpeechGenerator: Successfully generated audio: {output_filename} ---") # This line was missing in the prompt's shortened version
            return output_filename
        except Exception as e:
            print(f"--- SpeechGenerator: Error during TTS synthesis for {speaker_name}: {e} ---") # This line was missing in the prompt's shortened version
            return ""

    def generate_speeches_from_script(self, debate_script: List[Dict[str, str]]) -> List[str]:
        print(f"--- SpeechGenerator: generate_speeches_from_script called. Output dir: {os.path.abspath(self.output_directory)} ---")
        audio_files = []
        if not os.path.exists(self.output_directory): os.makedirs(self.output_directory)
        for i, speech_part in enumerate(debate_script):
            speaker = speech_part.get("speaker", f"speaker_{i+1}")
            text = speech_part.get("text")
            if not text: continue # Simplified from prompt for brevity, original logic is fine
            filename = f"{speaker.lower().replace(' ', '_')}_script_part_{i+1}.mp3"
            output_filename = os.path.join(os.path.abspath(self.output_directory), filename)
            # Added print from original full version
            print(f"--- SpeechGenerator (from_script): Preparing for {speaker} (part {i+1}): '{text[:50]}...' -> {output_filename} ---")
            try:
                self.tts_service.synthesize_speech(text, output_filename)
                audio_files.append(output_filename)
                # Added print from original full version
                print(f"--- SpeechGenerator (from_script): Successfully generated audio for {speaker} (part {i+1}): {output_filename} ---")
            except Exception as e:
                print(f"--- SpeechGenerator (from_script): Error for {speaker} (part {i+1}): {e} ---")
        # Added print from original full version
        print(f"--- SpeechGenerator (from_script): Finished. {len(audio_files)} audio files generated. ---")
        return audio_files
