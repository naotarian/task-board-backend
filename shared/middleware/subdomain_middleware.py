class SubdomainMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # ヘッダーからサブドメイン取得して、リクエストオブジェクトに載せる
    request.subdomain = request.headers.get('x-subdomain')
    return self.get_response(request)
