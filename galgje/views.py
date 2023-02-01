from django.shortcuts import render
import ast

# Create your views here.


def index(request):
    if request.method == 'GET':
        try:
            if not guessedletters:
                gamevars = InitSpel()
        except UnboundLocalError:
            gamevars = InitSpel()

        status = gamevars['status']
        guessword = gamevars['guessword']
        word = gamevars['word']
        guessedletters = gamevars['guessedletters']
        score = gamevars['score']
        highscore = gamevars['highscore']

    if request.method == 'POST':
        letter = request.POST['letter']
        status = request.POST['status']
        guessword = request.POST['guessword']
        word = request.POST['word']
        guessedletters = ast.literal_eval(request.POST["guessedletters"])
        score = request.POST['score']
        highscore = request.POST['highscore']

        if letter == 'Nieuw':
            guessedletters = InitSpel()
        else:
            guessedletters = RaadWoord(letter, guessedletters)

    return render(
        request,
        "galgje/index.html", {
        'status': status,
        'guessword': guessword,
        'word': word,
        'guessedletters': guessedletters,
        'score': score,
        'highscore': highscore,
        }
    )


def InitSpel():
    word = "badjas"
    guessword = "......"
    score = 0
    highscore = 0


    gamevars = {
        'guessedletters': [],
        'status': 0,
        'word': word,
        'guessword': guessword,
        'score': score,
        'highscore': highscore,
    }
    
    return gamevars


def RaadWoord(letter, guessedletters):
    guessedletters.append(letter)
    
    return guessedletters
