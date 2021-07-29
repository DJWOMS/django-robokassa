from typing import List

from setuptools import (setup, find_packages)

__version__: str = '0.3'


def read_file_lines(filename: str) -> List[str]:
    with open(filename, 'r') as fr:
        # читаем зависимости из файла
        readed_requriements: List[str] = fr.read().splitlines()
        # убираем лишние пробелы из строк
        dirty_requirements: List[str] = [require.strip() for require in readed_requriements]
        # отбрасываем комментарии из списка
        requirements: List[str] = list(filter(lambda require: not require.startswith('#'), dirty_requirements))
        return requirements


setup(
    name='django-robokassa',
    version='0.3',
    packages=find_packages(),
    url='https://github.com/DJWOMS/django-robokassa',
    license='',
    author='Omelchenko Michael',
    author_email='socanime@gmail.com',
    description='Скрипт для работы сайта на Django с Robokassa.',
    python_requires=">=3.4",
    install_requires=read_file_lines('requirements.txt'),
)
