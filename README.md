# py_audiobook
I just want to listen to my PDFs

## How to use it
1. Install Python3 (python 3.11+ preferably)
2. Create a virtual environment
```sh
python -m venv env
```
then activate the virtual environment, by running this
> for unix-based systems (linux and macOS)
```
source env/bin/activate
```
3. Install the necessary requirements with
```sh
pip install -r requirements.txt
```
4.  Open your terminal and run
```sh
python main.py <pdf_file_path>
```
> [!Note]
> <pdf_file_path> is a placeholder for the path the pdf file
> This is a prototype, I intend to move the code to C (not C++ 😏)