import os
import nltk
import sys
import typing as t
import logging
import fitz
from enum import Enum, IntEnum

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
from transformers import AutoProcessor, BarkModel
import torch
import pathlib as p


if not p.Path().home().joinpath("nltk_data").is_dir():
    nltk.download('punkt_tab')


@dataclass
class PDFAudioBind: 
    file_path: str
    audio_file_path: str
    


def get_pdf_content(pdf_file_path: str) -> str | None:
    """Parse PDF and extract the content in the PDF as str of texts 
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
    """Generate sentences from pdf_content
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
    tts_model_path: str="suno/bark-small",
    device: str="cpu", 
    voice_preset: str="v2/en_speaker_6",
    target_dir: str="output",
) -> PDFAudioBind | None:
    """Generate audio files from sentence_list
    Args:
        file_path (str): The file path.
        sentence_list (List[str]): The list of sentences.
    Returns:
        PDFAudioBind | None: The generated audio file.
    """
    try:
        device: str = device
        model: BarkModel = BarkModel.from_pretrained(tts_model_path,)
        processor: t.Any = AutoProcessor.from_pretrained(tts_model_path,)
        model.to(device)
        sample_rate = model.generation_config.sample_rate
        silence = np.zeros(int(0.25 * sample_rate))
        pieces = []
        for sentence in sentence_list:
            inputs_ = processor(sentence, voice_preset=voice_preset, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs_.items()}
            
            with torch.no_grad():
                audio_array = model.generate(**inputs, pad_token_id=10000)

            audio_array = audio_array.cpu().numpy().squeeze()
            pieces += [audio_array, silence.copy()]
        write_wav(f"{target_dir}/{get_pdf_filename_unix(file_path)}.wav", sample_rate, np.concatenate(pieces)) # side-effect
        return PDFAudioBind(
            file_path, 
            f"{target_dir}/{get_pdf_filename_unix(file_path)}.wav") # I will revisit the output file
    except:
        return None


# unix-path
def get_pdf_filename_unix(file_path: str) -> str:
    """Get PDF file name from file path
    Args:
        file_path (str): The file path.
    Returns:
        str: filename
    """
    file_path_list = file_path.split("/")
    filename_list = file_path_list[len(file_path_list) - 1].split(".")
    filename = ".".join(filename_list[:len(filename_list) - 1])
    return filename