from fyers_api import accessToken


client_id = "GE5QQJSV08-100"
secret_key = "YLW55TI687"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"
grant_type = "authorization_code"


auth_code = open("auth_code").read()

session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)

session.set_token(auth_code)
response = session.generate_token()
print(response["access_token"])
