import json, os
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from vosk import Model, KaldiRecognizer, SetLogLevel
from llama_cpp import Llama

class ModelService(QObject):
    loaded   = pyqtSignal(bool, str)
    answered = pyqtSignal(str)
    failed   = pyqtSignal(str)

    _do_load = pyqtSignal(str)
    _do_ask  = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._model = None
        self._thread = QThread()
        self.moveToThread(self._thread)

        self._do_load.connect(self._load)
        self._do_ask.connect(self._ask)
        self._thread.start()

    # ── публичные функции ──
    def load_model(self, path_model: str):
        self._do_load.emit(path_model)

    def answer_model(self, text: str):
        self._do_ask.emit(text)

    # ── слоты в рабочем потоке ──
    @pyqtSlot(str)
    def _load(self, path_model: str):
        try:
            with open("model_settings.json", encoding="utf-8") as f:
                s = json.load(f)
            self._model = Llama(
                model_path=path_model,
                n_ctx=s["chat_max_token"],
                n_threads=s["threads"],
                use_mmap=s["mmap"],
                use_mlock=s["mlock"],
            )
            self.loaded.emit(True, "")
        except Exception as e:
            self.loaded.emit(False, str(e))

    @pyqtSlot(str)
    def _ask(self, text: str):
        if self._model is None:
            self.failed.emit("Модель не загружена")
            return
        try:
            with open("model_settings.json", encoding="utf-8") as f:
                s = json.load(f)
            r = self._model.create_chat_completion(
                messages=[
                    {"role": "system", "content": "Ты асистент помощник. Пытаешься помочь настолько насколько способен и клавное правило отвечаешь всегда коротко."},
                    {"role": "user", "content": text},
                ],
                max_tokens=s["answer_max_token"],
                temperature=s["temperature"],
            )
            self.answered.emit(r["choices"][0]["message"]["content"])
        except Exception as e:
            self.failed.emit(str(e))

    def close_model(self):
        if None == self._model:
            self._model = None
        else:
            self._model.close()
            self._model = None