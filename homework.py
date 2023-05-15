from dataclasses import dataclass


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
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_IN_MINS = 60
    CALORIES_MEAN_SPEED_MULTIPLIER = None
    CALORIES_MEAN_SPEED_SHIFT = None

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
        ...

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

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        speed = Running.get_mean_speed(self)
        time_train = self.duration * self.HOUR_IN_MINS
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * time_train)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int

    KM_IN_M = 0.278
    SM_IN_M = 100
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029

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
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2

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
    classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in classes:
        return classes[workout_type](*data)
    return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    massage = info.get_message()
    print(massage)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
