# -*- coding: utf-8 -*-

import os
import unittest
from anjuke import pinyin

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWordMap(self):
        map = pinyin.WordMapper()
        self.assertEqual([['zhong1', 'zhong4']], map[u'中'])
        map[u'中文'] = ['zhong1', 'wen2']
        self.assertEqual(['zhong1', 'wen2'], map[u'中文'])

    def testConverter(self):
        converter = pinyin.Converter()
        print converter.convert(u'123 1.中文测试1。', fmt='tn', sc=False, pp=True)

    def testConverterWithFile(self):
        converter = pinyin.Converter()
        converter.load_word_file(os.path.dirname(os.path.abspath(__file__)) + '/words.txt')
        print converter.convert('什么莘莘莘莘学子莘庄闵行区北翟路')

if __name__ == '__main__':
    unittest.main()
