import sys
from unicodedata import decomposition

def get_kumimoji():
    """ Unicodeにある片仮名や平仮名を使用した組文字の配列を返す
    """

    return [chr(x) for x in range(13056, 13143+1)] + [chr(127488)]

def decomp(c):
    """ >>> decomp('㍗')
        ['ワ', 'ッ', 'ト']
    """

    return [chr(int(x, 16)) for x in decomposition(c).split(' ')[1:]]

def get_square_pattern_kumimoji():
    """ ㌐/㌃/㌀ ○
        ㌕/㌙/㌖ ☓
    """

    return [x for x in get_kumimoji() if len(decomp(x)) in [2, 3, 4]]

def fill_gram_set(aset, gram, km):
    aset['list'].append(gram)
    aset['map'][gram] = km
    return aset

def build_ngram_sets(spkm, mark_ends, only_full):
    """ 引数：　組文字の配列、マーカー設定、組文字部分集合設定
        返り値：横１行目・２行目・縦１行目・２行目それぞれの配列

        例：　　>>> build_ngram_sets(['㌐','㌳'], True, False)
                [['ギ$','$フィ','フィ$','フィ'],
                 ['$ガ','$ート','ート$','ート'],
                 ['ギ$'],
                 ['$ガ','$ィト','ィト$','ィト']]

        注１：　㌳とかの「ー」は縦書きで使えない
        注２：　$は文字列の始まり・終わりを表すマーカー
    """

    yoko_t = {'label':'横書き１行目','list':[], 'map':{}}
    yoko_b = {'label':'横書き２行目','list':[], 'map':{}}
    tate_r = {'label':'縦書き１行目','list':[], 'map':{}}
    tate_l = {'label':'縦書き２行目','list':[], 'map':{}}
    for km in spkm:
        dc = decomp(km)
        if len(dc) == 2 and not only_full:    # 例：㌔
            if dc[0] == 'ほ':
                dc = ['ホ','カ']
            if mark_ends:
                yoko_t = fill_gram_set(yoko_t, '{}$'.format(dc[0]), km)
                yoko_b = fill_gram_set(yoko_b, '${}'.format(dc[1]), km)
            else:
                yoko_t = fill_gram_set(yoko_t, '{}'.format(dc[0]), km)
                yoko_b = fill_gram_set(yoko_b, '{}'.format(dc[1]), km)
            if 'ー' not in dc[0]:
                if mark_ends:
                    tate_l = fill_gram_set(tate_l, '{}$'.format(dc[0]), km)
                else:
                    tate_l = fill_gram_set(tate_l, '{}'.format(dc[0]), km)
            if 'ー' not in dc[1]:
                if mark_ends:
                    tate_r = fill_gram_set(tate_r, '${}'.format(dc[1]), km)
                else:
                    tate_r = fill_gram_set(tate_r, '{}'.format(dc[1]), km)
        elif len(dc) == 3 and not only_full:  # 例：㌵
            if mark_ends:
                yoko_t = fill_gram_set(yoko_t, '${}{}'.format(dc[0], dc[1]), km)
                yoko_t = fill_gram_set(yoko_t, '{}{}$'.format(dc[0], dc[1]), km)
                yoko_t = fill_gram_set(yoko_t, '{}{}'.format(dc[0], dc[1]), km)
                yoko_b = fill_gram_set(yoko_b, '{}$'.format(dc[2]), km)
            else:
                yoko_t = fill_gram_set(yoko_t, '{}{}'.format(dc[0], dc[1]), km)
                yoko_b = fill_gram_set(yoko_b, '{}'.format(dc[2]), km)
            if 'ー' not in dc[0]+dc[2]:
                if mark_ends:
                    tate_l = fill_gram_set(tate_l, '${}{}'.format(dc[0], dc[2]), km)
                    tate_l = fill_gram_set(tate_l, '{}{}$'.format(dc[0], dc[2]), km)
                    tate_l = fill_gram_set(tate_l, '{}{}'.format(dc[0], dc[2]), km)
                else:
                    tate_l = fill_gram_set(tate_l, '{}{}'.format(dc[0], dc[2]), km)
            if 'ー' not in dc[1]:
                if mark_ends:
                    tate_r = fill_gram_set(tate_r, '{}$'.format(dc[1]), km)
                else:
                    tate_r = fill_gram_set(tate_r, '{}'.format(dc[1]), km)
        elif len(dc) == 4:  # 例：㌀
            if mark_ends:
                yoko_t = fill_gram_set(yoko_t, '${}{}'.format(dc[0], dc[1]), km)
                yoko_t = fill_gram_set(yoko_t, '{}{}$'.format(dc[0], dc[1]), km)
                yoko_t = fill_gram_set(yoko_t, '{}{}'.format(dc[0], dc[1]), km)
                yoko_b = fill_gram_set(yoko_b, '${}{}'.format(dc[2], dc[3]), km)
                yoko_b = fill_gram_set(yoko_b, '{}{}$'.format(dc[2], dc[3]), km)
                yoko_b = fill_gram_set(yoko_b, '{}{}'.format(dc[2], dc[3]), km)
            else:
                yoko_t = fill_gram_set(yoko_t, '{}{}'.format(dc[0], dc[1]), km)
                yoko_b = fill_gram_set(yoko_b, '{}{}'.format(dc[2], dc[3]), km)
            if 'ー' not in dc[0]+dc[2]:
                if mark_ends:
                    tate_l = fill_gram_set(tate_l, '${}{}'.format(dc[0], dc[2]), km)
                    tate_l = fill_gram_set(tate_l, '{}{}$'.format(dc[0], dc[2]), km)
                    tate_l = fill_gram_set(tate_l, '{}{}'.format(dc[0], dc[2]), km)
                else:
                    tate_l = fill_gram_set(tate_l, '{}{}'.format(dc[0], dc[2]), km)
            if 'ー' not in dc[1]+dc[3]:
                if mark_ends:
                    tate_r = fill_gram_set(tate_r, '${}{}'.format(dc[1], dc[3]), km)
                    tate_r = fill_gram_set(tate_r, '{}{}$'.format(dc[1], dc[3]), km)
                    tate_r = fill_gram_set(tate_r, '{}{}'.format(dc[1], dc[3]), km)
                else:
                    tate_r = fill_gram_set(tate_r, '{}{}'.format(dc[1], dc[3]), km)

    return [yoko_t, yoko_b, tate_r, tate_l]

def composable(word_kat, word_norm, grams, used, rest):
    if rest == '':
        components = [grams['map'][g] for g in used]
        if '縦' in grams['label']:
            msg = '{} ⬎'.format(word_norm)
            for c in components:
                msg += '\n{} {}'.format('　'*len(word_norm), c)
        else:
            msg = '{} → {}'.format(word_norm, ''.join(components))
        print(msg)
    if rest == False:
        rest = word_kat
    if rest[0:4] in grams['list']:
        used.append(rest[0:4])
        composable(word_kat, word_norm, grams, used, rest[4:])
    elif rest[0:3] in grams['list']:
        used.append(rest[0:3])
        composable(word_kat, word_norm, grams, used, rest[3:])
    elif rest[0:2] in grams['list']:
        used.append(rest[0:2])
        composable(word_kat, word_norm, grams, used, rest[2:])
    elif rest[0:1] in grams['list']:
        used.append(rest[0:1])
        composable(word_kat, word_norm, grams, used, rest[1:])

STRICT = False
SUPER_STRICT = False

spkm = get_square_pattern_kumimoji()
sets = build_ngram_sets(spkm, STRICT, SUPER_STRICT)

if len(sys.argv) < 2:
    with open('freqlist.tsv') as f:
        words = f.readlines()
elif len(sys.argv) == 2:
    words = sys.argv[1].split(',')
else:
    sys.exit(1)

words = [w.strip() for w in words if len(w.strip())]

for aset in sets:
    print('- - - - - - - - - - - - - - - - - - -')
    print('- - - - - - -{}- - - - - - -'.format(aset['label']))
    print('- - - - - - - - - - - - - - - - - - -')
    for w in words:
        parts = w.split('\t')
        if len(parts) == 2:
            kat = parts[0]
            norm = parts[1]
        else:
            kat = parts[0]
            norm = parts[0]
        composable(kat, norm, aset, [], False)
