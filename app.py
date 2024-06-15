from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('Model  files/popularity_based_model.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
book = pickle.load(open('book.pkl','rb'))
app = Flask(__name__)

@app.route('/')

def index():
    # render the UI template written in index.html file. 
    return render_template('index.html',
                           Book_name=list(popular_df['Book-Title'].values),
                           Book_author=list(popular_df['Book-Author'].values),
                           Book_image=list(popular_df['Image-URL-M'].values),
                           Book_no_rating=list(popular_df['Num_rating'].values),
                           Book_avg_rating=list(popular_df['Avg_rating'].values)
                           )


@app.route('/Recommender')
def Recommender_UI():
    # render the UI template written in Recommender.html file. 
    return render_template('recommender.html')

@app.route('/Recommend_books',methods=['post'])
def Recommed():
    User_input= request.form.get('User_input')
    '''
    This function takes book title as an input from user for making recommendations
    Arguments:
    book_title : title of the book
    '''
    if User_input == "":
        print("Enter the book name")
        return render_template('recommender.html',data=None)
    print(User_input)
    #for avoiding case sensitiveness
    book_title = User_input.upper()
    pt['title'] = pt.index  #copy all index(book titles) into a separate column book_title
    pt['title'] = pt['title'].str.upper()  #convert the entire book_title column to uppercase

    if book_title not in list(pt['title']):
        print("The book is not available")
        return render_template('recommender.html',data=None)
    else:
        print("The book is available")
        print("The recommendations are...")
        #index fetch of the entered title
        index_no_of_book = np.where(pt['title'] == book_title)[0][0]

        #Now access the similarity score vector at row no index,and find the 5 books with which the similarity score of the entered book is highest.
        sim_score_of_similar_books = sorted(list(similarity_scores[index_no_of_book]),key=lambda x:x, reverse = True)[1:6]   #[1:6]:the highest similarity of any book will be with itself, hence the book itself can't be recommended. Therefore, start from index 1 instead of 0 and go upto 5

        print(sim_score_of_similar_books)
        #find the index of each element of sim_score_of_similar_books in similarity_score matrix
        list_of_indexes = []
        for i in range(0,5):
            list_of_indexes.append(np.where(list(similarity_scores[index_no_of_book]) == sim_score_of_similar_books[i])[0][0])
            #print(list_of_indexes)
    
        #Return the original Book_Titles
        book_titles = list(pt.index[list_of_indexes])

        data=[] #list to store book-title, author, and image url of recommended books
        # Get more data about the book listed in book_titles
        for title in book_titles:
            item = []  # list to store book-title, author and image url of one book
            temp_df = book[book['Book-Title'] == title]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        print(data)
    return render_template('recommender.html',data=data)

if __name__== '__main__':
    app.run(debug=True)

    					