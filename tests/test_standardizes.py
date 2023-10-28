import pytest

from module.standardizes import (
    add_left_space_to_slice,
    add_right_space_to_slice,
    clean_string,
    make_slice_capitalized,
    make_string_capitalized,
    remove_extra_blank,
    remove_space_around_punctuation,
    remove_space_between_digits_in_slice,
)


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param(
            '    ',
            '',
            id='empty string',
        ),
        pytest.param(
            '  amet!  ',
            'amet!',
            id='single world',
        ),
        pytest.param(
            '  sit  ,  amet  (  mauris  )  commodo  .  quis  !  ',
            'sit , amet ( mauris ) commodo . quis !',
            id='string with punctuation',
        ),
        pytest.param(
            '  tellus  \n    elementum  sagittis  \n    vitae  et  .  ',
            'tellus\n    elementum sagittis\n    vitae et .',
            id='string with newlines',
        ),
        pytest.param(
            (
                ' level1          \n'
                '  *  level2      \n'
                '    -  level3    \n'
                '      +  level4  \n'
                '\n'
                '  level1         \n'
                '    *  level2    \n'
                '        - level3 \n'
                '\n'
                '   level1        \n'
            ),
            (
                'level1\n'
                '  * level2\n'
                '    - level3\n'
                '      + level4\n'
                '\n'
                '  level1\n'
                '    * level2\n'
                '        - level3\n'
                '\n'
                '   level1'
            ),
            id='string with multilevel',
        ),
    ),
)
def test_remove_extra_blank(raw, clean):
    assert remove_extra_blank(raw) == clean


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param(
            '    ',
            '    ',
            id='empty string',
        ),
        pytest.param(
            '  a  ',
            '  a  ',
            id='spaces around word char',
        ),
        pytest.param(
            '  .  ',
            ' . ',
            id='> 1 space around char',
        ),
        pytest.param(
            '  .  !  ',
            ' .! ',
            id='> 1 space around chars',
        ),
        pytest.param(
            '  . !  ',
            ' .! ',
            id='1 space between chars',
        ),
        pytest.param(
            'tellus ( elementum ) sagittis ? vitae ! et .',
            'tellus(elementum)sagittis?vitae!et.',
            id='base',
        ),
        pytest.param(
            '. . . tellus ? ? ( elementum ) ! ! et . . .',
            '...tellus??(elementum)!!et...',
            id='with duplicated chars',
        ),
    ),
)
def test_remove_space_around_punctuation(raw, clean):
    assert remove_space_around_punctuation(raw) == clean


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param(
            '! some . string . where more , than one space for dot .\n yes',
            '! Some . String . Where more , than one space for dot .\n Yes',
            id='case',
        ),
        pytest.param(
            'some . test . case ; for ; test\n new . line . add .\n more',
            'Some . Test . Case ; For ; Test\n new . Line . Add .\n More',
            id='case',
        ),
        pytest.param(
            '- some . test . case ; for ; test\n new . line . add .\n more',
            '- some . Test . Case ; For ; Test\n new . Line . Add .\n More',
            id='case',
        ),
    ),
)
def test_make_string_capitalized(raw, clean):
    assert make_string_capitalized(raw) == clean


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param('0 0', '00', id='space between'),
        pytest.param('00 ', '00 ', id='space on left'),
        pytest.param(' 00', ' 00', id='space on right'),
        pytest.param('a a', 'a a', id='incorrect type into slice'),
        pytest.param('a 0', 'a 0', id='incorrect type into slice'),
        pytest.param('00', None, id='too short slice'),
        pytest.param('0000', None, id='too long slice'),
    ),
)
def test_remove_space_between_digits_in_slice(raw, clean):
    if clean is not None:
        assert remove_space_between_digits_in_slice(raw) == clean
        return

    with pytest.raises(ValueError):
        remove_space_between_digits_in_slice(raw)


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param('e.e', 'e.E', id='after .'),
        pytest.param('e:e', 'e:E', id='after :'),
        pytest.param('e;e', 'e;E', id='after ;'),
        pytest.param('e!e', 'e!E', id='after !'),
        pytest.param('e?e', 'e?E', id='after ?'),
        pytest.param('e,e', 'e,e', id='after ,'),
        pytest.param('e', None, id='with short slice'),
        pytest.param('e.ee', None, id='with long slice'),
    ),
)
def test_make_slice_capitalized(raw, clean):
    if clean is not None:
        assert make_slice_capitalized(raw) == clean
        return

    with pytest.raises(ValueError):
        make_slice_capitalized(raw)


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param('e(e', 'e (e', id='before ('),
        pytest.param('e[e', 'e [e', id='before ['),
        pytest.param('e{e', 'e {e', id='before {'),
        pytest.param('e«e', 'e «e', id='before «'),
        pytest.param('e„e', 'e „e', id='before „'),
        pytest.param('e‘e', 'e ‘e', id='before ‘'),
        pytest.param('e№e', 'e №e', id='before №'),
        pytest.param('e!e', 'e!e', id='with incorrect char !'),
        pytest.param('e!ee', None, id='with incorrect slice len'),
    ),
)
def test_add_left_space_to_slice(raw, clean):
    if clean is not None:
        assert add_left_space_to_slice(raw) == clean
        return

    with pytest.raises(ValueError):
        add_left_space_to_slice(raw)


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param('e)e', 'e) e', id='after )'),
        pytest.param('e]e', 'e] e', id='after ]'),
        pytest.param('e}e', 'e} e', id='after }'),
        pytest.param('e»e', 'e» e', id='after »'),
        pytest.param('e“e', 'e“ e', id='after “'),
        pytest.param('e’e', 'e’ e', id='after ’'),
        pytest.param('e.e', 'e. e', id='after .'),
        pytest.param('e:e', 'e: e', id='after :'),
        pytest.param('e,e', 'e, e', id='after ,'),
        pytest.param('e;e', 'e; e', id='after ;'),
        pytest.param('e!e', 'e! e', id='after !'),
        pytest.param('e?e', 'e? e', id='after ?'),
        pytest.param('0.0', '0.0', id='digits dot separated'),
        pytest.param('0,0', '0, 0', id='digits comma separated'),
        pytest.param('ee', None, id='with incorrect slice len'),
    ),
)
def test_add_right_space_to_slice(raw, clean):
    if clean is not None:
        assert add_right_space_to_slice(raw) == clean
        return

    with pytest.raises(ValueError):
        add_right_space_to_slice(raw)


@pytest.mark.parametrize(
    argnames='raw,clean',
    argvalues=(
        pytest.param(
            '  some  ( test )  string ,  with . ошибками  !!  \n    ффф line.',
            'Some (test) string, with. Ошибками!!\n    Ффф line.',
            id='default',
        ),
        pytest.param(
            '1. string  number1  .    \n    2. string  number2.',
            '1. String number1.\n    2. String number2.',
            id='numbers dot separated new line',
        ),
        pytest.param(
            'some  numbers  1  1  ,  1  1  and  1  1  .  1  1  .',
            'Some numbers 11, 11 and 11.11.',
            id='with numbers',
        ),
        pytest.param(
            'some  "  test  "  string  .  some  test  "  string  "  .  ',
            'Some"test"string. Some test"string".',
            id='with "',
        ),
        pytest.param(
            "some  '  test  '  string  .  some  test  '  string  '  .  ",
            "Some'test'string. Some test'string'.",
            id="with '",
        ),
        pytest.param(
            'r  -  r  .  \nr  &  r  .  \nr  /  r  .  \nr  `  r  .  \n',
            'R-r.\nR&r.\nR/r.\nR`r.',
            id='string with middle chars',
        ),
        pytest.param(
            '  test  string  ',
            'Test string',
            id='case',
        ),
        pytest.param(
            '  Ф.О.Имя  ',
            'Ф. О. Имя',
            id='case',
        ),
        pytest.param(
            '  some  &  string  ',
            'Some&string',
            id='case',
        ),
        pytest.param(
            '  Хлопья  +  Отруби  ',
            'Хлопья+Отруби',
            id='case',
        ),
        pytest.param(
            '  Пюре яблоко   +груша+  персик  ',
            'Пюре яблоко+груша+персик',
            id='case',
        ),
        pytest.param(
            '  2  +  2  =  4  ',
            '2+2=4',
            id='case',
        ),
        pytest.param(
            '  (  2  +  2  )  *  2  =  8  ',
            '(2+2)*2=8',
            id='case',
        ),
        pytest.param(
            '  (  2  +  2  )  -  2  =  2  ',
            '(2+2)-2=2',
            id='case',
        ),
        pytest.param(
            '  (  (  (  2  -  2  )  +  (  1  + 1  )  )  /  2  )  *  2  =  2  ',
            '(((2-2)+(1+1))/2)*2=2',
            id='case',
        ),
        pytest.param(
            '  (  (  (  )  )  )  ',
            '((()))',
            id='case',
        ),
        pytest.param(
            '  some  !  string  ',
            'Some! String',
            id='case',
        ),
        pytest.param(
            '  some  ,  test  .  string  ',
            'Some, test. String',
            id='case',
        ),
        pytest.param(
            '  some  -String  ',
            'Some-String',
            id='case',
        ),
        pytest.param(
            '  Some  (  Test  )  case.  ',
            'Some (Test) case.',
            id='case',
        ),
        pytest.param(
            '  7  простых  ',
            '7 простых',
            id='case',
        ),
        pytest.param(
            '  4-  х  ',
            '4-х',
            id='case',
        ),
        pytest.param(
            '  капучино 3  0  0  мл  ',
            'Капучино 300 мл',
            id='case',
        ),
        pytest.param(
            '  Dr.dias  ',
            'Dr. Dias',
            id='case',
        ),
        pytest.param(
            '  йогурт 2  .  5  %  -  3  .  5  %  Слобода  ',
            'Йогурт 2.5%-3.5% Слобода',
            id='case',
        ),
        pytest.param(
            '  огурцы 6  -  9  см  ',
            'Огурцы 6-9 см',
            id='case',
        ),
        pytest.param(
            '  Оливки с косточкой  /  без косточки  ',
            'Оливки с косточкой/без косточки',
            id='case',
        ),
        pytest.param(
            '  Орех  Коко  -де-  мер  ',
            'Орех Коко-де-мер',
            id='case',
        ),
        pytest.param(
            '  какао  -  порошок обезжиренный  0  -  1  %  ',
            'Какао-порошок обезжиренный 0-1%',
            id='case',
        ),
        pytest.param(
            '  D  \'  Oro    D  `  Oro  ',
            'D\'Oro D`Oro',
            id='case',
        ),
        pytest.param(
            '  КСБ  -  УФ  -  55  ,  ADD  -  SSE  - 44  ',
            'КСБ-УФ-55, ADD-SSE-44',
            id='case',
        ),
        pytest.param(
            '  корейка свиная  б  /  к   (  карбонад)  ',
            'Корейка свиная б/к (карбонад)',
            id='case',
        ),
        pytest.param(
            '  1  -  го сорта  ,  мука пшеничная  ',
            '1-го сорта, мука пшеничная',
            id='case',
        ),
        pytest.param(
            '  хлопья  №  2   Агро  -  Альянс  ',
            'Хлопья №2 Агро-Альянс',
            id='case',
        ),
    ),
)
def test_clean_string(raw, clean):
    assert clean_string(raw) == clean
