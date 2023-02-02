from django.shortcuts import render
import ast

# Create your views here.


def index(request):
    if request.method == 'GET':
        try:
            if not highscore:
                gamevars = InitSpel(highscore)
        except UnboundLocalError:
            highscore = 0
            gamevars = InitSpel(highscore)

    if request.method == 'POST':
        letter = request.POST['letter']
        status = request.POST['status']
        guessword = request.POST['guessword']
        word = request.POST['word']
        guessedletters = ast.literal_eval(request.POST["guessedletters"])
        score = request.POST['score']
        highscore = request.POST['highscore']

        gamevars = {
            'guessedletters': guessedletters,
            'status': int(status),
            'word': word,
            'guessword': guessword,
            'score': score,
            'highscore': highscore,
        }

        if letter == 'Nieuw':
            gamevars = InitSpel(highscore)
        else:
            gamevars = RaadWoord(letter, gamevars)

    status = gamevars['status']
    guessword = gamevars['guessword']
    word = gamevars['word']
    guessedletters = gamevars['guessedletters']
    score = gamevars['score']
    highscore = gamevars['highscore']

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


def InitSpel(highscore):
    word = "badjas"
    guessword = "......"
    score = 0

    gamevars = {
        'guessedletters': [],
        'status': 0,
        'word': word,
        'guessword': guessword,
        'score': score,
        'highscore': highscore,
    }
    
    return gamevars


def RaadWoord(letter, gamevars):
    guessedletters = gamevars['guessedletters']
    guessedletters.append(letter)
    gamevars['guessedletters'] = guessedletters
    status = gamevars['status'] + 1
    gamevars['status'] = status
    
    return gamevars
