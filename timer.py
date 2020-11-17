from collections import deque
from functools import wraps
from inspect import signature
from timeit import default_timer
from typing import Any, Callable, ClassVar, Deque, Dict, Generator, Tuple, Sequence


class Timer:
    '''
    及其方便的性能分析用装饰器

    --------------------------------------

    TODO 注释待添加

    '''
    funcs: ClassVar[Deque[Callable]] = deque() # 存储被装饰过的函数
    times: ClassVar[Dict[str, float]] = {} # 记录函数及其对应运行所耗时间  规范：函数名 : 耗时


    def __init__(self, func: Callable) -> None:
        self = wraps(func)(self) # type: ignore
        self.funcs.append(self)


    def __call__(self, *args, **kwargs) -> Callable:
        self.start_time: float = default_timer()
        result = self.__wrapped__(*args, **kwargs) # type: ignore
        self.elapsted_time: float = default_timer() - self.start_time

        self.times[self.__wrapped__.__name__] = self.elapsted_time # type: ignore

        return result


    @classmethod
    def run(cls, args: Sequence[Sequence[Any]] = [], omit: bool = True) -> None:
        # TODO 之后尝试使用元编程重构它，并重新加回 prt：选择是否打印返回值
        if omit == True:
            iter_args = iter(args)
            for func in cls.funcs:
                if str(signature(func)) != '()':
                    func(*next(iter_args))
                else:
                    func()
        else:
            for index, func in enumerate(cls.funcs):
                if str(signature(func)) != '()':
                    func(*args[index])
                else:
                    func()


    @classmethod
    def run1arg(cls, *args, **kwargs):
        for func in cls.funcs:
            func(*args, **kwargs)


    @classmethod
    def report(cls) -> Generator[Tuple[str, float, float], None, None]:
        return ((i[0], i[1], i[1] / sum(cls.times.values())) for i in cls.times.items())


    @classmethod
    def print_report(cls) -> None:
        print('-' * 38)
        for name, time in cls.times.items():
            print(f'| {name : <8} | {time : <10.5f} | {time / sum(cls.times.values()) : <10.5%} |')
        print('-' * 38)

