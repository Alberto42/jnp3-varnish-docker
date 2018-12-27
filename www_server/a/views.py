import re

from django.http import HttpResponse
from django.shortcuts import render
import hashlib
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from www_server.utils import string_generator


def string_hash_searcher(request):
    return render(request,'a/string_hash_searcher.html')

@csrf_exempt
def brute_force_hash(request):
    hash_prefix = request.GET['hash_prefix']

    # pattern = re.compile("^[1-9a-f]+[0-9a-f]*$")
    if ( not re.match(r"^[1-9a-f]+[0-9a-f]*$",hash_prefix) ):
        return render(request,'a/brute_force_hash_error.html')

    for i in string_generator():
        str = ''.join(i)
        m = hashlib.sha256()
        m.update(str.encode())
        hash = m.hexdigest()
        if (hash[0:len(hash_prefix)] == hash_prefix):
            return render(request, 'a/brute_force_hash.html', {'hash_prefix': hash_prefix, 'word': str, 'hash' : hash})
    return HttpResponse("Something went wrong")


