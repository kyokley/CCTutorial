from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Help fix the bug to get the expected output"""

    help = 'Help fix the bug to get the expected output'

    def handle(self, *args, **kwargs):
        """
        Something is wrong with the output data. We expect it to look like:
        [0]
        [1]
        [2]
        [3]
        [4]
        [5]
        [6]
        [7]
        [8]
        [9]

        But we end up getting:
        [0]
        [0, 1]
        [0, 1, 2]
        [0, 1, 2, 3]
        [0, 1, 2, 3, 4]
        [0, 1, 2, 3, 4, 5]
        [0, 1, 2, 3, 4, 5, 6]
        [0, 1, 2, 3, 4, 5, 6, 7]
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        Fix the bug so we get the expected output.
        """

        def manipulate_data(default_list=None, data=None):
            """
            For a given data list, append it to the default list and return the results
            """
            if default_list is None:
                default_list = []

            default_list.append(data)
            return default_list

        for i in range(10):
            results = manipulate_data(data=i)
            print(results)
