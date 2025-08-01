import nltk
import sys
import typing as t
import logging
import fitz

import numpy as np
from bark.generation import (
    generate_text_semantic,
    preload_models,
)
from bark.api import semantic_to_waveform
from bark import generate_audio, SAMPLE_RATE
from scipy.io.wavfile import write as write_wav
from dataclasses import dataclass


nltk.download('punkt_tab')

# I will revisit this to normalize it as I understand the data
@dataclass
class PDFAudioDenorm: 
    file_path: str
    audio_file_path: str
    


def get_pdf_content(pdf_file_path: str) -> str | None:
    """
    Parse PDF and extract the content in the PDF as str of texts 
    Args:
        pdf_file_path (str): The input text to be processed.
    Returns:
        str | None: The generated response.
    """
    print("Chunking files...")
    try:
        pdf_content: str = ""
        with fitz.open(pdf_file_path) as f:
            doc: t.Any = f
            # f.close()
            for page in doc:
                pdf_content += f"{page.get_text()}\n"
        return pdf_content
    except:
        return None


def generate_sentences(pdf_content: str) -> t.List[str]:
    """
    Generate sentences from pdf_content
    Args:
        pdf_content (str): The input text to be processed.
    Returns:
        PDFAudioDenorm | None: The generated audio file.

    """
    _pdf_content = pdf_content.replace("\n", " ").strip()    
    return nltk.sent_tokenize(_pdf_content) 


def generate_audio_file(
    file_path: str, 
    sentence_list: t.List[str], 
    device: str="cpu", 
    tts_model: str="v2/en_speaker_6",
    gen_temp = 0.6,
) -> PDFAudioDenorm | None:
    """
    Generate audio files from sentence_list
    Args:
        file_path (str): The input text to be processed.
        sentence_list (List[str]): The input text to be processed.
    Returns:
        PDFAudioDenorm | None: The generated audio file.

    """
    try:
        silence = np.zeros(int(0.25 * SAMPLE_RATE))
        pieces = []
        for sentence in sentence_list:
            semantic_tokens = generate_text_semantic(
                sentence,
                history_prompt=tts_model,
                temp=gen_temp,
                min_eos_p=0.05,
            )
            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=tts_model)
            pieces += [audio_array, silence.copy()]
        write_wav(f"output/sample.wav", SAMPLE_RATE, audio_array) # side-effect
        return PDFAudioDenorm(
            file_path, 
            f"output/sample.wav") # I will revisit the output file
    except:
        return None




def main(argv: t.List[str]) -> int:
    if len(argv) != 2:
        logging.error("Invalid command.")
        print("Usage: python main.py <file_path>")
        return 1
    else:
        file_path: str = argv[1]
        pdf_chunks: str | None = get_pdf_content(file_path)
        sentence_list: t.List[str] = generate_sentences(pdf_chunks) if pdf_chunks else []
        generate_audio_file(file_path, sentence_list)
        return 0


if __name__ == "__main__":
    main(sys.argv)


