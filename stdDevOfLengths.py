def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """
    if not L:
        return float('NaN') 
    
    #Calculate the mean of the set
    totSom = 0
    for el in L:
        totSom += len(el)
    mean = totSom/float(len(L))
   
    #Calculate the sum of computed quantities
    totQ = 0
    for el in L:
        totQ += (len(el) - mean) ** 2
 
    #Calculate the standard deviation
    return (totQ / float(len(L))) ** 0.5   

def stdDev(L):
   """
   L: list of integers
   
   returns: float. the standard deviation of the list of integers
       or NaN if L is empty
   """
   if not L:
       return float('NaN')
   
   #Calculate the mean of the list
   mean = sum(L) / float(len(L))
   print 'mean is ' + str(mean)
   
   #Calculate the standard deviation
   totQ = 0
   for el in L:
       totQ += (el - mean) ** 2
   return (totQ / float(len(L))) ** 0.5
   
   
      

print stdDevOfLengths([])
print stdDevOfLengths(['apples', 'oranges', 'kiwis', 'pineapples'])
print stdDev([10, 4, 12, 15, 20, 5])