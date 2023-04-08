from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spam.db'
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        input_comments = text.split('\n')

        try:
            for comment in input_comments:
                db.session.add(Comment(text=comment))
            db.session.commit()
            comments = Comment.query.all()
            comments = [comment.text for comment in comments]
            comments = np.array(comments)
            predict = model.predict(comments)
            result = []
            for i in range(len(comments)):
                result.append((comments[i], predict[i]))
            # TODO: Implement ml model
            # comments -- predict set
            # make a result list of tuples (comment, spam: bool)
            return render_template('index.html', result=result)
        except:
            return 'Error'
    else:
        return render_template("index.html")


@app.route('/delete')
def delete():
    comments = Comment.query.all()
    try:
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()
        return "Error"


if __name__ == '__main__':
    app.run(debug=True)