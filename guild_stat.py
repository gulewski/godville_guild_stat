import json
import godville_stat_functions as gsf

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


# формирование списков богов
god_list_old = list(data_old.keys())  # список богов из начала статистики
god_list_new = list(data_new.keys())  # список богов из конца статистики
god_list_actual = sorted(list(set(god_list_old) & set(god_list_new)))  # список богов, которые есть в обоих списках
god_leaved = sorted(list(set(god_list_old).difference(set(god_list_new))))  # ушедшие боги
god_entered = sorted(list(set(god_list_new).difference(set(god_list_old))))  # пришедшие боги

# переменные для всех позиций статистики
new_level_list_all, new_level_list_worthy = {}, {}  # списки богов с новыми уровнями (все и кардинал+)
new_t_level_list = {}  # список богов с новыми торговыми уровнями
clan_position_change = {}  # изменение ранга в гильдии
bricks_change = {}  # изменение по собранным кирпичам
wood_change, savings_change = {}, {}  # изменение по собранным брёвнам и отложенной пенсии
words_change = {}  # изменение по собранным словам
fm_change = {}  # изменения по тварям
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
    # обновляем словари с уровнями героев
    gsf.update_level_list(data_new, data_old, god, new_level_list_worthy, new_level_list_all)
    # уровни торговца
    gsf.update_trade_level_list(data_new, data_old, god, new_t_level_list)
    # позиция в гильдии
    gsf.update_clan_position_list(data_new, data_old, god, clan_position_change)
    # количество собранных кирпичей и новые храмы
    gsf.update_brickers_and_temples(data_new, data_old, god, bricks_change, new_temple)
    # количество собранных брёвен и новые ковчеги
    gsf.update_wooders_and_arks(data_new, data_old, god, wood_change, new_arks)
    # количество отложенной пенсии и новые лавки
    gsf.update_savers_and_shops(data_new, data_old, god, savings_change, new_shop)
    # общая статистика по количеству собранных тварей (самцов и самок) и новые лабы
    gsf.update_fm_and_labs(data_new, data_old, god, fm_change, new_lab)
    # новые боссы
    gsf.update_bosses(data_new, data_old, god, new_bosses)
    # количество вписанных слов в книгу
    gsf.update_writers(data_new, data_old, god, words_change)
    # изменение в счётчике дуэлей
    gsf.update_fighters(data_new, data_old, god, fight_change)
    # питомцы
    gsf.update_petters(data_new, data_old, god, pet_change_level_worthy, pet_change_level_all, pet_change_status)

# сортируем все списки
god_leaved = sorted(god_leaved)
god_entered = sorted(god_entered)
new_level_list_all = gsf.sort_dict(new_level_list_all, 1)  # по количеству полученных уровней
new_level_list_worthy = gsf.sort_dict(new_level_list_worthy, 0)  # по уровню
new_t_level_list = gsf.sort_dict(new_t_level_list, 0)  # по уровню
bricks_change = gsf.sort_dict(bricks_change, 1)  # по количеству собранных кирпичей
wood_change = gsf.sort_dict(wood_change, 1)  # по количеству собранных брёвен
new_arks = sorted(new_arks.items())  # по новым палубам
savings_change = gsf.sort_dict(savings_change, 1)  # по количеству отложенной пенсии
fm_change = gsf.sort_dict(fm_change, 3)  # по сумме собранных самцов и самок
words_change = gsf.sort_dict(words_change, 1)  # по количеству вписанных слов
fight_change = gsf.sort_dict(fight_change, 3)  # по разнице побед-поражений
pet_change_level_all = gsf.sort_dict(pet_change_level_all, 1)  # по уровню питомца
pet_change_level_worthy = gsf.sort_dict(pet_change_level_worthy, 1)  # по уровню питомца

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
write_stat_file = 0
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
    bricks_list_for_places[key] = list(gsf.list_flatten(value))
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
    wood_list_for_places[key] = list(gsf.list_flatten(value))
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
    fm_list_for_places[key] = list(gsf.list_flatten(value))
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
    savings_list_for_places[key] = list(gsf.list_flatten(value))
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
    words_list_for_places[key] = list(gsf.list_flatten(value))
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
    fight_list_for_places[key] = list(gsf.list_flatten(value))
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
write_forum_file = 0
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
