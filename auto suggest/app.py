from flask import Flask, Blueprint,render_template, request, redirect, url_for
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
recommender_bp = Blueprint('recommender_bp', __name__, template_folder='templates')
# Load dataset
try:
    df = pd.read_json('Concepts_Dataset.json')
except ValueError as e:
    print("Error loading JSON file:", e)
    df = pd.DataFrame(columns=['Concept', 'Video Link', 'Popularity Score'])

# Drop rows with missing concepts or video links
df = df.dropna(subset=['Concept', 'Video Link'])

# Store concept information in a dictionary
concept_info = df.set_index('Concept').T.to_dict()

# Compute TF-IDF matrix and similarity
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(df['Concept'])
concepts = df['Concept'].tolist()
similarity_matrix = cosine_similarity(X_tfidf)

# Recommender function
def recommend_concepts(concept):
    if concept not in concepts:
        return None
    index = concepts.index(concept)
    similar_concepts = similarity_matrix[index]
    top_similar_indices = similar_concepts.argsort()[-5:][:-1][::-1]  # Top 3 excluding self
    recommended_concepts = [concepts[i] for i in top_similar_indices[:3]]
    recommended_info = [{
        "Concept": rec,
        "Video Link": concept_info[rec]["Video Link"],
        "Popularity Score": concept_info[rec]["Popularity Score"]
    } for rec in recommended_concepts]
    return recommended_info

# NEW: Function to get similarity scores for a given concept
def get_similar_with_scores(concept):
    if concept not in concepts:
        return []
    index = concepts.index(concept)
    similar_concepts = similarity_matrix[index]
    top_similar_indices = similar_concepts.argsort()[-5:][:-1][::-1]
    results = []
    for i in top_similar_indices[:3]:
        results.append({
            "Concept": concepts[i],
            "Score": round(similar_concepts[i], 2)
        })
    return results

@recommender_bp.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    if request.method == 'POST':
        concept = request.form['concept']
        recommendations = recommend_concepts(concept)
        if recommendations is None:
            recommendations = [{
                "Concept": "Concept not found.",
                "Video Link": "#",
                "Popularity Score": "N/A"
            }]
    return render_template('index.html', recommendations=recommendations)

@recommender_bp.route('/play_video')
def play_video():
    video_link = request.args.get('video_link')
    concept = request.args.get('concept')

    if not video_link or not concept:
        return "Video link or concept missing.", 400

    # Clean YouTube links
    if "watch?v=" in video_link:
        video_link = video_link.replace("watch?v=", "embed/")

    # Get 3 similar recommendations
    recommendations = recommend_concepts(concept)

    return render_template('video.html', video_link=video_link, concept=concept, recommendations=recommendations)



