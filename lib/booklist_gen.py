import typing as t
from dataclasses import dataclass
import logging

@dataclass
class BookMeta:
    book_title: str
    book_file_path: str # book absolute path
    audio_file_path: str # audio absolute path


@dataclass
class BookList:
    version: str
    title: str
    created_at: str
    encoding: str
    book_meta_list: t.List[BookMeta]


def add_to_booklist(
    new_book_meta: BookMeta, 
    dest_booklist: BookList | None,
) -> BookList:
    new_dest_booklist: t.List[BookMeta] = dest_booklist.book_meta_list + [new_book_meta]
    return BookList(
        version=dest_booklist.version, 
        title=dest_booklist.title, 
        created_at=dest_booklist.created_at, 
        encoding=dest_booklist.encoding, 
        book_meta_list=new_dest_booklist)


def update_booklist(
    book_title: str, 
    book_file_path: str, 
    audio_file_path: str,
    booklist_file_path: str,
) -> None:
    new_book_meta: BookMeta = BookMeta(
        book_title=book_title, 
        book_file_path=book_file_path, 
        audio_file_path=audio_file_path,)
    booklist_node: BookList | None = parse_booklist(booklist_file_path)
    if booklist_node:
        booklist: BookList = add_to_booklist(new_book_meta, booklist_node)
    return None



def parse_booklist(booklist_file_path: str) -> BookList | None:
    
    return None


def render_booklist(booklist: BookList) -> str:    
    header = (
        f"#BOOKLIST\n"
        f"#VERSION: {booklist.version}\n"
        f"#TITLE: {booklist.title}\n"
        f"#CREATED: {booklist.created_at}\n"
        f"#ENCODING: {booklist.encoding}\n")
    
    body = "\n".join([
        f"#EXTBOOK: {item.book_title}\n"
        f"{item.book_file_path}\n"
        f"#EXTAUDIO: {item.audio_file_path}\n"
        for item in booklist.book_meta_list])
    return (header + "\n" + body)


def commit_booklist(booklist: BookList, book_list_file_path: str) -> None:
    booklist_str = render_booklist(booklist)
    try:
        with open(book_list_file_path, "w") as f:
            f.write(booklist_str)
            f.close()
    except:
        logging.error("Unable to commit booklist.")
    return None