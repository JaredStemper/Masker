# Masker
Analyze a list of passwords and provide an analysis of the the passwords into a mask ingestible to hashcat.

This approach gains us a nearly 10% decrease in computation when tested against standard sorting approaches using a 1.6 million sample size from [available breach data](https://github.com/berzerk0/Probable-Wordlists/blob/master/Real-Passwords/Real-Password-Rev-2-Torrents/ProbWL-v2-Real-Passwords-7z.torrent). 

The full breakdown of the approach is detailing in the code, but the high-level understanding is as follows.

Given a wordlist of the following:    
```python
[
    "password",
    "testings",
    "firstlyr",
    "bigglynr",
    "Yesmaam!",
    "Noopsir!",
    "yggrasilShallfall",
]
```
A mask list will be generated in this organization: 
```python
[
    [],
    ["?l?l?l?l?l?l?l?l?u?l?l?l?l?l?l?l?l"],
    ["?u?l?l?l?l?l?l?s"],
    [],
    ["?l?l?l?l?l?l?l?l"]
]
```
Looking to the indexes, we can see the pattern emerge more clearly:
```python
[
  [0], # no iteration ever occurred 
  [1], # a single iteration of this mask was created
  [2], # two iterations of this mask were created
  [3], # three iterations of a mask never occurred
  [4], # four iterations occurred of this mask
]
```
