import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout

class AnswerInput(BoxLayout):
    pass

class Main(TabbedPanel):
    pass


class MyApp(App):

    def build(self):
        return  Main()


if __name__ == '__main__':
    MyApp().run()