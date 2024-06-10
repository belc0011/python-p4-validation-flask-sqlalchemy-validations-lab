from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    
    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if not len(number) == 10:
            raise ValueError('Phone number must be 10 digits')
        for char in number:
            int(char)
        return number
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name must be non-empty string")
        existing_name = Author.query.filter_by(name=name).first()
        if (existing_name):
            raise ValueError("Two authors can not have same name")
        return name
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Must be at least 250 characters")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Can not be more than 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if not category == 'Fiction' and not category == 'Non-Fiction':
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        no_keyword = True
        keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        for keyword in keywords:
            if keyword in title:
                no_keyword = False
        if (no_keyword):
            raise ValueError('Not click-baity enough')
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
