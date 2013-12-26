from forms import UploadImage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from kirkifier import Kirkify
from django.shortcuts import RequestContext
kirkify = Kirkify()
def upload_image(request):
    if request.method == 'POST':
        form = UploadImage(request.POST, request.FILES)
        if form.is_valid():
        	kirkify.main(request.FILES['file'])
        	return HttpResponseRedirect('/success/url/')
    else:
        form = UploadImage()
    return render_to_response('index.html', {'form': form}, RequestContext(request))