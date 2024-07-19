import os
import CharSimilarity
import sijiao_dict
from googletrans import Translator
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')  # if necessary...

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]

def translate_subtitle(text, src_lang='zh-CN', dest_lang='en'):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def similarity(x, y):
    """ 
    Returns the similarity between two lists.
    
    Parameters:
    x (list): First list of elements.
    y (list): Second list of elements.
    
    Returns:
    float: Jaccard similarity between two lists.
    """
    intersection_cardinality = len(set(x).intersection(set(y)))
    union_cardinality = len(set(x).union(set(y)))
    if union_cardinality == 0:
        return 0.0
    return intersection_cardinality / float(union_cardinality)

def map_characters_to_numbers(text, char_map):
    """
    Map characters in the input text to their corresponding numbers using the provided character map.
    
    Parameters:
    text (str): Input string with Chinese characters.
    char_map (dict): Dictionary mapping Chinese characters to numbers.
    
    Returns:
    list: List of numbers corresponding to the input characters.
    """
    return [char_map[char] for char in text if char in char_map]

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
        
        # Check if the current end time is greater than the new start time and adjust if needed
        if current_end and start_time <= current_end:
            start_time = current_end
            
        if current_text is None:
            current_start = start_time
            current_end = end_time
            current_text = text
        elif (similarity(map_characters_to_numbers(current_text, sijiao_dict.dic), map_characters_to_numbers(text, sijiao_dict.dic)) == 1 or 
              cosine_sim(translate_subtitle(text), translate_subtitle(current_text)) == 1):
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
