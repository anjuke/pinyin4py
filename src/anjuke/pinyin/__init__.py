# -*- coding: utf-8 -*-

import os
import re

_punctuation_mapper = dict(zip(
    u'？！。，、：《》“”‘’　',
    u'?!.,,:<>""\'\' '))

def _load_character_mapper():
    mapper = dict()
    filename = os.path.dirname(__file__)
    filename += '/chars.txt'
    f = open(filename)
    try:
        for line in f:
            if re.match('^[\s]*#', line):
                continue
            line = line.strip()
            columns = re.split('[\s(,)]+', line)
            ch = unichr(int(columns[0], 16))
            pinyin = columns[1:-1]
            if len(pinyin) > 1:
                mapper[ch] = pinyin
            else:
                mapper[ch] = pinyin[0]
    finally:
        f.close()
    return mapper

_character_mapper = _load_character_mapper()

class Tokenizer:
    def __init__(self, text):
        assert isinstance(text, unicode)

        self._text = text
        self._pos = 0
        self._length = len(text)

    def __iter__(self):
        return self

    def next(self):
        if self._pos >= self._length:
            raise StopIteration

        i = self._pos
        type = self._char_type(self._text[i])

        while True:
            i += 1
            if i >= self._length or self._char_type(self._text[i]) != type:
                break

        try:
            return type, self._text[self._pos:i]
        finally:
            self._pos = i

    def _char_type(self, ch):
        if re.match('[\s]', ch):
            return 4
        elif ch in _punctuation_mapper:
            return 3
        elif ord(ch) <= 255:
            return 1
        else:
            return 2

class WordMapper:
    def __init__(self):
        self._mapper = dict()

    def load_from_file(self, filename):
        f = open(filename)
        try:
            for line in f:
                if re.match('^[\s]*#', line):
                    continue
                line = line.strip()
                columns = re.split('[\s]+', line)
                word = unicode(columns[0], 'UTF-8')
                pinyin = columns[1:]
                self[word] = pinyin
        finally:
            f.close()

    def __setitem__(self, word, pinyin):
        assert isinstance(word, unicode)

        mapper = self._mapper
        for ch in word:
            if not ch in mapper:
                mapper[ch] = dict()
            mapper = mapper[ch]

        mapper['PY'] = pinyin

    def __getitem__(self, word):
        assert isinstance(word, unicode)

        length = len(word)

        pinyin = []
        pos = 0
        last_pinyin = None
        last_pos = 0
        mapper = self._mapper

        while pos < length:
            ch = word[pos]
            if ch in mapper:
                mapper = mapper[ch]
                if 'PY' in mapper:
                    last_pinyin = mapper['PY']
                    last_pos = pos
                pos += 1
                if pos < length:
                    continue

            if last_pinyin is None:
                ch = word[last_pos]
                if ch in _character_mapper:
                    last_pinyin = _character_mapper[ch]
                else:
                    last_pinyin = ch
                if len(last_pinyin) > 1:
                    pinyin.append(last_pinyin)
                else:
                    pinyin.extend(last_pinyin)
            else:
                pinyin.extend(last_pinyin)

            pos = last_pos + 1
            mapper = self._mapper
            last_pinyin = None
            last_pos = pos

        if last_pinyin is not None:
            pinyin.extend(last_pinyin)

        return pinyin

class Converter:
    def __init__(self, word_mapper=WordMapper()):
        self._word_mapper = word_mapper

    def load_word_file(self, filename):
        self._word_mapper.load_from_file(filename)

    def convert(self, text, fmt='df', sc=True, pp=False, fuzzy=0):
        if not isinstance(text, unicode):
            text = unicode(text, 'UTF-8')

        tokenizer = Tokenizer(text)
        tokens = map(self._convert_token, tokenizer)

        pinyin = ''
        last_type = 4
        for type, word in tokens:
            if type == 2:
                if last_type != 4:
                    pinyin += ' '
                pinyin += self._format_word(word, fmt, sc, pp, fuzzy)
                pass
            elif type == 3:
                pinyin += word
            elif type == 4:
                pinyin += word
            else:
                if last_type == 2:
                    pinyin += ' '
                pinyin += word

            last_type = type

        return pinyin

    def _convert_token(self, token):
        type, word = token
        if type == 2:
            return type, self._word_mapper[word]
        elif type == 3:
            return type, _punctuation_mapper[word]
        else:
            return type, word.encode('UTF-8')

    def _format_word(self, word, fmt, sc, pp, fuzzy):
        if pp and not sc:
            pinyin_set = set()
            pinyin_list = [None] * len(word)
            def func(idx):
                if idx >= len(word):
                    pinyin_set.add(''.join(pinyin_list))
                    return
                ch = word[idx]
                if isinstance(ch, list):
                    for c in ch:
                        pinyin_list[idx] = self._format_ch(c, fmt, fuzzy)
                        func(idx+1)
                else:
                    pinyin_list[idx] = self._format_ch(ch, fmt, fuzzy)
                    func(idx+1)
            func(0)
            return '|'.join(pinyin_set)

        def func(ch):
            if isinstance(ch, list):
                pinyin_list = []
                if pp:
                    for c in ch:
                        pinyin_list.append(self._format_ch(c, fmt, fuzzy))
                else:
                    pinyin_list.append(self._format_ch(ch[0], fmt, fuzzy))
                return '|'.join(set(pinyin_list))
            else:
                return self._format_ch(ch, fmt, fuzzy)

        pinyin_list = map(func, word)
        if sc:
            return ' '.join(pinyin_list)
        else:
            return ''.join(pinyin_list)

    def _format_ch(self, ch, fmt, fuzzy):
        if fuzzy > 0:
            raise Exception('Not implemented')

        if fmt == 'df':
            return ch[:-1]

        if fmt == 'tn':
            return ch

        if fmt == 'fl':
            return ch[0]

        raise Exception('Not implemented')
