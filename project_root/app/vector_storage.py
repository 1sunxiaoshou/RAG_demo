import os
import json
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader, CSVLoader, \
    TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveJsonSplitter


class VectorStorageObject(object):

    def __init__(self):
        self.loader = {
            ".pdf": PyPDFLoader,
            ".txt": TextLoader,
            ".docx": Docx2txtLoader,
            ".md": UnstructuredMarkdownLoader,
            ".csv": CSVLoader,
            ".json": self.handle_json,
        }

        self.txt_splitter = CharacterTextSplitter(chunk_size=240, chunk_overlap=30, length_function=len,
                                                  add_start_index=True)
        self.json_splitter = RecursiveJsonSplitter(max_chunk_size=240)

    def get_file(self, filename):
        file_extension = os.path.splitext(filename)[-1]
        loader = self.loader.get(file_extension, None)
        if loader:
            if file_extension == ".json":
                return loader(filename)
            elif file_extension in [".txt", ".csv"]:
                encodings_to_try = ['utf-8', 'gbk', 'latin1', 'big5']
                for encoding in encodings_to_try:
                    try:
                        load_info = loader(filename, encoding=encoding).load()
                        return load_info
                    except:
                        continue  # 继续执行下一次循环
            else:
                load_info = loader(filename).load()
                print(load_info)
                return load_info

        else:
            return None

    def handle_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()
        return data

    def is_json(self, data):
        try:
            json.loads(data)
            return True
        except:
            return False

    def split_text(self, filename):
        load_info = self.get_file(filename)
        if load_info:
            if self.is_json(load_info):
                self.end_splitter = self.json_splitter.split_text(json.loads(load_info), ensure_ascii=False)
            else:
                self.end_splitter = self.txt_splitter.split_documents(load_info)
                self.end_splitter = [doc.page_content for doc in self.end_splitter]

            return self.end_splitter

        else:
            raise "文件格式不支持"


if __name__ == "__main__":
    # 创建VectorStorageObject的实例
    vector_storage = VectorStorageObject()

    # 定义要测试的文件路径列表
    test_files = ['aa.txt', r"C:\Users\sunxiaoshou\Downloads\LLM_RAG-main\LLM_RAG-main\README.md"]

    # 遍历文件列表，测试加载和分割功能
    for file in test_files:
        print(f"处理文件: {file}")
        # 获取文件内容
        content = vector_storage.get_file(file)
        if content:
            print(f"文件 {file} 加载成功，内容类型: {type(content)}")
            # 分割文本
            splitted_content = vector_storage.split_text(file)
            print(f"文件 {file} 分割后的内容块数: {len(splitted_content)}")
            for i, chunk in enumerate(splitted_content, 1):
                print(f"块 {i}: {chunk[:100]}...")  # 打印每个块的前100个字符
        else:
            print(f"文件 {file} 加载失败或文件格式不支持")
