from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []
QUESTIONS = survey.questions
curr_number = 0

@app.get("/")
def start_survey():
    """ renders start of survey """
    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", title=title,
        instructions=instructions)

@app.post("/begin")
def go_to_question():


    return redirect(f"/questions/{curr_number}")


@app.get("/questions/<int:number>")
def get_question(number):
    survey = QUESTIONS[number]
    curr_question = survey.prompt
    curr_choice = survey.choices


    return render_template("question.html", question_prompt=curr_question,
        question_choice=curr_choice)


@app.post("/answer")
def retrieve_answer():
    answer = request.form["answer"]

    responses.append(answer)
    breakpoint()
    curr_number = curr_number + 1

    return redirect(f"/questions/{curr_number}")



