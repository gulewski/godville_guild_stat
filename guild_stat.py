import json

# прописываем имена файлов для старта статистики и финиша
path_old = 'old.json'
path_new = 'new.json'

# открываем и выгружаем файлы со статистикой
json_open_old = open(path_old, 'r', encoding='utf-8')
json_open_new = open(path_new, 'r', encoding='utf-8')
json_old = json_open_old.read()
json_new = json_open_new.read()
json_open_old.close()
json_open_new.close()

# формируем датасеты с данными
try:
    data_old = json.loads(json_old)['data']
except KeyError:
    data_old = json.loads(json_old)
try:
    data_new = json.loads(json_new)['data']
except KeyError:
    data_new = json.loads(json_new)


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


# формирование списков богов
god_list_old = list(data_old.keys())  # список богов из начала статистики
god_list_new = list(data_new.keys())  # список богов из конца статистики
god_list_actual = sorted(list(set(god_list_old) & set(god_list_new)))  # список богов, которые есть в обоих списках
god_leaved = sorted(list(set(god_list_old).difference(set(god_list_new))))  # ушедшие боги
god_entered = sorted(list(set(god_list_new).difference(set(god_list_old))))  # пришедшие боги


# просто для интереса, сколько раз срабатывал пустой except
exceptions = 0

# переменные для всех позиций статистики
new_level_list_all, new_level_list_worthy = {}, {}  # списки богов с новыми уровнями (все и кардинал+)
new_t_level_list = {}  # список богов с новыми торговыми уровнями
clan_position_change = {}  # изменение ранга в гильдии
bricks_change = {}  # изменение по собранным кирпичам
wood_change, savings_change = {}, {}  # изменение по собранным брёвнам и отложенной пенсии
words_change = {}  # изменение по собранным словам
female_change, male_change, fm_change, = {}, {}, {}  # изменения по тварям (ж, м, всё вместе)
fight_change = {}  # изменения по боям (разница побед и поражений)
new_temple, new_shop, new_lab = [], [], []  # списки богов с новыми храмами/ковчегами/лавками/лабами
new_arks, new_bosses = {}, {}  # информация по богам с новым боссом
pet_change_level_all, pet_change_level_worthy = {}, {}  # списки богов с новыми уровнями у петов (все и кардинал+)
# список изменений статусов питомцев - потеря питомца, потеря уровня, новый питомец
pet_change_status = {'Герой остался без питомца': [],
                     'Питомец героя остался без уровня': [],
                     'Герой завёл нового питомца': []}

# список званий ниже кардинала для фильтрации
clan_positions_unworthy = ['фанат', 'рекрут', 'стажёр', 'адепт', 'мастер', 'магистр', 'советник', 'грандмастер']

# формирование списков по всем позициям статистики
for god in god_list_actual:

    # уровни героя
    if data_new[god]['level'] - data_old[god]['level'] > 0:  # если есть изменение в уровнях между датами
        if data_new[god]['clan_position'] not in clan_positions_unworthy:  # если бог со званием кардинал+
            # записываем его в список для статистики по уровням
            new_level_list_worthy[god] = [data_new[god]['level'], data_new[god]['level'] - data_old[god]['level']]
        # в любом случае записываем бога в список изменения уровней
        new_level_list_all[god] = [data_new[god]['level'], data_new[god]['level'] - data_old[god]['level']]

    # уровни торговца
    try:  # проверяем, есть ли у бога вообще лавка через запрос в json
        if data_new[god]['t_level'] - data_old[god]['t_level'] > 0:  # если есть и уровень лавки изменился
            # записываем его в список богов с изменившимся торговым уровнем
            new_t_level_list[god] = [data_new[god]['t_level'], data_new[god]['t_level'] - data_old[god]['t_level']]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # позиция в гильдии
    if data_new[god]['clan_position'] != data_old[god]['clan_position']:  # если старая и новая позиции не равны
        clan_position_change[god] = data_new[god]['clan_position']  # вносим бога в список

    # количество собранных кирпичей и новые храмы
    if data_new[god]['bricks_cnt'] - data_old[god]['bricks_cnt'] > 0:  # если количество кирпичей изменилось
        if data_new[god]['bricks_cnt'] == 1000:  # и новое число равно 10000
            new_temple.append(god)  # вносим бога в список построивших храм
        # вносим бога в список изменений по количеству кирпичей
        bricks_change[god] = [data_new[god]['bricks_cnt'], data_new[god]['bricks_cnt'] - data_old[god]['bricks_cnt']]

    # количество собранных брёвен и новые ковчеги
    try:  # проверяем, начал ли бог строить ковчег через запрос в json
        if data_new[god]['wood_cnt'] - data_old[god]['wood_cnt'] > 0:  # если да и количество изменилось
            if data_old[god]['wood_cnt'] // 1000 != data_new[god]['wood_cnt'] // 1000:  # и тысячные разряды разные
                # если инфа по этой палубе уже есть в словаре
                if data_new[god]['wood_cnt'] // 1000 in new_arks:
                    # добавляем нового бога в эту запись
                    new_arks[data_new[god]['wood_cnt'] // 1000].append(god)
                # если инфы по этой палубе нет в словаре
                else:
                    # создаём и записываем туда бога
                    new_arks[data_new[god]['wood_cnt'] // 1000] = [god]
            # вносим бога в список изменений по количеству брёвен
            wood_change[god] = [data_new[god]['wood_cnt'], data_new[god]['wood_cnt'] - data_old[god]['wood_cnt']]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # количество отложенной пенсии и новые лавки
    try:  # проверяем, начал ли бог собирать пенсию через запрос в json
        if data_new[god]['savings'] != data_old[god]['savings']:  # если да и количество изменилось
            if data_new[god]['savings'] == '30000 тысяч':  # и новое число равно "30000 тысяч"
                new_shop.append(god)  # вносим бога в список построивших лавку
            # вносим бога в список изменений по сбору пенсии
            savings_change[god] = [data_new[god]['savings'],
                                   int(data_new[god]['savings'].split(' ')[0]) -
                                   int(data_old[god]['savings'].split(' ')[0])]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # количество собранных тварей (самцов)
    try:  # проверяем, начал ли бог собирать тварей (самцов) через запрос в json
        if data_new[god]['ark_m'] - data_old[god]['ark_m'] > 0:  # если да и количество изменилось
            # вносим бога в список изменений по количеству тварей (самцов)
            male_change[god] = [data_new[god]['ark_m'], data_new[god]['ark_m'] - data_old[god]['ark_m']]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass
    # количество собранных тварей (самок)
    try:  # проверяем, начал ли бог собирать тварей (самок) через запрос в json
        if data_new[god]['ark_f'] - data_old[god]['ark_f'] > 0:  # если да и количество изменилось
            # вносим бога в список изменений по количеству тварей (самок)
            female_change[god] = [data_new[god]['ark_f'], data_new[god]['ark_f'] - data_old[god]['ark_f']]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass
    # общая статистика по количеству собранных тварей (самцов и самок)
    try:  # проверяем, начал ли бог собирать тварей (самцов и самок) через запрос в json
        # если да, формируем словарь со всеми изменениями
        fm_change[god] = [str(data_new[god]['ark_m']) + 'м/' + str(data_new[god]['ark_f']) + 'ж',  # общее количество
                          male_change[god][1],  # изменение по самцам
                          female_change[god][1],  # изменение по самкам
                          male_change[god][1] + female_change[god][1]]  # изменение по самцам и самкам вместе
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # новые лаборатории
    try:  # проверяем, начал ли бог собирать тварей (самцов и самок) через запрос в json
        # если да и оба новых счётчика равны тысяче, а также один из старых счётчиков не равен тысяче
        if (data_new[god]['ark_m'] == 1000 and data_new[god]['ark_f'] == 1000) and \
                (data_old[god]['ark_m'] < 1000 or data_old[god]['ark_f'] < 1000):
            new_lab.append(god)  # вносим бога в список построивших лабораторию
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # новые боссы
    try:  # проверяем, есть ли изменения в имени или мощи босса через запрос в json
        if data_old[god]['boss_name'] != data_new[god]['boss_name'] or \
                data_old[god]['boss_power'] != data_new[god]['boss_power']:
            # если да, вносим бога в список ожививших нового босса
            new_bosses[god] = [data_new[god]['boss_name'], data_new[god]['boss_power']]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # количество вписанных слов в книгу
    try:  # проверяем, начал ли бог писать книгу через запрос в json
        if data_new[god]['words'] - data_old[god]['words'] > 0:  # если да и количество изменилось
            # вносим бога в список изменений по количеству слов
            words_change[god] = [data_new[god]['words'], data_new[god]['words'] - data_old[god]['words']]
    except KeyError:  # если для бога такого ключа нет, увеличиваем счётчик
        exceptions += 1
        pass

    # изменение в счётчике дуэлей
    change_won = data_new[god]['arena_won'] - data_old[god]['arena_won']  # изменение побед текущего бога
    change_los = data_new[god]['arena_lost'] - data_old[god]['arena_lost']  # изменение поражений текущего бога
    if change_won > 0 or change_los > 0:  # если количество побед или поражений изменилось
        # вносим бога в список изменений по аренной статистике
        fight_change[god] = [str(data_new[god]['arena_won']) + ' побед/' +
                             str(data_new[god]['arena_lost']) + ' поражений',
                             change_won,  # изменение по победам
                             change_los,  # изменение по поражениям
                             change_won - change_los  # разница побед и поражений
                             ]

    # питомцы
    try:  # проверяем, был ли у бога питомец
        check = data_old[god]['pet']['pet_level']
        try:  # если был, проверяем, есть ли у бога питомец сейчас
            check = data_new[god]['pet']['pet_level']
            # если питомец был раньше, есть сейчас, в обоих случаях имел уровень и изменил уровень на больший
            if data_new[god]['pet']['pet_level'] - data_old[god]['pet']['pet_level'] > 0:
                if data_new[god]['clan_position'] not in clan_positions_unworthy:  # если бог со званием кардинал+
                    # записываем его в список для статистики по уровням питомцев
                    pet_change_level_worthy[god] = [data_new[god]['pet']['pet_class'],
                                                    data_new[god]['pet']['pet_level'],
                                                    data_new[god]['pet']['pet_level'] -
                                                    data_old[god]['pet']['pet_level']
                                                    ]
                # в любом случае записываем бога в список изменения уровней питомцев
                pet_change_level_all[god] = [data_new[god]['pet']['pet_class'],
                                             data_new[god]['pet']['pet_level'],
                                             data_new[god]['pet']['pet_level'] - data_old[god]['pet']['pet_level']]
            elif data_new[god]['pet']['pet_level'] - data_old[god]['pet']['pet_level'] < 0:
                pet_change_status['Герой завёл нового питомца'].append([god, data_new[god]['pet']['pet_class']])
        except TypeError:
            # проверяем, был ли у него уровень раньше
            if isinstance(data_old[god]['pet']['pet_level'], int):
                # если да, а сейчас нет, делаем пометку
                pet_change_status['Питомец потерял уровень'].append(god)
            # если нет, проверяем, есть ли у него уровень сейчас
            elif isinstance(data_new[god]['pet']['pet_level'], int):
                # если да, делаем пометку
                pet_change_status['Герой завёл нового питомца'].append([god, data_new[god]['pet']['pet_class']])
        except KeyError:  # если у бога питомец был, а сейчас его нет
            #  вносим бога в список с пометкой о потере питомца
            pet_change_status['Герой остался без питомца'].append(god)
    except KeyError:  # если у бога питомца не было
        try:  # проверяем, есть ли он сейчас
            check = data_new[god]['pet']['pet_level']
            # если появился, вносим бога в список с пометкой о новом питомце
            pet_change_status['Герой завёл нового питомца'].append([god, data_new[god]['pet']['pet_class']])
        except KeyError:  # если не было и не появился, увеличиваем счётчик
            exceptions += 1
            pass

# сортируем все списки
god_leaved = sorted(god_leaved)
god_entered = sorted(god_entered)
new_level_list_all = sort_dict(new_level_list_all, 1)  # по количеству полученных уровней
new_level_list_worthy = sort_dict(new_level_list_worthy, 0)  # по уровню
new_t_level_list = sort_dict(new_t_level_list, 0)  # по уровню
bricks_change = sort_dict(bricks_change, 1)  # по количеству собранных кирпичей
wood_change = sort_dict(wood_change, 1)  # по количеству собранных брёвен
new_arks = sorted(new_arks.items())  # по новым палубам
savings_change = sort_dict(savings_change, 1)  # по количеству отложенной пенсии
fm_change = sort_dict(fm_change, 3)  # по сумме собранных самцов и самок
words_change = sort_dict(words_change, 1)  # по количеству вписанных слов
fight_change = sort_dict(fight_change, 3)  # по разнице побед-поражений
pet_change_level_all = sort_dict(pet_change_level_all, 1)  # по уровню питомца
pet_change_level_worthy = sort_dict(pet_change_level_worthy, 1)  # по уровню питомца

# сырая инфа по показу всего собранного в консоль
show_stat = 1
if show_stat == 1:
    print('Ушедшие:\n', god_leaved)
    print('\nПришедшие:\n', god_entered)
    print('\nНовые уровни (все):\n', new_level_list_all)
    print('\nНовые уровни (кардинал и выше):\n', new_level_list_worthy)
    print('\nНовые торговые уровни:\n', new_t_level_list)
    print('\nНовые звания:\n', clan_position_change)
    print('\nКирпичей собрано:\n', bricks_change)
    print('\nНовые храмы:\n', new_temple)
    print('\nБрёвен собрано:\n', wood_change)
    print('\nНовые ковчеги:\n', new_arks)
    print('\nПенсии собрано:\n', savings_change)
    print('\nНовые лавочники:\n', new_shop)
    print('\nОбщая статистика по тварям:\n', fm_change)
    print('\nНовая лаборатория:\n', new_lab)
    print('\nНовый босс:\n', new_bosses)
    print('\nВписано новых слов в книгу:\n', words_change)
    print('\nОбщая статистика по боям:\n', fight_change)
    print('\nИзменения по уровням питомцев (все):\n', pet_change_level_all)
    print('\nИзменения по уровням питомцев (кардинал и выше):\n', pet_change_level_worthy)
    print('\nИзменения по статусам питомцев:\n', pet_change_status)

# запись в файл всей статистики в сыром виде (файл results.txt)
write_stat_file = 1
if write_stat_file == 1:
    f = open('results.txt', 'w', encoding='utf-8')
    f.write('Ушедшие:\n' + str(god_leaved) + '\n\n')
    f.write('Пришедшие:\n' + str(god_entered) + '\n\n')
    f.write('Новые уровни (все):\n' + str(new_level_list_all) + '\n\n')
    f.write('Новые уровни (кардинал и выше):\n' + str(new_level_list_worthy) + '\n\n')
    f.write('Новые торговые уровни:\n' + str(new_t_level_list) + '\n\n')
    f.write('Новые звания:\n' + str(clan_position_change) + '\n\n')
    f.write('Кирпичей собрано:\n' + str(bricks_change) + '\n\n')
    f.write('Новые храмы:\n' + str(new_temple) + '\n\n')
    f.write('Брёвен собрано:\n' + str(wood_change) + '\n\n')
    f.write('Новые ковчеги:\n' + str(new_arks) + '\n\n')
    f.write('Пенсии собрано:\n' + str(savings_change) + '\n\n')
    f.write('Новые лавочники:\n' + str(new_shop) + '\n\n')
    f.write('Общая статистика по тварям:\n' + str(fm_change) + '\n\n')
    f.write('Новая лаборатория:\n' + str(new_lab) + '\n\n')
    f.write('Новый босс:\n' + str(new_bosses) + '\n\n')
    f.write('Вписано новых слов в книгу:\n' + str(words_change) + '\n\n')
    f.write('Общая статистика по боям:\n' + str(fight_change) + '\n\n')
    f.write('Изменения по уровням питомцев (все):\n' + str(pet_change_level_all) + '\n\n')
    f.write('Изменения по уровням питомцев (кардинал и выше):\n' + str(pet_change_level_worthy) + '\n\n')
    f.write('Изменения по статусам питомцев:\n' + str(pet_change_status))
    f.close()

# формирование адекватных строк для статистики на форум

clan_position_change_for_text = ''  # строка для гильдзваний
# словарь званий в порядке возрастания старшинства
clan_positions = {'фанат': [], 'рекрут': [], 'стажёр': [], 'адепт': [], 'мастер': [], 'магистр': [], 'советник': [],
                  'грандмастер': [], 'кардинал': [], 'иерарх': [], 'патриарх': [], 'регент': [], 'пророк': [],
                  'спецзвание': []}
# для каждой записи в списке богов с изменением ранга
for key, value in clan_position_change.items():
    clan_positions[value].append(key)  # добавляем бога в словарь по званиям
# для каждой записи в словаре званий
for key, value in clan_positions.items():
    if len(value) > 0:  # если есть хотя бы один бог в звании
        # добавляем текст строки (имя бога, звание)
        clan_position_change_for_text += f'* {key} {len(value)}: {", ".join(value)}\n'

pet_change_lvl_for_text = ''  # строка по уровням питомцев
# для каждого, кто старше кардинала
for key in pet_change_level_worthy.keys():
    # добавляем текст строки (имя бога, имя питомца, уровень питомца, изменение в уровне питомца)
    pet_change_lvl_for_text += f'{key}: ' \
                               f'{pet_change_level_worthy[key][0]}: ' \
                               f'{pet_change_level_worthy[key][1]} ' \
                               f'({pet_change_level_worthy[key][2]}); '

pet_change_status_for_text = ''  # строка для статусов питомцев
# добавляем инфу по героям, оставшимся без питомца (если такие есть)
if len(pet_change_status['Герой остался без питомца']) > 0:
    pet_change_status_for_text += ' * Герой остался без питомца: '
    for value in pet_change_status['Герой остался без питомца']:
        pet_change_status_for_text += f'{value}, '
    pet_change_status_for_text = pet_change_status_for_text[:-2]
# добавляем инфу по героям, чей питомец остался без уровня (если такие есть)
if len(pet_change_status['Питомец героя остался без уровня']) > 0:
    pet_change_status_for_text += '\n * Питомец потерял уровень: '
    for value in pet_change_status['Питомец героя остался без уровня']:
        pet_change_status_for_text += f'{value}, '
    pet_change_status_for_text = pet_change_status_for_text[:-2]
# добавляем инфу по героям, которые завели нового питомца (если такие есть)
if len(pet_change_status['Герой завёл нового питомца']) > 0:
    pet_change_status_for_text += '\n * Герой завёл нового питомца: '
    for value in pet_change_status['Герой завёл нового питомца']:
        pet_change_status_for_text += f'{value[0]} ({value[1]}), '
    pet_change_status_for_text = pet_change_status_for_text[:-2]
pet_change_status_for_text += '\n'

bricks_change_for_text = ''  # строка для кирпичесборщиков
bricks_list, i, counter = [], 0, 1
bricks_list_for_places = {'1 место:': [], '2 место:': [], '3 место:': []}
# для всех в списке изменений по кол-ву собранных кирпичей
for key in bricks_change.keys():
    # разбиваем строку на слова и вносим в список списков (имя бога, собранных кирпичей, всего кирпичей)
    bricks_list.append(f'{key}: '
                       f'{bricks_change[key][1]} '
                       f'({bricks_change[key][0]} всего);'.split(' '))
# ставим первого в списке на первое место
bricks_list_for_places['1 место:'].append(bricks_list[0])
# пока список не закончится
while i < len(bricks_list) - 1:
    # если количество собранных кирпичей следующего бога равно предыдущему
    if bricks_list[i][-3] == bricks_list[i + 1][-3]:
        # добавляем его на то же самое место
        bricks_list_for_places[f'{counter} место:'].append(bricks_list[i + 1])
    # если нет, увеличиваем счётчик мест
    else:
        counter += 1
        # если внесли всех в топ-3
        if counter == 4:
            # выходим из цикла и завершаем формирование строки
            break
        # если топ-3 ещё не заполнен
        else:
            # вносим бога на следующее место
            bricks_list_for_places[f'{counter} место:'].append(bricks_list[i + 1])
    i += 1
# для каждого места
for key, value in bricks_list_for_places.items():
    # распаковываем список, чтобы получить один список вместо нескольких
    bricks_list_for_places[key] = list(list_flatten(value))
    # собираем строку
    bricks_change_for_text += f'{key} {" ".join(bricks_list_for_places[key])[:-1]}\n'

wood_change_for_text = ''  # строка для бревносборщиков
wood_list, i, counter = [], 0, 1
wood_list_for_places = {'1 место:': [], '2 место:': [], '3 место:': []}
# для всех в списке изменений по кол-ву собранных брёвен
for key in wood_change.keys():
    # разбиваем строку на слова и вносим в список списков (имя бога, собранных брёвен, всего брёвен)
    wood_list.append(f'{key}: '
                     f'{wood_change[key][1]} '
                     f'({wood_change[key][0]} всего);'.split(' '))
# ставим первого в списке на первое место
wood_list_for_places['1 место:'].append(wood_list[0])
# пока список не закончится
while i < len(wood_list) - 1:
    # если количество собранных брёвен следующего бога равно предыдущему
    if wood_list[i][-3] == wood_list[i + 1][-3]:
        # добавляем его на то же самое место
        wood_list_for_places[f'{counter} место:'].append(wood_list[i + 1])
    # если нет, увеличиваем счётчик мест
    else:
        counter += 1
        # если внесли всех в топ-3
        if counter == 4:
            # выходим из цикла и завершаем формирование строки
            break
        # если топ-3 ещё не заполнен
        else:
            # вносим бога на следующее место
            wood_list_for_places[f'{counter} место:'].append(wood_list[i + 1])
    i += 1
# для каждого места
for key, value in wood_list_for_places.items():
    # распаковываем список, чтобы получить один список вместо нескольких
    wood_list_for_places[key] = list(list_flatten(value))
    # собираем строку
    wood_change_for_text += f'{key} {" ".join(wood_list_for_places[key])[:-1]}\n'

new_arks_for_text = ''  # строка для новых ковчегов
# для всех в списке собравших новые палубы
for i in new_arks:
    # собираем строку (номер новой палубы, имена богов)
    new_arks_for_text += f'{i[0]}: {", ".join(i[1])} \n'

fm_change_for_text = ''  # строка для тваресборщиков
fm_list, i, counter = [], 0, 1
fm_list_for_places = {'1 место:': [], '2 место:': [], '3 место:': []}
# для всех в списке изменений по кол-ву собранных тварей
for key in fm_change.keys():
    # разбиваем строку на слова и вносим в список списков (имя бога, всего тварей, +самцов, + самок, сумма)
    fm_list.append(f'{key}: {fm_change[key][3]} ({fm_change[key][1]}♂ '
                   f'({fm_change[key][0][:fm_change[key][0].find("м")]} всего) / '
                   f'{fm_change[key][2]}♀ '
                   f'({fm_change[key][0][fm_change[key][0].find("/") + 1:-1]} всего));'.split(' '))
# ставим первого в списке на первое место
fm_list_for_places['1 место:'].append(fm_list[0])
# пока список не закончится
while i < len(fm_list) - 1:
    # если количество собранных тварей следующего бога равно предыдущему
    if fm_list[i][-8] == fm_list[i + 1][-8]:
        # добавляем его на то же самое место
        fm_list_for_places[f'{counter} место:'].append(fm_list[i + 1])
    # если нет, увеличиваем счётчик мест
    else:
        counter += 1
        # если внесли всех в топ-3
        if counter == 4:
            # выходим из цикла и завершаем формирование строки
            break
        # если топ-3 ещё не заполнен
        else:
            # вносим бога на следующее место
            fm_list_for_places[f'{counter} место:'].append(fm_list[i + 1])
    i += 1
# для каждого места
for key, value in fm_list_for_places.items():
    # распаковываем список, чтобы получить один список вместо нескольких
    fm_list_for_places[key] = list(list_flatten(value))
    # собираем строку
    fm_change_for_text += f'{key} {" ".join(fm_list_for_places[key])[:-1]}\n'

savings_change_for_text = ''  # строка для пенсиесборщиков
savings_list, i, counter = [], 0, 1
savings_list_for_places = {'1 место:': [], '2 место:': [], '3 место:': []}
# для всех в списке изменений по кол-ву отложенной пенсии
for key in savings_change.keys():
    # разбиваем строку на слова и вносим в список списков (имя бога, всего пенсии, собрано пенсии)
    savings_list.append(f'{key}: '
                        f'{savings_change[key][1]} '
                        f'({savings_change[key][0][:savings_change[key][0].find(" ")]} всего);'.split(' '))
# ставим первого в списке на первое место
savings_list_for_places['1 место:'].append(savings_list[0])
# пока список не закончится
while i < len(savings_list) - 1:
    # если у следующего бога отложено столько же пенсии, сколько и у предыдущего
    if savings_list[i][-3] == savings_list[i + 1][-3]:
        # добавляем его на то же самое место
        savings_list_for_places[f'{counter} место:'].append(savings_list[i + 1])
    # если нет, увеличиваем счётчик мест
    else:
        counter += 1
        # если внесли всех в топ-3
        if counter == 4:
            # выходим из цикла и завершаем формирование строки
            break
        # если топ-3 ещё не заполнен
        else:
            # вносим бога на следующее место
            savings_list_for_places[f'{counter} место:'].append(savings_list[i + 1])
    i += 1
# для каждого места
for key, value in savings_list_for_places.items():
    # распаковываем список, чтобы получить один список вместо нескольких
    savings_list_for_places[key] = list(list_flatten(value))
    # собираем строку
    savings_change_for_text += f'{key} {" ".join(savings_list_for_places[key])[:-1]}\n'

words_change_for_text = ''  # строка для словосборщиков
words_list, i, counter = [], 0, 1
words_list_for_places = {'1 место:': [], '2 место:': [], '3 место:': []}
# для всех в списке изменений по кол-ву собранных слов
for key in words_change.keys():
    # разбиваем строку на слова и вносим в список списков (имя бога, всего слов, собрано слов)
    words_list.append(f'{key}: '
                      f'{words_change[key][1]} '
                      f'({words_change[key][0]} всего);'.split(' '))
# ставим первого в списке на первое место
words_list_for_places['1 место:'].append(words_list[0])
# пока список не закончится
while i < len(words_list) - 1:
    # если у следующего бога собрано столько же слов, сколько и у предыдущего
    if words_list[i][-3] == words_list[i + 1][-3]:
        # добавляем его на то же самое место
        words_list_for_places[f'{counter} место:'].append(words_list[i + 1])
    # если нет, увеличиваем счётчик мест
    else:
        counter += 1
        # если внесли всех в топ-3
        if counter == 4:
            # выходим из цикла и завершаем формирование строки
            break
        # если топ-3 ещё не заполнен
        else:
            # вносим бога на следующее место
            words_list_for_places[f'{counter} место:'].append(words_list[i + 1])
    i += 1
# для каждого места
for key, value in words_list_for_places.items():
    # распаковываем список, чтобы получить один список вместо нескольких
    words_list_for_places[key] = list(list_flatten(value))
    # собираем строку
    words_change_for_text += f'{key} {" ".join(words_list_for_places[key])[:-1]}\n'

fight_change_for_text = ''  # строка для ареносборщиков
fight_list, i, counter = [], 0, 1
fight_list_for_places = {'1 место:': [], '2 место:': [], '3 место:': []}
# для всех в списке изменений по кол-ву выигранных и проигранных арен
for key in fight_change.keys():
    # разбиваем строку на слова и вносим в список списков (имя бога, всего арен, +побед, +поражений, разница)
    fight_list.append(f'{key}: '
                      f'{fight_change[key][3]} '
                      f'({fight_change[key][1]} 🏆 '
                      f'({fight_change[key][0][:fight_change[key][0].find(" ")]} всего) / '
                      f'{fight_change[key][2]} ☠️ '
                      f'({fight_change[key][0][fight_change[key][0].find("/") + 1:-10]} всего));'.split(' '))
# ставим первого в списке на первое место
fight_list_for_places['1 место:'].append(fight_list[0])
# пока список не закончится
while i < len(fight_list) - 1:
    # если у следующего бога такая же разница побед и поражений, сколько и у предыдущего
    if fight_list[i][-10] == fight_list[i + 1][-10]:
        # добавляем его на то же самое место
        fight_list_for_places[f'{counter} место:'].append(fight_list[i + 1])
    # если нет, увеличиваем счётчик мест
    else:
        counter += 1
        # если внесли всех в топ-3
        if counter == 4:
            # выходим из цикла и завершаем формирование строки
            break
        # если топ-3 ещё не заполнен
        else:
            # вносим бога на следующее место
            fight_list_for_places[f'{counter} место:'].append(fight_list[i + 1])
    i += 1
# для каждого места
for key, value in fight_list_for_places.items():
    # распаковываем список, чтобы получить один список вместо нескольких
    fight_list_for_places[key] = list(list_flatten(value))
    # собираем строку
    fight_change_for_text += f'{key} {" ".join(fight_list_for_places[key])[:-1]}\n'

new_boss_for_text = ''  # строка для новых боссов
# для всех в списке собравших нового босса
for key, value in new_bosses.items():
    # собираем строку (имя бога, имя босса, мощь босса в %)
    new_boss_for_text += f'{key}: ' \
                         f'{value[0]} ' \
                         f'мощью в {value[1]}%\n'

# формирование общей строки для копирования на форум
write_forum_file = 1
if write_forum_file == 1:
    text = ''
    text += '"За чашкой вечернего чая":https://d.radikal.ru/d14/2004/7b/2fd6bd48f5e3.png\n\n' \
            'Цт. *Чеширские чиселки*\n\n'
    if len(god_leaved) > 0:
        text += f'📤 *Ушли из гильдии* - {len(god_leaved)} богов:\n{", ".join(god_leaved)}\n\n'
    if len(god_entered) > 0:
        text += f'📥 *Пришли в гильдию* - {len(god_entered)} богов:\n{", ".join(god_entered)}\n\n'
    if len(clan_position_change) > 0:
        text += f'👑 *Боги достигли званий:* \n{clan_position_change_for_text}\n'
    if len(new_level_list_worthy) > 0:
        nll = "; ".join("".join((k, ": ", str(v[0]), " (", str(v[1]), ")")) for k, v in new_level_list_worthy.items())
        text += f'🔝 *Герои достигли уровней* (кардинал и выше):\n{nll}\n\n'
    if len(new_t_level_list) > 0:
        ntll = "; ".join("".join((k, ": ", str(v[0]), " (", str(v[1]), ")")) for k, v in new_t_level_list.items())
        text += f'📈 *Герои достигли торговых уровней:*\n{ntll}\n\n'
    if len(pet_change_level_worthy) > 0:
        text += f'🐾 *Питомцы достигли уровней* (кардинал и выше):\n{pet_change_lvl_for_text}\n\n'
    if len(pet_change_status) > 0:
        text += f'👀 *Изменения по статусам питомцев*:\n{pet_change_status_for_text}\n'
    if len(new_temple) > 0:
        text += f'⛪ *Построено храмов:*\n{", ".join(new_temple)}\n\n'
    if len(new_arks) > 0:
        text += f'🛶 *Построено ковчегов (палуб):*\n{new_arks_for_text}\n\n'
    if len(new_lab) > 0:
        text += f'🔬 *Построено лабораторий:*\n{", ".join(new_lab)}\n\n'
    if len(new_bosses) > 0:
        text += f'👾 *Собрано новых боссов:*\n{new_boss_for_text}\n\n'
    if len(new_shop) > 0:
        text += f'⚖ *Построено лавок:*\n{", ".join(new_shop)}\n\n'
    if len(bricks_change) > 0:
        text += f'⛔ *Собрано кирпичей:*\n{bricks_change_for_text}\n'
    if len(wood_change) > 0:
        text += f'🌳 *Собрано брёвен:*\n{wood_change_for_text}\n'
    if len(fm_change) > 0:
        text += f'♀️♂️ *Собрано тварей* (самцы плюс самки):\n{fm_change_for_text}\n'
    if len(savings_change) > 0:
        text += f'💰 *Собрано сбережений* (тысяч):\n{savings_change_for_text}\n'
    if len(words_change) > 0:
        text += f'📖 *Собрано слов в книгах*:\n{words_change_for_text}\n'
    if len(fight_change) > 0:
        text += f'⚔ *Достигнуто аренных перевесов* (победы минус поражения):\n{fight_change_for_text}'
    text += '\nВся статистика доступна по "ссылке":https://drive.google.com/open?id=1-vWZTAmWmW3oPVU-qHhk_5Xk5lAiXEFk'
    f = open('results_text.txt', 'w', encoding='utf-8')
    f.write(text)
    f.close()
