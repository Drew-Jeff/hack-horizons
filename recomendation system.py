import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import messagebox, simpledialog

df = pd.read_excel('sr.xlsx')
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(df['Concepts'])
concept_matrix = df.pivot_table(index='Concepts', columns='Subjects', fill_value=0)
similarity_matrix = cosine_similarity(concept_matrix)

def recommend_concepts(concept):
    if concept not in concept_matrix.index:
        return None
    index = concept_matrix.index.get_loc(concept)
    similar_concepts = similarity_matrix[index]
    top_similar_indices = similar_concepts.argsort()[-4:][:-1]
    recommended_concepts = concept_matrix.index[top_similar_indices]
    return recommended_concepts.tolist()

def show_recommendations():
    concept = simpledialog.askstring("Input", "Enter a concept:")
    if concept:
        recommendations = recommend_concepts(concept)
        if recommendations:
            messagebox.showinfo("Recommendations", "\n".join(recommendations))
        else:
            messagebox.showwarning("Not Found", "Concept not found.")

root = tk.Tk()
root.title("Concept Recommendation System")
root.geometry("300x150")

recommend_button = tk.Button(root, text="Get Recommendations", command=show_recommendations)
recommend_button.pack(pady=20)

root.mainloop()
