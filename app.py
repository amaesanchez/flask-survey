from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

QUESTIONS = survey.questions

@app.get("/")
def start_survey():
    """ renders start of survey """
    title = survey.title
    instructions = survey.instructions

    session['responses'] = []
    session['curr_number'] = 0
    #injecct survey
    return render_template("survey_start.html", title=title,
        instructions=instructions)


@app.post("/begin")
def go_to_question():
    """ redirects to question at current question index """
    #clear responses
    return redirect(f"/questions/{session['curr_number']}")


@app.get("/questions/<int:number>")
def get_question(number):
    """ renders current question with current number """

    question = QUESTIONS[number]
    curr_question = question.prompt
    curr_choice = question.choices

    return render_template("question.html", question_prompt=curr_question,
        question_choice=curr_choice)

# add logic for moving ahead
@app.post("/answer")
def retrieve_answer():
    """ redirects to next question if within QUESTION range
    and appends user response to responses key in session.
    Renders Thank You template when finished with survey"""

    answer = request.form["answer"]

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if session["curr_number"] < (len(QUESTIONS) - 1):
        curr_number = session["curr_number"]
        curr_number += 1
        session["curr_number"] = curr_number

        return redirect(f"/questions/{session['curr_number']}")
    else:
        return render_template("completion.html")
