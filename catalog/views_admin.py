from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
import io
import traceback


def _token_ok(request):
    token = getattr(settings, 'IMPORT_TOKEN', None)
    if not token:
        return None
    header = request.META.get('HTTP_X_IMPORT_TOKEN')
    return header == token


@csrf_exempt
@require_POST
def trigger_import(request):
    """Trigger the `importdata` management command.

    Authorization logic:
    - If `settings.IMPORT_TOKEN` is set: allow request when either the
      `X-IMPORT-TOKEN` header matches or the user is authenticated staff.
    - If no token is configured: allow only authenticated staff users.
    """
    token = getattr(settings, 'IMPORT_TOKEN', None)
    token_ok = _token_ok(request)
    user_is_staff = bool(getattr(request, 'user', None) and request.user.is_authenticated and request.user.is_staff)

    if token:
        if not (token_ok or user_is_staff):
            return HttpResponseForbidden('Forbidden')
    else:
        if not user_is_staff:
            return HttpResponseForbidden('Forbidden')

    out = io.StringIO()
    try:
        call_command('importdata', stdout=out)
    except Exception:
        out.write('\n')
        out.write(traceback.format_exc())
        return JsonResponse({'ok': False, 'log': out.getvalue()}, status=500)

    return JsonResponse({'ok': True, 'log': out.getvalue()})
