import pandas as pd
import os
import sys
import numpy as np

class Tree():
    def __init__(self):
        self.texto = pd.read_csv("casas_arvore_decisao.csv", sep=';', index_col="ID")


    def ask_question(self):
        return self.question


    def check_answer(self, answer):
        if answer <= float(self.logica):
            return self.leftNode
        elif answer > float(self.logica):
            return self.rightNode
        else:
            return False


    def rec_build_tree(self, linha):
        row = self.texto.loc[linha]
        if row["Pergunta"] == "NÓ FOLHA":
            return row["A"]
        node = Tree()
        node.leftNode = Tree.rec_build_tree(self, float(row["Nó A"]))
        node.rightNode = Tree.rec_build_tree(self, float(row["Nó B"]))
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
                print("\nMe desculpe, não conheço essa opção, vamos tentar novamente? :)\n")
                response = input(self.arvore.ask_question())
                count_erros += 1

        return response, count_erros


    def verifica_saida(self, response):

        if str(response).lower() == "sair":
            print("\nFim.\n")
            sys.exit()
        else:
            pass


    def execute(self):
        counter_tickets = 0
        print("DIGITE 'SAIR' PARA FINALIZAR O PROGRAMA")
        while True:
            self.arvore = Tree.rec_build_tree(self, 1)
            count_erros=0
            while True:
                if count_erros == 2:
                    print("ERROS SUCESSIVOS\nVERIFIQUE AS OPÇÕES ANTES DE TENTAR NOVAMENTE\n")
                    print("\nMuitas informações! :/ \nPor favor me reinicie.")
                    break
                response = input(self.arvore.ask_question())
                Tree.verifica_saida(self, response)
                response, count_erros = Tree.verifica_entrada(self, response, count_erros)

                answer = self.arvore.check_answer(response)
                if answer == False:
                    print("\nMe desculpe, não conheço essa opção, vamos tentar novamente? :)")
                    count_erros+=1
                elif not Tree.is_obj(self, answer):
                    break
                else:
                    self.arvore = answer

            print(answer)

            print("-------------------------------------")


def Orquestrador_chatbot():

    """

        ORQUESTRADOR DE EXECUÇÃO DO CÓDIGO.

        # Arguments

        # Returns

    """

    # INICIANDO O APP
    app_proc = Tree()

    # EXECUTANDO
    app_proc.execute()


if __name__ == '__main__':
    sys.exit(Orquestrador_chatbot())