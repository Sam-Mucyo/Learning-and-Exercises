open Printf

let rec cummulative (x:int) : int = 
    match x with
    | 0 -> 0
    | _ -> x + cummulative (x-1);;

printf "The answer is %d", cummulative 5;;