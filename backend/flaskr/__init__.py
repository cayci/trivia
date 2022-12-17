import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*10
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    cors = CORS(app, resouces={r"/api/*": {"origins": "*"}})

    """
    DONE
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('ACCESS-CONTROL-ALLOW-HEADERS','Content-Type,Authorization,true')
        response.headers.add('ACCESS-CONTROL-ALLOW-METHODS','GET, PUT, POST, DELETE, OPTIONS')
        return response

    """
    DONE
    @TODO:Create an endpoint to handle GET requests for all categories.
    """
    
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        body=request.get_json()
        categories = Category.query.order_by(Category.id).all()

        cat_dict = {}
        for cat in categories:
            cat_dict[cat.id] = cat.type
        
        if len(categories) == 0:
            abort(404)

        return jsonify({
            'categories': cat_dict
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    
    @app.route('/questions', methods=['GET', 'DELETE', 'POST'])
    def get_all_questions():
        body=request.get_json()
        selection = Question.query.order_by(Question.id).all()
        data=[]                                    
        for q in selection:
            data.append({
               "id": q.id,
               "name": q.question,
               "answer": q.answer,
               "difficulty": q.difficulty,
               "category": q.category
            })                                 
        
        if len(selection) == 0:
            abort(404)
        
        json_formatted_questions = [question.format() for question in selection]
        return jsonify({
            'success': True,
            'questions': json_formatted_questions,
            'total_questions': len(selection)
        })
          
       
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO: Create an endpoint to DELETE question using a question ID.
    DONE
    """
                                            
    def delete_a_question():
        
        selection = Question.query.order_by(Question.id).all()
        current_questions=paginate_questions(request, selection)
            
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': l0 + QUESTIONS_PER_PAGE
        })
    
    """
    TEST: Click trash icon next to a question to removed the ?
    This removal will persist in the DB and when you refresh the page.
    """

    """  
    @TODO: Create an endpoint to POST a new question
    DONE
    """
    
    @app.route('/questions/create', methods=['POST'])
    def create_question():
        id = request.get('id')
        question = request.get('question')
        answer = request.get('answer')
        difficulty = request.get('difficulty')
        category = request.get('category')
                                            
        new_question = Question(id=id, question=question, answer=answer, difficulty=difficulty, category=category)
                                            
        db.session.add(new_question)
        db.session.commit()
    
    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    def 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
