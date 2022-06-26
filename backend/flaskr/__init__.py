import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """ @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """ @TODO: Use the after_request decorator to set Access-Control-Allow """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """ @TODO: Create an endpoint to handle GET requests or all available categories. """

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories_formatted = {category.id: category.type for category in categories}
        return jsonify({'success': True, 'categories': categories_formatted})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """

    @app.route('/questions')
    def get_questions():
        try:
            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)
            categories = Category.query.all()
            categories_formatted = {category.id: category.type for category in categories}
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': categories_formatted,
                'current_category': None
            })
        except:
            abort(422)
    """

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
        try:
            question = Question(question=new_question, answer=new_answer, category=new_category,
                                difficulty=new_difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id
            })

        except:

            abort(422)

    """
    TEST: When you submit a question to the endpoint,
    it will be added to the database and returned in the questions route
    """

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
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = paginate_questions(request, questions)
            categories = Category.query.all()
            categories_formatted = {category.id: category.type for category in categories}
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': categories_formatted,
                'current_category': None
            })
        except:
            abort(422)
    """
    TEST: When you search for "a" you should get a list of 10 questions.
    """

    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """

    @app.route('/categories/<string:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            current_questions = paginate_questions(request, questions)
            categories = Category.query.all()
            categories_formatted = {category.id: category.type for category in categories}
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(categories),
                'categories': categories_formatted,
                'current_category': category_id
            })
        except:
            abort(422)

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause a list of questions for that category to appear.
    """

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause a list of questions to
    appear for that category.
    """

    """
    TEST: I
    

    """
    """
n the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            body = request.get_json()
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            if category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category['id']).all()
            filtered_questions = [question for question in questions if question.id not in previous_questions]
            question = random.choice(filtered_questions)
            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    """
    TEST: In the "Play" tab, after a user selects "All Questions",
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
