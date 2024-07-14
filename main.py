import cv2
from paddleocr import PaddleOCR
import os
import CharSimilarity

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def char_similarity(str1, str2):
    if not str1 or not str2:
        return 0.0
    return CharSimilarity.similarity(str1, str2, tone=True, shape=False)

def extract_frames(video_path, output_folder, frames_per_second=4):
    cap = cv2.VideoCapture(video_path)
    count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frames_per_second)

    success, image = cap.read()
    while success:
        frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if frame_id % interval == 0:
            cropped_image = crop_subtitle(image)
            cv2.imwrite(os.path.join(output_folder, f"frame_{count}.jpg"), cropped_image)
            count += 1
        success, image = cap.read()
    cap.release()

def crop_subtitle(image):
    height, width, _ = image.shape
    crop_top = int(height * 0.85)
    crop_bottom = height
    crop_left = 0
    crop_right = width
    cropped_image = image[crop_top:crop_bottom, crop_left:crop_right]
    return cropped_image

def process_frames(frames_folder, output_file, frames_per_second):
    last_written_text = ""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        index = 1
        for frame_name in sorted(os.listdir(frames_folder), key=lambda x: int(x.split('_')[1].split('.')[0]) if 'frame_' in x else float('inf')):
            if frame_name.endswith('.jpg') and 'frame_' in frame_name:
                frame_path = os.path.join(frames_folder, frame_name)
                img = cv2.imread(frame_path)
                results = ocr.ocr(img)

                if results and len(results) > 0:
                    result_list = results[0]
                    if result_list:
                        text_list = [box[1][0] for box in result_list]
                    else:
                        text_list = []
                else:
                    text_list = []

                frame_number = int(frame_name.split('_')[1].split('.')[0])
                start_time = frame_number / frames_per_second
                end_time = start_time + 1 / frames_per_second

                for text in text_list:
                    similarity = char_similarity(text, last_written_text)
                    
                    if similarity < 0.85:
                        start_hours = int(start_time // 3600)
                        start_minutes = int((start_time % 3600) // 60)
                        start_seconds = int(start_time % 60)
                        start_milliseconds = int((start_time % 1) * 1000)

                        end_hours = int(end_time // 3600)
                        end_minutes = int((end_time % 3600) // 60)
                        end_seconds = int(end_time % 60)
                        end_milliseconds = int((end_time % 1) * 1000)

                        time_format = f"{start_hours:02}:{start_minutes:02}:{start_seconds:02},{start_milliseconds:03} --> {end_hours:02}:{end_minutes:02}:{end_seconds:02},{end_milliseconds:03}"

                        f.write(f"{index}\n")
                        f.write(f"{time_format}\n")
                        f.write(text + '\n')
                        f.write('\n')
                        
                        last_written_text = text
                        index += 1

video_path = 'video/Video1.mp4'
frames_folder = 'frames'
output_file = 'output.srt'

if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

frames_per_second = 5
extract_frames(video_path, frames_folder, frames_per_second)
process_frames(frames_folder, output_file, frames_per_second)

print("Hoàn thành trích xuất phụ đề!")
