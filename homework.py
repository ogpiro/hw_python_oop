from dataclasses import dataclass
from typing import Optional


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    """
    action: Кол-во шагов и/или гребков.
    duration: Кол-во часов.
    weight: Вес в кг.
    LEN_STEP: Средняя длина шага в метрах.
    M_IN_KM: Кол-во метров в киллометрах.
    HOUR_IN_MINS: Кол-во минут в часе.
    CALORIES_MEAN_SPEED_MULTIPLIER: Коэфф. для рассчетов №1.
    CALORIES_MEAN_SPEED_SHIFT: Коэфф. для рассчетов №2.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MINS: int = 60
    CALORIES_MEAN_SPEED_MULTIPLIER: Optional[float] = None
    CALORIES_MEAN_SPEED_SHIFT: Optional[float] = None

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        time = self.duration
        return distance / time

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Необходимо для каждого вида тренировок '
                                  'определить метод рассчета каллорий.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        speed = Running.get_mean_speed(self)
        time_train = self.duration * self.HOUR_IN_MINS
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * time_train)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    """
    height: Рост в см.
    KM_IN_M: Коэфф. для перевода км в м.
    SM_IN_M: Кол-во сантиметров в метрах.
    """

    KM_IN_M: float = 0.278
    SM_IN_M: int = 100
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed = (SportsWalking.get_mean_speed(self)
                 * self.KM_IN_M)
        height_in_m = self.height / self.SM_IN_M
        time_mins = self.duration * self.HOUR_IN_MINS
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                + (speed**2 / height_in_m)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * time_mins)


class Swimming(Training):
    """Тренировка: плавание."""

    """
    length_pool: Длина бассейна в м.
    count_pool: Кол-во проплытых бассейнов.
    """

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SPEED_SHIFT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        return ((speed + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    wrkt_dict: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in wrkt_dict:
        return wrkt_dict[workout_type](*data)
    raise ValueError(f'Неизвестный класс тренировки, '
                     f'проверте значение {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    massage = info.get_message()
    print(massage)


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
