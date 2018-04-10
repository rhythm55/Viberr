from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.views import generic
from django.views.generic import View
from django.db.models import Q
from .models import Album, song
from .forms import UserForm, AlbumForm

IMAGE_FILE_TYPE=['JPG']

def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form=AlbumForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            album=form.save(commit=False)
            album.user=request.user
            album.album_logo=request.FILES['album_logo']
            file_type=album.album_logo.url.split('.')[-1]
            file_type=file_type.lower()
            if file_type not in IMAGE_FILE_TYPE:
                context={
                    'album': album,
                    'form': form,
                    'error_message': 'image file must be JPG'
                }
                return render(request, 'music/create_album.html', context)
            context={
                "form": form,
            }
            return render(request, 'music/create_album.html', context)

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'



class AlbumUpdate(UpdateView):
    model = Album
    fields =['artist', 'album_title', 'genere', 'album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self,request):
        form = self.form_class(None)
        return  render(request, self.template_name, {'form': form})

    #process form data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

            return render(request, self.template_name,{'form': form})