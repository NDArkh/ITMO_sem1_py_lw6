from random import choices, shuffle, randint, choice
from time import sleep


class Human:
    prt_type = 'Human'

    def __init__(self):
        self.name = f'{self.get_rand_name()} ({self.prt_type})'
        self.is_alive = True
        self.sex = randint(0, 1)
        self.years_left = 60

    def attack(self, other):
        print(f'{self.name} attacked {other.name}')
        other.years_left -= 5

    def produce(self, other):
        print(f'{self.name} /{self.g(self.sex)}/ <3 /{self.g(other.sex)}/ {other.name}')
        if self.sex != other.sex:
            new_obj = type(self)()
            print(f'{new_obj.name} was born!')
            return new_obj

    def time_step(self):
        self.years_left -= 1
        if self.years_left <= 0:
            self.is_alive = False

    @staticmethod
    def get_rand_name() -> str:
        abc = [ch for ch in 'qwrtpsdfghjklzxcvbnm']
        abc_ = [ch for ch in 'eyuioa']
        ret = choices(population=abc, k=randint(2, 3)) \
              + choices(population=abc_, k=randint(2, 4))
        shuffle(ret)
        return ''.join(ret).capitalize()

    @staticmethod
    def g(s: int):
        return ('F', 'M')[s]


class Warrior(Human):
    prt_type = 'Warrior'

    def __init__(self):
        super().__init__()

    def _kill(self, other):
        print(f'{other.name} was killed by {self.name}')
        other.is_alive = False

    def attack(self, other):
        super().attack(other)
        kube_res = randint(0, 100)
        if isinstance(other, Citizen):
            if kube_res <= 90:
                self._kill(other)
        if isinstance(other, type(self)):
            if kube_res <= 40:
                self._kill(other)
        if isinstance(other, Witch):
            if kube_res <= 10:
                self._kill(other)


class Citizen(Human):
    prt_type = 'Citizen'

    def __init__(self):
        super().__init__()

    def i_am_warrior(self):
        kube_res = randint(0, 100)
        if kube_res <= 20:
            print(f'{self.name} became a Warrior!')
            new_warrior = Warrior()
            new_warrior.__dict__.update(self.__dict__)
            new_warrior.name = self.name.replace(type(self).prt_type, Warrior.prt_type)

            return new_warrior
        return self


class Witch(Human):
    prt_type = 'Witch'

    def __init__(self):
        super().__init__()

    def _grab_soul(self, other):
        print(f'{self.name} grabbed soul of the {other.name}')
        delt = int(other.years_left * 0.8)
        other.years_left -= delt
        self.years_left += delt

    def attack(self, other):
        super().attack(other)
        kube_res = randint(0, 100)
        if kube_res <= 70:
            self._grab_soul(other)

    def produce(self, other):
        return other.produce(self)


class App:
    def __init__(self, start_population_n: int):
        self.population = list()
        self._init_population(start_population_n)
        self.small_wait = 1
        self.big_wait = 10

    def _init_population(self, n: int):
        for _ in range(max(10, n)):
            self.population.append((Citizen, Citizen, Citizen, Warrior, Warrior, Witch)[randint(0, 5)]())

    def love_step(self, intense_n: int = 10):
        for _ in range(intense_n):
            left = choice(self.population)
            right = choice(self.population)
            if left is not right:
                if (res := left.produce(right)) is not None:
                    self.population.append(res)
                sleep(self.small_wait)

    def aggressive_step(self, intense_n: int = 10):
        for _ in range(intense_n):
            left = choice(self.population)
            right = choice(self.population)
            left.attack(right)
            if not right.is_alive:
                self.population.remove(right)
            sleep(self.small_wait)

    def update_population(self):
        for pers in self.population.copy():
            pers.years_left -= 1
            if not pers.is_alive:
                print(f'{pers.name} was found dead!')
                self.population.remove(pers)
                sleep(1)

        for pers in self.population:
            if isinstance(pers, Citizen):
                pers = pers.i_am_warrior()

    def show_stats(self):
        cnts = {'ct': 0, 'wr': 0, 'wt': 0}
        for pers in self.population:
            if isinstance(pers, Citizen):
                cnts['ct'] += 1
            elif isinstance(pers, Warrior):
                cnts['wr'] += 1
            elif isinstance(pers, Witch):
                cnts['wt'] += 1

        print(f'There are...'
              f'\n\tcitizens:\t{cnts["ct"]:>6}'
              f'\n\twarriors:\t{cnts["wr"]:>6}'
              f'\n\twitches:\t{cnts["wt"]:>6}')

    def sim_loop(self, borders: tuple[int, int]):
        self.show_stats()

        while borders[0] < len(self.population) < borders[1]:
            print(f'\n--- stage: "love" ---------------\n')
            self.love_step()
            print(f'\n--- stage: "aggressive" ---------\n')
            self.aggressive_step()
            print(f'\n--- stage: "population stats" ---\n')
            self.update_population()
            self.show_stats()
            sleep(self.big_wait)


if __name__ == '__main__':
    App(25).sim_loop((10, 100))
