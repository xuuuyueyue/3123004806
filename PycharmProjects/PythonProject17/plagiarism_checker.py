# 创建 plagiarism_checker.py 文件，包含以下基本功能：

import sys
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class PlagiarismChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def preprocess_text(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        words = jieba.cut(text)
        return ' '.join(words)

    def calculate_similarity(self, original_text, copied_text):
        original_processed = self.preprocess_text(original_text)
        copied_processed = self.preprocess_text(copied_text)
        tfidf_matrix = self.vectorizer.fit_transform([original_processed, copied_processed])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]

    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"错误：文件 {file_path} 不存在")
            sys.exit(1)
        except Exception as e:
            print(f"读取文件时出错：{e}")
            sys.exit(1)

    def check_plagiarism(self, original_path, copied_path):
        original_text = self.read_file(original_path)
        copied_text = self.read_file(copied_path)
        similarity = self.calculate_similarity(original_text, copied_text)
        print(f"查重完成！重复率：{similarity:.2%}")
        return similarity

def main():
    if len(sys.argv) != 3:
        print("用法: python plagiarism_checker.py <原文文件> <抄袭版文件>")
        sys.exit(1)

    checker = PlagiarismChecker()
    checker.check_plagiarism(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()


