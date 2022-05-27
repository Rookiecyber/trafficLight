import orm


def addUser(db, username):
    user = orm.User(name=username)
    db.add(user)
    db.commit()


def updateUser(db, id, username):
    user = orm.User.findById(db, id)
    user.name = username
    db.commit()


def deleteUser(db, id):
    user = orm.User.findById(db, id)
    db.delete(user)
    db.commit()


def findUserList(db):
    users = db.query(orm.User).all()
    return users


def addCar(db, direction, flow, time):
    car = orm.Car(direction=direction, flow=flow, time=time)
    db.add(car)
    db.commit()


def updateCar(db, id, direction, flow, time):
    car = orm.Car.findById(db, id)
    car.direction = direction
    car.flow = flow
    car.time = time
    db.commit()


def deleteCar(db, id):
    car = orm.Car.findById(db, id)
    db.delete(car)
    db.commit()


def findFlowList(db):
    flows = db.query(orm.Car).all()
    return flows


# 可信度知识
def addKL(db, E, H, CFE, CFHE):
    kl = orm.Knowledge(E=E, H=H, CFE=CFE, CFHE=CFHE)
    db.add(kl)
    db.commit()


def updateKL(db, id, E, H, CFE, CFHE):
    kl = orm.Knowledge.findByID(db, id)
    kl.E = E
    kl.H = H
    kl.CFE = CFE
    kl.CFHE = CFHE
    db.commit()


def deleteKL(db, id):
    # rule = orm.Knowledge.findById(db,id)
    r = orm.Knowledge.findByID(db, id)
    db.delete(r)
    db.commit()


def findKLList(db):
    KLS = db.query(orm.Knowledge).all()
    return KLS


def insertFuzzy(db, name, map_input_2_membership_vec, matrix_r):
    # rule = orm.Knowledge.findById(db,id)
    obj = orm.Fuzzy(name=name, map_input_2_membership_vec=map_input_2_membership_vec, matrix_r=matrix_r)
    db.add(obj)
    db.commit()


def getFuzzy(db):
    items = db.query(orm.Fuzzy).all()
    import json
    for i in range(len(items)):
        items[i].map_input_2_membership_vec = json.dumps(
            json.loads(items[i].map_input_2_membership_vec),
            sort_keys=True, indent=4, separators=(',', ': ')
        )
        items[i].matrix_r = json.dumps(
            json.loads(items[i].matrix_r),
            sort_keys=True, indent=4, separators=(',', ': ')
        )
    return items


def getWeather(db):
    item = db.query(orm.Weather).all()
    for i in range(len(item)):
        return item[i]


def setWeather(db, id, rain, snow, wind):
    wea = orm.Weather.get(db, id)
    wea.rain = rain
    wea.snow = snow
    wea.wind = wind
    db.commit()


def insertResult(db, name,
                weather_rain, weather_snow, weather_wind,
                 base_pass_time, public_time, car_numbers, public_allocated_times, weather_add_times, final_results, time):
    import json

    obj = orm.Result(
        name=name,
        base_pass_time=base_pass_time,
        public_time=public_time,
        weather_rain=weather_rain,
        weather_snow=weather_snow,
        weather_wind=weather_wind,
        car_numbers=json.dumps(car_numbers),
        public_allocated_times=json.dumps(public_allocated_times),
        weather_add_times=json.dumps(weather_add_times),
        final_results=json.dumps(final_results),
        time=time,
    )

    db.add(obj)
    db.commit()


def listResults(db):
    return db.query(orm.Result).all()
