# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# forkleft[dot]py - Python3 implementation of Forkleft
#
# github.com/ferhatgec/forkleft.py
# github.com/ferhatgec/forkleft
#

from enum import IntEnum


class Keywords(IntEnum):
    H1, \
    H2, \
    H3, \
    H4, \
    H5, \
    H6, \
    \
    Italic, \
    Bold, \
    Blockquote, \
    \
    Newline, \
    Undefined = range(0, 11)


class Forkleft:
    keywords = [
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',

        'italic',
        'bold',
        'blockquote',

        '~newline~'
    ]

    html_keywords = [
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',

        'em',
        'strong',

        'blockquote'
    ]

    class Codegen:
        @staticmethod
        def init_type(html: str, data: str):
            return f'<{html}>{data}</{html}>'

        @staticmethod
        def init(keyword: Keywords, generated: str, data: str, newline: bool) -> str:
            if Keywords.H1 or \
                    Keywords.H2 or \
                    Keywords.H3 or \
                    Keywords.H4 or \
                    Keywords.H5 or \
                    Keywords.H6 or \
                    \
                    Keywords.Italic or \
                    Keywords.Bold or \
                    Keywords.Blockquote:
                if newline:
                    return generated + Forkleft.Codegen.init_type('p',
                                                                  Forkleft.Codegen.init_type(
                                                                      Forkleft.html_keywords[keyword], data)) + '\n'

                return generated + Forkleft.Codegen.init_type(Forkleft.html_keywords[keyword], data) + '\n'

    class Parser:
        def __init__(self):
            self.tokens = []

            self.is_found = False
            self.is_newline = False

            self.is_setter = False
            self.is_data = False

            self.data = ''
            self.keyword_data = ''
            self.generated = ''

            self.current_token = Keywords.Undefined

        def init(self, data: []):
            self.tokens = data

        def get(self):
            return self.generated

        def parse(self):
            for data in self.tokens:
                if self.is_found:
                    if self.is_setter:
                        if len(data) == 0:
                            self.is_found = self.is_setter = False
                            continue

                        if self.is_data:
                            for ch in data:
                                if ch != '\'':
                                    self.keyword_data += ch
                                else:
                                    self.is_data = self.is_setter = self.is_found = False

                                    self.generated = Forkleft.Codegen.init(self.current_token,
                                                                           self.generated,
                                                                           self.keyword_data,
                                                                           self.is_newline)

                                    print(f'{self.data} : {self.keyword_data}')

                                    self.keyword_data = self.data = ''

                                    break

                    if data.startswith('\''):
                        self.is_data = True

                        check = ''

                        for ch in data[1:]:
                            if check == '\\' and ch == '\'':
                                self.keyword_data += '\''
                                check = ' '

                                continue

                            if ch == '\'':
                                check = ch
                                continue

                            self.keyword_data += ch

                        continue

                    if data == Forkleft.keywords[Keywords.Newline]:
                        self.is_newline = True
                        continue

                    if data == ':=':
                        self.is_setter = True
                        continue

                check = self.is_keyword(data)

                if check != Keywords.Undefined:
                    self.is_found = True
                    self.data = data
                    self.current_token = check

                    continue

        def is_keyword(self, data: str) -> Keywords:
            for index, keyword in enumerate(Forkleft.keywords):
                if keyword == data:
                    return Keywords(index)

            return Keywords.Undefined

    class Tokenize:
        def __init__(self):
            self.tokens = []

            self.parser = Forkleft.Parser()

        def get(self):
            return self.parser.get()

        def init(self, data: str):
            is_data = False

            for line in data.splitlines():
                for token in line.split(' '):
                    if len(token) >= 2 and not is_data:
                        # supported comment blocks
                        # ~=
                        # =~
                        if (token.startswith('~') or token.startswith('=')) \
                                and (token[1] == '=' or token[1] == '~'):
                            break

                    if token.startswith('\''):
                        is_data = True

                    if is_data:
                        if token.endswith('\''):
                            self.tokens.append(token)
                            is_data = False
                        else:
                            self.tokens.append(token + ' ')

                        continue

                    self.tokens.append(token)

            self.parser.init(self.tokens)
            self.parser.parse()

            self.tokens.clear()
