import sys
import typing as t
import logging


class PDFChunks:
    order_list_of_paragraphs : t.List[str]


def chunk_pdf_files(pdf_file_path: str) -> t.List[str]:
    print("Chunking files...")
    return None



def main(argv: t.List[str]) -> int:
    if (len(argv) != 3):
        logging.error("Invalid command.")
        print("Usage: python main.py <file_path>")
        return 1
    else:
        file_path: str = argv[1]
        pdf_chunks : t.List[str] = chunk_pdf_files(file_path)
        return 0


if __name__ == "__main__":
    main(sys.argv)


