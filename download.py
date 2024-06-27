# from pycrawlers import huggingface
#
# # 实例化类
# hg = huggingface()
# #
# # # 1.批量下载
# # urls = ['https://huggingface.co/ziqingyang/chinese-llama-2-13b/tree/main',
# #         'https://huggingface.co/ziqingyang/chinese-llama-2-7b/tree/main']
# #
# # # 默认保存位置在当前脚本所在文件夹 ./
# # hg.get_batch_data(urls)
#
# # 2.单个下载
# url = 'https://huggingface.co/BAAI/bge-small-zh-v1.5'
#
# # # 默认保存位置在当前脚本所在文件夹 ./
# # hg.get_data(url)
#
# # # 自定义下载位置
# # # 多个不同位置
# # paths = ['/home/model-gpt/chinese-llama-2-13b', '/home/model-gpt/chinese-llama-2-7b']
# # hg.get_batch_data(urls, paths)
#
# # 单一位置
# path = './model'
# hg.get_data(url, path)

from huggingface_hub import snapshot_download
snapshot_download(repo_id="internlm/internlm2-chat-7b")