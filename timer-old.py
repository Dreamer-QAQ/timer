from functools import wraps
from timeit import default_timer
from typing import Any, Iterable, List, Dict

'''

timer - 1.0

此版本调用起来不够优雅，以及类型注解等一些细节没做好
故重构为 1.1 版本，该版本源码留作纪念

'''

funcs: List[Any] = []
times: List[float] = []
funcs_times: Dict[str, float] = {}

def timer(flag: str = None, input: Iterable = None):
    if flag != 'run' and flag != 'run1arg' and input is not None:
        raise AttributeError("flag != 'run' and flag != 'run1arg'，不要输入 input")

    elif flag == 'report':
        return ((i for i in times), (i / sum(times) for i in times))

    elif flag == 'print_report':
        print('-' * 38)
        for key, value in funcs_times.items():
            print(f'| {key : <8} | {value : <10.5f} | {value / sum(funcs_times.values()) : <10.5%} |')
        print('-' * 38)

    elif flag == 'run':
        for index, func in enumerate(funcs):
            func(*input[index])

    elif flag == 'run1arg':
        for func in funcs:
            func(*input)

    def inner(func: Any) -> Any:
        @wraps(func)
        def clock(*args, **kwargs) -> Any:
            start: float = default_timer()
            result: Any = func(*args, **kwargs)
            end: float = default_timer() - start

            times.append(end)
            funcs_times[func.__name__] = end

            return result
        funcs.append(clock)
        return clock
    return inner

