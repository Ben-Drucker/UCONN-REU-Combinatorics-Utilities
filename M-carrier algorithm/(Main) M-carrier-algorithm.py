from M_carrier_algorithm_functions import carrier_algorithm


def main():
    pi = [1, 4, 6, 7, 2, 3, 5]  # The permutation
    finite = True  # Finite or infinite carrier algorithm
    number_of_carriers = 5  # Number of carriers (M)
    number_of_Es = 5  # Number of e's to inject during flushing
    print_steps = True  # Whether or not to print each step of the M-carrier algorithm

    carrier_algorithm(pi, number_of_carriers, number_of_Es, finite, print_steps)


main()
