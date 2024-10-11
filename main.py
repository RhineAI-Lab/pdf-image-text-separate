import os
import fitz  # PyMuPDF
import filetype  # 用于检测文件类型

pdf_file = './data/f1.pdf'
nwt = os.path.splitext(os.path.basename(pdf_file))[0]
output_dir = os.path.join('./output', nwt)

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打开PDF文件
doc = fitz.open(pdf_file)

# 初始化一个列表，用于存储修改后的文本
modified_text = []

# 遍历PDF中的每一页
for page_number in range(len(doc)):
    page = doc[page_number]
    # 获取页面的文本和图像，以字典形式
    page_dict = page.get_text('dict')
    blocks = page_dict['blocks']

    # 用于跟踪当前页的图像索引
    image_counter = 1

    # 处理每个块
    for block in blocks:
        # 如果块的类型是图像
        if block['type'] == 1:
            # 获取图像数据
            image_bytes = block['image']
            # 检测图像类型
            kind = filetype.guess(image_bytes)
            if kind is not None:
                image_ext = kind.extension
            else:
                image_ext = 'png'  # 默认使用 png

            image_name = f'image_{page_number + 1}_{image_counter}.{image_ext}'
            image_counter += 1

            # 将图片保存到文件
            with open(os.path.join(output_dir, image_name), 'wb') as image_file:
                image_file.write(image_bytes)

            # 在文本中用图片文件名替换图片位置
            modified_text.append(f'[{image_name}] ')
        elif block['type'] == 0:
            # 文本块
            for line in block['lines']:
                for span in line['spans']:
                    modified_text.append(span['text'] + ' ')
        else:
            # 其他类型的块，可以根据需要处理
            continue

    # 每页结束后添加换行符
    modified_text.append('\n')

# 将列表中的文本合并成一个字符串
output_text = ''.join(modified_text)

# 将修改后的文本保存到文件
with open(os.path.join(output_dir, 'pdf_text.txt'), 'w', encoding='utf-8') as text_file:
    text_file.write(output_text)
