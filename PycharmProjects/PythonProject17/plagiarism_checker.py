# 创建 plagiarism_checker.py 文件，包含以下基本功能：

import sys
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import datetime

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

    def check_plagiarism(self, original_path, copied_path, output_path=None):
        original_text = self.read_file(original_path)
        copied_text = self.read_file(copied_path)
        similarity = self.calculate_similarity(original_text, copied_text)

        if output_path:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(output_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n{'=' * 50}\n")
                    f.write(f"查重时间：{current_time}\n")
                    f.write(f"原文文件：{original_path}\n")
                    f.write(f"对比文件：{copied_path}\n")
                    f.write(f"重复率：{similarity:.2%}\n")
                    f.write(f"相似度分数：{similarity:.4f}\n")
                print(f"结果已追加保存到：{output_path}")
            except Exception as e:
                print(f"写入输出文件时出错：{e}")
                sys.exit(1)

        print(f"查重完成！重复率：{similarity:.2%}")
        return similarity


def main():
    if len(sys.argv) < 3:
        print("用法: python plagiarism_checker.py <原文文件> <抄袭版文件> [输出文件]")
        sys.exit(1)

    checker = PlagiarismChecker()
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    checker.check_plagiarism(sys.argv[1], sys.argv[2], output_path)

if __name__ == "__main__":
    main()


