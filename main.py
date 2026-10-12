from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import threading


class ChatApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Область истории чата
        self.scroll = ScrollView(size_hint_y=0.8)
        self.history = Label(
            text="Neurodip: Привет! Задай вопрос.\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        self.history.bind(
            width=lambda *x: setattr(self.history, 'text_size', (self.history.width, None)),
            texture_size=lambda *x: setattr(self.history, 'height', self.history.texture_size[1])
        )
        self.scroll.add_widget(self.history)
        root.add_widget(self.scroll)

        # Поле ввода и кнопка
        input_layout = BoxLayout(size_hint_y=0.2, spacing=5)
        self.input_box = TextInput(multiline=False, hint_text="Напиши сообщение...")
        input_layout.add_widget(self.input_box)

        self.send_btn = Button(text="Отправить", size_hint_x=0.3)
        self.send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(self.send_btn)

        root.add_widget(input_layout)
        return root

    def send_message(self, instance):
        user_text = self.input_box.text.strip()
        if not user_text:
            return
        self.history.text += f"\nТы: {user_text}\n"
        self.input_box.text = ""
        threading.Thread(target=self.get_ai_response, args=(user_text,)).start()

    def get_ai_response(self, user_text):
        try:
            r = requests.post(
                "http://127.0.0.1:8080/v1/chat/completions",
                json={
                    "messages": [
                        {"role": "system", "content": "Ты — Нейродип, полезный ассистент. Отвечай кратко."},
                        {"role": "user", "content": user_text}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 512
                },
                timeout=180
            )
            reply = r.json()["choices"][0]["message"]["content"].strip()
            self.history.text += f"Neurodip: {reply}\n"
        except Exception as e:
            self.history.text += f"Neurodip: [Ошибка: {e}]\n"


if __name__ == "__main__":
    ChatApp().run()
