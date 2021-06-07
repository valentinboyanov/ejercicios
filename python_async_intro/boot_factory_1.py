import asyncio
import random
import time

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

async def main():
    await asyncio.gather(
        boots_printer(),
        worker()
    )

asyncio.run(main())
