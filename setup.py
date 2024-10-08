from setuptools import setup, find_packages

setup(
    name="my_redis_package",  # Название пакета
    version="0.1",
    packages=find_packages(),  # Автоматический поиск всех пакетов
    install_requires=[
        'redis==5.1.1',  # Зависимость Redis версии 5.1.1
    ],
    description="Модуль взаимодействия с Redis",
    author="Дмитрий Прокофьев",
    author_email="",
    url="https://github.com/DmitryProkofev/redis_package.git",  # Ссылка на репозиторий (если есть)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.7',
)