from flask import Flask, render_template, request
import mysql.connector

# Load your data


app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password",
        database="erp"
    )
    return conn

@app.route('/')
def home():
    return render_template('bujus clone.html')

@app.route('/assignments')
def assignments():
    return render_template('HomeWork.html')

@app.route('/lessons')
def lessons():
    return render_template('videos.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/recommend', methods=['GET'])
@app.route('/recommend', methods=['GET', 'POST'])
def recommend_concepts():
    if request.method == 'POST':
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        df = pd.read_excel('sr.xlsx')
        concept_matrix = df.pivot_table(index='Concepts', columns='Subjects', fill_value=0)
        tfidf_vectorizer = TfidfVectorizer()
        X_tfidf = tfidf_vectorizer.fit_transform(df['Concepts'])
        similarity_matrix = cosine_similarity(concept_matrix)
        concept = request.form.get('topic')  # Use form.get for POST data
        if not concept or concept not in concept_matrix.index:
            return render_template('recomend.html', recommendations=[])
        
        index = concept_matrix.index.get_loc(concept)
        similar_concepts = similarity_matrix[index]
        top_similar_indices = similar_concepts.argsort()[-4:][:-1]  # Exclude the concept itself
        recommended_concepts = concept_matrix.index[top_similar_indices]
        
        return render_template('recomend.html', recommendations=recommended_concepts)
    
    return render_template('recomend.html', recommendations=[])  # For GET requests
@app.route('/report')
def report_card():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT name, marks FROM course, exam_result WHERE student_id=1 AND course.course_id=exam_result.course_id;"""
    cursor.execute(query)
    res = cursor.fetchall()
    report_data = [{"subject": row[0], "marks": row[1]} for row in res]
    cursor.close()
    conn.close()  # Close the connection after the query
    return render_template('report.html', report_data=report_data)

@app.route('/attendance')
def attendance():
    attendance_data = [
        {"sno": 1, "subject": "Maths", "attendance": "80%"},
        {"sno": 2, "subject": "Science", "attendance": "90%"},
        {"sno": 3, "subject": "CS", "attendance": "85%"},
    ]
    return render_template('attendance.html', attendance_data=attendance_data)

@app.route('/details')
def details():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT * FROM student WHERE student_id=1;"""
    cursor.execute(query)
    res = cursor.fetchall()
    student = {
        "id": res[0][0],
        "email": res[0][1],
        "fname": res[0][2],
        "lname": res[0][3],
        "dob": res[0][4],
        "phone": res[0][5],
        "mobile": res[0][6]
    }
    cursor.close()
    conn.close()  # Close the connection after the query
    return render_template('details.html', student=student)

@app.route('/work')
def work():
    assignments_data = [
        {"title": "Assignment 1", "link": "#assignment-1"},
        {"title": "Assignment 2", "link": "#assignment-2"},
    ]
    return render_template('work.html', assignments_data=assignments_data)

if __name__ == '__main__':
    app.run(debug=True)
