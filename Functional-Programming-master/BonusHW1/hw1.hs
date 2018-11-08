-- Created By Safa Keskin
-- 22.02.2018
-- For Bonus Homework 1

dayOfWeek :: Integer -> Integer -> Integer -> Integer
dayOfWeek y m d = mod ( d + t1 + k + t2 + t3 + 5 * j ) 7
    where
        m' = if m <= 2 then m + 12 else m
        j  = floor ( fromIntegral y / 100.0 )
        k  = mod y 100
        t1 = floor (fromIntegral (13 * (m' + 1)) / 5.0)
        t2 = floor (fromIntegral k / 4.0 )
        t3 = floor (fromIntegral j / 4.0 )

sundays1 :: Integer -> Integer -> Integer
sundays1 start end = sundays' start 1
    where
        sundays' :: Integer -> Integer -> Integer
        sundays' y m
            | y > end = 0
            | otherwise = if dayOfWeek y m 1 == 1 then rest + 1 else rest
                where
                    nextY = if nextM < m then y + 1 else y
                    nextM = if m == 12 then 1 else mod (m + 1) 13
                    rest  = sundays' nextY nextM

-- sundays' function calculates the months that's first day is sunday
--   between the start year and the end year. If it took 4 parameter instead
--   of 2 ( 3rd is end year and 4th is end month ), we would not need sundays1
--   function anymore.

-- if we don't declate rest and put its expression in the position of rest,
--   function becomes recursive. Because instead of calculating first rest and
--   then putting it into if-else clause, it directly works as a recursive 
--   function.

tRsundays1 :: Integer -> Integer -> Integer
tRsundays1 start end = tRsundays' start 1 0
    where
        tRsundays' :: Integer -> Integer -> Integer -> Integer
        tRsundays' y m acc
            | y > end   = acc
            | otherwise = tRsundays' nextY nextM nextAcc
                where
                    nextAcc = if dayOfWeek y m 1 == 1 then acc + 1 else acc
                    nextY   = if nextM < m then y + 1 else y
                    nextM   = if m == 12 then 1 else mod (m + 1) 13


-- 23.2.2018
leap :: Integer -> Bool
leap y = mod y 4 == 0 && mod y 100 /= 0 || mod y 400 == 0

daysInMonth :: Integer -> Integer -> Integer
daysInMonth m y
    | m == 2                                = if leap y then 29 else 28
    | m == 4 || m == 6 || m == 9 || m == 11 = 30
    | otherwise                             = 31

sundays2 :: Integer -> Integer -> Integer
sundays2 strYear endYear = sundays' strYear 2 1 0
    where
        sundays' :: Integer -> Integer -> Integer -> Integer -> Integer
        sundays' y dow m acc
            | y > endYear   = acc
            | otherwise     = sundays' nextY nextDow nextM nextAcc
                where
                    nextDow = dow + (daysInMonth m y `mod` 7)
                    nextAcc = if nextDow `mod` 7 == 0 then acc + 1 else acc
                    nextY   = if nextM < m then y + 1 else y
                    nextM   = if m == 12 then 1 else mod (m + 1) 13


question5 :: Integer -> Bool
question5 year = mod ( year * 365 + mult4 - mult100 + mult400 ) 7 == 0
    where
        mult4   = floor (fromIntegral year / 4.0)
        mult100 = floor (fromIntegral year / 100.0)
        mult400 = floor (fromIntegral year / 400.0)

-- question 400 gives 'True' as result. That means all the days have equally
-- likely probability. Because there are exactly n weeks ( n is an integer )
-- and every week consist of 7 days. That means all the days in a week have 
-- 1/7 probability at a random selection from 400 days.
