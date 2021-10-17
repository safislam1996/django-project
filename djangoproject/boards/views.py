from .models import Board
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    boards=Board.objects.all()
    boards_name=list()

    # for board in boards:
    #     boards_name.append(board.name)
    
    # html_response='<br>'.join(boards_name)

    return render(request,'home.html',{'boards':boards})