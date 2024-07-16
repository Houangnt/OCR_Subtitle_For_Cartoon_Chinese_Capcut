conda create --name OCR-China python=3.8 <br>
conda activate OCR-China <br>
pip install -r requirements.txt

### Run OCR for video
-Case 1: With low subtitle run: <br>
python main.py --format 1  <br>
-Case 2: With high subtitle run: <br>
python main.py --format 2 

### Export to output capcut format
python postprocess.py

### Optimize srt format
python capcut.py

### Demo output capcut format
![res](https://github.com/Houangnt/OCR_Subtitle_For_Cartoon_Chinese_Capcut/blob/main/output.png?raw=true)
