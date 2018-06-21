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
greetings = ( 'ку', 'алоха', 'привет', 'превед', 'здорово', 'здарова', 'здравствуй')


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

      try:
        last_message = last_update['message']
        last_chat_id = last_message['chat']['id']
        last_username = last_message['from']['username']
        last_firstname = last_message['from']['first_name']

        try:
          last_text = last_message['text']
        except Exception as e:
          last_text = None
          print("%s: Message: %s" % (timestamp, last_update['message']))
          print(e.message)

      except Exception as e:
        last_message = None
        print("%s: Update: %s" % (timestamp, last_update))
        print(e.message)


      if last_text:
        print("%s: Username: %-10s Chat_id: %-10s Msg_id: %-10s Offset: %-10s Text: %s" %
          (timestamp, last_username, last_chat_id, last_update_id, offset, last_text))

        if last_text.lower() in greetings:
          if 5 <= hour < 11:
            greet_bot.send_message(last_chat_id, "Доброе утро, {}!".format(last_firstname))

          elif 11 <= hour < 17:
            greet_bot.send_message(last_chat_id, "Добрый день, {}!".format(last_firstname))

          elif 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, "Добрый вечер, {}!".format(last_firstname))

          else:
            greet_bot.send_message(last_chat_id, "Доброй ночи, {}!".format(last_firstname))
        else:
          greet_bot.send_message(last_chat_id, "Сам {}!".format(last_text))

      offset = last_update_id + 1
    else:
      print("%s: None" % timestamp)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print("\nРабота прервана!")
    exit()

