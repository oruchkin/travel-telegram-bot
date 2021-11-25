import random

count_of_hotels = 9  # макимальное кол-во отелей, которое выводит бот (в main.py 232 нужно подредактировать
# клавиатуру при изменении этого параметра)

count_of_photo = 6  # макимальное кол-во фотографий отеля, которое выводит бот(в main.py 292 нужно подредактировать
# клавиатуру при изменении этого параметра)

page_number = 3  # макимальное кол-во страниц, которые запрашивает бот, если первой страницы ему не хватило в /bestdeal

number_stories = 6  # макимальное кол-во строк историй, которое выводит бот

time_out = 15  # время ожидания ответа с API


def hello() -> str:
    """
    Стикер, отправляемый с командой start
    """
    sticker: str = random.choice(['CAACAgIAAxkBAAEDQxBhjXzPDr7ckygFQf9V4zEWygU1fgAC5w0AAkwAAalLKPSbhF1cTYkiBA',
                                  'CAACAgIAAxkBAAEDQwRhjXxigXI86OK58F6nmT7whqosowACdQ8AAh4V8UuN549XMF_AnyIE',
                                  'CAACAgIAAxkBAAEDQm9hjTzUQmofflyiFV_l4Naw7NR7BwAC5QUAAj-VzAqeiXTPHeYV8SIE',
                                  'CAACAgIAAxkBAAEDQxhhjX4Qkge22q0-cRJKSE3zBiC9xQACswUAAj-VzApWmZVJF3xr0CIE',
                                  'CAACAgIAAxkBAAEDQ1phjZM5a8ToIGxyW4CNWfpOO_lX5wACoAADlp-MDmce7YYzVgABVSIE',
                                  'CAACAgIAAxkBAAEDQ1xhjZNGhN_4SC4iOrwF7wfOGIFu_wACNAEAAlKJkSMTzddv9RwHWCIE',
                                  'CAACAgIAAxkBAAEDQ15hjZNwJdHH-69xSUyY3AsyKRdhpAACSgADWbv8JZ3yyYHsNyFgIgQ'])
    return sticker


def misunderstand() -> str:
    """
    Стикер, отправляемый с командой not_understand
    """
    sticker: str = random.choice(['CAACAgIAAxkBAAEDQxRhjX3kHeBhgy3A8GUgccjwXwNzLQACUw8AAkcG-EsYhXwrKl3SnCIE',
                                  'CAACAgIAAxkBAAEDQwxhjXy5GhY-emfjhj3S_FYykd3n6wACxw8AAhat2Ul-GYhU8r2driIE',
                                  'CAACAgIAAxkBAAEDQwZhjXyYslua77jXoIqJ9JApfgMoSQAC-hEAAknF8EuBzj23_M8x3iIE',
                                  'CAACAgIAAxkBAAEDQwABYY18NxYf3GcvI3PiVqMySaOu2s0AAp8RAAIIoNBJeY4rQ3fKpYkiBA',
                                  'CAACAgIAAxkBAAEDQ2RhjZPk9IlduomXMUXjO-mI72nXAQAC2QADlp-MDv77WrBGeX1cIgQ',
                                  'CAACAgIAAxkBAAEDQ2ZhjZP5O8VkOvunjTmD0EDaFJnUvAAC1AUAAj-VzApct6L9SQE6PiIE',
                                  'CAACAgIAAxkBAAEDQ2hhjZQedJBdVt202c5xb0FQ8o7Z6gACbQAD5KDOB4hThnKtsh0bIgQ',
                                  'CAACAgIAAxkBAAEDQ2phjZQzqEkkPY4Rm_cgXn2d0j27yAACIQEAAvcCyA9E9UdZozFIriIE',
                                  'CAACAgIAAxkBAAEDQ29hjZShJczaArpnqDZHlEe54VNBYAACNAIAAladvQoxjc5OT0KBdyIE',
                                  'CAACAgEAAxkBAAEDQ3FhjZTFzQl6Hd4PJOhJ4kIaRvKIzQACjgEAAlWn0UV0hzIynaFaNiIE'])
    return sticker


def fail_searching() -> str:
    """
    Стикер отправляется если не найдено ни одного отеля
    """
    sticker: str = random.choice(['CAACAgIAAxkBAAEDQxphjYH0KA7LnIf40U0W5VbwovcJVgACShIAApQn0EljczZtGB_D8iIE',
                                  'CAACAgIAAxkBAAEDQx5hjYJtrBCH0rsXf6eMxhp3hw0xigACJAIAArrAlQVxH1p18x0QKyIE',
                                  'CAACAgIAAxkBAAEDQw5hjXzDEb0JuI4iDNYn5Wfd2UkifQACzQ8AArmr6Upe0YrDKbm3ZyIE',
                                  'CAACAgIAAxkBAAEDQyBhjYLkrZSR6iOWmOHiNgdIegr6CQACLgQAAj-VzApLBXfNu16CKyIE',
                                  'CAACAgIAAxkBAAEDQ0BhjYs_bpcrGuNuL2_jrbg1SwSwYwACMQEAAlKJkSNy74zuyFRhcyIE',
                                  'CAACAgIAAxkBAAEDQ3NhjZTewvvqUVYibrGhzxXpI_qwtAACBgMAAvPjvgtM9RvZ9valGCIE',
                                  'CAACAgIAAxkBAAEDQ3VhjZT7PGW5LaB9bExZNx5wAzviOQACPgADWbv8JciUxtK8a7dJIgQ',
                                  'CAACAgIAAxkBAAEDQ3thjZUsDeHHPzvfZKysoIbW0gZXxgACDAEAAvcCyA8bE6ozG0L6syIE',
                                  'CAACAgIAAxkBAAEDQ31hjZVU7DpstgLfqT4qUQteojM7ZgACJQkAAhhC7ghh9lneJtpq5SIE'])
    return sticker


def good_search() -> str:
    """
    Стикер, отправляемый при окончании поиски и если найден хотя бы 1 отель
    """
    sticker: str = random.choice(['CAACAgIAAxkBAAEDQyJhjYRSUh0gv-n9SljdbbSZHdjJqQACOQ0AAqef6UitbBViw4Y2WyIE',
                                  'CAACAgIAAxkBAAEDQyxhjYVcz6A7NJsjBMs-BXw8js6z7wADEQAC1-3gST1xM630SaByIgQ',
                                  'CAACAgIAAxkBAAEDQzJhjYZVasuGkPzUWjrjzl8od9gdwQACqg0AAh4dmUun3jjGWXCp9CIE',
                                  'CAACAgIAAxkBAAEDQzZhjYa-jLGHOildFwHWaX8Kt8vm5QAC7AADwZGyJM9plDKLR7hyIgQ',
                                  'CAACAgIAAxkBAAEDQ39hjZVocAABGTxEuVC_JvFMomtwZj0AAt4AA1advQql73c4VYMVxCIE',
                                  'CAACAgIAAxkBAAEDQ4VhjZWlxIq_pEqYRtNPposChA_7KAACFgADlp-MDhoIJB4TZLWPIgQ',
                                  'CAACAgIAAxkBAAEDQ4dhjZW3rDqhswpH2RFyC69ZJNtaFgACTAADRA3PF00ba9Q6BAfQIgQ',
                                  'CAACAgIAAxkBAAEDQ4thjZXhCSr5DhmNaw9o4MwOYZ9A7gACPg0AAtLXoUr3veGQuCeSqyIE',
                                  'CAACAgIAAxkBAAEDQ41hjZXugEUBIrmVm4R2X3MJpLIy5wACaQIAArrAlQUw5zOp4KLsaCIE',
                                  'CAACAgIAAxkBAAEDQ49hjZX_qD-a3UEWjXTa1YCtdKr9DAAC1QIAAvPjvgulRvceSfViLiIE',
                                  'CAACAgIAAxkBAAEDQ5FhjZYSdVLUo2pQmFkycphmvMhgtwACDwADlp-MDq9TsUcYhhw7IgQ',
                                  'CAACAgIAAxkBAAEDQ5NhjZYmeCzTTxBrGU6UECEMCQMdrQACYgADwDZPEwr306VKt5-UIgQ',
                                  'CAACAgIAAxkBAAEDQ5dhjZaydg1apzIjNL-DNBu5zRBvAgACZAADDbbSGRbBZmuQEnSJIgQ',
                                  'CAACAgIAAxkBAAEDQ5lhjZbJ7HZwI2zBAcg0hvjSNz_6OAAChgADRA3PF5hySbZkSauxIgQ',
                                  'CAACAgIAAxkBAAEDQ5thjZbeM9mhPRw5GHfsOnZ9OIiNgAACBgADJHFiGh-IenHizlbCIgQ',
                                  'CAACAgIAAxkBAAEDQ51hjZb0aTpeOdEy00hU-YiZSinrmAACNwEAAlKJkSPVFECnfG0SGiIE',
                                  'CAACAgIAAxkBAAEDQ59hjZcHIWQrW897oL5Nt7B5OFfbQQACyg8AAksokUnNTYPQyezO3CIE',
                                  'CAACAgIAAxkBAAEDQ6FhjZcVUPzeEOKvLbsQaXFN0weJGQACGAQAAn7yxQwRs0pjWvkH3yIE',
                                  'CAACAgIAAxkBAAEDQ6NhjZcnVta3WtnE52L2ECOXgOLmeAACWAAD5KDOB6zQ7H5i9f3_IgQ',
                                  'CAACAgIAAxkBAAEDQ6VhjZdKZr0WCOJUTiZK9OG_sb-yWQACUgADO2AkFEndYaMOmpblIgQ',
                                  'CAACAgIAAxkBAAEDQ6lhjZduSQZIBT64Ss-7psz7He8F7gACxg4AApXLQEqNb_xqmLajBCIE',
                                  'CAACAgIAAxkBAAEDQ6thjZeMuqO-f0qVdK3Qvry5x2mYkAACtwADwZxgDPilirtWD6kDIgQ',
                                  'CAACAgIAAxkBAAEDQ61hjZek1OlTYWyUs582bGOjT6ukigAC4Q0AAjEMmEqyiN2bo6-JXiIE',
                                  'CAACAgEAAxkBAAEDQ7FhjZfdJU26sz-8Dgg3rk4CfJKeYwACFQEAAjgOghGqOtb4EGwFOyIE',
                                  'CAACAgIAAxkBAAEDQ7NhjZfrucjHD8acZpfD9pzNSic4FgACAQEAAvcCyA--Bt0rrVjiJCIE',
                                  'CAACAgIAAxkBAAEDQ7lhjZgYF5dzdeKUhNBeO-77uFQkNQAChgADwZxgDOa4iNxdyRwEIgQ'])
    return sticker


def wait():
    """
    Стикер, отправляемый когда пользователь ждет результат
    """
    sticker: str = random.choice(['CAACAgIAAxkBAAEDQzhhjYqDNsmQTwnKCRlb-fcAAdV09DQAAl0OAAI7YKBLdQ2NqtLq9qAiBA',
                                  'CAACAgIAAxkBAAEDQz5hjYr0rijMRP8NgWc6Bpss6tyIaAAC6Q0AAoQJ4Uou2uzPddEWOCIE',
                                  'CAACAgIAAxkBAAEDQ0JhjYtayTrmSW3AIsV7hog-6_N3OQAC1wcAAkb7rAT1kHU4SQWQniIE',
                                  'CAACAgIAAxkBAAEDQ0ZhjYvEnrTOA1-_PLxqaSQKOnD_bQACTgADWbv8JQ3rz9n50HgqIgQ',
                                  'CAACAgIAAxkBAAEDQ0xhjYwifSukpna-fwRt-ZmPh3SJfQACUgADr8ZRGgSvecXtKHqOIgQ',
                                  'CAACAgIAAxkBAAEDQ05hjYxGgaXpDSJypEQnt2eks1njdwAC7wIAAvPjvgswbGXFtnD2ByIE',
                                  'CAACAgIAAxkBAAEDQ1JhjYzygM1FxSP6Q9LDO5tC0lmnmgACkAIAAladvQoy0qlxuNTQtSIE',
                                  'CAACAgIAAxkBAAEDQ1RhjY0KXE0NEtJSaanzvjnbG02OhwACIQQAAn7yxQwcyUR04TwmYiIE',
                                  'CAACAgIAAxkBAAEDQ1ZhjY0kAtrGCrVatBmEtL0wq_R2pQAC6QADUomRI8qrjxSfK0fJIgQ',
                                  'CAACAgIAAxkBAAEDQ1hhjY1WFa1bSEZL2tIirKccaRc-0QACSAMAAvPjvgs3pUbsiijoLyIE',
                                  'CAACAgIAAxkBAAEDQ7thjZguH-1TmKPVW6aSaJpFpVrQQwACDAQAAn7yxQyRKz6IhAoWTCIE',
                                  'CAACAgIAAxkBAAEDQ79hjZip1YX2CyDXjGeWrNnBskTmKQAC6QcAAkb7rASeqE0qlQtMbSIE',
                                  'CAACAgIAAxkBAAEDQ8FhjZjOBd3lphzJ5V0STkT_VMDhFAACXQUAAj-VzAqkBNzb9zv7KiIE',
                                  'CAACAgIAAxkBAAEDQ8NhjZjw37tsNqGzBtqJIbA3TQsvXgACgA4AAu7XsUu9fgMBjLx4_iIE',
                                  'CAACAgIAAxkBAAEDQ8VhjZkRn8wyOWhnD9czVCwKPwABVhcAAjEPAALtAuFKhBZaT-fC7ZUiBA',
                                  'CAACAgIAAxkBAAEDQ8dhjZklX_edVvtI-O58brZXSuxs6wAC4wwAAmZ88Evrogot8pA9ECIE',
                                  'CAACAgIAAxkBAAEDQ8lhjZk59UXyy2lDOTIRYwibojvzdgACeQwAAqGuQEjW9dENyNgsjCIE',
                                  'CAACAgIAAxkBAAEDQ8thjZlHMVa2fqtGTOdXQ-_JxDU1rAACzw8AAq_pSEv9aT0u6BZOXSIE',
                                  'CAACAgIAAxkBAAEDQ81hjZlTYU7NXfftz2uFSY6wzJapRQACtQADrWW8FCtKB7bVMynCIgQ',
                                  'CAACAgIAAxkBAAEDQ89hjZliBYpIYDTt1996sQRhIi_BNQACxQ4AAoxEmUgDii518Wg0eyIE',
                                  'CAACAgIAAxkBAAEDQ9FhjZlxoEh1LKBcJIPfusnEoX1ZJgACpAAD5KDOBx54SxCBG0A9IgQ',
                                  'CAACAgIAAxkBAAEDQ9NhjZl_7dO-74364ZintmHr6boGXAACDgMAAm2wQgMXWqCVVdoCpiIE',
                                  'CAACAgIAAxkBAAEDQ9VhjZmOSXjoxzo6jhHKnr6hQHpyDwACYg4AAsfaSUkwUi9jOMoXpyIE',
                                  'CAACAgIAAxkBAAEDQ9dhjZmZ4jMSkVluwVrdBdmDPzENIgACOQMAArVx2gYjUGZnvEY4rSIE',
                                  'CAACAgIAAxkBAAEDQ9lhjZnOu2l_BJX9chYxImmAgm4h5AACXwwAAmBWOUvXevjvfIJylCIE',
                                  'CAACAgIAAxkBAAEDQ9lhjZnOu2l_BJX9chYxImmAgm4h5AACXwwAAmBWOUvXevjvfIJylCIE',
                                  'CAACAgIAAxkBAAEDQ9thjZnTVU3Qbd-WMnnA3nimSXfjeAACHA0AAhOCwEkYiMrX3brt9iIE',
                                  'CAACAgEAAxkBAAEDQ91hjZnZyLvPuXbsKxL0IGDSQdMs_AAC7QEAAjgOghE8J4BsgBeaAyIE',
                                  'CAACAgIAAxkBAAEDQ99hjZng5oTKegABuwErNQzUZkq_5dcAAtsTAAJ_h4lLyRt_VfZmAw4iBA',
                                  'CAACAgIAAxkBAAEDQ99hjZng5oTKegABuwErNQzUZkq_5dcAAtsTAAJ_h4lLyRt_VfZmAw4iBA',
                                  'CAACAgIAAxkBAAEDQ-FhjZnn2s4diUPU7MVIiHMiuAH5GgACWwADWbv8JWRSp1P6Y54eIgQ',
                                  'CAACAgIAAxkBAAEDQ-NhjZnw8bHf0hz4UNv_L0piqN9S9gACvgsAAlFbWEpmK133A-RvvCIE',
                                  'CAACAgIAAxkBAAEDQ-VhjZn2Saoa2m-vcnl8yXNAQWU3XgAC9wYAAkb7rARWm6hbD5l2HSIE',
                                  'CAACAgIAAxkBAAEDQ-dhjZn5EY-HuZtmi-VHpaynq3qK5wACpRAAAjpR2ErTa1u1cj92oyIE',
                                  'CAACAgIAAxkBAAEDQ-lhjZn9cjA7mmb0lVjugQHyWKnzqAACNAcAAkb7rAR38PeESQbBHiIE',
                                  'CAACAgIAAxkBAAEDQ-1hjZoSp4VFMYkTMPiGJEJPTYfC3QAC6w0AAlIjkUoCzPNw-Lv9LCIE',
                                  'CAACAgIAAxkBAAEDQ-9hjZoVMsRmtuwQkbQaM7DD7zcL7AACCgsAAi8P8AaHQje1ciNWiiIE',
                                  'CAACAgIAAxkBAAEDQ_FhjZoZEa1gQwTy24yaf0wcrSKFKAACIQAD5KDOB_ejN70KJ-nCIgQ',
                                  'CAACAgIAAxkBAAEDQ_NhjZoeA4elLn16QY-j3g5f_BK1lgADCwACLw_wBmV5BhlD44WoIgQ'])
    return sticker
