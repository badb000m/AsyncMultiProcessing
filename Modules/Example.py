class Example:
    """
    This is an example of what you are supposed to do for the 'Processes'
    """
    def __init__(self) -> None:
        # main() if you have added 'main'

        # or 

        # n = 1
        # while n < 100000000:
        #     n += n * 5

        # print(n)

    def main(self) -> int:
        """
        This is optional, but you must call 'main' in '__init__' if you are trying to return a value.
        I recommend you to return it to stdout instead of directly adding a value to __init__ as __init__ will return None, always!
        """
        n = 1
        while n < 100000000:
            n += n * 5

        print(n)
