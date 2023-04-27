from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import TwoLineRightIconListItem
from kivymd.uix.list import ImageRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.logger import Logger

from kivy.clock import Clock
import sys, time, threading
import subprocess
from functools import partial
from ping3 import ping
from config import Config
from util import comando_shutdown

class Computadores(MDFloatLayout):
    def __init__(self, **kwargs):
        super(Computadores, self).__init__(**kwargs)
        self.computadores = Config.get_computadores()
        self.itens_lista = []
        self.thread_loop = True
        threading.Thread(target=self.thread_verifica_computadores_ligados).start()
        Clock.schedule_interval(self.atualizar_lista_computadores, 5)
        
    def thread_verifica_computadores_ligados(self):
        Logger.info('Iniciando Thread')
        
        while self.thread_loop:
            self.itens_lista.clear()
            for computador in self.computadores:
                #desativado = False
            
                comp_esta_ligado = ping(computador['IP'], timeout=0.1)
                Logger.info('comp_esta_ligado: {}'.format(comp_esta_ligado))
                if comp_esta_ligado is not None:
                    #icon = ImageRightWidget(source='icons/ligado.png')
                    computador['status'] = True  
                else:
                    computador['status'] = False
                    #icon = ImageRightWidget(source='icons/desligado.png')
                    #desativado = True
                
                ''' item = TwoLineRightIconListItem(text=computador['nome'], secondary_text=computador['descricao'], 
                                    on_press=partial(self.show_confirmar_desligamento, computador), disabled=desativado)
                
                item.add_widget(icon) '''
                
                self.itens_lista.append(computador)
            
            time.sleep(3)
        
        
    def atualizar_lista_computadores(self, *args):
        
        Logger.info('Atualizando MDList')
        self.ids.lista_computadores.clear_widgets()
            
        for computador in self.itens_lista:
            desativado = False
            if computador['status']:
                icon = ImageRightWidget(source='icons/ligado.png')
            else:
                icon = ImageRightWidget(source='icons/desligado.png')
                desativado = True
                
            item = TwoLineRightIconListItem(text=computador['nome'], secondary_text=computador['descricao'], 
                                    on_press=partial(self.show_confirmar_desligamento, computador), disabled=desativado)
            
            item.add_widget(icon)
            self.ids.lista_computadores.add_widget(item)
            
            
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
        threading.Thread(target=subprocess.run, args=(comando, )).start()
        
        self.dialog.dismiss()
        
    def fechar_dialog(self, inst):
        self.dialog.dismiss()
        
    def fechar_programa(self):
        self.thread_loop = False
        sys.exit()

    
        
        

class Tela_principalApp(MDApp):
    
    title = 'Computadores Ligados'
    Window.size = (500,600)
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Computadores()
    
