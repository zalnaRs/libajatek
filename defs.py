import random as r

def count(adat:list|str, elem) -> int:
    c = 0
    for e in adat:
        if e == elem:
            c += 1

    return(c)


def generate_drotok() -> list[tuple[int, bool]]:
    ures = [0, 0, 0]
    ures[0] += r.randint(0,4)
    ures[1] += r.randint(ures[0]+1,5)

    drotok = []
    c = 0
    for i in range(6):
        if ures[c] != i:
            while True:
                rand_num = r.randint(0,3)
                if count(drotok, [rand_num, False]) < 2:
                    drotok.append([rand_num, False])
                    break

        else:
            drotok.append(None)
            c += 1

    return(drotok)


def password() -> tuple[str, list[list[str]]]:
    words = ['libák', 'szent', 'lámpa', 'hálás', 'pince', 'újbor', 'vihar', 'bunda', 'kabát', 'deres', 'fehér', 'keres', 'talál', 'erény', 'áldás', 'gágog', 'tojás', 'arany', 'óriás', 'fióka']
    letter = [['l', 's', 'h', 'p', 'ú', 'v', 'b', 'k', 'd', 'f', 't', 'e', 'á', 'g', 'a', 'ó'], #1
    ['i', 'z', 'á', 'j', 'u', 'a', 'e', 'r', 'l', 'o'],                                         #2
    ['b', 'e', 'm', 'l', 'n', 'h', 'r', 'é', 'd', 'g', 'j', 'a', 'i', 'ó'],                     #3
    ['á', 'n', 'p', 'c', 'o', 'a', 'd', 'e', 'é', 'k'],                                         #4
    ['k', 't', 'a', 's', 'e', 'r', 'l', 'y', 'g']                                               #5
    ]
    p_pair = ['lb', 'se', 'lm', 'hl', 'pn', 'úb', 'vh', 'bn', 'kb', 'dr', 'fh', 'kr', 'tl', 'eé', 'ád', 'gg', 'tj', 'aa', 'ói', 'fó']
    #első és harmadik karakter összetétele különböző mindegyik szónál

    p_word = r.randint(0, len(words)-1)
    matrix = []
    p_black_list = []

    p_row = []
    while len(p_row) < 5:
        rand = r.randint(0,3)
        if count(p_row, rand) < 3:
            p_row.append(rand)


    while True:
        for i in range(5):
            matrix.append([])

            have_it = [words[p_word][i]]

            for j in range(4):
                if j == p_row[i]:
                    matrix[i].append(words[p_word][i])       

                else:
                    l = 0
                    while l < 100:
                        index = r.randint(0,len(letter[i])-1)
                        if letter[i][index] not in have_it:
                            if i == 2:
                                if letter[i][index] not in p_black_list:
                                    matrix[i].append(letter[i][index])
                                    have_it.append(letter[i][index])
                                    break

                            else:
                                if i == 0:
                                    for e in p_pair:
                                        if e[0] == letter[i][index]:
                                            p_black_list.append(e[1])
                                            print(p_black_list)
                                
                                matrix[i].append(letter[i][index])
                                have_it.append(letter[i][index])
                                break

                        l += 1

                    if l == 100:
                        break

            if l == 100:
                break

        if l != 100:
            break

    return (words[p_word], matrix)


#8 karakter a szériaszám ebböl 4 szám 4 betű
def szerianumber(spec:bool) -> str:
    sz_n = ""
    letters = ["s", "o", "x", "h", "a", "i", "d", "z", "t", "l"]
    spec_chart = ["+", "<", "@", "&", "#", "$"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if spec:
        s_num = r.randint(0,3)

    n_index = []
    while len(n_index) < 4:
        rand_n = r.randint(0,7)
        if rand_n not in n_index:
            n_index.append(rand_n)

    digital_root = []
    i = 0
    while len(sz_n) < 8:
        r_num = r.randint(0,9)

        if i in n_index:
            if i != 0 or r_num != 0:
                sz_n += numbers[r_num]
                digital_root.append(int(numbers[r_num]))
                i += 1

        elif count(sz_n, letters[r_num]) < 3:
            if spec:
                if s_num != 0:
                    s_num -= 1
                    sz_n += letters[r_num]

                else:
                    sz_n += spec_chart[r.randint(0, len(spec_chart))-1]
                    spec = False

                i += 1

            else:
                sz_n += letters[r_num]
                i += 1

    while len(digital_root) > 1:
        s = 0
        for e in digital_root:
            s += e

        digital_root = []
        s = str(s)
        for e in s:
            digital_root.append(int(e))

    return sz_n, digital_root[0]