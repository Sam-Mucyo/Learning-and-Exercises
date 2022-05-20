(* A function that returns factorial of a given number *)

let rec fact x =
if x = 1 then 1 else x * fact (x-1)

(* Using Pattern matching*)

 let rec fact2 x = 
 match x with
 | 0|1 -> 1
 | _ -> x * fact2(x-1)
 
 (*In fact, we may simplify further with the function keyword which introduces pattern-matching directly:
*)

let rec fact3 = function
| 0|1 -> 1
| x -> x * fact3(x-1)

(* A Grading Function *)

let grade (x:int) : string = 
    if x < 60 then "F"
    else if x >= 60 && x < 70 then "D"
    else if x >= 70 && x < 80 then "C"
    else if x >= 80 && x < 90 then "B"
    else if x >= 90 && x <= 100 then "A"
    else "N/A"

