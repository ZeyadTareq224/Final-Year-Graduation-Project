from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def doctor_required(function=None, login_url='unauthorized'):
    '''
    Decorator for views that checks that the logged in user is a doctor,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_doctor,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def normal_user_required(function=None, login_url='unauthorized'):
    '''
    Decorator for views that checks that the logged in user is a normal user,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_normal_user,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
