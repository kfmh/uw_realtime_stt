# ============================================================================
# print_document.py
# 
# ============================================================================

from runtime_test import LogExecutionTime
import os
    
class Create_Document:
    def __init__(self, title="stt_doc"):
        self.file         = f"./print_documents/{title}.txt"
        self.string_obj   = ""

    def clear_screen(self):
        clear = os.system('cls' if os.name == 'nt' else 'clear')
        return clear

    def document(self, words:str, cli_print:bool = True):
        self.string_obj += f"[ {words}]"
        self.clear_screen()

        if cli_print:
            print(self.string_obj)
