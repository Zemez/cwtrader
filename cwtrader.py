import requests
import datetime


class BotHandler:

  def __init__(self, token):
    self.token = token
    self.api_url = "https://api.telegram.org/bot{}/".format(token)
    self.proxies = { 'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050' }

  def get_updates(self, offset=None, timeout=60):
    method = 'getUpdates'
    params = { 'timeout': timeout, 'offset': offset }
    resp = requests.get(self.api_url + method, proxies = self.proxies, data = params)
    result_json = resp.json()['result']
    return result_json

  def send_message(self, chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    method = 'sendMessage'
    resp = requests.post(self.api_url + method, proxies = self.proxies, data = params)
    return resp

  def get_last_update(self):
    last_update = None
    results = self.get_updates()

    if len(results) > 0:
      #print("Results: {}\nIndex: {}".format(results, len(results)))
      last_update = results[-1]
    else:
      try:
        last_update = results[len(results)]
      except IndexError:
        last_update = None
        #print("Results: {} Index: {}".format(results, len(results)))
    return last_update


token = '561732479:AAGlQ5W0Q_8PurdQLgzkZ-mXgXnemuZQd6M'
greet_bot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')


def main():
  offset = None

  while True:
    greet_bot.get_updates(offset)
    last_update = greet_bot.get_last_update()

    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")

    if last_update:
      hour = now.hour
      last_update_id = last_update['update_id']
      last_chat_text = last_update['message']['text']
      last_chat_id = last_update['message']['chat']['id']
      last_chat_name = last_update['message']['chat']['first_name']

      print("%s: Name: %-10s Chat_id: %-10s Msg_id: %-10s Offset: %-10s Text: %s" %
        (timestamp, last_chat_name, last_chat_id, last_update_id, offset, last_chat_text))

      if last_chat_text.lower() in greetings:
        if 5 <= hour < 11:
          greet_bot.send_message(last_chat_id, "Доброе утро, {}".format(last_chat_name))

        elif 11 <= hour < 17:
          greet_bot.send_message(last_chat_id, "Добрый день, {}".format(last_chat_name))

        elif 17 <= hour < 23:
          greet_bot.send_message(last_chat_id, "Добрый вечер, {}".format(last_chat_name))

        else:
          greet_bot.send_message(last_chat_id, "Доброй ночи, {}".format(last_chat_name))
      else:
        greet_bot.send_message(last_chat_id, "Сам {}!".format(last_chat_text))

      offset = last_update_id + 1
    else:
      print("%s: None" % timestamp)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

