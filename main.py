from lib import *


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
        print(sentence_list)
        pdf_audio_bind: PDFAudioBind | None = generate_audio_file(abs_file_path, sentence_list)
        print(pdf_audio_bind)
        return 0


if __name__ == "__main__":
    main(sys.argv)


