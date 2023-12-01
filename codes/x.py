import asyncio
import threading


async def do_first():
    print("Running do_first block 1")
    await asyncio.sleep(0)
    print("Running do_first block 2")


async def do_second():
    print("Running do_second block 1")
    await asyncio.sleep(0)
    print("Running do_second block 2")


async def main():
    task_1 = asyncio.create_task(do_first())
    task_2 = asyncio.create_task(do_second())
    await asyncio.wait([task_1, task_2])


def first_thd():
    print("Running do_first line 1")
    print("Running do_first line 2")
    print("Running do_first line 3")


def second_thd():
    print("Running do_second line 1")
    print("Running do_second line 2")
    print("Running do_second line 3")


def main_thd():
    t1 = threading.Thread(target=first_thd)
    t2 = threading.Thread(target=second_thd)
    t1.start(), t2.start()
    t1.join(), t2.join()


if __name__ == "__main__":
    asyncio.run(main())
    main_thd()