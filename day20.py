# day20.py 2023
import unittest

from queue import Queue
import networkx as nx


class Gate(object):
    gates: dict[str:"Gate"]
    runq: Queue[str]
    broadcaster: "Broadcaster"
    count: list[int, int]
    G: nx.DiGraph

    @classmethod
    def parse(cls, lines: list[str]):
        cls.gates = {}
        cls.runq = Queue()
        cls.broadcaster = None
        cls.count = [0, 0]
        cls.G = nx.DiGraph()

        for line in lines:
            if line[0] == "#":
                continue
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

        # cls.gates["output"] = Gate("output")
        # cls.gates["rx"] = Gate("rx")

        gate, destnames = None, None
        for line in lines:
            if line[0] == "#":
                continue
            if line.startswith("broadcaster"):
                gate = cls.gates["broadcaster"]
                # dest = [cls.gates[s.strip()] for s in line.strip()[15:].split(",")]
                destnames = [s.strip() for s in line.strip()[15:].split(",")]
            elif line[0] in "%&":
                source, sinks = line.strip().split("->")
                gate = cls.gates[source[1:].strip()]
                # dest = [cls.gates[s.strip()] for s in sinks.split(",")]
                destnames = [s.strip() for s in sinks.split(",")]
            else:
                continue

            # dest = [cls.gates[name] if name in cls.gates else ]

            for name in destnames:
                if name not in cls.gates:
                    cls.gates[name] = Gate(name)
            dest = [cls.gates[name] for name in destnames]
            for g in dest:
                g.add_input(gate)
            gate.add_outputs(dest)

            cls.G.add_node(gate)
            cls.G.add_edges_from(list(zip([gate] * len(gate.outputs), gate.outputs)))

    @classmethod
    def load(cls, file: str):
        cls.parse([line.strip() for line in open(file, "r")])

    @classmethod
    def printrx(cls):
        rx = cls.gates["rx"]
        roots = [rx]
        for i in range(6):
            next_roots = []
            for root in roots:
                print(f"{' '*(i*2)}{root} {list(root.inputs.keys())}")
                next_roots += root.inputs
            roots = next_roots

    @classmethod
    def printbd(cls):
        roots = [cls.broadcaster]
        for i in range(6):
            next_roots = []
            for k, root in enumerate(roots):
                print(f"{i}{' '*(i*2)}{k:2} {root} => ", end="")
                for r in root.outputs:
                    print(f"{r} ", end="")
                print()
                next_roots += root.outputs
            roots = next_roots

    @classmethod
    def push2(cls, lines: list[str]):
        cls.parse(lines)

        # cls.printbd()
        # for gate in cls.gates:
        #     print(gate)
        inv: Inverter = cls.gates["jz"]
        invstates: set[str] = set()
        pulse = 0
        while True:
            pulse += 1

            cls.broadcaster.run()
            while not cls.runq.empty():
                gate = cls.runq.get()
                if gate.run():
                    if gate.name == "rx":
                        return pulse
            v = inv.invalue()
            # if v == "1" * len(inv.inputs):
            #     print(pulse, v, len(invstates))
            if v not in invstates:
                invstates.add(v)
                print(pulse, v, len(invstates), len(v))

    @classmethod
    def push(cls, lines: list[str], pulses: int):
        cls.parse(lines)
        for pulse in range(pulses):
            # button push
            cls.count[0] += 1
            cls.broadcaster.run()
            while not cls.runq.empty():
                gate = cls.runq.get()
                gate.run()
            # print(pulse, cls.gates["nd"], cls.gates["nd"].invalue())
            # for name in ["vz"]:  # ["vz", "bq", "qh", "lt"]:
            #     inv: Inverter = cls.gates[name]
            #     if inv.invalue() == "1":
            #         print(pulse, inv)
            for name in ["vz"]:  # ["vz", "bq", "qh", "lt"]:
                inv: Inverter = cls.gates[name]
                if inv.changed:
                    print(pulse, inv, inv.invalue())

        return cls.count[0] * cls.count[1]

    @classmethod
    def related(cls, source: "Gate", nodes: set["Gate"] = None) -> list["Gate"]:
        if nodes is None:
            nodes = set([cls.broadcaster, cls.gates["ft"]])
        nodes.add(source)
        for g in source.outputs:
            if g not in nodes:
                cls.related(g, nodes)
        for g in source.inputs:
            if g not in nodes:
                cls.related(g, nodes)
        return nodes

    @classmethod
    def run_subset(cls, name):
        inv = cls.gates[name]
        nodes = cls.related(inv)

        for gate in nodes:
            gate.outputs = [g for g in gate.outputs if g in nodes]
            # gate.inputs = [g for g in gate.inputs if g in nodes]

        invstates: set[str] = set()
        pulse = 0
        while True:
            pulse += 1

            Gate.broadcaster.run()
            while not Gate.runq.empty():
                gate = Gate.runq.get()
                if gate.run():
                    if gate.name == "ft":
                        return pulse
            v = inv.invalue()
            # if v == "1" * len(inv.inputs):
            #     print(pulse, v, len(invstates))
            if v not in invstates:
                invstates.add(v)
            elif len(invstates) == (2 ** len(inv.inputs)) - 1:
                # print(inv, pulse, v, len(invstates), len(v))
                return pulse

    def __init__(self, name: str):
        self.name = name
        self.outputs: list["Gate"] = []
        self.gates[name] = self
        self.last_pulse = None
        self.pulse_count = 0
        self.debug = False
        self.color = "blue"
        self.inputs = {}

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def add_input(self, source: "Gate"):
        self.inputs[source] = 0
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
        super().__init__("broadcaster")
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

    # def __repr__(self):
    #     return self.name
    #     # return f"FF {self.name}:{self.value}"
    #     # return f"%{self.name}"

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
        self.value = 0
        self.color = "green"
        self.changed = False

    # def __repr__(self):
    #     return f"({self.name})"
    # return f"Inv {self.invalue()}=>{self.value}"
    # return f"Inv {self.inputs} {self.value}"

    def invalue(self) -> str:
        return "".join([str(v) for v in self.inputs.values()])

    # def add_input(self, source: Gate):
    #     super().add_input(source)
    #     self.inputs[source] = 0

    def pulse(self, source: Gate, p: int):
        # if isinstance(source, str):
        #     raise TypeError
        # print("PULSE", self, source)
        super().pulse(source, p)
        # if self.name == "FT" and self.inputs[source] != p:
        #     print(self, source, p)
        # delta = False
        # if self.name == "ft" and self.inputs[source] != p:
        #     delta = True
        # self.changed = len(self.inputs) > 0 and self.inputs[source] != p
        self.inputs[source] = p
        # if delta:
        #     print(source, self, self.invalue())

    def run(self) -> bool:
        self.value = 0 if all(self.inputs.values()) else 1
        # print("Run", self, self.inputs, self.inputs.values(), self.value)
        for sink in self.outputs:
            sink.pulse(self, self.value)
        return False


def part1(lines: list[str], pushes: int = 1000) -> int:
    return Gate.push(lines, pushes)


def part2(lines: list[str]) -> int:
    p = 1
    for name in ["jz", "sl", "pq", "rr"]:
        Gate.parse(lines)
        p *= Gate.run_subset(name)
    return p


class TestDay20(unittest.TestCase):
    # def test_1a(self):
    #     with open("./test20.txt", "r") as f:
    #         self.assertEqual(part1(list(f)), 32000000)

    # def test_1b(self):
    #     with open("./test20b.txt", "r") as f:
    #         self.assertEqual(part1(list(f)), 11687500)

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

    # def test_2b(self):
    #     with open("./input20b.txt", "r") as f:
    #         self.assertEqual(part2(list(f)), None)

    # def test_2c(self):
    #     with open("./input20.txt", "r") as f:
    #         self.assertEqual(part1(list(f), 100000), None)

    # def test_2(self):
    #     with open("./input20.txt", "r") as f:
    #         self.assertEqual(part2(list(f)), None)  # 737679780 too low

    def test_2(self):
        with open("./input20.txt", "r") as f:
            self.assertEqual(part2(list(f)), 227411378431763)  # 737679780 too low


if __name__ == "__main__":
    unittest.main()
