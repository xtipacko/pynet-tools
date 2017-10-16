# -*- coding: utf-8 -*-
from colorama import Fore
from colorama import init as initcolor

def main():
    initcolor()
    programmslist =  [('dhcp249 ', 'Для рассчета опции 249'),
                      ('gu',       'Для сбора информации о сессии и подключении абонента'),
                      ('n',        'Для генерации сообщения о выдачи IP абоненту'),
                      ('ml',       'Для поиска вендора по мак адресу'),
                      ('h',        'Справка'),
                      ('pipe',     'Для рассчета номера пайпа'  )]

    colorlist = [Fore.CYAN, '', Fore.GREEN]
    print('{} {:<14}{}{}'.format(Fore.YELLOW, 'Скрипт', 'Предназначение', Fore.RESET))
    for i, item in enumerate(programmslist):
        color = colorlist[i%2]
        print(f'{color}  {item[0]:<14}{item[1]}{Fore.RESET}')


if __name__ == '__main__':
    main()