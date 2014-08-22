
def bubbleSort(sortlist):
    for i in range(1, len(sortlist)):
        while i >= 1:
            if sortlist[i] < sortlist[i-1]:
                sl = sortlist[i]
                sortlist[i] = sortlist[i-1]
                sortlist[i-1] = sl
            i -= 1
    return sortlist

def straightInsertSort(sortlist):
    for i in range(1, len(sortlist)):
        j = i
        while j > 0 and sortlist[j-1] > sortlist[i]:
            j -= 1
        sortlist.insert(j, sortlist[i])
        sortlist.pop(i+1)
    return sortlist


if __name__ == "__main__":
    sorting = [23,56,2,56,232,523,231,12121,5,0,3,2,9,0,1]
    print bubbleSort(sorting)
    #print straightInsertSort(sorting)
