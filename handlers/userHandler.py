import tornado.web
import tornado.ioloop
import json
import orm
import dbUtil

global db


class UserHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        db = self.settings['db']
        dic = {"status": True, "message": ""}
        type = self.get_argument("type")
        if type == 'add':
            username = self.get_argument("username")
            print(username)
            dbUtil.addUser(db, username)
        elif type == 'edit':
            id = self.get_argument("id")
            username = self.get_argument("username")
            print(username)
            dbUtil.updateUser(db, id, username)
        elif type == 'delete':
            id = self.get_argument("id")
            dbUtil.deleteUser(db, id)

        self.write(json.dumps(dic))

    def get(self, *args, **kwargs):
        self.render("index.html")


class CarHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        db = self.settings['db']
        dic = {"status": True, "message": ""}
        type = self.get_argument("type")
        if type == 'add':
            direction = self.get_argument("direction")
            print(direction)
            flow = self.get_argument("flow")
            print(flow)
            time = self.get_argument("time")
            print(time)
            dbUtil.addCar(db, direction, flow, time)
        elif type == 'edit':
            id = self.get_argument("id")
            direction = self.get_argument("direction")
            print(direction)
            flow = self.get_argument("flow")
            print(flow)
            time = self.get_argument("time")
            print(time)
            dbUtil.updateCar(db, id, direction, flow, time)
        elif type == 'delete':
            id = self.get_argument("id")
            dbUtil.deleteCar(db, id)

        self.write(json.dumps(dic))

    def get(self, *args, **kwargs):
        self.render("index.html")


class KLHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        db = self.settings['db']
        dic = {"status": True, "message": ""}
        type = self.get_argument("type")
        if type == 'add':
            E = self.get_argument("E")
            print(E)
            H = self.get_argument("H")
            print(H)
            CFE = self.get_argument("CFE")
            print(CFE)
            CFHE = self.get_argument("CFHE")
            print(CFHE)
            dbUtil.addKL(db, E, H, CFE, CFHE)
        elif type == 'edit':
            id = self.get_argument("id")
            E = self.get_argument("E")
            print(E)
            H = self.get_argument("H")
            print(H)
            CFE = self.get_argument("CFE")
            print(CFE)
            CFHE = self.get_argument("CFHE")
            print(CFHE)
            dbUtil.updateKL(db, id, E, H, CFE, CFHE)
        elif type == 'delete':
            id = self.get_argument("id")
            dbUtil.deleteKL(db, id)

        self.write(json.dumps(dic))

    def get(self, *args, **kwargs):
        self.render("index.html")


class Result:
    def __init__(self, error, data):
        self.__error = error
        self.__data = data

    def data(self):
        return self.__data

    def error(self):
        return self.__error


def compute_fuzzy(input_var2vec, output_var2vec, input_var2output_var):
    """
        example:
            input_var2vec: '{
                "small":    [0.8, 0.2, 0, 0],
                "mid":      [0, 0.5, 0.5, 0],
                "large":    [0, 0, 0.2, 0.8]
            }'
            output_var2vec: '{
                "small":    [0.8, 0.2, 0, 0],
                "mid":      [0, 0.5, 0.5, 0],
                "large":    [0, 0, 0.2, 0.8]
            }'
            input_var2output_var: '{
                "small": "small",
                "mid": "mid",
                "large": "large"
            }'
        example_output:
            [
                [0.8, 0.2, 0, 0],
                [0.2, 0.5, 0.5, 0],
                [0, 0.5, 0.5, 0.2],
                [0, 0, 0.2, 0.8]
            ]
    """

    input2vec_obj = json.loads(input_var2vec)
    output2vec_obj = json.loads(output_var2vec)
    input2output_obj = json.loads(input_var2output_var)

    # compute matrix by input_var2output_var.
    relation_matrix_list = []
    for input_var_name in input2output_obj:
        output_var_name = input2output_obj[input_var_name]

        if input2vec_obj.get(input_var_name) is None:
            return Result(True, "input key not found " + input_var_name)
        if output2vec_obj.get(output_var_name) is None:
            return Result(True, "output key not found " + output_var_name)

        get_matrix_result = do_and_op_on_vec(
            input2vec_obj[input_var_name],
            output2vec_obj[output_var_name]
        )

        if get_matrix_result.error():
            return get_matrix_result

        relation_matrix_list.append(get_matrix_result.data())

    return composite_matrix(relation_matrix_list)


def do_and_op_on_vec(vec_a, vec_b):
    """
        example:
            vec_a: [0.8, 0.2, 0, 0]
            vec_b: [0.8, 0.2, 0, 0]
        result:
            (vec_a x vec_b^T) => [
                [0.8, 0.8, 0, 0],
                [0.8, 0.2, 0, 0],
                [0  , 0  , 0, 0]
                [0  , 0  , 0, 0]
            ]
    """

    # check vec size
    if len(vec_a) != len(vec_b):
        return Result(True, "vector size not equal")

    vec_size = len(vec_a)

    return Result(False, [[min(vec_a[i], vec_b[j]) for j in range(vec_size)] for i in range(vec_size)])


def composite_matrix(matrix_list):
    """
        example:
            matrix_list:
            [
                [
                    [0.8, 0.8, 0, 0],
                    [0.8, 0.2, 0, 0],
                    [0  , 0  , 0, 0]
                    [0  , 0  , 0, 0]
                ],
                [
                    [0 , 0  , 0  , 0],
                    [0 , 0.5, 0.5, 0],
                    [0 , 0.5, 0.5, 0]
                    [0 , 0  , 0  , 0]
                ],
            ]
        return: [
            [0.8, 0.8, 0  , 0],
            [0.8, 0.5, 0.5, 0],
            [0  , 0.5, 0.5, 0]
            [0  , 0  , 0  , 0]
        ]
    """

    print("composite ", matrix_list)

    shape = [len(matrix_list[0]), len(matrix_list[0][0])]

    ret_matrix = [[0 for j in range(shape[1])] for i in range(shape[0])]

    for i in range(shape[0]):
        for j in range(shape[1]):
            max_value_of = []
            for find_max_matrix in matrix_list:
                max_value_of.append(find_max_matrix[i][j])

            ret_matrix[i][j] = max(max_value_of)

    return Result(False, ret_matrix)


class FuzzyHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        db = self.settings['db']
        dic = {"status": True, "message": ""}

        # compute and insert fuzzy info into db.
        get_r_matrix_result = compute_fuzzy(
            self.get_argument("create_fuzzy_input_var_desc"),
            self.get_argument("create_fuzzy_output_var_desc"),
            self.get_argument("create_fuzzy_input_output_relation")
        )

        if get_r_matrix_result.error():
            self.write(json.dumps({
                "error": get_r_matrix_result.error(),
                "data": get_r_matrix_result.data()
            }))
            return

        # save result into db.
        dbUtil.insertFuzzy(
            db=db,
            name=self.get_argument("create_fuzzy_name"),
            map_input_2_membership_vec=self.get_argument("create_fuzzy_input_var_desc"),
            matrix_r=json.dumps(get_r_matrix_result.data()),
        )

        # write back result.
        self.write(json.dumps(dic))

    def get(self, *args, **kwargs):
        self.render("index.html")


class WeatherHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        db = self.settings['db']
        dic = {"status": True, "message": ""}

        # compute and insert fuzzy info into db.
        rain = self.get_argument("rain")
        snow = self.get_argument("snow")
        wind = self.get_argument("wind")

        # save result into db.
        dbUtil.setWeather(
            db=db,
            id=1,
            rain=rain,
            snow=snow,
            wind=wind
        )

        # write back result.
        self.write(json.dumps(dic))

    def get(self, *args, **kwargs):
        self.render("index.html")


class ResultHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


default_handlers = [
    (r"/user", UserHandler),
    (r"/car", CarHandler),
    (r"/rule", KLHandler),
    (r"/fuzzy", FuzzyHandler),
    (r"/weather", WeatherHandler),
]

if __name__ == "__main__":
    input_var2vec = {
        "small": [0.8, 0.2, 0, 0],
        "mid": [0, 0.5, 0.5, 0],
        "large": [0, 0, 0.2, 0.8]
    }
    output_var2vec = {
        "small": [0.8, 0.2, 0, 0],
        "mid": [0, 0.5, 0.5, 0],
        "large": [0, 0, 0.2, 0.8]
    }
    input_var2output_var = {
        "small": "small",
        "mid": "mid",
        "large": "large"
    }

    r_matrix = compute_fuzzy(json.dumps(input_var2vec), json.dumps(output_var2vec), json.dumps(input_var2output_var))
    print(r_matrix)
