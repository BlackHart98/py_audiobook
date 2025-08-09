import os
import sys
import logging
import typing as t
from lib import *
import pathlib as p
import pygame
import pygame_gui


# def main(argv: t.List[str]) -> int:
#     my_args = argv[1:]
#     if len(my_args) != 1:
#         logging.error("Invalid command.")
#         print("Usage: python main.py <file_path>")
#         return 1
#     else:
#         file_path: str = my_args[0]
#         if not p.Path(file_path).exists():
#             logging.error("File does not exist.")
#             return 1
#         abs_file_path: str = str(os.path.abspath(file_path))
#         pdf_chunks: str | None = get_pdf_content(abs_file_path)
#         sentence_list: t.List[str] = generate_sentences(pdf_chunks) if pdf_chunks else []
#         pdf_audio_bind: PDFAudioBind | None = generate_audio_file(abs_file_path, sentence_list)
#         print(pdf_audio_bind)
#         return 0




# up next the simple ui 
def main(argv: t.List[str]) -> int:
    pygame.init()
    pygame.display.set_caption('pyAudiobook')
    window_surface = pygame.display.set_mode((800, 600))
    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#FFFFFF'))
    
    manager = pygame_gui.UIManager((800, 600))
    create_audiobook = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (200, 50)),
        text='Create audiobook',
        manager=manager,
    )
    is_running = True

    clock = pygame.time.Clock()    
    
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == create_audiobook:
                    print('Hello World!')
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()
    return 0


if __name__ == "__main__":
    main(sys.argv)


