import os.path

from gpt4 import call_generator

work_dir = './output/f1'

pdf_text_file = open(os.path.join(work_dir, 'pdf_text.txt'), 'r', encoding='utf-8')
text = pdf_text_file.read()
print('PDF Length:', len(text))

images = []
for file in os.listdir(work_dir):
  if file.startswith('image_'):
    images.append(file)
print('Images Length:', len(images))


system_prompt = '''你是个语言能力和逻辑理解能力很强的AI助手。'''

user_prompt = '''
我从一个PDF论文文件中抽取出了他所有的文本。
PDF文件中的图片部分已经单独抽出为图片文件，所有的图片在文本中都被被替换为了文件名，例如 [image_7_1.jpg] 。

我希望你帮我找到与图片 [IMAGE] 相关的上下文文本，以便我对这张图片做信息标注。

注意事项：
1. 你的回答不需要有任何多余的文字，例如“好的，下面是...”等 都不需要，直接返回我结果，你回答的所有文本我将直接标注至图片。
2. 图片相关文本大概率出现在图片上下文附近。
3. 请尽可能多找几处上下文，并合并。每一处不需要是完整的段落，只需要是完整的句子，每一处尽可能精简。
4. 可以略微修改补充或总结，请主要都以原文为主！
5. 论文原文为英文时，你返回的上下文也应是英文。
6. 你的回答中不要出现图片名 [image_x_x.jpg] ，这在原PDF中是不存在的。


以下是PDF完整文本：

[PDF_TEXT]
'''


for image in images:
  print('\n')
  print(image, '\n')
  prompt = user_prompt.replace('[IMAGE]', '[' + image + ']').replace('[PDF_TEXT]', text)
  result = ''
  for current in call_generator(prompt, system_prompt, True):
    result = current
    
  open(os.path.join(work_dir, os.path.splitext(image)[0] + '.txt'), 'w', encoding='utf-8').write(result)
  