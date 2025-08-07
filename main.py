import os
import nltk
import sys
import typing as t
import logging
import fitz

import numpy as np
from bark.generation import (
    generate_text_semantic,
    # preload_models,
)
from bark.api import semantic_to_waveform
from bark import (
    # generate_audio, 
    SAMPLE_RATE,
)
from scipy.io.wavfile import write as write_wav
from dataclasses import dataclass
import pathlib as p


nltk.download('punkt_tab')


@dataclass
class PDFAudioBind: 
    file_path: str
    audio_file_path: str
    


def get_pdf_content(pdf_file_path: str) -> str | None:
    """
    Parse PDF and extract the content in the PDF as str of texts 
    Args:
        pdf_file_path (str): PDF file path.
    Returns:
        str | None: The generated response.
    """
    try:
        pdf_content: str = ""
        with fitz.open(pdf_file_path) as f:
            doc: t.Any = f
            for page in doc:
                pdf_content += f"{page.get_text()}\n"
        return pdf_content
    except:
        return None


def generate_sentences(pdf_content: str) -> t.List[str]:
    """
    Generate sentences from pdf_content
    Args:
        pdf_content (str): Content of the PDF.
    Returns:
        PDFAudioBind | None: The generated audio file.
    """
    _pdf_content: str = pdf_content.replace("\n", " ").strip()    
    return nltk.sent_tokenize(_pdf_content) 


# unix-path
def generate_audio_file(
    file_path: str, 
    sentence_list: t.List[str], 
    device: str="cpu", 
    tts_model: str="v2/en_speaker_6",
    gen_temp: float=0.6,
    sample_rate: int=SAMPLE_RATE,
    target_dir: str="output"
) -> PDFAudioBind | None:
    """
    Generate audio files from sentence_list
    Args:
        file_path (str): The file path.
        sentence_list (List[str]): The list of sentences.
    Returns:
        PDFAudioBind | None: The generated audio file.
    """
    try:
        silence = np.zeros(int(0.25 * sample_rate))
        pieces = []
        for sentence in sentence_list:
            semantic_tokens: t.Any = generate_text_semantic(
                sentence,
                history_prompt=tts_model,
                temp=gen_temp,
                min_eos_p=0.05,)
            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=tts_model)
            pieces += [audio_array, silence.copy()] # interleave silence with generated speech
        write_wav(f"{target_dir}/{get_pdf_filename_unix(file_path)}.wav", sample_rate, audio_array) # side-effect
        return PDFAudioBind(
            file_path, 
            f"{target_dir}/{get_pdf_filename_unix(file_path)}.wav") # I will revisit the output file
    except:
        return None


# unix-path
def get_pdf_filename_unix(file_path: str) -> str:
    """
    Get PDF file name from file path
    Args:
        file_path (str): The file path.
    Returns:
        str: filename
    """
    file_path_list = file_path.split("/")
    file_name = file_path_list[len(file_path_list) - 1].replace(".", "__") # I will revisit this guy
    print(file_name)
    return file_name


def main(argv: t.List[str]) -> int:
    my_args = argv[1:]
    if len(my_args) != 1:
        logging.error("Invalid command.")
        print("Usage: python main.py <file_path>")
        return 1
    else:
        file_path: str = my_args[0]
        abs_file_path = str(os.path.abspath(file_path))
        pdf_chunks: str | None = get_pdf_content(abs_file_path)
        sentence_list: t.List[str] = generate_sentences(pdf_chunks) if pdf_chunks else []
        pdf_audio_bind: PDFAudioBind | None = generate_audio_file(abs_file_path, sentence_list)
        print(pdf_audio_bind)
        return 0


if __name__ == "__main__":
    main(sys.argv)


