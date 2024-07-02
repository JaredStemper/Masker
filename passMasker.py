import argparse
import time

def prettyPrint(results, wordCountDict, numOfPasses):
    """Print function that shows the provided list of resultant masks and their occurence count"""
    if numOfPasses == -1:
        print(f'\tTop Password Masks')
    else:
        print(f'\tTop {numOfPasses} Password Masks')
    print('-----------------------------')
    counter = 1
    for result in results:
        print(f'{counter}. {result:20s}: {wordCountDict[result]}')
        counter += 1

def ingestWordlist(file, encodingFormat, length):
        """Ingests wordlist and converts each word to its mask
        
        returns the bucket-sorted masks and the total length of the wordlist"""
        # dictionary to hold the index tracking how many times a string has occured
        #   should look like this:
        #       given: ["a","b","b","c"]
        #       [[],["a","c"],["b"],[],[]]
        #        0      1       2    3  4
        wordCountDict = {}
        totalWordlistCount = 0
        
        with open(file, encoding=encodingFormat) as wordlist:
            for word in wordlist:
                # avoid analyzing words that are above the provided length (barring -1, which is used to rep. all lengths)
                if len(word) >= length or length == -1:
                    totalWordlistCount += 1
                    # ensure line endings/spaces are stripped off while reading the file
                    # trailine newline
                    password = list(word.strip())

                    # convert the word to the proper password pattern
                    mask = ""
                    for i, char in enumerate(password):
                        if char.islower():
                            password[i] = "?l"
                        elif char.isupper():
                            password[i] = "?u"
                        elif char.isdigit():
                            password[i] = "?d"
                        else:
                            password[i] = "?s"
                    mask = mask.join(password)
                    # record the word in a dict and track its count
                    wordCountDict[mask] = 1 + wordCountDict.get(mask, 0)
        return wordCountDict,totalWordlistCount

def buildFrequencyList(args):
    # tracking to build 2d word frequency array
    totalWordlistCount = 0

    wordCountDict,totalWordlistCount = ingestWordlist(args.wordlist, args.encodingFormat, args.length)
    
    # build a 2d array of n size (where n is the wordlist)
    frequencyList = [[] for i in range(totalWordlistCount + 1)]
    
    for word, wordCount in wordCountDict.items():
        # using the list index to track the highest occurences, add the word (as a list to track multiple of the same frequency)
        frequencyList[wordCount].append(word)

    outputList = []
    # for words in wordFreq[::-1]:
    #     for word in words:
    # iterate through the word frequency list; note going backwords since the index is the frequency itself (and we want to start from the highest frequency)
    for i in range(len(frequencyList) -1, 0, -1):
        # ensure you loop through each list, since a frequency index can have multiple words in it
        for n in frequencyList[i]:
            outputList.append(n)
            # case where the length of the results is equal to the amount we want to pull out
            if len(outputList) == args.numOfPasses:
                prettyPrint(outputList, wordCountDict, args.numOfPasses)
    # case where all masks are provided
    if args.numOfPasses == -1:
        prettyPrint(outputList, wordCountDict, args.numOfPasses)

def input():
    # Take user input for the file location and how many of the top masks you'd like to see
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest = "wordlist", default = "/usr/share/wordlists/rockyou.txt", help = "File to analyze; Default is Kali location of rockyou.txt")
    parser.add_argument("-n", "--number", dest = "numOfPasses", default=3, type = int, help = "How many top most common masks you'd like to output; Defaults to 3; If you'd like to output all, enter -1")
    parser.add_argument("-e", "--encoding", dest = "encodingFormat", default = "utf-8", help = "Encoding to use for the file, default is utf-8; If you get a UnicodeDecode error try using 'latin-1'")
    parser.add_argument("-l", "--length", dest = "length", default = -1, type = int,help = "Only analyze passwords of the specified length or greater; Defaults to analyzing all passwords")
    args = parser.parse_args()
    return args

def main():
    args = input()
    buildFrequencyList(args)
    
if __name__ == "__main__":
	main()
