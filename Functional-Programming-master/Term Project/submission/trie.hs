-- Safa Keskin
-- 150140137

-- This program is written by Safa Keskin for Term Project of BLG458E Lecture
-- Given by H. Turgut UYAR
-- After evaluation, can be used for educational purpose.

-- NOTE: This program would be written much more efficiently and much more clear
--      but due to lack of time and my busy schedule, it could not be written
--      very efficiently for this project. I did my best in my limited time.

-- Best regards.

import qualified Data.Map as M
import Data.Maybe
import qualified Data.List as Dlist
import System.Environment
import System.IO
import Prelude hiding (Word)

data Trie = Trie { end :: Bool, children :: M.Map Char Trie }
    deriving (Eq, Show)

type Word   = String
type Words  = [Word]

data Action = Add Word | Search Word | Find Word | Print | Exit | Ntn
data Out    = Tri Trie | Boo Bool | Words [Word] | Wrd Word | Sth (Maybe [Word])

-- function that creates an empty Trie
empty :: Trie
empty = Trie False M.empty

-- function for inserting element to trie. used in insertList function and during
-- runtime
insert :: Word -> Trie -> Trie
insert w tr@(Trie en ch)
    |  w == []  = Trie True (children tr)
    | otherwise = if M.member (head w) ch
        then Trie en $ M.insert (head w) (insert (tail w) ( ch M.! (head w) ) ) ch
        else Trie en $ M.insert (head w) (insert (tail w) empty) ch

-- function for inserting list of elements to trie. used only at the beginning
-- insertList function written with foldr
insertList :: [Word] -> Trie
insertList ws = foldr insert empty ws

-- insertList function written with recursion
-- insertList :: [Word] -> Trie
-- insertList ws@(w:ws')   = insert w $ insertList ws'
-- insertList []           = empty

-- search function. works recursively, returns true or false
search :: Word -> Trie -> Bool
search [] tr = end tr
search word@(w:ws) tr@(Trie en ch) = case M.lookup w ch of
    Just a  -> search ws $ ch M.! w
    Nothing -> False

-- function that returns list of words in Trie
getWords :: Trie -> [Word]
getWords tr@(Trie en ch) = getWords' "" trielist
    where
        trielist = M.toList ch
        getWords' :: Word -> [(Char, Trie)] -> [Word]
        getWords' w trlist = case trlist of
            [] -> []
            otherwise -> if end $ snd ( head trlist )
                then [w'] ++ sumValue
                else sumValue
                    where
                        w'      = w ++ [fst (head trlist)]
                        sumValue= getWords' w' (M.toList ( children ( snd (head trlist) ) ) ) ++ getWords' w (tail trlist)

-- function that returns list of elements with specified prefix
prefix :: Word -> Trie -> Maybe [Word]
prefix word tr = getPrefix word $ getWords tr
    where
        getPrefix :: Word -> [Word] -> Maybe [Word]
        getPrefix wrd wList = case wordlist of
            []  -> Nothing
            x   -> Just x
            where
                wordlist = [ wo | wo <- wList, Dlist.isPrefixOf wrd wo ]

-- function for reading input file and inserting the words in this file to Trie
readListFromFile :: IO Trie
readListFromFile = do
    args <- getArgs
    contents <- readFile (head args)
    return $ insertList (words contents)

-- user menu printer function
printOptions :: IO ()
printOptions = do
    putStrLn "a) Add Word\ns) Search Word\nf) Find words with prefix"
    putStrLn "p) Print all words\ne) Exit\n"
    putStrLn "Enter the action: "
    return ()

-- function to take user's input
getInput :: IO [Char]
getInput = do
    x <- getLine
    -- putStrLn ""
    return x

-- function to take user's choice
getChoice :: IO Char
getChoice = do
    x <- getLine
    putStrLn ""
    return $ head x

-- function to convert a string into action. used for generating appropriate
-- input for doAction function
convertAction :: [Char] -> Action
convertAction act@(x:xs) = case x of
    'a' -> Add (tail xs)
    'f' -> Find (tail xs)
    's' -> Search (tail xs)
    'p' -> Print
    'e' -> Exit
    _   -> Ntn

-- function to convert actions to a result "Out" that will be used in
-- getResult function. Code can be written without this function, too. But I
-- prefered that way
doAction :: Trie -> Action -> Out
doAction tr act = case act of
    Add xs      -> Tri $ insert xs tr
    Find xs     -> Sth $ prefix xs tr
    Search xs   -> Boo $ search xs tr
    Print       -> Words $ getWords tr
    _           -> Wrd "Exit"

-- function that takes "Out" and performs neccessary operations, and then returns
-- "Maybe Trie" to get give updated Trie. In my implementation, a trie should be
-- returned, so, if the trie is not updated, I returned the same trie that is
-- taken as parameter as "Maybe Trie"
getResult :: Trie -> Out -> IO (Maybe Trie)
getResult oldtrie out = case out of
    Tri tr      -> return (Just tr)
    Sth (Just x) -> do
        putStrLn "Found words:"
        putStrLn $ unlines x
        return (Just oldtrie)
    Sth Nothing -> do
        putStrLn "No words found with that prefix!\n"
        return (Just oldtrie)
    Boo bl      -> do
        if bl
            then do
                putStrLn "Exists in dictionary!\n"
                return (Just oldtrie)
            else do
                putStrLn "NOT Exist!\n"
                return (Just oldtrie)
    Words ws    -> do
        putStrLn $ unlines ws
        return (Just oldtrie)
    otherwise   -> return (Just oldtrie)

-- function to update Tri
updateTrie :: Trie -> Maybe Trie -> Trie
updateTrie tr mtr = case mtr of
    Nothing   -> tr
    Just x    -> x

-- doSth function to perform all neccessary operations inside. In order to
-- make code more clear. All the functions about actions are performed in this
-- function
doSth :: [Char] -> Trie -> IO (Trie)
doSth acti trie = do
    let action  = convertAction acti
    let out     = doAction trie action
    res <- getResult trie out
    let trie    = updateTrie trie res
    return trie

-- function to make program runs until 'e' or wrong input is given
infloop :: Trie -> IO (Trie)
infloop trie = do
    printOptions
    choice <- getChoice
    if choice == 'a' then do
            putStrLn "Enter the word to insert"
            wd <- getInput
            let c = choice : ' ' : wd
            newtrie <- doSth c trie
            putStrLn "New word is added!\n"
            tr <- infloop newtrie
            return tr
    else
        if choice == 's' then do
            putStrLn "Enter the word to search"
            wd <- getInput
            let c = choice: ' ' : wd
            newtrie <- doSth c trie
            tr <- infloop newtrie
            return tr
        else
            if choice == 'f' then do
                putStrLn "Enter the prefix"
                wd <- getInput
                let c = choice: ' ' : wd
                newtrie <- doSth c trie
                tr <- infloop newtrie
                return tr
            else
                if choice == 'p' then do
                    putStrLn "List of words in directory:"
                    newtrie <- doSth [choice] trie
                    tr <- infloop newtrie
                    return tr
                else do
                    let c = choice
                    newtrie <- doSth [choice] trie
                    return newtrie

-- main function
main = do
    trie <- readListFromFile
    newtrie <- infloop trie
    return ()
