import json


def compute_fuzzy_result(input_membership_vec, matrix_r):
    """
    compute fuzzy result of fuzzy reasoning.
    example:
        input_membership_vec: [0.8, 0.2, 0, 0]
        matrix_r: [
            [0.8, 0.2, 0, 0],
            [0.2, 0.5, 0.5, 0],
            [0, 0.5, 0.5, 0.2],
            [0, 0, 0.2, 0.8]
        ]

        return: 0.2 = 0.8 * 0 + 0.2 * 1 + 0 * 2 + 0 * 3
    """

    res = 0

    for inx_vec, val_vec in enumerate(input_membership_vec):
        min_result = [min(val_vec, row[inx_vec]) for row in matrix_r]
        res += inx_vec * max(min_result)

    return res


class Fuzzy:
    def __init__(self, map_input_2_membership_vec, matrix_r):
        """
            init create a fuzzy object from orm.Fuzzy items
        """
        self.__input2vec = json.loads(map_input_2_membership_vec)
        self.__r = json.loads(matrix_r)

    def get_result_by_input(self, in_name):
        """
        get fuzzy result by input name.
        example:
            :in_name: "small"
            :return: 0.2
        """

        if self.__input2vec.get(in_name) is None:
            raise "input name not found in map_input_2_membership_vec"

        return compute_fuzzy_result(self.__input2vec[in_name], self.__r)


def get_default_fuzzy():
    return Fuzzy(
        """
        {
            "small": [0.6, 0.4, 0, 0],
            "mid": [0, 0.5, 0.5, 0],
            "large": [0, 0, 0.4, 0.6]
        }
        """
        ,
        """
        [
            [0.6, 0.4, 0, 0],
            [0.4, 0.5, 0.5, 0],
            [0, 0.5, 0.5, 0.4],
            [0, 0, 0.4, 0.6]
        ]
        """
        ,
    )


if __name__ == "__main__":
    fuzzy = Fuzzy(
        """
        {
            "small": [0.8, 0.2, 0, 0],
            "mid": [0, 0.5, 0.5, 0],
            "large": [0, 0, 0.2, 0.8]
        }
        """
        ,
        """
        [
            [0.8, 0.2, 0, 0],
            [0.2, 0.5, 0.5, 0],
            [0, 0.5, 0.5, 0.2],
            [0, 0, 0.2, 0.8]
        ]
        """
        ,
    )

    print(fuzzy.get_result_by_input("small"))
    print(fuzzy.get_result_by_input("mid"))
    print(fuzzy.get_result_by_input("large"))
