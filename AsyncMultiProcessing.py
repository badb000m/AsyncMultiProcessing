import asyncio
import importlib
import os
import pathlib
import aioconsole

from lib.Process import Process
from typing import Union


class AsyncMultiProcessing:
    def __init__(self, **kwargs) -> None:
        self._processes: dict[str, Process, str] = {}

        self.modules_path: Union[str, pathlib.Path]
        self.modules_path = kwargs.get('modules_path')
        if self.modules_path is None:
            raise ValueError('modules_path must be specified.')

        asyncio.run(self.load_processes())  # Converts Python files with classes to 'Processes' in a dictionary.
        asyncio.run(self.run())

    async def load_processes(self) -> None:
        """
        How you want to load processes is only your decision. This is an overridable method where you can convert
        Python files with classes to asyncio processes in a dictionary.

        I would recommend to use 'import_module' from 'importlib' to load modules.
        This is the quickest and cleanest way dynamically.
        :return: dict[str, lib.Process]
        """
        for entry in os.scandir(self.modules_path):
            if entry.is_file() and entry.name.endswith('.py') and entry.name != '__init__.py':
                split_entry = os.path.splitext(entry.name)
                module_name = split_entry[0]

                if module_name is None:
                    continue

                process = self.python_file_to_process(module_name, self.modules_path)
                await self.add_process(process, module_name)

        return None

    def python_file_to_process(self, python_file_path: str, package: str = None) -> Process:
        """
        Converts a Python file with classes to a lib.Process object.
        :param package: Module
        :param python_file_path: path to Python file with classes
        :return: lib.Process
        """
        module_full = os.path.splitext(python_file_path)
        if len(module_full) < 2 or module_full[1] == '.py':
            raise TypeError('python_file_path must have a Python extension.')

        module_name = module_full[0]
        module_pythonic_path = os.path.join(self.modules_path, module_name).replace(os.sep, '.')

        imported_module = importlib.import_module(module_pythonic_path, package)
        module = getattr(imported_module, module_name)

        return Process(target=module)

    async def add_process(self, process_object: Process, process_name: str) -> None:
        """
        Adds a lib.Process object to the dictionary.
        :param process_name:
        :param process_object: object to add to the dictionary
        :return: None if successful
        """
        if not isinstance(process_object, Process):
            raise TypeError('process_object must be a lib.Process object.')

        if process_name in self._processes:
            raise ValueError('{} is already in self._processes'.format(process_name))

        self._processes[process_name] = process_object

        return None

    @property
    def processes(self) -> dict[str, Process]:
        """
        Returns the processes dictionary.
        :return: dict[str, lib.Process]
        """
        return self._processes

    def get_process(self, process_name: str) -> Process:
        """
        Gets a lib.Process object from the dictionary.
        :param process_name: name of process.
        :return: lib.Process
        """
        return self._processes[process_name]

    async def start_process(self, process_name: str) -> None:
        """
        Starts a lib.Process object.
        :param process_name: has to be the name of an object you want to start
        :return: None
        """
        process = self._processes[process_name]
        process.start()
        process.join(timeout=1)

    async def terminate_proc_add(self, process_name: str) -> None:
        """
        Terminates a lib.Process object and adds it back to the dictionary as a new process.
        :param process_name: Has to be the name of an object you want to terminate.
        :return: None
        """
        process = self._processes[process_name]
        process.terminate()

        self._processes[process_name] = Process(target=process.target_class)

        return None

    async def run(self) -> None:
        """
        This method is overridable. But you must return None as the result will be ignored.
        :return: None
        """
        while True:
            command_input = await aioconsole.ainput('Enter command: ')
            if not command_input:
                continue

            command_arguments = command_input.split()
            command_name = command_arguments[0]

            command_excess_arguments = command_arguments[1:]
            command_excess_name = command_excess_arguments[0]
            if command_name == 'enable':
                await self.start_process(command_excess_name)
            elif command_name == 'disable':
                await self.terminate_proc_add(command_excess_name)
            else:
                print('Unknown command.')


if __name__ == '__main__':
    AsyncMultiProcessing(modules_path='')
