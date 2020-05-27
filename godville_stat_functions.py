clan_positions_unworthy = ['фанат', 'рекрут', 'стажёр', 'адепт', 'мастер', 'магистр', 'советник', 'грандмастер']

"""           ОБЩИЕ ФУНКЦИИ           """


# функция сортировки словаря по заданному параметру
def sort_dict(dictionary, param):
    result = {}
    list_d = list(dictionary.items())
    list_d.sort(key=lambda t: t[1][param])
    list_d.reverse()
    for item in list_d:
        result[item[0]] = item[1]
    return result


# упаковка списков
def list_flatten(lst):
    while lst:
        sublist = lst.pop(0)
        if isinstance(sublist, list):
            lst = sublist + lst
        else:
            yield sublist


"""           ФУНКЦИИ ДЛЯ САМОЙ СТАТИСТИКИ           """


def update_level_list(new_data: dict, old_data: dict, god: str, list_worthy: dict, list_all: dict):
    """Обновление словарей по получению новых уровней"""
    if new_data[god]['level'] - old_data[god]['level'] > 0:  # если есть изменение в уровнях между датами
        if new_data[god]['clan_position'] not in clan_positions_unworthy:  # если бог со званием кардинал+
            # записываем его в список для статистики по уровням
            list_worthy[god] = [new_data[god]['level'], new_data[god]['level'] - old_data[god]['level']]
        # в любом случае записываем бога в список изменения уровней
        list_all[god] = [new_data[god]['level'], new_data[god]['level'] - old_data[god]['level']]


def update_trade_level_list(new_data: dict, old_data: dict, god: str, list_all: dict):
    """Обновление словарей по получению новых торговых уровней"""
    try:  # проверяем, есть ли у бога вообще лавка через запрос в json
        if new_data[god]['t_level'] - old_data[god]['t_level'] > 0:  # если есть и уровень лавки изменился
            # обновляем список богов с изменившимся торговым уровнем
            list_all[god] = [new_data[god]['t_level'], new_data[god]['t_level'] - old_data[god]['t_level']]
    except KeyError:  # если для бога такого ключа нет, возвращаем изначальный список
        pass


def update_clan_position_list(new_data: dict, old_data: dict, god: str, list_all: dict):
    """Обновление словарей по получению новых званий"""
    if new_data[god]['clan_position'] != old_data[god]['clan_position']:  # если старая и новая позиции не равны
        list_all[god] = new_data[god]['clan_position']  # вносим бога в список


def update_brickers_and_temples(new_data: dict, old_data: dict, god: str, brickers: dict, temples: list):
    """Обновление словарей по сбору кирпичей и новых храмах"""
    if new_data[god]['bricks_cnt'] - old_data[god]['bricks_cnt'] > 0:  # если количество кирпичей изменилось
        if new_data[god]['bricks_cnt'] == 1000:  # и новое число равно 10000
            temples.append(god)  # вносим бога в список построивших храм
        # вносим бога в список изменений по количеству кирпичей
        brickers[god] = [new_data[god]['bricks_cnt'], new_data[god]['bricks_cnt'] - old_data[god]['bricks_cnt']]


def update_wooders_and_arks(new_data: dict, old_data: dict, god: str, wooders: dict, arks: dict):
    """Обновление словарей по сбору брёвен и новых палубах"""
    try:  # проверяем, начал ли бог строить ковчег через запрос в json
        if new_data[god]['wood_cnt'] - old_data[god]['wood_cnt'] > 0:  # если да и количество изменилось
            if old_data[god]['wood_cnt'] // 1000 != new_data[god]['wood_cnt'] // 1000:  # и тысячные разряды разные
                # добавляем бога в словарь с соответствующим значением палуб
                try:  # если инфа по этому количеству палуб уже была, добавляем бога в список
                    arks[new_data[god]['wood_cnt'] // 1000].append(god)
                except KeyError:  # если нет, создаём новую запись
                    arks.setdefault(new_data[god]['wood_cnt'] // 1000, [god])
            # вносим бога в список изменений по количеству брёвен
            wooders[god] = [new_data[god]['wood_cnt'], new_data[god]['wood_cnt'] - old_data[god]['wood_cnt']]
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass


def update_savers_and_shops(new_data: dict, old_data: dict, god: str, savers: dict, shops: list):
    """Обновление словарей по сбору пенсии и новых лавках"""
    try:  # проверяем, начал ли бог собирать пенсию через запрос в json
        if new_data[god]['savings'] != old_data[god]['savings']:  # если да и количество изменилось
            if new_data[god]['savings'] == '30000 тысяч':  # и новое число равно "30000 тысяч"
                shops.append(god)  # вносим бога в список построивших лавку
            # вносим бога в список изменений по сбору пенсии
            savers[god] = [new_data[god]['savings'],
                           int(new_data[god]['savings'].split(' ')[0]) -
                           int(old_data[god]['savings'].split(' ')[0])]
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass


TODO: 'Переписать сбор статы по тварям.' \
      '1. сделать один общий try/except' \
      '2. отловить случай, если в data_old сбора не было,' \
      '   а в data_new он появился'


def update_fm_and_labs(new_data: dict, old_data: dict, god: str, fm: dict, labs: list):
    """Обновление словарей по сбору тварей и новых лабораториях"""
    female_change, male_change = {}, {}
    # количество собранных тварей (самцов)
    try:  # проверяем, начал ли бог собирать тварей (самцов) через запрос в json
        if new_data[god]['ark_m'] - old_data[god]['ark_m'] > 0:  # если да и количество изменилось
            # вносим бога в список изменений по количеству тварей (самцов)
            male_change[god] = [new_data[god]['ark_m'], new_data[god]['ark_m'] - old_data[god]['ark_m']]
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass
    # количество собранных тварей (самок)
    try:  # проверяем, начал ли бог собирать тварей (самок) через запрос в json
        if new_data[god]['ark_f'] - old_data[god]['ark_f'] > 0:  # если да и количество изменилось
            # вносим бога в список изменений по количеству тварей (самок)
            female_change[god] = [new_data[god]['ark_f'], new_data[god]['ark_f'] - old_data[god]['ark_f']]
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass
    # общая статистика по количеству собранных тварей (самцов и самок)
    try:  # проверяем, начал ли бог собирать тварей (самцов и самок) через запрос в json
        # если да, формируем словарь со всеми изменениями. пример: {'Manuchao': ['422м/411ж', 14, 12, 26]}
        fm[god] = [str(new_data[god]['ark_m']) + 'м/' + str(new_data[god]['ark_f']) + 'ж',  # общее количество
                   male_change[god][1],  # изменение по самцам
                   female_change[god][1],  # изменение по самкам
                   male_change[god][1] + female_change[god][1]]  # изменение по самцам и самкам вместе
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass
    # новые лаборатории
    try:  # проверяем, начал ли бог собирать тварей (самцов и самок) через запрос в json
        # если да и оба новых счётчика равны тысяче, а также один из старых счётчиков не равен тысяче
        if (new_data[god]['ark_m'] == 1000 and new_data[god]['ark_f'] == 1000) and \
                (old_data[god]['ark_m'] < 1000 or old_data[god]['ark_f'] < 1000):
            labs.append(god)  # вносим бога в список построивших лабораторию
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass


def update_bosses(new_data: dict, old_data: dict, god: str, bosses: dict):
    """Обновление словарей о новых боссах"""
    try:  # проверяем, есть ли изменения в имени или мощи босса через запрос в json
        if old_data[god]['boss_name'] != new_data[god]['boss_name'] or \
                old_data[god]['boss_power'] != new_data[god]['boss_power']:
            # если да, вносим бога в список ожививших нового босса
            bosses[god] = [new_data[god]['boss_name'], new_data[god]['boss_power']]
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass


def update_writers(new_data: dict, old_data: dict, god: str, writers: dict):
    """Обновление словарей о книгописцах"""
    try:  # проверяем, начал ли бог писать книгу через запрос в json
        if new_data[god]['words'] - old_data[god]['words'] > 0:  # если да и количество изменилось
            # вносим бога в список изменений по количеству слов
            writers[god] = [new_data[god]['words'], new_data[god]['words'] - old_data[god]['words']]
    except KeyError:  # если для бога такого ключа нет, идём дальше
        pass


def update_fighters(new_data: dict, old_data: dict, god: str, fighters: dict):
    """Обновление словарей про аренные бои"""
    change_won = new_data[god]['arena_won'] - old_data[god]['arena_won']  # изменение побед текущего бога
    change_los = new_data[god]['arena_lost'] - old_data[god]['arena_lost']  # изменение поражений текущего бога
    if change_won > 0 or change_los > 0:  # если количество побед или поражений изменилось
        # вносим бога в список изменений по аренной статистике
        fighters[god] = [str(new_data[god]['arena_won']) + ' побед/' +
                         str(new_data[god]['arena_lost']) + ' поражений',
                         change_won,  # изменение по победам
                         change_los,  # изменение по поражениям
                         change_won - change_los]  # разница побед и поражений


def update_petters(new_data: dict, old_data: dict, god: str, petters_worthy: dict, petters_all: dict, pet_change: dict):
    """Обновление словарей про изменения в питомцах"""
    try:  # проверяем, был ли у бога питомец
        check = old_data[god]['pet']['pet_level']
        try:  # если был, проверяем, есть ли у бога питомец сейчас
            check = new_data[god]['pet']['pet_level']
            # если питомец был раньше, есть сейчас, в обоих случаях имел уровень и изменил уровень на больший
            if new_data[god]['pet']['pet_level'] - old_data[god]['pet']['pet_level'] > 0:
                if new_data[god]['clan_position'] not in clan_positions_unworthy:  # если бог со званием кардинал+
                    # записываем его в список для статистики по уровням питомцев
                    petters_worthy[god] = [new_data[god]['pet']['pet_class'],
                                           new_data[god]['pet']['pet_level'],
                                           new_data[god]['pet']['pet_level'] -
                                           old_data[god]['pet']['pet_level']]
                # в любом случае записываем бога в список изменения уровней питомцев
                petters_all[god] = [new_data[god]['pet']['pet_class'],
                                    new_data[god]['pet']['pet_level'],
                                    new_data[god]['pet']['pet_level'] - old_data[god]['pet']['pet_level']]
            elif new_data[god]['pet']['pet_level'] - old_data[god]['pet']['pet_level'] < 0:
                pet_change['Герой завёл нового питомца'].append([god, new_data[god]['pet']['pet_class']])
        except TypeError:
            # проверяем, был ли у него уровень раньше
            if isinstance(old_data[god]['pet']['pet_level'], int):
                # если да, а сейчас нет, делаем пометку
                pet_change['Питомец потерял уровень'].append(god)
            # если нет, проверяем, есть ли у него уровень сейчас
            elif isinstance(new_data[god]['pet']['pet_level'], int):
                # если да, делаем пометку
                pet_change['Герой завёл нового питомца'].append([god, new_data[god]['pet']['pet_class']])
        except KeyError:  # если у бога питомец был, а сейчас его нет
            #  вносим бога в список с пометкой о потере питомца
            pet_change['Герой остался без питомца'].append(god)
    except KeyError:  # если у бога питомца не было
        try:  # проверяем, есть ли он сейчас
            check = new_data[god]['pet']['pet_level']
            # если появился, вносим бога в список с пометкой о новом питомце
            pet_change['Герой завёл нового питомца'].append([god, new_data[god]['pet']['pet_class']])
        except KeyError:  # если не было и не появился, идём дальше
            pass
