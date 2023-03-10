import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    new_question = {'question':'What do you call a group of crows', 'answer':'A murder', 'difficulty': 1, 'category': 1}
    bad_question = {'question':'What do you call a group of crows', 'answer':'A murder', 'difficulty': 1}
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path ="postgresql://{}:{}@{}/{}".format('postgres', 'abc','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertTrue(len(data['categories']))
        
    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))
        
    def test_get_questions_per_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']),3)
        self.assertEqual(data['current_category'],'Entertainment')
    
    """
    TEST: Search by any phrase. The questions list will update to include
    only questions that include that string. Use "title" to start.
    """
    
    def test_search_question_by_string(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)
                                
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])
    
    """
    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_get_question_by_id(self):
        res = self.client().get('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_delete_question_by_id(self):
        res = self.client().delete('/question/1')
        data = json.loads(res.data)
        question=Question.query.filter(Question.id==1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data[question, None])

    def test_422_if_question_does_not_exist_on_delete(self):
        res = self.client().delete('/question/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')
    """
    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the    last page of the questions list in the "List" tab.
    """

    def test_post_new_question(self):
        res = self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    
    def test_422_if_question_creation_not_allowed(self):
        res = self.client().post('/question/add', json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    """
    def test_post_new_quiz(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))  

   """

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()