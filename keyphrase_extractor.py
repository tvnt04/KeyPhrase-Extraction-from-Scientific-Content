import nltk
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Ensure necessary resources are downloaded
nltk.data.path.append('/home/bonebreaker/nltk_data')  # Ensure it looks in the correct directory

nltk.download("stopwords", download_dir="/home/bonebreaker/nltk_data")
nltk.download("punkt", download_dir="/home/bonebreaker/nltk_data")
nltk.download("wordnet", download_dir="/home/bonebreaker/nltk_data")
nltk.download("averaged_perceptron_tagger", download_dir="/home/bonebreaker/nltk_data")

def preprocess_text(text):
    """Cleans the text: removes numbers, punctuation, and stopwords."""
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words("english")]
    return " ".join(words)

def extract_keyphrases(text, num_phrases=10):
    """Extracts top keyphrases using TF-IDF, gets definitions from WordNet, and adds POS tagging."""
    processed_text = preprocess_text(text)
    words = word_tokenize(processed_text)
    pos_tags = dict(pos_tag(words))  # Store POS tagging

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text])
    feature_array = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    ranked_phrases = sorted(zip(feature_array, scores), key=lambda x: x[1], reverse=True)[:num_phrases]

    phrases_with_details = {}
    for phrase, _ in ranked_phrases:
        definition = wordnet.synsets(phrase)
        phrases_with_details[phrase] = {
            "definition": definition[0].definition() if definition else "No definition available.",
            "pos": pos_tags.get(phrase, "N/A")  # Get POS tag or default to "N/A"
        }

    return phrases_with_details
