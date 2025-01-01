from django.http import HttpResponse, JsonResponse


def home_page(request):
    print("Home page requested")
    friens = [
        'Mahboob',
        'Devendra',
        'Manoj',
        'Sheshram',
    ]
    return JsonResponse(friens, safe=False)
