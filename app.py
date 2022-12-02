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

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def go_to_question():
    """ redirects to question at current question index """

    session['responses'] = []
    return redirect(f"/questions/{len(session['responses'])}")


@app.get("/questions/<int:number>")
def get_question(number):
    """ renders current question with current number """

    if number != len(session['responses']):
        # session.pop("_flashes", None) # doubles
        flash("Quit cheating. Get back in line")
        return redirect(f"/questions/{len(session['responses'])}")

    else:
        question = QUESTIONS[number]
        return render_template("question.html", question=question)


@app.post("/answer")
def retrieve_answer():
    """ redirects to next question if within QUESTION range
    and appends user response to responses key in session.
    Renders Thank You template when finished with survey"""

    answer = request.form["answer"]

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(session['responses']) < (len(QUESTIONS)):
        return redirect(f"/questions/{len(session['responses'])}")
    else:
        print(session['responses'])
        return render_template("completion.html")
