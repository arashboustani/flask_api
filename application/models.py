from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class tor_ip_model(db.Model):
    __tablename__ = 'tor_ip'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True, )
    ip = db.Column("ip", db.Text, nullable=False)

    def __init__(self, ip):
        self.ip = ip

    def __repr__(self):
        return str({'ip':self.ip})

    @property
    def serialize(self):
        return {'ip':self.ip}
