from app import db

class Detected(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label_description = db.Column(db.String(256), index=True)
    label_category = db.Column(db.String(256))
    start_time = db.Column(db.Float)
    end_time = db.Column(db.Float)
    confidence = db.Column(db.Float)

    def __repr__(self):
        return '<Detected {}>'.format(self.label_description) 