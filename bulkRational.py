import PalindromeRatioAutomataGenerator as PRAG
import math
from multiprocessing import Pool
import tqdm # For getting a progress bar
import sys

if __name__ == "__main__":
    def info():
        print("Bulk processing for the PalindromeRatioAutomataGenerator.py")
        print("Usage: bulkRational.py start stop base ASet BSet threads")
        print("    start, stop, base \in N")
        print("    ASet, BSet \in {\"pal\", \"apal\"}")
        print("    threads = number of threads to use")
        print("Output: Each line is p, q, A, B where p = A/B, A is in ASet, B is in BSet, start <= p < stop, 1 <= q < p")
        exit()

    if len(sys.argv) != 7:
        info()
        exit()

    b = int(sys.argv[3])
    ASet = sys.argv[4]
    BSet = sys.argv[5]
    threads = int(sys.argv[6])
    if ASet not in ["pal", "apal"] or BSet not in ["pal", "apal"]:
        info()
        exit()

    Ns = []
    for p in range(int(sys.argv[1]), int(sys.argv[2])):
        for q in range(1, p):
            if math.gcd(p, q) != 1:
                continue
            Ns.append((p, q, b, ASet, BSet))

    with Pool(threads) as pool:
        for result in tqdm.tqdm(pool.imap(PRAG.getSmallestRatioPacked, Ns)):
            print(result[0], result[1], result[2], result[3], flush=True)
