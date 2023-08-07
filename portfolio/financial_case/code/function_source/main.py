def handler(request):
    print(request.get_json(silent=True))
    return "Hello World"
