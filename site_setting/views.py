from django.shortcuts import render


def custom_404_view(request, exception):
    return render(request, '404 page/404_page.html', status=404)
