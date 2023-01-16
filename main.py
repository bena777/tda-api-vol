from tda import auth
import config

def tda_auth():
    try:
        c = auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
            c = auth.client_from_login_flow(
                driver, config.api_key, config.redirect_uri, config.token_path)
    return c

tda_auth()