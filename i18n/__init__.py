import json
import os

class I18n:
    def __init__(self, language='zh_CN'):
        self.language = language
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), f'{self.language}.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"Translation file for {self.language} not found. Using original strings.")

    # ... 其余代码保持不变 ...

# 创建全局翻译实例
i18n = I18n()
_ = i18n._

def translate_class(cls):
    for key, value in cls.__dict__.items():
        if isinstance(value, str):
            setattr(cls, key, _(value))
    return cls