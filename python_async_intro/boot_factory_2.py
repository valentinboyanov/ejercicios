import asyncio
import random
import time
import argparse

BOOTS = 0

async def make_boot():
    global BOOTS
    manufacturing_time = random.choice([1,3,5])
    await asyncio.sleep(manufacturing_time)
    BOOTS += 1

async def worker():
    while 1:
        await make_boot()

async def boots_printer():
    start = time.perf_counter()
    while 1:
        diff = time.perf_counter() - start
        print(f"seconds: {diff:0.2f} boots: {BOOTS}")
        await asyncio.sleep(1)

async def main(num_workers: int = 1):
    workers: List = [worker() for i in range(0,num_workers)]
    await asyncio.gather(
        *workers,
        boots_printer(),
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_workers", type=int, help="number of workers")
    args = parser.parse_args()

    asyncio.run(main(args.num_workers))
