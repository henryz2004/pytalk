from kivy.app import App
from kivy.uix.scrollview import ScrollView

class ScrollLayout(ScrollView):

    pass

class ScrollApp(App):

    def build(self):
        return ScrollLayout()

if __name__ == '__main__':
    ScrollApp().run()
