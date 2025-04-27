from django.http import JsonResponse
from organizations.models import Organization


def check_subdomain(request):
  subdomain = request.headers.get('x-subdomain')

  if Organization.objects.filter(sub_domain=subdomain).exists():
    return JsonResponse({'ok': True})
  else:
    return JsonResponse({'ok': False}, status=400)
