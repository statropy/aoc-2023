# day20.py 2023
import unittest

from queue import Queue


class Gate(object):
    gates: dict[str:"Gate"]
    runq: Queue[str]
    broadcast: list[str]
    count: list[int, int]
    statecount: dict[int : tuple[int, int, int]]
    done: str | None

    @classmethod
    def _parse(cls, lines: list[str]):
        cls.runq = Queue()
        cls.gates = {}
        cls.count = [0, 0]
        cls.totalcount = [0, 0]
        cls.states = []
        cls.statecount = {}

        for line in lines:
            if line[0] == "%":
                source, sinks = line.strip().split("->")
                name = source[1:].strip()
                cls.gates[name] = FlipFlop(name, [s.strip() for s in sinks.split(",")])
            elif line[0] == "&":
                source, sinks = line.strip().split("->")
                name = source[1:].strip()
                cls.gates[name] = Inverter(name, [s.strip() for s in sinks.split(",")])
            elif line.startswith("broadcaster"):
                cls.broadcast = [s.strip() for s in line.strip()[15:].split(",")]

        for ff in [gate for gate in cls.gates.values() if isinstance(gate, FlipFlop)]:
            # print("found", ff)
            for inv in [
                cls.gates[gate]
                for gate in ff.outputs
                if isinstance(cls.gates[gate], Inverter)
            ]:
                # print("connecting", ff, inv)
                inv.add_input(ff.name)

    @classmethod
    def push2(cls, lines: list[str]):
        cls._parse(lines)
        cls.gates["rx"] = Gate("rx", [])
        pulse = 1
        while True:
            # button push
            # cls.count[0] += 1
            for name in cls.broadcast:
                cls.gates[name].pulse("broadcast", 0)
            while not cls.runq.empty():
                name = cls.runq.get()
                if cls.gates[name].run():
                    return pulse
            pulse += 1

    @classmethod
    def push(cls, lines: list[str], pulses: int):
        cls._parse(lines)
        cls.gates["output"] = Gate("output", [])
        cls.gates["rx"] = Gate("rx", [])
        for pulse in range(pulses):
            # button push
            cls.count[0] += 1
            for name in cls.broadcast:
                cls.gates[name].pulse("broadcast", 0)
            while not cls.runq.empty():
                name = cls.runq.get()
                cls.gates[name].run()
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
        return cls.count[0] * cls.count[1]

    def __init__(self, name: str, outputs: list[str] = []):
        self.name = name
        self.outputs = outputs
        self.gates[name] = self
        self.last_pulse = None
        self.pulse_count = 0

    def add_input(self, source: str):
        pass

    def pulse(self, source: str, p: int, push: bool = True):
        # print(self.name, p)
        self.count[p] += 1
        self.pulse_count += 1
        if push:
            self.runq.put(self.name)
        self.last_pulse = p

    def run(self) -> bool:
        # print(self.pulse_count, self.last_pulse)
        return self.last_pulse == 0


class FlipFlop(Gate):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.pulses: Queue[int] = Queue()
        self.value = 0

    def __repr__(self):
        return f"FF {self.name}:{self.value}"

    def pulse(self, source: str, p: int):
        super().pulse(source, p, p == 0)
        if p == 0:
            self.pulses.put(p)

    def run(self) -> bool:
        if not self.pulses.empty():
            p = self.pulses.get()
            if p == 0:
                self.value = (1, 0)[self.value]
                for sink in self.outputs:
                    self.gates[sink].pulse(self.name, self.value)
        return False


class Inverter(Gate):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.inputs = {}
        self.value = 0

    def __repr__(self):
        return f"Inv {''.join([str(v) for v in self.inputs.values()])}=>{self.value}"
        # return f"Inv {self.inputs} {self.value}"

    def add_input(self, source: str):
        self.inputs[source] = 0  # Gate or name?

    def pulse(self, source: str, p: int):
        super().pulse(source, p)
        self.inputs[source] = p

    def run(self) -> bool:
        self.value = 0 if all(self.inputs.values()) else 1
        for sink in self.outputs:
            self.gates[sink].pulse(self.name, self.value)
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

    # def test_2a(self):
    #     with open('./test20.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)

    # def test_2(self):
    #     with open("./input20.txt", "r") as f:
    #         self.assertEqual(part2(list(f)), None)  # 737679780 too low


if __name__ == "__main__":
    unittest.main()
