from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.properties import ColorProperty
from kivy.core.text import LabelBase
from kivy.core.window import Window

#Window.size = (300, 500)

KV = '''
#:import KivyLexer kivy.extras.higeLight.KivyLexer
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer

BoxLayout:
  HotReloadViewer:
    path: app.path_to_kv_file
    errors: True
    errors_text_color: 0, 0, 0, 0
    errors_background_color: app.theme_cls.bg_dark

'''

class Example(MDApp):
  path_to_kv_file = 'mainScreen.kv'
  bg_color = ColorProperty()
  def build(self):
      return Builder.load_string(KV)

# затирание экрана сверху  
  def __init__ (self, **kwargs):
    super().__init__(**kwargs)
    self.bg_color = self.theme_cls.primary_color
    
Example().run()
