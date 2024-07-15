import os
import CharSimilarity  

def char_similarity(str1, str2):
    if not str1 or not str2:
        return 0.0
    return CharSimilarity.similarity(str1, str2, tone=True, shape=False)

def merge_subtitles(srt_content):
    subtitles = srt_content.strip().split('\n\n')
    
    merged_subtitles = []
    current_start = None
    current_end = None
    current_text = None
    
    for subtitle in subtitles:
        parts = subtitle.split('\n')
        if len(parts) < 3:
            continue
        number = parts[0]
        time_range = parts[1]
        text = ''.join(parts[2:])
        
        start_time, end_time = time_range.split(' --> ')
        
        if current_text is None:
            current_start = start_time
            current_end = end_time
            current_text = text
        elif char_similarity(current_text, text) == 1:
            current_end = end_time
        else:
            merged_subtitles.append(f'{len(merged_subtitles) + 1}\n{current_start} --> {current_end}\n{current_text}')
            current_start = start_time
            current_end = end_time
            current_text = text
    
    if current_text is not None:
        merged_subtitles.append(f'{len(merged_subtitles) + 1}\n{current_start} --> {current_end}\n{current_text}')
    
    return '\n\n'.join(merged_subtitles)

def process_srt_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.srt'):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)
            
            with open(input_file_path, 'r', encoding='utf-8') as file:
                srt_content = file.read()
            
            merged_srt_content = merge_subtitles(srt_content)
            
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(merged_srt_content)
    
    print("Processing completed!")

# Example usage
input_folder = 'srt_files_processed'
output_folder = 'capcut_format'

process_srt_files(input_folder, output_folder)
