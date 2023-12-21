# day20.py 2023
import unittest

from queue import Queue
import random
import networkx as nx


class Gate(object):
    gates: dict[str:"Gate"]
    runq: Queue[str]
    # broadcast: list[str]
    broadcaster: "Broadcaster"
    count: list[int, int]
    G: nx.DiGraph
    # statecount: dict[int : tuple[int, int, int]]
    # done: str | None

    @classmethod
    def _parse(cls, lines: list[str]):
        cls.runq = Queue()
        cls.gates = {}
        cls.count = [0, 0]
        # cls.totalcount = [0, 0]
        # cls.states = []
        # cls.statecount = {}
        cls.G = nx.DiGraph()

        # , [s.strip() for s in sinks.split(",")]
        # , [s.strip() for s in sinks.split(",")]
        # [s.strip() for s in line.strip()[15:].split(",")]
        for line in lines:
            if line[0] == "%":
                source = line.strip().split("->")[0]
                name = source[1:].strip()
                cls.gates[name] = FlipFlop(name)
            elif line[0] == "&":
                source, sinks = line.strip().split("->")
                name = source[1:].strip()
                cls.gates[name] = Inverter(name)
            elif line.startswith("broadcaster"):
                cls.broadcaster = Broadcaster()
                cls.gates["broadcaster"] = cls.broadcaster

        cls.gates["output"] = Gate("output")
        cls.gates["rx"] = Gate("rx")

        gate, dest = None, None
        for line in lines:
            if line.startswith("broadcaster"):
                gate = cls.gates["broadcaster"]
                dest = [cls.gates[s.strip()] for s in line.strip()[15:].split(",")]
            else:
                source, sinks = line.strip().split("->")
                gate = cls.gates[source[1:].strip()]
                dest = [cls.gates[s.strip()] for s in sinks.split(",")]

            # elif line[0] == "&":
            #     source, sinks = line.strip().split("->")
            #     name = source[1:].strip()
            #     cls.gates[name].add_outputs(
            #         [cls.gates[s.strip()] for s in sinks.split(",")]
            #     )
            # elif line.startswith("broadcaster"):
            #     cls.gates["broadcaster"].add_outputs(
            #         [cls.gates[s.strip()] for s in line.strip()[15:].split(",")]
            #     )
            gate.add_outputs(dest)
            # print("adding", dest)
            for g in dest:
                g.add_input(gate)

        # for ff in [gate for gate in cls.gates.values() if isinstance(gate, FlipFlop)]:
        #     # print("found", ff)
        #     for inv in [
        #         cls.gates[gate]
        #         for gate in ff.outputs
        #         if isinstance(cls.gates[gate], Inverter)
        #     ]:
        #         # print("connecting", ff, inv)
        #         inv.add_input(ff.name)

    @classmethod
    def load(cls, lines: list[str]):
        cls._parse(lines)
        cls.gates["rx"] = Gate("rx", [])

    @classmethod
    def push2(cls, lines: list[str]):
        cls._parse(lines)
        # cls.gates["rx"] = Gate("rx", [])
        last_ft = None
        pulse = 0
        while True:
            pulse += 1

            for name in cls.broadcast:
                cls.gates[name].pulse(cls.broadcaster, 0)
            while not cls.runq.empty():
                gate = cls.runq.get()
                if gate.run():
                    return pulse
            # if cls.gates["ft"].invalue() != last_ft:
            #     last_ft = cls.gates["ft"].invalue()
            #     print(pulse, cls.gates["ft"])

    @classmethod
    def push(cls, lines: list[str], pulses: int):
        cls._parse(lines)
        # print(cls.gates["inv"], cls.gates["inv"].outputs)
        for pulse in range(pulses):
            # button push
            cls.count[0] += 1
            # for name in cls.broadcaster.outputs:
            #     cls.gates[name].pulse("broadcast", 0)
            cls.broadcaster.run()
            # print(cls.count)
            while not cls.runq.empty():
                gate = cls.runq.get()
                # print(gate)
                gate.run()
            # print(cls.count)
            # state = 0
            # for gate in cls.gates.values():
            #     if isinstance(gate, FlipFlop):
            #         state = (state << 1) + gate.value
            # # print(cls.count, state)
            # if state in cls.statecount:
            #     # print("DUP!", cls.states.index(state), len(cls.states), pulse)
            #     # start_of_loop = cls.states.index(state)

            # #     start_of_loop = cls.statecount[state][0]
            # #     loop_size = pulse - start_of_loop
            # #     to_run = pulses - start_of_loop
            # #     loop_runs = to_run // loop_size
            # #     leftover = to_run % loop_size
            # #     # offset = to_run % loop_size

            # #     cls.count = [0, 0]
            # #     for state, (pulse, lows, highs) in cls.statecount.items():
            # #         mult = 0
            # #         if pulse < start_of_loop:
            # #             mult = 1
            # #         else:
            # #             mult = loop_runs
            # #             if pulse < start_of_loop + leftover:
            # #                 mult += 1
            # #         cls.count[0] += lows * mult
            # #         cls.count[1] += highs * mult
            # #     return cls.count[0] * cls.count[1]
            # # else:
            # #     cls.statecount[state] = (pulse, cls.count[0], cls.count[1])
            # #     cls.totalcount[0] += cls.count[0]
            # #     cls.totalcount[1] += cls.count[1]
            # #     cls.count = [0, 0]

        # return cls.totalcount[0] * cls.totalcount[1]
        # print(cls.count)
        return cls.count[0] * cls.count[1]

    def __init__(self, name: str):
        self.name = name
        self.outputs: list["Gate"] = []
        self.gates[name] = self
        self.last_pulse = None
        self.pulse_count = 0
        self.debug = False
        self.color = "blue"

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def add_input(self, source: "Gate"):
        pass
        # print(self, "<-", source)

    def add_output(self, other: "Gate"):
        # print(self, "->", other)
        self.outputs.append(other)

    def add_outputs(self, others: list["Gate"]):
        # for other in others:
        #     print(self, "->", other)
        self.outputs += others

    def pulse(self, source: "Gate", p: int, push: bool = True):
        # print(self.name, p)
        self.count[p] += 1
        self.pulse_count += 1
        if push:
            self.runq.put(self)
        self.last_pulse = p

    def run(self) -> bool:
        # print(self.pulse_count, self.last_pulse)
        return self.last_pulse == 0


class Broadcaster(Gate):
    def __init__(self):
        super().__init__("Broadcaster")
        self.color = "orange"

    def run(self) -> bool:
        for gate in self.outputs:
            gate.pulse(self, 0)
        return False

    def pulse(self, source: Gate, p: int):
        raise TypeError("Brodcaster cannot be pulsed")


class FlipFlop(Gate):
    def __init__(self, name: str):
        super().__init__(name)
        self.pulses: Queue[int] = Queue()
        self.value = 0
        self.color = "red"

    def __repr__(self):
        return f"FF {self.name}:{self.value}"
        # return f"%{self.name}"

    def pulse(self, source: Gate, p: int):
        super().pulse(source, p, p == 0)
        if p == 0:
            self.pulses.put(p)

    def run(self) -> bool:
        if not self.pulses.empty():
            p = self.pulses.get()
            if p == 0:
                self.value = (1, 0)[self.value]
                for sink in self.outputs:
                    sink.pulse(self, self.value)
        return False


class Inverter(Gate):
    def __init__(self, name: str):
        super().__init__(name)
        self.inputs = {}
        self.value = 0
        self.color = "green"

    def __repr__(self):
        # return f"&{self.name}"
        return f"Inv {self.invalue()}=>{self.value}"
        # return f"Inv {self.inputs} {self.value}"

    def invalue(self) -> str:
        return "".join([str(v) for v in self.inputs.values()])

    def add_input(self, source: Gate):
        super().add_input(source)
        self.inputs[source] = 0

    def pulse(self, source: Gate, p: int):
        # if isinstance(source, str):
        #     raise TypeError
        # print("PULSE", self, source)
        super().pulse(source, p)
        self.inputs[source] = p

    def run(self) -> bool:
        self.value = 0 if all(self.inputs.values()) else 1
        # print("Run", self, self.inputs, self.inputs.values(), self.value)
        for sink in self.outputs:
            sink.pulse(self, self.value)
        return False


def part1(lines: list[str]) -> int:
    return Gate.push(lines, 1000)


def part2(lines: list[str]) -> int:
    return Gate.push2(lines)


class TestDay20(unittest.TestCase):
    def test_1a(self):
        with open("./test20.txt", "r") as f:
            self.assertEqual(part1(list(f)), 32000000)

    def test_1b(self):
        with open("./test20b.txt", "r") as f:
            self.assertEqual(part1(list(f)), 11687500)

    def test_1(self):
        with open("./input20.txt", "r") as f:
            self.assertEqual(part1(list(f)), 737679780)

    # def test_all(self):
    #     #  self.value = 0 if all(self.inputs.values()) else 1
    #     size = 48
    #     for _ in range(10000):
    #         r = [random.randint(0, 1) for _ in range(size - 1)] + [0]
    #         self.assertFalse(all(r))

    # def test_ones(self):
    #     size = 48
    #     for _ in range(1000000):
    #         r = [1] * size
    #         self.assertTrue(all(r))

    # ones = [1] * size

    # def test_sum(self):
    #     size = 48
    #     for _ in range(1000000):
    #         r = [1] * size
    #         self.assertEqual(sum(r), size)

    # def test_2a(self):
    #     with open('./test20.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)

    # def test_2(self):
    #     with open("./input20.txt", "r") as f:
    #         self.assertEqual(part2(list(f)), None)  # 737679780 too low


if __name__ == "__main__":
    unittest.main()
