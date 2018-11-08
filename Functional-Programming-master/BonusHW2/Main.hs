import Data.Char

data Color = Red | Black
    deriving (Eq, Show)

data Suit  = Clubs | Diamonds | Hearts | Spades
    deriving (Eq, Show)

data Rank  = Num Int | Jack | Queen | King | Ace
    deriving (Eq, Show)

data Card  = Card { suit :: Suit, rank :: Rank }
    deriving (Eq, Show)

data Move = Draw | Discard Card
    deriving (Eq, Show)

data State = Ongoing | Finished
    deriving (Eq, Show)

cardColor :: Card -> Color
cardColor c
    | suit c == Spades   || suit c == Clubs  = Black
    | suit c == Diamonds || suit c == Hearts = Red
    | otherwise = error "Color is not specified!"

cardValue :: Card -> Int
cardValue c = case rank c of
    Num x -> x
    Ace   -> 11
    _     -> 10

removeCard :: [Card] -> Card -> [Card]
removeCard []  _            = error "card not in list"
removeCard xs@(x':xs') c    = if x' == c then xs' else x' : (removeCard xs' c)

allSameColor :: [Card] -> Bool
allSameColor []              = True
allSameColor [a]             = True
allSameColor xs@(x':xs') = if cardColor x' == cardColor (head xs') then allSameColor xs' else False

sumCards :: [Card] -> Int
sumCards [] = 0
sumCards xs = summer xs 0
    where
        summer :: [Card] -> Int -> Int
        summer cards osum
            | cards == []      = osum
            | otherwise        = summer (tail cards) (osum + cardValue (head cards))

score :: [Card] -> Int -> Int
score xs g = if allSameColor xs then floor ( fromIntegral presc / 2) else presc
    where presc = if sumCards xs > g then 3 * ( sumCards xs - g ) else g - sumCards xs

runGame :: [Card] -> [Move] -> Int -> Int
runGame cl ml go = currentState cl [] ml go Ongoing
    where
        currentState :: [Card] -> [Card] -> [Move] -> Int -> State -> Int
        currentState cls hls [] go st = score hls go
        currentState cls hls mls@(Draw : cs) go st
            | st == Finished || sumCards hls > go = score hls go
            | otherwise = currentState cls' hls' mls' go st'
                where
                    st'  = if cls == [] then Finished else Ongoing
                    mls' = if cls == [] then [] else tail mls
                    cls' = if cls == [] then [] else tail cls
                    hls' = if cls == [] then hls else (head cls):hls
        currentState cardls heldls mvlist@(Discard c:cs) go st
            | st == Finished || sumCards heldls > go = score heldls go
            | otherwise = currentState cardls' heldls' mvlist' go st'
                where
                    st' = Ongoing
                    mvlist' = tail mvlist
                    cardls' = tail cardls
                    heldls' = removeCard heldls c

convertSuit :: Char -> Suit
convertSuit c = case c of
    'C' -> Clubs
    'c' -> Clubs
    'D' -> Diamonds
    'd' -> Diamonds
    'H' -> Hearts
    'h' -> Hearts
    'S' -> Spades
    's' -> Spades
    _   -> error "Suit not found!"

convertRank :: Char -> Rank
convertRank c
    | c == 't'  || c == 'T'             = Num 10
    | c == 'j'  || c == 'J'             = Num 10
    | c == 'q'  || c == 'Q'             = Num 10
    | c == 'k'  || c == 'K'             = Num 10
    | isDigit c && c == '1'             = Ace
    | isDigit c                         = Num (digitToInt c)
    | otherwise                         = error "Rank is unknown!"

convertCard :: Char -> Char -> Card
convertCard s r = Card  (convertSuit s) (convertRank r )

readCards :: IO [Card]
readCards = do
    x <- getLine
    if x == "."
        then return []
        else
            if length x < 2 then error "Error" else
                do
                    xs <- readCards
                    return ( (convertCard (head x) (head (tail x)) ) : xs )

convertMove :: Char -> Char -> Char -> Move
convertMove mv st rn
    | mv == 'd' || mv == 'D' = Draw
    | mv == 'r' || mv == 'R' = Discard (Card (convertSuit st) (convertRank rn) )
    | otherwise              = error "Error while converting move!"

readMoves :: IO [Move]
readMoves = do
    x <- getLine
    if x == "."
        then return []
        else
            if length x /= 1 && length x /= 3 then error "Reading moves error!" else
                do
                    xs <- readMoves
                    return ( ( curMove x ) : xs )
                        where
                            curMove :: String -> Move
                            curMove s
                                | length s == 1 = convertMove (head s) ' ' ' '
                                | otherwise
                                    = convertMove (head s) (head (tail s) ) (head (tail (tail s) ))

main = do
    putStrLn "Enter cards: "
    cards <- readCards
    -- putStrLn (show cards)
    putStrLn "Enter moves:"
    moves <- readMoves
    --putStrLn (show moves)
    putStrLn "Enter goal:"
    line <- getLine
    let goal = read line :: Int
    let score = runGame cards moves goal
    putStrLn ("Score: " ++ show score)
