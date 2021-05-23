def format_data(data):
    """
    Функция форматирования данных

    :param data: дата для форматирования
    :return: time_list, adj_close: лист с датами, лист со средней ценой
    """
    ADJ_CLOSE_INDEX = 4  # для данных с YahooFinance

    time_list = data.index.tolist()  # в формате Timestamp
    adj_close = list(map(lambda x: x[ADJ_CLOSE_INDEX], data.values.tolist()))

    return time_list, adj_close
