import logging
import threading
import multiprocessing
import asyncio
import time

logger = logging.getLogger(__name__)

class ParallelCompareWithUrl:
    def __init__(self, items: list, sync_method: callable, async_method: callable):
        self._items = items
        self._sync_method = sync_method
        self._async_method = async_method


    def _do_something(self, item):
        self._sync_method(item)

    async def _do_something_async(self, item):
        await self._async_method(item)

    def _execute_by_for(self):
        try:
            for item in self._items:
                self._do_something(item)

            logger.debug("_execute_by_for done!")

        except Exception as err:
            logger.exception(f"_execute_by_for 에러 ({err})")

    def _execute_by_threading(self):
        try:
            work_threads = []
            for item in self._items:
                work_thread = threading.Thread(target=self._do_something, args=(item,))
                work_threads.append(work_thread)

            for work_thread in work_threads:
                work_thread.start()

            for work_thread in work_threads:
                work_thread.join()

            logger.debug("_execute_by_threading done!")

        except Exception as err:
            logger.exception(f"_execute_by_threading 에러 ({err})")

    def _execute_by_multiprocessing(self):
        try:
            processes = []
            for item in self._items:
                p = multiprocessing.Process(target=self._do_something, args=(item,))
                processes.append(p)

            for p in processes:
                p.start()

            for p in processes:
                p.join()

            logger.debug("_execute_by_multiprocessing done!")

        except Exception as err:
            logger.exception(f"_execute_by_multiprocessing 에러 ({err})")

    async def _execute_by_async(self):
        try:
            tasks = [self._do_something_async(item) for item in self._items]
            await asyncio.gather(*tasks)

            logger.debug("_execute_by_async done!");
        
        except Exception as err:
            logger.exception(f"_execute_by_async 에러 ({err})")
            

    def compare(self):
        logger.info("--- Main Start ---")

        header_list_for_async = []
        elapsed_time_list_for_async = []
        elapsed_time_list_for_threading = []
        elapsed_time_list_for_multiprocessing = []
        
        logger.info(f"first synchronous for execution time :{self._measure_execute_by_for():.2f}")

        logger.info("test 1 - order : async -> threading -> multiprocessing")
        header_list_for_async.append("1(a->t->m)")
        elapsed_time_list_for_async.append(self._measure_execute_by_async());
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());

        logger.info("test 2 - order : async -> threading -> multiprocessing")
        header_list_for_async.append("2(a->t->m)")
        elapsed_time_list_for_async.append(self._measure_execute_by_async());
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());

        logger.info("test 3 - order : async -> multiprocessing -> threading")
        header_list_for_async.append("3(a->m->t)")
        elapsed_time_list_for_async.append(self._measure_execute_by_async());
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());

        logger.info("test 4 - order : threading -> async -> multiprocessing")
        header_list_for_async.append("4(t->a->m)")
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());
        elapsed_time_list_for_async.append(self._measure_execute_by_async());
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());

        logger.info("test 5 - order : threading -> multiprocessing -> async")
        header_list_for_async.append("5(t->m->a)")
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());
        elapsed_time_list_for_async.append(self._measure_execute_by_async());

        logger.info("test 6 - order : multiprocessing -> async -> threading")
        header_list_for_async.append("6(m->a->t)")
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());
        elapsed_time_list_for_async.append(self._measure_execute_by_async());
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());

        logger.info("test 7 - order : multiprocessing -> threading -> async")
        header_list_for_async.append("7(m->t->a)")
        elapsed_time_list_for_multiprocessing.append(self._measure_execute_by_multiprocessing());
        elapsed_time_list_for_threading.append(self._measure_execute_by_threading());
        elapsed_time_list_for_async.append(self._measure_execute_by_async());

        logger.info(f"last synchronous for execution time :{self._measure_execute_by_for():.2f}")
        
        logger.info("    " + " ".join([f"{header:s}".rjust(12) for header in header_list_for_async]))
        logger.info("asy " + " ".join([f"{num:.2f}".rjust(12) for num in elapsed_time_list_for_async]))
        logger.info("thr " + " ".join([f"{num:.2f}".rjust(12) for num in elapsed_time_list_for_threading]))
        logger.info("mul " + " ".join([f"{num:.2f}".rjust(12) for num in elapsed_time_list_for_multiprocessing]))
        
        logger.info("--- Main End ---")

    def _measure_execute_by_for(self):
        start_time = time.time()
        self._execute_by_for()
        return time.time() - start_time
    
    def _measure_execute_by_threading(self):
        start_time = time.time()
        self._execute_by_threading()
        return time.time() - start_time

    def _measure_execute_by_async(self):
        start_time = time.time()
        asyncio.run(self._execute_by_async())
        return time.time() - start_time

    def _measure_execute_by_multiprocessing(self):
        start_time = time.time()
        self._execute_by_multiprocessing()
        return time.time() - start_time

