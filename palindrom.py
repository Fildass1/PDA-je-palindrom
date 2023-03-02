from typing import Optional, Set, List, Dict, Tuple

class Stack:
    def __init__(self) -> None:
        self.__contents__ = []

    def peek(self) -> str:
        if self.__contents__ == []:
            return ""
        return self.__contents__[-1]

    def pop(self) -> str:
        if self.__contents__ == []:
            return ""
        return self.__contents__.pop()

    def push(self, elem) -> None:
        if elem == "":
            return
        self.__contents__.append(elem)


class PDA:
    def __init__(self) -> None:
        self.transition_function: Dict[(str, str, str), (str, List[str])] = {}
        self.start_state: Optional[str] = None
        self.accepting_state = "Acc"
        self.rejecting_state = "Rej"
        self.alphabet: Set[str] = set()
        self.stack_alphabet: Set[str] = set()
        self.stack: 'Stack' = Stack()

    def transition(self, state, letter, stack_letter, i) -> Tuple[Optional[str], bool, int]:
        if self.transition_function.get((state, letter, stack_letter), None) is not None:
            state, temp = self.transition_function[(state, letter, stack_letter)]
            if stack_letter != "":
                self.stack.pop()
            for elem in temp:
                self.stack.push(elem)
            if letter != "":
                i += 1
            return state, True, i
        return state, False, i

    def accepts_word(self, word) -> bool:
        state = self.start_state
        i = 0
        while i < len(word):
            top = self.stack.peek()
            for letter, stack_letter in [(word[i], top), ("", top), (word[i], ""), ("", "")]:
                state, used, i = self.transition(state, letter, stack_letter, i)
                if used:
                    break
            if not used or state == self.rejecting_state:
                return False
            if state == self.accepting_state and self.stack.peek() == "":
                return True
        while True:
            top = self.stack.peek()
            for letter, stack_letter in [("", top), ("", "")]:
                state, used, i = self.transition(state, letter, stack_letter, i)
                if used:
                    break
            if not used or state == self.rejecting_state:
                return False
            if state == self.accepting_state and self.stack.peek() == "":
                return True

def return_PDA() -> PDA:
    pda = PDA()
    pda.start_state = "q0"
    pda.transition_function = {
        ("q0", "a", ""): ("q0", ["A"]),
        ("q0", "b", ""): ("q0", ["B"]),

        ("q1", "", ""): ("Acc", []),
    }
    return pda

# Testy:
automata = return_PDA()
print(automata.accepts_word("aca")) # True
print(automata.accepts_word("abaacaaba")) # True
print(automata.accepts_word("aabca")) # False
automata = return_PDA()
print(automata.accepts_word("aaabaaa")) # False
automata = return_PDA()
print(automata.accepts_word("aabb#ca")) # True
