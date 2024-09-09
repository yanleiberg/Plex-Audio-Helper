import json
import os

class I18n:
    def __init__(self, language='zh_CN'):
        self.language = language
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), f'locales/{self.language}.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"Translation file for {self.language} not found. Using original strings.")

    def _(self, text):
        return self.translations.get(text, text)

    def translate_class(self, cls):
        for key, value in cls.__dict__.items():
            if isinstance(value, str):
                setattr(cls, key, self._(value))
        return cls

    def set_language(self, language):
        self.language = language
        self.load_translations()

# 创建全局翻译实例
i18n = I18n()
_ = i18n._
translate_class = i18n.translate_class