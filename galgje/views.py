from django.shortcuts import render
import ast
import random
from django.conf import settings
from . import words

# Create your views here.


def index(request):
    if request.method == 'GET':
        try:
            totalscore == gamedone['totalscore']
            if not totalscore:
                gamevars = InitSpel(gamevars)
        except UnboundLocalError:
            gamevars = {
                    'totalscore': 0,
                    'gamedone': False,
                }
            gamevars = InitSpel(gamevars)

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
        try: 
            eerste = request.POST['eerste']
        except:
            eerste = False
        try:
            laatste = request.POST['laatste']
        except:
            laatste = False

        gamevars = {
            'guessedletters': guessedletters,
            'status': int(status),
            'word': word,
            'guessword': guessword,
            'score': score,
            'totalscore': totalscore,
            'statustext': statustext,
            'gamedone': gamedone,
            'eerste': eerste,
            'laatste': laatste,
        }

        if letter == 'Nieuw':
            gamevars = InitSpel(gamevars)
        elif letter == "Eerste":
            gamevars['eerste'] = "True"
            gamevars = eersteletter(gamevars)
        elif letter == "Laatste":
            gamevars['laatste'] = "True"
            gamevars = laatsteletter(gamevars)
        else:
            if not gamedone:
                gamevars = RaadWoord(letter, gamevars)

    useragent = request.headers['User-Agent']
    status = gamevars['status']
    guessword = gamevars['guessword']
    word = gamevars['word']
    guessedletters = gamevars['guessedletters']
    score = gamevars['score']
    totalscore = gamevars['totalscore']
    statustext = gamevars['statustext']
    gamedone = gamevars['gamedone']
    eerste = str(gamevars['eerste'])
    laatste = str(gamevars['laatste'])

    statusimage = getstatusimage(status)

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
        'statusimage': statusimage,
        'gamedone': gamedone,
        'eerste': eerste,
        'laatste': laatste,
        'useragent': useragent,
        }
    )


def getstatusimage(status):
    if status < 7:
        return settings.STATIC_URL + "images/galgje" + str(status) + ".png"

    return settings.STATIC_URL + "images/galgje7.png"

def InitSpel(gamevars):
    random.seed()
    allwords = list(set(words.orgwords) | set(words.newwords))
    word = allwords[random.randint(0, len(allwords)-1)]
    
    totalscore = gamevars['totalscore']
    gamedone = gamevars['gamedone']

    if gamedone == False:
        totalscore = 0

    i = 0
    guessword = ""
    while i < len(word):
        guessword += "."
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
        'eerste': "False",
        'laatste': "False",
    }
    
    return gamevars


def eersteletter(gamevars):
    guessword = gamevars['guessword']
    word = gamevars['word']

    guessword = word [0] + guessword[1:]

    gamevars['guessword'] = guessword

    return gamevars


def laatsteletter(gamevars):
    guessword = gamevars['guessword']
    word = gamevars['word']

    guessword = guessword [0:len(guessword)-1] + word[len(guessword)-1:]

    gamevars['guessword'] = guessword

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
    eerste = gamevars['eerste']
    laatste = gamevars['laatste']

    gamedone = False
    LetterFound = False
    strMeer = ""
    if eerste == "True":
        iStart = 1
        strMeer = " niet meer"
    else:
        iStart = 0
    if laatste == "True":
        iEnd = len(word) - 1
        strMeer = " niet meer"
    else:
        iEnd = len(word)
    i = iStart
    while i < iEnd:
        if letter == word[i]:
            guessword = guessword [0:i] + letter + guessword[i+1:]
            LetterFound = True
        i += 1

    if LetterFound:
        statustext = "Ja, de " + letter + " is goed."
    else:
        status = status + 1
        statustext = "Nee, de " + letter + " zit er" + strMeer + " niet in."

    if guessword == word:
        gamedone = True
        score = int(512 / (2**(status+1)))
        if eerste == "True":
            score = int(score / 2)
        if laatste == "True":
            score = int(score / 2)
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
