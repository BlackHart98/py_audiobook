import typing as t
from dataclasses import dataclass

@dataclass
class BookMeta:
    book_title: str
    book_file_path: str # book absolute path
    audio_file_path: str # audio absolute path


@dataclass
class BookList:
    version: str
    booklist_title: str
    book_meta_list: t.List[BookMeta]


def add_to_booklist(
    new_book_meta: BookMeta, 
    dest_booklist: BookList | None,
) -> BookList:
    new_dest_booklist: t.List[BookMeta] = dest_booklist.book_meta_list + [new_book_meta]
    return BookList(
        version=dest_booklist.version, 
        booklist_title=dest_booklist.booklist_title, 
        book_meta_list=new_dest_booklist)


def commit_to_booklist(
    book_title: str, 
    book_file_path: str, 
    audio_file_path: str,
    book_list_file_path: str,
) -> None:
    new_book_meta: BookMeta = BookMeta(
        book_title=book_title, 
        book_file_path=book_file_path, 
        audio_file_path=audio_file_path)
    booklist_node: BookList | None = parse_booklist(book_list_file_path)
    if booklist_node:
        booklist: BookList = add_to_booklist(new_book_meta, booklist_node)
    return None



def parse_booklist(book_list_file_path: str) -> BookList | None:
    
    return None