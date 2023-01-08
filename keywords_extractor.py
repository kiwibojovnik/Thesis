from multi_rake import Rake

rake = Rake(
    min_chars=3,
    max_words=3,
    min_freq=1,
    language_code="cs",  # 'en'
    stopwords=None,  # {'and', 'of'}
    lang_detect_threshold=50,
    max_words_unknown_lang=2,
    generated_stopwords_percentile=80,
    generated_stopwords_max_len=1,
    generated_stopwords_min_freq=2,
)

def open_file(filename):
    """Function for opening file with article"""
    with open(filename, "r", encoding="utf8") as saved_links:
        full_text = saved_links.read()
    return full_text

def extract_keywords(filename):
    """Function for extracting keywords"""
    full_text = open_file(filename)
    rake = Rake()
    keywords = rake.apply(full_text)
    print(keywords[:4])



extract_keywords("newarticle.txt")
