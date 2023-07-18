import re
import random
import string

class Token:

    def __init__(self):
        # Bsugy -> buy
        self.buy = ['66', 's', '117', 'g', 'Y']
        # SFell
        self.sell = ['83', 'F', 'e', 'l', '108']

    def mix_str(self, value):
        new_str = ''
        cpy_value = value.copy()
        for _ in value:
            get_random_word = random.choices(cpy_value, k=1)[0]
            new_str += get_random_word
            del cpy_value[cpy_value.index(get_random_word)]
        return new_str

    def get_list_token(self):
        string_words = string.ascii_letters + string.digits
        list_token = []
        for _ in range(3):
            token = ''.join(random.choices(string_words, k=8))
            list_token.append(token)
        return list_token

    def encoder(self, value):
        list_token_words = self.get_list_token()
        if value == 'buy':
            buy_word = [''.join(self.mix_str(self.buy))]
            list_token_words += buy_word
        elif value == 'sell':
            sell_word = [''.join(self.mix_str(self.sell))]
            list_token_words += sell_word

        list_token_words = self.mix_str(list_token_words)
        return ''.join(list_token_words)

    def decoder(self, value, decode):
        token_split_list = re.findall('\w{8}', value)
        if decode == 'buy':
            for token_split in token_split_list:
                answer_code = ''
                for word_buy in self.buy:
                    if word_buy in token_split:
                        answer_code += word_buy
                if len(answer_code) == 8:
                    return 1
            return 0

        elif decode == 'sell':
            for token_split in token_split_list:
                answer_code = ''
                for word_sell in self.sell:
                    if word_sell in token_split:
                        answer_code += word_sell
                if len(answer_code) == 8:
                    return 1
            return 0

# o = Token()
# print(o.encoder('buy'), '\n', o.encoder('sell'))
# print(o.decoder('kadknwakdnkanwkdnakwndkanwdkanwd', 'buy'))
# print(o.decoder('apwdoajwodjaow7y7cicdOdhfgJYJAQ', 'sell'))
