from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template, request, Flask, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client = db.Column(db.String(80), nullable=False)
    client_priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_area = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Feature %r>' % self.title


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/feature_requests")
def show_requests():
    features = Feature.query.all()
    return render_template('feature_requests.html', result=features)


@app.route("/submit_request", methods=['POST',])
def submit_request():
    data = request.form
    print data
    new_feature = Feature(title=data['title'],
                          description=data['description'],
                          client=data['client'],
                          client_priority=int(data['client_priority']),
                          target_date=datetime.strptime(data['target_date'],'%Y-%m-%d'),
                          product_area=data['productArea'])
    db.session.add(new_feature)
    db.session.commit()
    return redirect("/")