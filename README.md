conda create --name OCR-China python=3.8 <br>
conda activate OCR-China <br>
pip install -r requirements.txt

### Run OCR for video
python main.py 

### Export to output capcut format
python postprocess.py

### Demo output capcut format
![res](https://github.com/Houangnt/OCR_Subtitle_For_Cartoon_Chinese_Capcut/blob/main/output.png?raw=true)
