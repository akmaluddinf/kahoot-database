from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import Users, Quizzes, Questions, OptionList, Game, Leaderboard
from random import randint

app = Flask(__name__)

POSTGRES = {
    'user' : 'postgres',
    'pw' : 'lupalagi',
    'db' : 'kahoot',
    'host' : 'localhost',
    'port' : '5432'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# postgresql://username:password@localhost:5432/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES 

db.init_app(app)

# ========================================================USER=============================================
@app.route("/getAllUser", methods=['GET'])
def get_all_user():
    try:
        users = Users.query.order_by(Users.user_id).all()
        return jsonify([usr.serialize() for usr in users])
    except Exception as e:
        return (str(e))

@app.route("/getUser/<id_>", methods=['GET'])
def get_users_by(id_):
    try:
        users = Users.query.filter_by(user_id=id_).first()
        return jsonify(users.serialize())
    except Exception as e:
        return(str(e))


@app.route("/addUser", methods=['POST'])
def add_user():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request .args.get('email')

    try:
        users = Users(
            username = username,
            password = password,
            email = email
            )
        db.session.add(users)
        db.session.commit()
        return "User added. user id={}".format(users.user_id)

    except Exception as e:
        return (str(e))

@app.route("/removeUser/<id_>", methods=['DELETE'])
def remove_user(id_):
    try:
        users = Users.query.filter_by(user_id=id_).first()
        db.session.delete(users)
        db.session.commit()
        return "User id = " + str(id_) + " deleted."
    except Exception as e:
        return (str(e))
    finally:
        db.session.close()


@app.route('/updateUser/<id_>', methods=["PUT"])
def update_user(id_):
    user_existing = get_users_by(id_).json
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    if request.args.get('username') == None:
        username = user_existing['username']
    if request.args.get('password') == None:
        password = user_existing['password']
    if request.args.get('email') == None:
        email = user_existing['email']
    try:
        userUpdate = {
            'username' : username,
            'password' : password,
            'email' : email
        }
        users = Users.query.filter_by(user_id=id_).update(userUpdate)
        db.session.commit()
        return "User updated."

    except Exception as e:
        return(str(e))

# ========================================================QUIZ=============================================
@app.route("/getAllQuiz", methods=['GET'])
def get_all_quiz():
    try:
        quizzes = Quizzes.query.order_by(Quizzes.quiz_id).all()
        return jsonify([qzs.serialize() for qzs in quizzes])
    except Exception as e:
        return (str(e))

@app.route("/getQuiz/<id_>", methods=['GET'])
def get_quiz_by(id_):
    try:
        quizzes = Quizzes.query.filter_by(quiz_id=id_).first()
        return jsonify(quizzes.serialize())
    except Exception as e:
        return(str(e))

@app.route("/addQuiz", methods=['POST'])
def add_quiz():
    creator_id = request.args.get('creator_id')
    quiz_name = request.args.get('quiz_name')
    quiz_category = request.args.get('quiz_category')

    try:
        quiz = Quizzes(
            creator_id = creator_id,
            quiz_name = quiz_name,
            quiz_category = quiz_category
            )
        db.session.add(quiz)
        db.session.commit()
        return "Quiz added. quiz id={}".format(quiz.quiz_id)
    
    except Exception as e:
        return (str(e))

@app.route("/removeQuiz/<id_>", methods=['DELETE'])
def remove_quiz(id_):
    try:
        quizzes = Quizzes.query.filter_by(quiz_id=id_).first()
        db.session.delete(quizzes)
        db.session.commit()
        return "Quiz id = " + str(id_) + " deleted."
    except Exception as e:
        return (str(e))
    finally:
        db.session.close()


@app.route('/updateQuiz/<id_>', methods=["PUT"])
def update_quiz(id_):
    
    quiz_existing = get_quiz_by(id_).json

    if request.args.get('creator_id') == None:
        creator_id = quiz_existing['creator_id']
    else:
        creator_id = request.args.get('creator_id')
    if request.args.get('quiz_name') == None:
        quiz_name = quiz_existing['quiz_name']
    else:
        quiz_name = request.args.get('quiz_name')
    if request.args.get('quiz_category') == None:
        quiz_category = quiz_existing['quiz_category']
    else:
        quiz_category = request.args.get('quiz_category')
        
    try:
        updateQuiz = {
            'creator_id' : creator_id,
            'quiz_name' : quiz_name,
            'quiz_category' : quiz_category
        }
        quizzes = Quizzes.query.filter_by(quiz_id=id_).update(updateQuiz)
        db.session.commit()
        return "Quiz updated."
    except Exception as e:
        return str(e)

# ========================================================QUESTION=============================================
@app.route('/getAllQuestion', methods=["GET"])
def get_all_question():
    try:
        questions = Questions.query.order_by(Questions.question_number).all()
        return jsonify([qstn.serialize() for qstn in questions])
    except Exception as e:
        return (str(e))

@app.route('/getQuestion/<number_>', methods=["GET"])
def get_question_by(number_):
    try:
        questions = Questions.query.filter_by(question_number = number_).first()
        return jsonify(questions.serialize())
    except Exception as e:
        return (str(e))

@app.route('/addQuestion', methods=["POST"])
def add_question():
    question_number = request.args.get('question_number')
    quiz_id = request.args.get('quiz_id')
    question = request.args.get('question')
    answer = request.args.get('answer')

    try:
        questions = Questions(
            question_number = question_number,
            quiz_id = quiz_id,
            question = question,
            answer = answer
        )
    except Exception as e:
        return str(e)
        
    db.session.add(questions)
    db.session.commit()
    return "Question added. question number={}".format(questions.question_number)

@app.route('/removeQuestion/<number_>', methods=["DELETE"])
def delete_question(number_):
    try:
        questions = Questions.query.filter_by(question_number=number_).first()
        db.session.delete(questions)
        db.session.commit()
        return "Question number = " + str(number_) + " deleted."
    except Exception as e:
        return str(e)

@app.route('/updateQuestion/<number_>', methods=["PUT"])
def update_Question(number_):
    question_existing = get_question_by(number_).json

    if request.args.get('quiz_id') == None:
        quiz_id = question_existing['quiz_id']
    else:
        quiz_id = request.args.get('quiz_id')
    if request.args.get('question_number') == None:
        question_number = question_existing['question_number']
    else:
        question_number = request.args.get('question_number')
    if request.args.get('question') == None:
        question = question_existing['question']
    else:
        question = request.args.get('question')
    if request.args.get('answer') == None:
        answer = question_existing['answer']
    else:
        answer = request.args.get('answer')
    
    try:
        questionUpdate = {
            'quiz_id' : quiz_id,
            'question_number' : question_number,
            'question' : question,
            'answer' : answer
        }
        questions = Questions.query.filter_by(question_number=number_).update(questionUpdate)
        db.session.commit()
        return "Question updated."

    except Exception as e:
        return str(e)


# ========================================================OPTION LIST=============================================
@app.route('/getAllOption', methods=["GET"])
def get_all_option():
    try:
        option_list = OptionList.query.order_by(OptionList.option_id).all()
        return jsonify([opl.serialize() for opl in option_list])
    except Exception as e:
        return str(e)

@app.route('/getOptionBy/<opsId_>', methods=["GET"])
def get_option_by(opsId_):
    try:
        option_list = OptionList.query.filter_by(option_id=opsId_).first()
        return jsonify(option_list.serialize())
    except Exception as e:
        return str(e)

@app.route('/addOption', methods=["POST"])
def add_option():
    question_number = request.args.get('question_number')
    option_id = request.args.get('option_id')
    a = request.args.get('a')
    b = request.args.get('b')
    c = request.args.get('c')
    d = request.args.get('d')

    try:
        option_list = OptionList(
            question_number = question_number,
            option_id = option_id,
            a = a,
            b = b,
            c = c,
            d = d
        )
        db.session.add(option_list)
        db.session.commit()
        return "optionn list added. option id={}".format(option_list.option_id)
    except Exception as e:
        return str(e)


@app.route('/removeOption/<opsId_>',methods=["DELETE"])
def delete_option(opsId_):
    try:
        option_list = OptionList.query.filter_by(option_id=opsId_).first()
        db.session.delete(option_list)
        db.session.commit()
        return "option delete"
    except Exception as e:
        return str(e)

@app.route('/updateOption/<opsId_>', methods=["PUT"])
def update_option(opsId_):
    option_existing = get_option_by(opsId_).json

    if request.args.get('question_number') == None:
        question_number = option_existing['question_number']
    else:
        question_number = request.args.get('question_number')
    if request.args.get('option_id') == None:
        option_id = option_existing['option_id']
    else:
        option_id = request.args.get('option_id')
    if request.args.get('a') == None:
        a = option_existing['a']
    else:
        a = request.args.get('a')
    if request.args.get('b') == None:
        b = option_existing['b']
    else:
        b = request.args.get('b')
    if request.args.get('c') == None:
        c = option_existing['c']
    else:
        c = request.args.get('c')
    if request.args.get('d') == None:
        d = option_existing['d']
    else:
        d = request.args.get('d')
    
    try:
        updateOption = {
                'question_number' : question_number,
                'option_id' : option_id,
                'a' : a,
                'b' : b,
                'c' : c,
                'd' : d
        }
        option_list = OptionList.query.filter_by(option_id=opsId_).update(updateOption)
        db.session.commit()
        return "Option updated."
    except Exception as e:
        return str(e)

# ========================================================GAME=============================================
@app.route('/getAllGame', methods=["GET"])
def get_all_game():
    try:
        game = Game.query.order_by(Game.game_pin).all()
        return jsonify([gm.serialize() for gm in game])
    except Exception as e:
        return str(e)

@app.route('/getGameBy/<gamePin_>', methods=["GET"])
def get_game_by(gamePin_):
    try:
        game = Game.query.filter_by(game_pin=gamePin_).first()
        return jsonify(game.serialize())
    except Exception as e:
        return str(e)

@app.route('/createGame', methods=["POST"])
def create_game():

    game_pin = randint(90000,100000)
    quiz_id = request.args.get('quiz_id')

    try:
        game = Game(
            game_pin = game_pin,
            quiz_id = quiz_id
        )
        db.session.add(game)
        db.session.commit()
        return "Game created. game pin = {}".format(game.game_pin)
    except Exception as e:
        return str(e)

@app.route('/removeGame/<gamePin_>', methods=["DELETE"])
def delete_game(gamePin_):
    try:
        game = Game.query.filter_by(game_pin=gamePin_).all()
        for delet in game:
            db.session.delete(delet)
            db.session.commit()
            return "game deleted"
    except Exception as e:
        return (str(e))

# ========================================================LEADERBOARD=============================================
@app.route('/getAllLeaderboard', methods=["GET"])
def get_all_leaderboard():
    try:
        leaderboard = Leaderboard.query.order_by(Leaderboard.player_name).all()
        return jsonify([pname.serialize() for pname in leaderboard])
    except Exception as e:
        return (str(e))

@app.route('/joinGame', methods=["POST"])
def join_game():

    game_pin = request.args.get('game_pin')
    score = 0
    player_name = request.args.get('player_name')

    try:
        leaderboard = Leaderboard(
                game_pin = game_pin,
                score = score,
                player_name = player_name
        )
        db.session.add(leaderboard)
        db.session.commit()
        return "Join to Game. player name = {}".format(leaderboard.player_name)

    except Exception as e:
        return str(e)

@app.route('/getLeaderboardBy/<gamepin_>', methods=["GET"])
def get_leaderboard_by(gamepin_):
    try:
        leaderboard = Leaderboard.query.filter_by(game_pin = gamepin_).all()
        return jsonify([ldb.serialize() for ldb in leaderboard])
    except Exception as e:
        return str(e)


@app.route('/deletePlayer/<name_>', methods=["DELETE"])
def delete_player(name_):
    try:
        leaderboard = Leaderboard.query.filter_by(player_name=name_).first()
        db.session.delete(leaderboard)
        db.session.commit()
        return "Player delete. Name {}".format(leaderboard.player_name)
    except Exception as e:
        return str(e)

@app.route('/answer', methods=["POST"])
def answer():
    gamePin_ = request.args.get('gamePin_')
    pName_ = request.args.get('pName_')
    answer_ = request.args.get('answer_')
    questionNumber_ = request.args.get('questionNumber_')
    question = get_question_by(questionNumber_).json
    leaderboard = get_leaderboard_by(gamePin_).json

    score = 0
    for i in leaderboard:
        if i['player_name'] == pName_:
            score = i['score']
            break

    if question['answer']==answer_:
        score += 100

    try:
        updateScore = {
            'game_pin': gamePin_,
            'player_name': pName_,
            'score': score

        }
        db.session.query(Leaderboard).filter_by(player_name=pName_, game_pin=gamePin_).update(updateScore)
        db.session.commit()
        return 'update score'
    
    except Exception as e:
        return str(e)


    

# if __name__ == '__main__':
#     app.run()