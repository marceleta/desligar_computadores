from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import TwoLineRightIconListItem
from kivymd.uix.list import ImageRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window

from kivy.clock import Clock
import sys
import subprocess
from functools import partial
from config import Config
from util import ping
from util import comando_shutdown

class Computadores(MDFloatLayout):
    def __init__(self, **kwargs):
        super(Computadores, self).__init__(**kwargs)
        self.computadores = Config.get_computadores()
        self.rodar_atualizacao()
        
    def carregar_lista_computadores(self):
        
        widget_lista = self.ids.lista_computadores
        
        for computador in self.computadores:
            icon = ImageRightWidget(source='icons/desligado.png')
            
            item = TwoLineRightIconListItem(text=computador['nome'], secondary_text=computador['descricao'], 
                                   on_press=partial(self.show_confirmar_desligamento, computador))
            item.add_widget(icon)
            
            widget_lista.add_widget(item)
            
            
    def show_confirmar_desligamento(self, computador, dt):
        
        self.dialog = MDDialog(
            text='Deseja desligar o computador: '+computador['nome'],
            title='Confirme sua escolha',
            buttons = [
                MDFlatButton(
                    text='Cancel',
                    on_release=self.fechar_dialog
                ),
                MDFlatButton(
                    text='Desligar',
                    on_release=partial(self.desligar_computador, computador)                    
                )
            ]
        )
        self.dialog.open()
        
        
    def desligar_computador(self, computador, dt):
        comando = comando_shutdown(computador)
        subprocess.run(comando)
        
        self.dialog.dismiss()
        
    def fechar_dialog(self, inst):
        self.dialog.dismiss()
        
    def fechar_programa(self):
        sys.exit()
        
        
    def atualizar_status_computadores(self, dt):
        
                
        self.ids.lista_computadores.clear_widgets()
        
        for computador in self.computadores:
            comp_ligado = ping(computador['IP'])
            desativado = False    
            
            if comp_ligado == 0:
                icon = ImageRightWidget(source='icons/ligado.png')
                
            else:
                icon = ImageRightWidget(source='icons/desligado.png')
                desativado = True
                
            linha = TwoLineRightIconListItem(text=computador['nome'], secondary_text=computador['descricao'], 
                            on_press=partial(self.show_confirmar_desligamento, computador), disabled=desativado)
            
            linha.add_widget(icon)
            self.ids.lista_computadores.add_widget(linha)
            
            
        print('atualizando lista de computadores')
            
    
    def rodar_atualizacao(self):
        Clock.schedule_once(self.atualizar_status_computadores, 2)
        Clock.schedule_interval(self.atualizar_status_computadores, 20)
        
    
        
        

class Tela_principalApp(MDApp):
    
    title = 'Computadores Ligados'
    Window.size = (500,600)
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Computadores()
    
