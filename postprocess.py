import re

def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def write_srt(lines, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def convert_time_to_ms(time_str):
    hours, minutes, seconds, milliseconds = map(int, re.split('[:,]', time_str))
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    return total_ms

def convert_ms_to_time(ms):
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'

def adjust_subtitle_times(lines):
    adjusted_lines = []
    for i in range(len(lines)):
        if '-->' in lines[i]:
            start_time, end_time = lines[i].split(' --> ')
            start_time_ms = convert_time_to_ms(start_time.strip())
            
            if i + 4 < len(lines) and '-->' in lines[i + 4]:
                next_start_time = lines[i + 4].split(' --> ')[0].strip()
                next_start_time_ms = convert_time_to_ms(next_start_time)
                new_end_time_ms = max(start_time_ms + 50, next_start_time_ms - 50)
                new_end_time = convert_ms_to_time(new_end_time_ms)
                adjusted_lines.append(f'{start_time.strip()} --> {new_end_time}\n')
            else:
                new_end_time_ms = start_time_ms + 2000  # Thêm 2 giây cho dòng cuối
                new_end_time = convert_ms_to_time(new_end_time_ms)
                adjusted_lines.append(f'{start_time.strip()} --> {new_end_time}\n')
        else:
            adjusted_lines.append(lines[i])
    
    return adjusted_lines


def process_srt_file(input_path, output_path):
    lines = read_srt(input_path)
    adjusted_lines = adjust_subtitle_times(lines)
    write_srt(adjusted_lines, output_path)

# Đường dẫn tệp đầu vào và đầu ra
input_srt_path = 'output.srt'
output_srt_path = 'output_post.srt'

# Thực hiện xử lý
process_srt_file(input_srt_path, output_srt_path)
