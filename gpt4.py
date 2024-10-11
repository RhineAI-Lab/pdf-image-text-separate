import random
import time

from openai import OpenAI


def get_stream(user_prompt, system_prompt):
  client = OpenAI(
    api_key=open('./secret/gpt4_key.txt').read().strip(),
    base_url="https://api.pumpkinaigc.online/v1",
    timeout=120,
  )
  messages = [{'role': 'system', 'content': system_prompt},
              {'role': 'user', 'content': user_prompt}]
  stream = client.chat.completions.create(
    model="gpt-4o-mini",
    # model="gpt-3.5-turbo",
    messages=messages,
    stream=True,
    timeout=120,
    top_p=0.2,
    temperature=0.2,
  )
  return client, stream


def call(user_prompt, system_prompt='你是个语言能力和逻辑理解能力很强的AI助手', print_in_stream=False):
  client = None
  try:
    client, stream = get_stream(user_prompt, system_prompt)
    text = ''
    for chunk in stream:
      if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        text += content
        if print_in_stream:
          print(content, end="")
    if print_in_stream:
      print('')
    client.close()
    if len(text) > 0:
      return text
    else:
      print('Empty response.')
  except Exception as e:
    print(e)
    client.close()
  return 'ERROR'


def call_generator(user_prompt, system_prompt='你是个语言能力和逻辑理解能力很强的AI助手', print_in_stream=False):
  client = None
  try:
    client, stream = get_stream(user_prompt, system_prompt)
    text = ''
    for chunk in stream:
      if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        text += content
        if print_in_stream:
          print(content, end="")
        if len(text) > 0:
          yield text
    if print_in_stream:
      print('')
    if len(text) > 0:
      yield text
    else:
      print('Empty response.')
      yield 'ERROR'
  except Exception as e:
    print(e)
    yield 'ERROR'
  client.close()


if __name__ == '__main__':
  while True:
    # call_with_print('详细解释transformer结构中的qkv的作用，以及他的代码和数学原理')
    time.sleep(random.randint(1, 5))
