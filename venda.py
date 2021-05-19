from datetime import date, datetime
import csv
import os

class Venda:

    def __init__(self, cod_venda="", nome="", data="", valor="", data_inicio="", data_fim=""):
        self.cod_venda = cod_venda
        self.nome = nome
        self.data = data
        self.valor = valor
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def select_lista(self):
        lista = []
        with open('vendas.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lista.append(row)

        return lista

    def add_venda(self):
        try:
            with open('vendas.csv', 'a', newline='') as csvfile:
                fieldnames = ['cod_venda', 'nome', 'data', 'valor']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if (os.stat('vendas.csv').st_size == 0):
                    writer.writeheader()

                self.cod_venda = int(self.ultimo_cod_venda()) + 1
                writer.writerow({'cod_venda': self.cod_venda, 'nome': self.nome, 'data': self.data, 'valor': self.valor})

            return "Venda adicionada com sucesso"
        except:
            return "Não foi possível adionar uma nova venda"
    
    def ultimo_cod_venda(self):
        with open('vendas.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.cod_venda = row['cod_venda']
        
        return self.cod_venda
    
    def altera_venda(self):
        try:
            reader_list = []

            with open('vendas.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row_to_override = {'cod_venda': self.cod_venda, 'nome': self.nome, 'data': self.data, 'valor': self.valor}
                    if (self.cod_venda == row['cod_venda']):
                        reader_list.append(row_to_override)
                    else: 
                        reader_list.append(row)
            
            with open('vendas.csv', 'w', newline='',) as csvfile:
                fieldnames = ['cod_venda', 'nome', 'data', 'valor']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

            with open('vendas.csv', 'a', newline='') as csvfile:
                fieldnames = ['cod_venda', 'nome', 'data', 'valor']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for row in reader_list:
                    writer.writerow(row)

            return "Venda alterada com sucesso"
        except:
            return "Não foi possível alterar a venda"

    def exclui_venda(self):
        try:
            reader_list = []
        
            with open('vendas.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if (self.cod_venda != row['cod_venda']):
                        reader_list.append(row)
            
            with open('vendas.csv', 'w', newline='',) as csvfile:
                fieldnames = ['cod_venda', 'nome', 'data', 'valor']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

            with open('vendas.csv', 'a', newline='') as csvfile:
                fieldnames = ['cod_venda', 'nome', 'data', 'valor']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for row in reader_list:
                    writer.writerow(row)
        
            return "Venda excluida com sucesso"
        except:
            return "Não foi possível excluir a venda"

    def busca_vendas(self):
        reader_list = []

        with open('vendas.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                nome_aux = row['nome']
                nome_aux = nome_aux.upper()

                self.nome = str(self.nome).upper()

                if (nome_aux.find(self.nome) >= 0):
                    reader_list.append(row)

        return reader_list

    def busca_maior_venda(self):
        reader_list = []

        with open('vendas.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            maior_venda = 0.0

            for row in reader:
                valor = float(row['valor'])

                if (valor > maior_venda):
                    maior_venda = valor
                    
                    if (len(reader_list) > 0):
                        reader_list = []
                
                    reader_list.append(row)

                elif (valor == maior_venda):
                    reader_list.append(row)
        
        return reader_list

    def busca_venda_data(self):
        reader_list = []

        with open('vendas.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
    
            for row in reader:
                data = row['data']
                data = datetime.strptime(data, '%d/%m/%Y').date()

                if (data >= self.data_inicio and data <= self.data_fim):
                    reader_list.append(row)

        return reader_list

            
