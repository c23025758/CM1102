'''Script to populate the database with some initial data.
   In reality you would probably create a separate editor or a tool for importing data from elsewhere,
   but for CM1102 we'll just use this script to populate the database.'''

from app4 import app, db, Book

with app.app_context():
    db.drop_all()  
    db.create_all()  
    
    books = [
        { "name": "1984", "price": 7.50, "description": "1984 is a dystopian novel by George Orwell. It depicts a totalitarian regime and explores themes of surveillance, propaganda, and individual freedom.", "environmental_impact": "Low" },
        { "name": "Great Gatsby", "price": 9.00, "description": "The Great Gatsby is a novel by F. Scott Fitzgerald set in the Jazz Age. It explores themes of wealth, love, and the American Dream.", "environmental_impact": "Moderate" },
        { "name": "High Rise Building", "price": 11.25, "description": "High Rise Building is a novel by J.G. Ballard depicting a luxury apartment building. It delves into themes of class, isolation, and societal breakdown.", "environmental_impact": "High" },
        { "name": "Little Life", "price": 8.50, "description": "A Little Life is a novel by Hanya Yanagihara. It follows the lives of four friends in New York City and deals with themes of trauma, friendship, and identity.", "environmental_impact": "Low" },
        { "name": "To Kill a Mockingbird", "price": 10.50, "description": "To Kill a Mockingbird is a novel by Harper Lee. Set in the 1930s in the Southern United States, it addresses issues of racial injustice and moral growth through the eyes of a young girl, Scout Finch.", "environmental_impact": "Moderate" },
        { "name": "A Thousand Splendid Suns", "price": 11.00, "description": "A Thousand Splendid Suns is a novel by Khaled Hosseini. It tells the story of two Afghan women and their struggles against the backdrop of political turmoil and war.", "environmental_impact": "High" }
    ]

    for book_data in books:
        existing_book = Book.query.filter_by(name=book_data["name"]).first()
        if not existing_book:
            book = Book(name=book_data["name"], price=book_data["price"], description=book_data["description"], environmental_impact=book_data["environmental_impact"])
            db.session.add(book)
    
    db.session.commit()
