from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
Window.size = [700, 500]

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, BooleanProperty, StringProperty
)

from kivy.graphics import Canvas, Rectangle, Color

import random

class Home(Screen):
    pass

class TabItem(FloatLayout):
    pass

class TabLayout(FloatLayout):
    orientation = StringProperty("left")
    multicolor = True
    tab_color = ListProperty([.2, .2, 1, 1])
    
    _menu = ListProperty([])
    layout_colors = ListProperty()
    menu_items = {}
    content_items = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Chama todas as funções no seu tempo devido para a redenrização correta.
        Clock.schedule_once(self.get_tab_items, .1)
        Clock.schedule_once(self.color, .2)
        Clock.schedule_once(self.menu, .3)
        Clock.schedule_once(self.content, .4)
        Clock.schedule_once(self.items, .5)
        Clock.schedule_once(self.tab_item_manager, .6)

    def get_tab_items(self, obj):
        # Copia endereços dos tab_items declarados no kv file.
        self.addresses = self.children[::-1]
        print(self.addresses)
        # Nomeia cada endereço encontrado como número.
        self._menu = [str(i) for i in range(len(self.addresses))]

    # Define as cores dos botões e screebs.
    def color(self, obj):
        self.layout_colors = [
            [random.random(), random.random(), random.random(), 1] 
            for i in range(len(self._menu))
        ] if self.multicolor == True else [self.tab_color for i in range(len(self._menu))]

    # Monta o layout do menu.
    def menu(self, obj):
        self.menu_content = Builder.load_string(f"""
ScrollView:
    do_scroll_y: True
    do_scroll_x: False
    size_hint_x: None
    width: {Window.size[0] * 0.2}
    canvas.before:
        Color:
            rgba: [.25, .25, .25, 1]
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        id: "container"
        orientation: "vertical"
        #padding: 5
        spacing: 5
        size_hint: [1, None]
        height: self.minimum_height
""")
        self.container = self.menu_content.children[0]
        self.add_widget(self.menu_content)    

    # Monta o layout das Screens
    def content(self, obj):
        self.screen_content = ScreenManager(
            size_hint = [None, None],
            size = [Window.size[0] * 0.8, Window.size[1]],
            pos = [self.menu_content.width, 0]
        )
        self.screen_content.transition.direction = 'right'
        with self.screen_content.canvas.before:
            Color(.2, .2, .2, 1)
            Rectangle(pos = self.screen_content.pos, size = self.screen_content.size)
        
        self.add_widget(self.screen_content)

    # Fazer a gestão dos botões como toggle button e das screens
    def switch(self, but):
        if but.background_color == [.2,.2,.2,1]:
            for b in self.menu_items:
                self.menu_items[b].background_color = [.2,.2,.2,1]
            but.background_color = self.content_items[but.text].background_color
            self.screen_content.current = but.id

    # Preenche o menu e a screencontent com items de estrutura.
    def items(self, obj):
        for i, mc in enumerate(self._menu):
            # Criar os botões para o menu
            self.menu_items[mc] = Button(
                id = f'screen{i}', text = mc, 
                size_hint_y = None, height = 60,
                background_color = [.2,.2,.2,1],
                background_normal = ''
            )
            self.menu_items[mc].bind(on_release = self.switch)

            # Adicionar o botão no container
            self.container.add_widget(self.menu_items[mc])

            # Criar as screens para o content
            self.content_items[mc] = Builder.load_string(f"""
Screen:
    name: '{'screen' + str(i)}'
    background_color: {self.layout_colors[i]}
    size_hint: None, None
    size: {self.screen_content.size}
    pos: {self.screen_content.pos}
    FloatLayout:
        #id: '{'screen' + 'str(i)'}'
        canvas.before:
            Color:
                rgba: root.background_color
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10,]
""")
            
            # Adicionar a screen criada na screen content
            self.screen_content.add_widget(self.content_items[mc])
            if i == 0:
                self.menu_items[mc].background_color = self.content_items[mc].background_color

    # Preenche cada screen da screen_content com os tab_item,
    def tab_item_manager(self, obj):
        for i, child in enumerate(self.addresses):
            self.remove_widget(child)
            self.content_items[str(i)].add_widget(child)

class MainApp(App):
    title = "ScreenLayout"

    def build(self):
        return Builder.load_string("""
<TabLayout>:
    orientation:
    multicolor:
    tab_color:
    menu:
    layout_colors:

Home:
    BoxLayout:
        orientation: 'vertical'
        TabLayout:
            TabItem:
                Label:
                    text: 'Screen 1'
            TabItem:
                TextInput:
                    hint_text: 'Screen 2'
            TabItem:
                Carousel:
                    Button:
                        text: 'Screen 3'

""")

if __name__ == "__main__":
    MainApp().run()