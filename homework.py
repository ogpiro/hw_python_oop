from dataclasses import dataclass
from typing import ClassVar, Optional


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


@dataclass
class Training:
    """Базовый класс тренировки.
    action: Кол-во шагов и/или гребков.
    duration: Кол-во часов.
    weight: Вес в кг.
    LEN_STEP: Средняя длина шага в метрах.
    M_IN_KM: Кол-во метров в киллометрах.
    HOUR_IN_MINS: Кол-во минут в часе.
    CALORIES_MEAN_SPEED_MULTIPLIER: Коэфф. для рассчетов №1.
    CALORIES_MEAN_SPEED_SHIFT: Коэфф. для рассчетов №2.
    """
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    HOUR_IN_MINS: ClassVar[int] = 60
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[Optional[float]] = None
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[Optional[float]] = None

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


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        speed = Running.get_mean_speed(self)
        time_train = self.duration * self.HOUR_IN_MINS
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * time_train)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    height: Рост в см.
    KM_IN_M: Коэфф. для перевода км в м.
    SM_IN_M: Кол-во сантиметров в метрах.
    """
    height: int

    KM_IN_M: ClassVar[float] = 0.278
    SM_IN_M: ClassVar[int] = 100
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        speed = (SportsWalking.get_mean_speed(self)
                 * self.KM_IN_M)
        height_in_m = self.height / self.SM_IN_M
        time_mins = self.duration * self.HOUR_IN_MINS
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                + (speed**2 / height_in_m)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * time_mins)


@dataclass
class Swimming(Training):
    """Тренировка: плавание.
    length_pool: Длина бассейна в м.
    count_pool: Кол-во проплытых бассейнов.
    """
    length_pool: int
    count_pool: int

    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 1.1
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[int] = 2

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
