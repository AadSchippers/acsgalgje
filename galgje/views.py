from django.shortcuts import render
import ast
import random
from . import words

# Create your views here.


def index(request):
    if request.method == 'GET':
        try:
            if not totalscore:
                gamevars = InitSpel(totalscore)
        except UnboundLocalError:
            totalscore = 0
            gamevars = InitSpel(totalscore)

    if request.method == 'POST':
        try:
            if request.POST['pressedkey']:
                letter = str(request.POST['pressedkey']).lower()
            else:
                letter = request.POST['letter']
        except:
            letter = ''
        status = request.POST['status']
        guessword = request.POST['guessword']
        word = request.POST['word']
        guessedletters = ast.literal_eval(request.POST["guessedletters"])
        score = int(request.POST['score'])
        totalscore = int(request.POST['totalscore'])
        statustext = request.POST['statustext']
        gamedone = ast.literal_eval(request.POST['gamedone'])

        gamevars = {
            'guessedletters': guessedletters,
            'status': int(status),
            'word': word,
            'guessword': guessword,
            'score': score,
            'totalscore': totalscore,
            'statustext': statustext,
            'gamedone': gamedone,
        }

        if letter == 'Nieuw':
            gamevars = InitSpel(totalscore)
        else:
            if not gamedone:
                gamevars = RaadWoord(letter, gamevars)

    status = gamevars['status']
    guessword = gamevars['guessword']
    word = gamevars['word']
    guessedletters = gamevars['guessedletters']
    score = gamevars['score']
    totalscore = gamevars['totalscore']
    statustext = gamevars['statustext']
    gamedone = gamevars['gamedone']

    return render(
        request,
        "galgje/index.html", {
        'status': status,
        'guessword': guessword,
        'word': word,
        'guessedletters': guessedletters,
        'score': score,
        'totalscore': totalscore,
        'statustext': statustext,
        'gamedone': gamedone,
        }
    )


def InitSpel(totalscore):
    random.seed()
    word = words.allwords[random.randint(0, len(words.allwords)-1)]

    i = 0
    guessword = ""
    while i < len(word):
        guessword = guessword + "."
        i += 1

    score = 0

    gamevars = {
        'guessedletters': [],
        'status': 0,
        'word': word,
        'guessword': guessword,
        'score': score,
        'totalscore': totalscore,
        'statustext': "", 
        'gamedone': False,
    }
    
    return gamevars


def evaluateletter(letter, gamevars):
    if letter < 'a' or letter > 'z':
        return "Dat is toch geen letter?"

    if letter in gamevars['guessedletters']:
        return "Die heb je al gehad joh!"

    return None

def RaadWoord(letter, gamevars):
    statustext = evaluateletter(letter, gamevars)
    if statustext:
        gamevars['statustext'] = statustext
        return gamevars


    guessedletters = gamevars['guessedletters']
    guessedletters.append(letter)
    gamevars['guessedletters'] = guessedletters

    guessword = gamevars['guessword']
    word = gamevars['word']
    status = gamevars['status']
    score = gamevars['score']
    totalscore = gamevars['totalscore']

    gamedone = False
    LetterFound = False
    i = 0
    while i < len(word):
        if letter == word[i]:
            guessword = guessword [0:i] + letter + guessword[i+1:]
            LetterFound = True
        i += 1

    if LetterFound:
        statustext = "Ja, de " + letter + " is goed."
    else:
        status = status + 1
        statustext = "Nee, de " + letter + " zit er niet in."

    if guessword == word:
        gamedone = True
        score = int(256 / (2**(status+1)))
        if status == 0:
            statustext = "Wauw, zonder fouten!"
        elif status == 1:
            statustext = "Zo, dat ging goed!"
        elif status == 2:
            statustext = "Prima gedaan!"
        elif status == 3:
            statustext = "Jippie geraden!"
        elif status == 4:
            statustext = "Het touw hing al klaar!"
        elif status == 5:
            statustext = "Je kreeg het knap benauwd!"
        elif status == 6:
            statustext = "Dat ging maar net!"
    elif status == 7:
        gamedone = True
        score = 0
        statustext = "Helaas pindakaas."

    if gamedone:
        if score > 0:
            totalscore = totalscore + score
        else:
            totalscore = 0
   
    gamevars['guessword'] = guessword
    gamevars['status'] = status
    gamevars['statustext'] = statustext
    gamevars['gamedone'] = gamedone
    gamevars['score'] = score
    gamevars['totalscore'] = totalscore

    return gamevars
