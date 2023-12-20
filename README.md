[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<h1 align="center">Undr Wolf Realtime STT</h1>
Undr Wolf is a chess game designed for players seeking to enhance their skills in blindfold chess. This speech to text package is created as a feature for the game. Current alpha build only works with apple silicon computers. 

#### Follow the journey on: 
[Youtube](https://www.youtube.com/@UndrWolf) 
<br> [Logbook](https://kfmh.github.io/) 
<br> [uw_chess repository](https://github.com/kfmh/uw_chess) 

<!--
<p align="center">
    <br>
    <img src="" width="500px"/>
    <br>
    Chessboard coordinates difficulty
    <img src="" width="80%"/>
    <br>
<p>
-->

## Requierements 
Apple Metal GPU

## Installation Mac with apple silicon
1. From terminal create a directory
```bash
mkdir <directory_name>
cd <directory_name>
``` 
2. Create and activate an environment
```bash
# Python environment
python3 -m venv <enviroment_neme>
source <enviroment_neme>/bin/activate
```
```bash
# Anaconda environment
conda create -n <enviroment_neme>
conda activate <enviroment_neme>
```
3. Install uw_chess package
```bash
# Pip install package directly from main branch
pip install git+https://github.com/kfmh/uw_realtime_stt.git
```

## Usage
<!-- Command line parsing.
| Long Flag | Short Flag | Default | Description |
|----------|----------|----------|----------|
| --engine_path           | -p   | None | File path to chess engin |
-->


Start program
```bash
# Run program
uw_realtime_stt
```

Quit program: ctrl + c


<!--
## Documentation
-->


