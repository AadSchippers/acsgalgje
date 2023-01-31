from django.shortcuts import render

# Create your views here.
status = 0
word = ""
guessword = ""
guessedletters = []


def index(request):
    if request.method == 'POST':
        letter = request.POST['letter']

        if letter == 'Nieuw':
            InitSpel()
        else:
            RaadWoord(letter)

    return render(
        request,
        "galgje/index.html", {
        'status': status,
        'guessword': guessword,
        'guessedletters': guessedletters
        }
    )


def InitSpel():
    global guessedletters
    guessedletters = []
    
    return


def RaadWoord(letter):
    global guessedletters
    guessedletters.append(letter)
    
    return
