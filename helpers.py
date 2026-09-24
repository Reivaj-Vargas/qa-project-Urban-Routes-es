import json
import time
from selenium.common.exceptions import WebDriverException

DEBUG = False  # ponlo en True y ejecuta con -s para ver las URLs que pasan por la red


def retrieve_phone_code(driver) -> str:
    """Recupera el código SMS desde los logs de rendimiento de Chrome.
    Úsala solo después de haber pulsado 'Siguiente' en la app."""
    request_ids = []

    for _ in range(10):
        time.sleep(1)
        try:
            logs = driver.get_log('performance')
        except WebDriverException as e:
            raise Exception(
                f"No se pudieron leer los logs de rendimiento ({e}). "
                "¿Habilitaste 'goog:loggingPrefs' al crear Chrome?")

        for log in logs:
            try:
                message = json.loads(log['message'])['message']
            except (ValueError, KeyError):
                continue
            if message.get('method') != 'Network.responseReceived':
                continue
            url = message['params']['response'].get('url', '')
            if DEBUG:
                print("URL:", url)
            if 'api/v1/number' in url or 'code' in url:
                request_ids.append(message['params']['requestId'])

        for request_id in reversed(request_ids):
            try:
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': request_id})['body']
            except WebDriverException:
                continue
            try:
                code = str(json.loads(body)['code'])
            except (ValueError, KeyError, TypeError):
                code = ''.join(c for c in body if c.isdigit())
            if code:
                return code

    raise Exception("No se encontró el código de confirmación en los registros.")