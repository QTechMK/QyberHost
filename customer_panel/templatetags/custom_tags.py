from django import template
from django.urls import resolve
from django.urls.exceptions import Resolver404


register = template.Library()

#This the custom filter, name is getitems
def getdata(json_data, args):    
    func_name=''
    try:
        myfunc, myargs, mykwargs = resolve(args)
        if myfunc:
            func_name=myfunc.__name__
    except Resolver404:
        pass

    if isinstance(json_data, dict):
        return json_data.get(func_name)
    return None


register.filter('getdata', getdata)



# request.path	                  /home/
# request.get_full_path	         /home/?q=test
# request.build_absolute_uri	 http://127.0.0.1:8000/home/?q=test
