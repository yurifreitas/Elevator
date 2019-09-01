from random import randint
from copy import deepcopy
import json
import os


class Elevator(object):
    """ lista de passageiros, piso atual e direção"""
    passager_list = list()
    current_floor = 0
    direction = 1

    def move(self):
        """função que move o elevador um andar acima ou abaixo"""

        self.current_floor += self.direction

    def exit_passagers(self):
        """
        Função que remove o passageiro do elevador caso ele estaja no seus respectivo andar
        """
        for passager in list(self.passager_list):
            if passager.destination_floor == self.current_floor:
                self.remove_passager(passager)

    def add_passager(self, passager):
        """Adiciona Passageiros da lista do elevador"""
        self.passager_list.append(passager)

    def remove_passager(self, passager):
        """Remove passageiros da lista do elevador"""
        self.passager_list.remove(passager)


class Passager(object):
    """Passager unico id ,
    andar de inicio e andar destino.
    """
    start_floor = None
    destination_floor = None
    id = None

    def __init__(self, id, floor_num_total):
        """Inicializa os passageiro e define seu destino
        """
        self.id = id
        self.start_floor = randint(0, floor_num_total - 1)
        self.destination_floor = randint(0, floor_num_total - 2)
        if self.destination_floor >= self.start_floor:
            self.destination_floor += 1


class Building(object):
    """numero de andares, lista de passageiros fora e dentro do objeto elevador,
    inteiro que define o numero da estratégia a ser usado.
    0 = direction_default_strategy()
    1 = direction_bad_strategy()
    """
    passager_list = list()
    elevator = None
    strategy = 0

    def __init__(self, num_of_floors, passagers_num):
        """Cria um edificio e adiciona uma lista de passageiros usando a
        função sort para embaralhar os pedidos
        """
        self.num_of_floors = num_of_floors
        self.passagers_num = passagers_num

        for i in range(passagers_num):
            self.passager_list.append(Passager(i, num_of_floors))
        self.passager_list = sorted(self.passager_list, key=lambda x: x.start_floor)
        self.elevator = Elevator()

    """LISTA DE ESTRATÉGIAS A SEREM USADAS"""

    def direction_default_strategy(self):
        """Estratégia padrão o elevador vai pra cima e para baixo"""
        if self.elevator.current_floor >= self.num_of_floors - 1:
            self.elevator.direction = -1
        elif self.elevator.current_floor <= 0:
            self.elevator.direction = 1

    def direction_bad_strategy(self):
        """Estratégia ruim o elevador segue para o andar que o primeiro passageiro
        informar e assim sucetivamente, caso não tenha passageiros fica subindo e descendo
        """
        if len(self.elevator.passager_list) is 0:
            self.direction_default_strategy()
            return
        firstval = self.elevator.passager_list[0].destination_floor
        if self.elevator.current_floor > firstval:
            self.elevator.direction = -1
        else:
            self.elevator.direction = 1

    def direction_new_strategy(self):
        """Estratégia ruim o elevador segue para o andar que o primeiro passageiro
        informar e assim sucetivamente, caso não tenha passageiros fica subindo e descendo
        """
        if len(self.elevator.passager_list) is 0:
            self.direction_default_strategy()
            return
        firstval = self.elevator.passager_list[-1].destination_floor
        if self.elevator.current_floor > firstval:
            self.elevator.direction = -1
        else:
            self.elevator.direction = 1

    def direction_new_order_strategy(self):
        """Estratégia ruim o elevador segue para o andar que o ultimo passageiro
        informar e assim sucetivamente, caso não tenha passageiros fica subindo e descendo
        """
        if len(self.elevator.passager_list) is 0:
            self.direction_default_strategy()
            return
        firstval = self.elevator.passager_list[randint(0, len(self.elevator.passager_list))].destination_floor
        if self.elevator.current_floor > firstval:
            self.elevator.direction = -1
        else:
            self.elevator.direction = 1

    def enter_passagers(self):
        """Pega todos os passsageiros  do piso adiciona ao elevador e remove da lista"""
        for passager in list(self.passager_list):
            if passager.start_floor == self.elevator.current_floor:
                self.elevator.add_passager(passager)
                self.passager_list.remove(passager)

    def run(self):
        """
        Função que roda o core do elevador
        """

        self.enter_passagers()
        if self.strategy == 0:
            self.direction_default_strategy()
        elif self.strategy == 1:
            self.direction_bad_strategy()
        elif self.strategy == 2:
            self.direction_new_strategy()
        elif self.strategy == 3:
            self.direction_new_order_strategy()
        self.elevator.move()
        self.elevator.exit_passagers()

    def output(self):
        """Retorna a quantidade de paradas que o elevador fez de acordo com a estratégia.
        """
        total_number = 0

        while self.awaiting_passagers():
            self.run()
            total_number += 1

        return str(total_number)

    def awaiting_passagers(self):
        """Se não houver passageiro no elevador retorna falso"""
        if len(self.passager_list) > 0 or len(self.elevator.passager_list) > 0:
            return True
        return False


def start():
    """Cria o objetos Build e gera uma copia identica dos objetos"""
    building_default = Building(10, 8)
    building_bad = deepcopy(building_default)
    building_new = deepcopy(building_default)
    building_new_order = deepcopy(building_default)

    default = building_default.output()
    default_str = {"name": "Padrao", "steps": default}

    building_bad.strategy = 1
    bad = building_bad.output()
    bad_str = {"name": "Ruim", "steps": bad}

    building_new.strategy = 2
    new = building_new.output()
    new_str = {"name": "Nova", "steps": new}

    building_new.strategy = 3
    new_order = building_new_order.output()
    new_order_str = {"name": "NovaOrdem", "steps": new_order}

    fname = 'elevator.json'

    if not os.path.isfile(fname):
        entry = [default_str, bad_str, new_str, new_order_str]
        with open(fname, mode='w') as f:
            f.write(json.dumps(entry))
    else:

        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(default_str)
        feeds.append(bad_str)
        feeds.append(new_str)
        feeds.append(new_order_str)
        with open(fname, mode='w') as f:
            f.write(json.dumps(feeds))


if __name__ == "__main__":
    start()
