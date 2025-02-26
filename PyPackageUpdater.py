'''
Python Program to check and update packages.

'''

import os
import subprocess
import sys
import time


# ********** Functions **********

def check_for_outdated() -> list[str]:
    '''
    Function to get for outdated packages, including pip.

    Returns:
     list of str: each string is "name currentVersionm latestVersion"
    '''
    # Get a list of outdated modules
    outdated = subprocess.check_output(
        ['python', '-m', 'pip', 'list', '--outdated'],
        text=True
    )
    outdated = outdated.strip().split('\n')[2:]
    return [' '.join(pkg.split()[:3]) for pkg in outdated]


def update_packages(outdated_packages) -> None:
    '''
    Function to update a gicen list of outdated packages using pip.

    Parameters:
        outdated_packages list[str]:
        list of str: each string is "name currentVersionm latestVersion"
    '''

    count = len(outdated_packages)
    for ind, package in enumerate(outdated_packages, 1):
        name, cur, new = package.split()
        print(f'{ind}/{count}: Updating "{name}" from {cur} to {new}')
        if name.lower() == 'pip':
            subprocess.check_call(
                ['python', '-m', 'pip', 'install', '--upgrade', name])
        else:
            subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', name])
        print()
    print('Done Updating!')


# ********** Main Program **********

if __name__ == '__main__':
    # Banner
    print("Welcome to the Python Package updater!\n")

    # Checkings for updates immediately, since it an "intensive" process
    print("Checking for outdated packages...\n")
    outdated = check_for_outdated()

    # No packages to update
    if not outdated:
        print("All packages are up to date.\n")

    # Outdated Packages exist
    else:
        # sorting so pip is first, this helps avoid update issues from not using the latest pip verison.
        outdated = sorted(outdated, key=lambda pkg: pkg.split()[0] != 'pip')

        # Calculating the maximum width for each column then printing package name, current verison and latest version.
        max_name_length = max(len(pkg.split()[0]) for pkg in outdated)
        max_current_version_length = max(
            len(pkg.split()[1]) for pkg in outdated)
        max_latest_version_length = max(
            len(pkg.split()[2]) for pkg in outdated)
        print(f'There are {len(outdated)} outdated packages')
        for ind, pkg in enumerate(outdated, 1):
            details = pkg.split()
            print(f"{ind:2}: {details[0].ljust(max_name_length)} | "
                  f"Current Version: {details[1].ljust(
                      max_current_version_length)} | "
                  f"Latest Version: {details[2].ljust(max_latest_version_length)}")

        # Asking user if they want to update ALL package.
        user = input('\nWould you like to update all of them (y/n)? ')
        if user.lower() == 'y':
            print(f'Updating all packages...\n')
            update_packages(outdated)
            outdated = []  # clearing list of outdated pkgs

        # Asking user if they want to update ANY package.
        else:
            while True:
                user = input('\nWould you like to update any? (y/n)? ')
                match (user.lower()):
                    case 'y':
                        picked = []
                        print('Pick what packages you want to update by '
                              'entering the number from the list, one at a time.\n'
                              'Once finished selecting, type "done" to update them.\n')
                        while (True):
                            user = input('Enter a number: ')
                            if user.lower() == 'done':
                                print('Finished picking packages.\n')
                                break
                            elif user.isnumeric():
                                # appending picked packages
                                picked.append(outdated[int(user) - 1])
                            else:
                                print("Invalid Entry. Try again", end='')

                        if picked:
                            print(f'Updating {len(picked)
                                              } selected packages...')
                            update_packages(picked)
                        else:
                            print("No packages were selected.")
                        break
                    case 'n':
                        break
                    case _:
                        # default case
                        print("Invalid entry, try again.\n")


# Asking user if they want to quit program
u = input('Everything is done. Enter any key to quit the program. ')
time.sleep(.5)
print("Program Terminated.")
sys.exit(0)
