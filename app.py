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
        comments = text.split('\n')

        try:
            for comment in comments:
                db.session.add(Comment(text=comment))
            db.session.commit()
            return redirect('/result')
        except:
            return 'Error'
    else:
        return render_template("index.html")


@app.route('/result')
def result():
    comments = Comment.query.all()
    return render_template('result.html', comments=comments)

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
        return "error"


if __name__ == '__main__':
    app.run(debug=True)
