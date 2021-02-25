#GoogleGeeks
#Sagnik Ghosh

from types import SimpleNamespace
def reader(fname):
    streetsname = {}
    vehicle = []
    information = {}
    with open(fname) as f:
        line = f.readline()
        # line 1
        # D(uration of simulation) I(intersections) S(treets) V(num vehicle) F(bonus points)
        information['D'], information['I'], information['S'], information['V'], information['F'] = [int(i) for i in line.split()]

        # next S lines (descriptions of streetsname)
        # B(egin of street) E(nd of street) string(name) L(time to traverse)
        for _ in range(information['S']):
            line = f.readline()
            B, E, name, L = line.split()
            streetsname[name] = Street(int(B), int(E), int(L), name)

        # next V lines (paths of vehicle)
        #  P(num of streetsname to travel) P*string(road names)
        for _ in range(information['V']):
            line = f.readline()
            vehicle.append(Car(line.split()[1:]))

    return streetsname, vehicle, information

# intersection is a collection of streetsname


def writer(intersections, fname='out.txt'):
    with open(fname, 'w') as f:
        f.write(f'{str(len(intersections))}\n')
        for i in intersections.values():
            f.write(i.output() + '\n')


class Intersection():
    """
    Takes a list of in and out streetsname
    """

    def __init__(self, in_streetsname, ID):
        """
        in_streetsname list(obj(Street))
        stack list(vehicle)
        """
        self.in_streetsname = in_streetsname
        self.ID = ID
        self.now = 0
        self.schedule = self.simple_schedule()
        self._sched_loc = 0

    def turn_green(self, target_street, time):
        target_street.traffic_green = True

    def simple_schedule(self):
        return [(1, street) for street in self.in_streetsname]

    def update_time(self):
        """
        Updates internal timer, handles schedule
        """
        if self.now == self.schedule[self._sched_loc][0]:
            self.schedule[self._sched_loc][1].traffic_green = False
            self._sched_loc = (self._sched_loc + 1) % len(self.schedule)
            self.schedule[self._sched_loc][1].traffic_green = True
            self.now = 0
        self.now += 1

    def output(self):
        output = [str(self.ID), str(len(self.in_streetsname))]
        for duration, street in self.schedule:
            output.append(f'{str(street.name)} {str(duration)}')
        output = "\n".join(output)
        return output


class Street:
    def __init__(self, begin, end, duration, name):
        self.begin = begin
        self.end = end
        self.duration = duration
        self.driving = []
        self.waiting = []  # vehicle at the intersection
        self.now = 0
        self.name = name
        self.traffic_green = False

    def add_car(self, car):
        """
        Add a car to the driving list with a delay.
        """
        car.route.pop(0)  # Remove first street in vehicle route
        self.driving.append([self.duration + self.now, car])

    def update_time(self):
        """
        Tick 1 second.

        Returns:
         - Next car through the lights!
        """
        skip = 0
        for i, d in enumerate(self.driving):
            if d[0] == self.now:
                self.waiting.append(d[1])
            else:
                skip = i
        self.driving = self.driving[skip:]

        if self.traffic_green and self.waiting:
            return self.waiting.pop(0)
        self.now += 1

        return None


class Car:
    def __init__(self, route):
        """
        route list(string)
        """
        self.route = route


def get_intersections(streetsname):
    intersections = {}
    for street in streetsname.values():
        if street.end not in intersections:
            intersections[street.end] = Intersection([street], street.end)
        else:
            intersections[street.end].in_streetsname.append(street)
    for intersection in intersections.values():
        intersection.schedule = intersection.simple_schedule()
    return intersections


def run_simulation(fname):
    streetsname, vehicle, information = reader(fname)
    score = 0
    now = 0
    intersections = get_intersections(streetsname)
    # Puts vehicle into start positions
    for car in vehicle:
        streetsname[car.route[0]].add_car(car)

    for T in range(information['D']):

        moved_vehicle = []
        #
        for intersection in intersections.values():
            intersection.update_time()
        for street in streetsname.values():
            next_car = street.update_time()
            if next_car is not None:
                moved_vehicle.append(next_car)
        for car in moved_vehicle:
            if len(car.route) == 0:
                score += information['F'] + (information['D'] - T)
            else:
                streetsname[car.route[0]].add_car(car)

    return score


def generate_output(fname):
    streetsname, vehicle, information = reader(fname)
    score = 0
    now = 0
    intersections = get_intersections(streetsname)
    writer(intersections, fname+'.out')


if __name__ == "__main__":
    # generate_output('a.txt')
    # generate_output('b.txt')
    # generate_output('c.txt')
    # generate_output('d.txt')
    # generate_output('e.txt')
    # generate_output('f.txt')
    run_simulation('a.txt')