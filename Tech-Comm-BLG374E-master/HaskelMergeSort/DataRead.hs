-- This code part is taken from https://stackoverflow.com/questions/7867723/haskell-file-reading
-- and optimized. It is an answer to question and can be found via link.
import System.IO
import System.Environment

main = do
    args <- getArgs
    contents <- readFile (head args)-- "../Data/data10000.txt"
    let numList = map readInt . words $ contents
    let sList = mergesort numList
    --print sList

    --Writing part
    writeFile "output.txt" $ unlines (map show sList)

mergesort'merge :: (Ord a) => [a] -> [a] -> [a]
mergesort'merge [] xs = xs
mergesort'merge xs [] = xs
mergesort'merge (x:xs) (y:ys)
    | (x < y) = x:mergesort'merge xs (y:ys)
    | otherwise = y:mergesort'merge (x:xs) ys

mergesort'splitinhalf :: [a] -> ([a], [a])
mergesort'splitinhalf xs = (take n xs, drop n xs)
    where n = (length xs) `div` 2

mergesort :: (Ord a) => [a] -> [a]
mergesort xs
    | (length xs) > 1 = mergesort'merge (mergesort ls) (mergesort rs)
    | otherwise = xs
    where (ls, rs) = mergesort'splitinhalf xs

readInt :: String -> Int
readInt = read
