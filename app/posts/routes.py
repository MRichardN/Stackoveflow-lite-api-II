'''this module is intented to do all the routing in question api'''
import datetime
from flask import request,jsonify, abort, make_response 
from app.main.models import Question, Answer
from . import question_list, answer_list
from flask import Blueprint

questions = Blueprint("questions", __name__, url_prefix='/api/v1')

question = Question(question_list)
answer=Answer(answer_list)


@questions.errorhandler(404)
def item_not_found(e):
    """
    Custom response to 404 errors.
    """
    return make_response(jsonify({'Failed' : 'Item not found'}), 404)


@questions.errorhandler(400)
def bad_method(e):
    """
    Custom response to 400 errors.
    """
    return make_response(jsonify({'Failed': 'bad request'}))

@questions.route("/questions/", methods=["GET","POST"])
def get_all_questions():
    """
    View all questions.
    """
    if question:
        for quiz in question.show_questions():
            #get number of answers
            quiz["answer"]=len(answer.show_answers(quiz["id"]))
        return jsonify({"Questions": question.show_questions()}),200
    abort(404)

@questions.route('/questions/<int:question_id>/', methods=['GET','POST','PUT','DELETE'])
def get_a_specific_question(question_id):
    """
    Get a specific question.
    """
    if request.method == 'GET':
        question_list = question.show_questions()
        my_question=[my_question for my_question in question_list if my_question["id"] == question_id]
        if my_question:
            question_answers=answer.show_answers(my_question[0]["id"])
            my_question[0]["answers"]=question_answers
            return jsonify({"question": my_question}),200
        abort(404)
    elif request.method == "POST":
        if not request.json or not "updated_answer" in request.json:
            abort(404)
        new_answer = {
            "id": answer_list[-1]["id"]+1,
            "updated_answer": request.json["updated_answer"],
            "date_posted":"1900hrs",
            "question_id": question_id
        }
        answer.add_answer(new_answer)
        return jsonify({"Answer":new_answer})

@questions.route('/add_question/', methods=["POST"])
def post_question():
    """
    Post a question.
    """
    if not request.json or not 'title' in request.json:
        abort(400)
    post_question = {
    'id': question_list[-1]['id'] + 1,
    'title': request.json['title'],
    'description': request.json['description'],
    'date_posted': datetime.datetime.now(),
    "answer": 0}
    question.add_question(post_question)
    return jsonify({'question': post_question}),201

@questions.route('/update_question/<int:question_id>/', methods=["PUT"])
def update_question(question_id):
    """
    Update a question.
    """
    if not request.json:
          abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
         abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
         abort(400)
    current_question=[current_question for current_question in question_list if current_question["id"]==question_id]
    if current_question:
        title = request.json.get('title', current_question[0]["title"])
        description= request.json.get('description', current_question[0]['description'])
        date_posted = datetime.datetime.now()
        updated_question=question.update_question(question_id, title, description, date_posted)
        return jsonify({"Question": updated_question}),201
    abort (404)



@questions.route('/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """
    Delete a question.
    """
    if question.delete_question(question_id):
        return jsonify({"Success": "deleted successfully"}),200
    abort(404)




