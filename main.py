class AssaultRifle:
    def __init__(self, magazine_capacity=None, firing_rate=None,
                 firing_distance=None):
        """
        base class of weapon classes hierarchy
        parameters are equals to class fields, so you can easily change it
        at child by super.init call with *args
        
        :arg magazine_capacity: capacity of one magazine
        :arg firing_rate: shots that can be done while a minute
        :arg firing_distance: effective distance of shooting in metres
        """
        self.magazine_capacity = 30 if magazine_capacity is None \
            else magazine_capacity
        self.firing_rate = 600 if firing_rate is None \
            else firing_rate
        self.firing_distance = 800 if firing_distance is None \
            else firing_distance

    def __add__(self, other):
        """
        :param other: AssaultRiffle | child class object
        :return: **kwargs that contains absolute difference between objects fields
        """
        return {
            'magazine_capacity':
                abs(self.magazine_capacity - other.magazine_capacity),
            'firing_rate':
                abs(self.firing_rate - other.firing_rate),
            'firing_distance':
                abs(self.firing_distance - other.firing_distance)
        }

    def __str__(self):
        return f'\t{self.magazine_capacity=}' \
               f'\n\t{self.firing_rate=}' \
               f'\n\t{self.firing_distance=}' \
               f'\n\t{self.get_magazine_shot_out_secs()=}' \
               f'\n\t{self.get_frate_to_fdistance_ratio()=}'

    def get_magazine_shot_out_secs(self) -> float:
        """
        :return: seconds to shot out full magazine
        """
        return self.magazine_capacity / self.firing_rate * 60

    def get_frate_to_fdistance_ratio(self) -> float:
        """
        :return: ratio of firing rate to firing effective distance
        (first divided to second)
        """
        return self.firing_rate / self.firing_distance


class Pistol(AssaultRifle):
    def __init__(self):
        """ the Pistol class with built-in parameters """
        super().__init__(
            magazine_capacity=8,
            firing_rate=20,
            firing_distance=100
        )


class Carbine(AssaultRifle):
    def __init__(self):
        """ the Carbine class with built-in parameters """
        super().__init__(
            magazine_capacity=10,
            firing_rate=4,
            firing_distance=600
        )


class SniperRifle(AssaultRifle):
    def __init__(self):
        """ the SniperRifle class with built-in parameters """
        super().__init__(
            magazine_capacity=10,
            firing_rate=2,
            firing_distance=1200
        )


if __name__ == '__main__':
    glsep = "-" * 50

    objects_list = [
        AssaultRifle(), Pistol(), Carbine(), SniperRifle()
    ]
    print(f'{glsep}\n{"CLASSES PRESENTATION":^50}\n{glsep}')
    for obj in objects_list:
        print(f'instance of {type(obj)}:\n{obj}')
    print(glsep)

    print(f'\n\n{glsep}\n{"SUMMATION EXAMPLES":^50}\n{glsep}')
    for i, obj1 in enumerate(objects_list[:-1]):
        for obj2 in objects_list[i + 1:]:
            print(f'obj1: instance of {type(obj1)}\nobj2: instance of {type(obj2)}')
            print(f'\t{(obj1 + obj2)=}')
    print(glsep)
