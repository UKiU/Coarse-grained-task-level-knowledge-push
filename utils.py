import jq
import numpy as np
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from langchain_core.documents import Document

from langchain_community.document_loaders.base import BaseLoader

class CustomJSONLoader(BaseLoader):
    """Load a `JSON` file using a `jq` schema.

    """

    def __init__(
            self,
            file_path: Union[str, Path],
            content_schema: str,
            metadata_schema: str,
    ):
        """Initialize the JSONLoader.

        参数:
            file_path (Union[str, Path]): JSON 或 JSON Lines 文件的路径。
            content_schema (str): 用来从 JSON 中提取数据或文本的 jq 模式。

        """

        self.file_path = Path(file_path).resolve()
        self._content_schema = jq.compile(content_schema)
        self._metadata_schema = jq.compile(metadata_schema)

    def load(self) -> List[Document]:
        """从 JSON 文件中加载并返回文档。"""
        docs: List[Document] = []
        self._parse(self.file_path.read_text(encoding="utf-8"), docs)
        return docs

    def _parse(self, content: str, docs: List[Document]) -> None:
        """将给定内容转换为文档。"""
        # content : 原始的JSON
        # json.loads(content)：JSON 格式的字符串 content 转换为 Python 的数据结构。具体转换为哪种形式的数据结构取决于原始 JSON 字符串的内容：

        # 根据jq编译查找到的结果
        data = self._content_schema.input(json.loads(content)).all()
        metadata = self._metadata_schema.input(json.loads(content)).all()

        for i, (sample1,sample2) in enumerate(zip(data,metadata), len(docs) + 1):
            if sample1 and sample2:
                metadata = {"result": sample1, "source": self.file_path}
                docs.append(Document(page_content=sample2, metadata=metadata))

def cosine_similarity(A, B):
    # 使用numpy的dot函数计算两个数组的点积
    # 点积是向量A和向量B在相同维度上对应元素乘积的和
    dot_product = np.dot(A, B)

    # 计算向量A的欧几里得范数（长度）
    # linalg.norm默认计算2-范数，即向量的长度
    norm_A = np.linalg.norm(A)

    # 计算向量B的欧几里得范数（长度）
    norm_B = np.linalg.norm(B)

    # 计算余弦相似度
    # 余弦相似度定义为向量点积与向量范数乘积的比值
    # 这个比值表示了两个向量在n维空间中的夹角的余弦值
    return dot_product / (norm_A * norm_B)