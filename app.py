from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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
        # TODO: split this text with \n as delimiter
        comment = Comment(text=text)

        try:
            db.session.add(comment)
            db.session.commit()
            return redirect('/result')
        except:
            return 'Error'

    else:
        return render_template('index.html')


@app.route('/result')
def result():
    comments = Comment.query.all()
    return render_template('result.html', comments=comments)


# TODO: delete all the records in the table

if __name__ == '__main__':
    app.run(debug=True)
