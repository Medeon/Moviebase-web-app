from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    #context dictionary to send over to the frontend
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.glendo.ru/upload/iblock/57d/57d5a8e1538e3b6c500879a7ac58eff7.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            # Notify on create
            messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'You ran into an error while trying to add a new movie: {}'.format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.glendo.ru/upload/iblock/57d/57d5a8e1538e3b6c500879a7ac58eff7.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            edition = AT.update(movie_id, data)
            # Notify on edit
            messages.success(request, 'The movie {} has been successfuly updated!'.format(edition['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'You ran into an error while trying to update a movie: {}'.format(e))

    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        # Notify on delete
        messages.warning(request, 'The movie {} has been deleted!'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'You ran into an error while trying to delete a movie: {}'.format(e))
    return redirect('/')
