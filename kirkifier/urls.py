from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import os
admin.autodiscover()

def get_static_root():
    global PROJECT_ROOT, STATIC_URL, STATIC_ROOT
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))


get_static_root()
urlpatterns = patterns('',
                       (r'^static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': STATIC_ROOT}), )


urlpatterns += patterns('',
    # Examples:
    url(r'^$', 'kirkifier.views.upload_image', name='home'),
    url(r'^kirkified$', 'kirkifier.views.kirkified', name='output'),


    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()