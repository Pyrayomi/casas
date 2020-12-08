import pandas as pd
import os
import sys
import numpy as np
import pygubu
import tkinter as tk
import threading
import time

class nos():
    def __init__(self):
        pass
    def ask_question(self):
        return self.question

    def check_answer(self, answer):
        if answer <= float(self.logica):
            return self.leftNode
        elif answer > float(self.logica):
            return self.rightNode
        else:
            return False


class Programa():
    def __init__(self):
        self.texto = pd.read_csv("casas_arvore_decisao.csv", sep=';', index_col="ID")

        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # 2 - INICIALIZANDO O OBJETO TKINTER
        caminho_parametro = os.getcwd() + "\interface.ui"
        builder.add_from_file(caminho_parametro)
        self.root = builder.get_object("Toplevel_1")
        self.root.state('zoomed')

        # 3 - CRIANDO A JANELA PRINCIPAL
        # ESTRUTURA
        self.mainwindow = builder.get_object('Frame_1', self.root)
        self.chat_historico = builder.get_object('Frame_historico', self.root)
        self.bt_enviar = builder.get_object('Button_1')
        self.entry_chat = builder.get_object('Entry_1')

        # VARIAVEL DE ATUALIZAÇÃO DA TELA
        self.counter_tickets = 0

        # aguarda resposta
        self.resposta = False




    def rec_build_tree(self, linha):
        row = self.texto.loc[linha]
        if row["Pergunta"] == "NÓ FOLHA":
            return row["A"]
        node = nos()
        node.leftNode = Programa.rec_build_tree(self, float(row["Nó A"]))
        node.rightNode = Programa.rec_build_tree(self, float(row["Nó B"]))
        node.question = row["Pergunta"]
        node.answerTrue = row["A"]
        node.answerFalse = row["B"]
        node.logica = row["Lógica"]
        return node


    def is_obj(self, obj):
        return False if type(obj).__name__ == "str" else True


    def verifica_entrada(self, response, count_erros):

        try:
            response = float(response)
        except:
            while (isinstance(response, float) or isinstance(response, int)) is False:
                if count_erros == 2:
                    print("\nMuitas informações! :/ \nPor favor me reinicie.")
                    sys.exit()
                tk.Label(self.chat_historico,
                         text="ERROS SUCESSIVOS\nVERIFIQUE AS OPÇÕES ANTES DE TENTAR NOVAMENTE\n").grid(sticky='e',
                                                                                                        row=self.counter_tickets,
                                                                                                        column=0)
                self.counter_tickets = self.counter_tickets + 1
                response = input(self.arvore.ask_question())
                count_erros += 1

        return response, count_erros


    def verifica_saida(self, response):

        if str(response).lower() == "sair":
            print("\nFim.\n")
            sys.exit()
        else:
            pass


    def atualiza_tela(self, texto):
        tk.Label(self.chat_historico, text=texto).grid(
            sticky='e', row=self.counter_tickets,
            column=0)
        self.counter_tickets = self.counter_tickets + 1


    def orquestra_logica(self):
        print("DIGITE 'SAIR' PARA FINALIZAR O PROGRAMA")
        Programa.atualiza_tela(self, "Olá, sou Eu... robo... e estou aqui\npara te ajudar a encontrar uma casa ideal,\nmas antes me tire umas dúvidas!!!")
        while True:
            self.arvore = Programa.rec_build_tree(self, 1)
            count_erros=0
            while True:
                if count_erros == 2:
                    Programa.atualiza_tela(self, "ERROS SUCESSIVOS\nVERIFIQUE AS OPÇÕES ANTES DE TENTAR NOVAMENTE\n")
                    Programa.atualiza_tela(self, "\nMuitas informações! :/ \nPor favor me reinicie.")
                    break

                Programa.atualiza_tela(self, self.arvore.ask_question())
                #response = input(self.arvore.ask_question())
                while self.resposta is False:
                    time.sleep(1)

                response = self.entry_chat.get()

                Programa.atualiza_tela(self, response)

                self.resposta = False
                self.entry_chat.delete(0, "end")

                Programa.verifica_saida(self, response)
                response, count_erros = Programa.verifica_entrada(self, response, count_erros)

                answer = self.arvore.check_answer(response)
                if answer == False:

                    Programa.atualiza_tela(self, "\nMe desculpe, não conheço essa opção, vamos tentar novamente? :)")
                    count_erros+=1
                elif not Programa.is_obj(self, answer):
                    Programa.atualiza_tela(self, answer)
                    Programa.atualiza_tela(self, "-------------------------------------")
                    Programa.atualiza_tela(self, "Bora mais uma vez ?")
                    break
                else:
                    self.arvore = answer

            print(answer)


    def bt_enviar(self):

        try:
            self.resposta = True
        except Exception as ex:
            print(ex)

    def bind_controle_telas(self):

        """
            FUNÇÃO RESPONSÁVEL POR DEFINIR OS COMANDOS DE TODOS OS BOTÕES

        @return:
        """

        try:
            self.bt_enviar.config(command=lambda: Programa.bt_enviar(self))
        except Exception as ex:
            print(ex)


    def execute(self):

        """

            EXECUTA A APLICAÇÃO.

            # Arguments

            # Returns

        """

        t = threading.Thread(target=Programa.orquestra_logica, daemon=False, args=(self,))
        t.start()

        # DEVOLVE PARA A BARRA DE TAREFAS
        self.root.iconify()
        # PUXA DA BARRA DE TAREFAS
        self.root.deiconify()
        # O MAINLOOP MANTÉM O FRAME SENDO UTILIZADO EM LOOP
        self.root.mainloop()


def Orquestrador_chatbot():

    """

        ORQUESTRADOR DE EXECUÇÃO DO CÓDIGO.

        # Arguments

        # Returns

    """

    # INICIANDO O APP
    app_proc = Programa()

    # APLICANDO FUNCAO NO BOTAO
    app_proc.bind_controle_telas()

    # EXECUTANDO
    app_proc.execute()


if __name__ == '__main__':
    sys.exit(Orquestrador_chatbot())