from collections.abc import Callable, Generator, Sequence
from functools import update_wrapper
from inspect import signature
from timeit import default_timer
from typing import Any, ClassVar


class Timer:
    '''
    及其方便的性能分析用装饰器

    --------------------------------------

    TODO 批量运行加入返回值打印功能（缩写：prt）

    '''
    funcs: ClassVar[list[Callable[..., Any]]] = [] # 存储被装饰过的函数
    times: ClassVar[dict[str, float]] = {} # 记录函数及其对应运行所耗时间  规范：函数名 : 耗时


    def __init__(self, func: Callable[..., Any]) -> None:
        '''
        将该类实例自身的属性替换为func的属性后添入funcs类变量中
        '''
        update_wrapper(self, func)
        self.funcs.append(self)


    def __call__(self, *args: tuple[Any], **kwargs: dict[str, dict[Any, Any]]) -> Any:
        '''
        运行原函数并计算耗时，后将计时数据添入times类变量中，并返回结果 \n
        注：可能是mypy的bug，mypy并不能检测到 __wrapped__ 的存在，故需要 “ # type: ignore ” 忽略该行类型检测 \n
        '''
        self.start_time: float = default_timer()
        result: Any = self.__wrapped__(*args, **kwargs) # type: ignore
        self.elapsted_time: float = default_timer() - self.start_time

        self.times[self.__wrapped__.__name__] = self.elapsted_time # type: ignore

        return result


    @classmethod
    def run(cls, args: Sequence[Sequence[Any]] = [], omit: bool = True) -> None:
        '''
        用序列按@Timer添加顺序传入各个函数所需参数组即可批量运行funcs类变量中的函数 \n
        args：参数组 \n
        omit：忽略无参函数对args的占位 \n
        例：当你需要运行的三个函数中只有两个需要参数，在开启omit后你只需传入两组参数即可，不需要多留一个空参数组
        '''
        # TODO 之后尝试使用元编程重构它，并重新加回 prt
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
    def run1arg(cls, *args: tuple[Any], **kwargs: dict[str, dict[Any, Any]]) -> None:
        '''
        统一传入一套参数运行funcs类变量中的函数
        '''
        for func in cls.funcs:
            func(*args, **kwargs)


    @classmethod
    def report(cls) -> Generator[tuple[str, float, float], None, None]:
        '''
        返回按 (函数名，耗时，该耗时占所有已运行函数总耗时的百分比) 封装的生成器
        '''
        return ((i[0], i[1], i[1] / sum(cls.times.values())) for i in cls.times.items())


    @classmethod
    def print_report(cls) -> None:
        '''
        从左到右，打印出各函数的（函数名，耗时，该耗时占所有已运行函数总耗时的百分比）数据
        '''
        print('-' * 38)
        for name, time in cls.times.items():
            print(f'| {name : <8} | {time : <10.5f} | {time / sum(cls.times.values()) : <10.5%} |')
        print('-' * 38)

