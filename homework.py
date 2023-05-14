class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration: .3f} ч.; '
                f'Дистанция: {self.distance: .3f} км; '
                f'Ср. скорость: {self.speed: .3f} км/ч; '
                f'Потрачено ккал: {self.calories: .3f}.')


LEN_STEP_SWM = 1.6
LEN_STEP = 0.65   # Расстояние, за один шаг или гребок.
M_IN_KM = 1000
SECOND_IN_HOUR = 3600   # Константа для перевода значений из м в км.

'''Константы для рассчета каллорий.'''

'''Константы для бега.'''
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79

'''Константы для ходьбы.'''
CALORIES_MEAN_SPEED_MULTIPLIER_WALK = 0.035
CALORIES_MEAN_SPEED_SHIFT_WALK = 0.029

'''Константы для плавания.'''
CALORIES_MEAN_SPEED_MULTIPLIER_SWIMM = 1.1
CALORIES_MEAN_SPEED_SHIFT_SWIMM = 2


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / M_IN_KM

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
        return InfoMessage(str(training),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

    def __str__(self) -> str:
        ...


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        super().get_spent_calories()
        speed = Running.get_mean_speed(self)
        time_train = self.duration * 60
        return ((CALORIES_MEAN_SPEED_MULTIPLIER * speed
                + CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / M_IN_KM * time_train)

    def __str__(self) -> str:
        return 'Бег'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        super().get_spent_calories()

        speed = SportsWalking.get_mean_speed(self) * M_IN_KM / SECOND_IN_HOUR
        height_in_m = self.height / 100
        time_mins = self.duration * 60
        return ((CALORIES_MEAN_SPEED_MULTIPLIER_WALK * self.weight
                + (speed**2 / height_in_m)
                * CALORIES_MEAN_SPEED_SHIFT_WALK * self.weight)
                * time_mins)

    def __str__(self) -> str:
        return 'Спортивная ходьба'


class Swimming(Training):
    """Тренировка: плавание."""
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
        return self.action * LEN_STEP_SWM / M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        super().get_spent_calories()
        speed = self.get_mean_speed()
        return ((speed + CALORIES_MEAN_SPEED_MULTIPLIER_SWIMM)
                * CALORIES_MEAN_SPEED_SHIFT_SWIMM
                * self.weight * self.duration)

    def __str__(self) -> str:
        return 'Плаванье'


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
