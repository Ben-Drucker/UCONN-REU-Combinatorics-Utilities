def carrier_algorithm(perm, M, num_of_Es, finite=True, print_steps=True):
    # Initialization:
    n = len(perm)
    carrier_list = [[n + 1 for j in range(n)] for i in range(M)]
    left_result = [[]]
    justLs = []

    # Insertion:
    def insertion():
        for permElt in perm:
            insertionElt = permElt
            for carrier in reversed(carrier_list):
                if insertionElt == n + 1:
                    enp = True
                else:
                    enp = False
                ejection_index = insertion_rule(carrier, insertionElt, n)
                ejectedElt = carrier[ejection_index]
                carrier[ejection_index] = insertionElt
                if enp:
                    popd = carrier[0]
                    carrier.pop(0)
                    carrier.append(popd)
                insertionElt = ejectedElt

            left_result[0].append(insertionElt)
            if not finite:
                for i in range(n + 1):
                    if i in left_result[0] and Flag:
                        print("Insertion Ended.\n===Not enough carriers for infinite carrier algorithm!===")
                        return False
            outSTR = str(display(left_result)) + "     " + str(display(carrier_list)) + "<---" + str(
                permElt if permElt < n + 1 else 0)
            if Flag:
                justLen = len(outSTR) + (n + num_of_Es) * 3
                justLs.append(justLen)
            if print_steps:
                print(outSTR.rjust(justLs[0]))
        return True

    # Display nicely.
    def display(carrierr_list):
        return [[carElt if carElt != n + 1 else 0 for carElt in carrier] for carrier in carrierr_list]

    Flag = True
    cont = insertion()
    if cont:
        perm = [n + 1 for i in range(num_of_Es)]
        if len(perm) > 0:
            Flag = False
            insertion()
        return left_result, carrier_list
    else:
        return None


def insertion_rule(carrier, insElt, n):
    # Returns the index of the smallest element in the carrier larger than the insertion element
    if insElt == n + 1:
        return 0
    else:
        for index in range(len(carrier)):
            if carrier[index] >= insElt:
                return index