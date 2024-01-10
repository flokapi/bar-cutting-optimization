

import copy


def _make_possibility_tree(target, remaining_lenth):
    poss_tree = {}
    for length in target.keys():
        if target[length] > 0:
            if length <= remaining_lenth:
                new_target = copy.deepcopy(target)
                new_target[length] -= 1
                new_remaining_length = remaining_lenth - length
                poss_tree[length] = _make_possibility_tree(
                    new_target, new_remaining_length)
    return poss_tree


def _make_possibility_list(poss):
    def build(lst, path, poss):
        if not poss.keys():
            lst.append(path)
        else:
            for key in poss.keys():
                build(lst, path+[key], poss[key])

    lst = []
    build(lst, [], poss)
    return lst


def _find_best(poss_list):
    best = None
    for poss in poss_list:
        if best:
            if sum(poss) > sum(best):
                best = poss
            if sum(poss) == sum(best) and max(poss) > max(best):
                best = poss
        else:
            best = poss
    return sorted(best, reverse=True)


def _update_target(target, poss):
    for elem in poss:
        target[elem] -= 1


def _dict_result(bars):
    result = {}
    bars = [[str(elem) for elem in bar] for bar in bars]
    bars = [' + '.join(bar) for bar in bars]

    for bar in bars:
        if bar in result:
            result[bar] += 1
        else:
            result[bar] = 1
    return result


def calc_result(bar_length, target):
    if any([l > bar_length for l in target.keys()]):
        return 'Bar Length too small'

    bars = []

    while any(target.values()):
        poss_tree = _make_possibility_tree(target, bar_length)
        poss_list = _make_possibility_list(poss_tree)
        best = _find_best(poss_list)
        _update_target(target, best)
        bars.append(best)

    return _dict_result(bars)


if __name__ == '__main__':
    bar_length = 12

    target = {
        3: 5,
        5: 4,
        7: 5
    }

    bars = calc_result(bar_length, target)

    print(bars)
