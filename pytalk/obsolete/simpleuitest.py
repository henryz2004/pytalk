from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
import random

class Workspace(FloatLayout):

    def click(self):
        self.ids.lbl.text = str(random.randint(1,6))

class KivyApp(App):

    def build(self):
        return Workspace()

if __name__ == '__main__':
    KivyApp().run()
