from flask import Flask,render_template,request
import pickle
import numpy as np

with open('popular.pkl','rb') as f:
    popular_df = pickle.load(f)

with open('pt.pkl','rb') as f:
    pt = pickle.load(f)

with open('similarity.pkl','rb') as f:
    similarity = pickle.load(f)

with open('books.pkl','rb') as f:
    books = pickle.load(f)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title']),
                           image = list(popular_df['Image-URL-M']),
                           author = list(popular_df['Book-Author']),
                           votes = list(popular_df['num_rating']),
                           rating = list(popular_df['avg_rating']),
                           
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index== user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:5]
    data =[]
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        items.extend(list(temp_df['Book-Title'].values))
        items.extend(list(temp_df['Book-Author'].values))
        items.extend(list(temp_df['Image-URL-M'].values))

        data.append(items)
    
    return render_template('recommend.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)