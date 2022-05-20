(*
                Basic Functions
*)

let addInt2 x y = x + y 
let addInt (x : int) (y : int) : int = 
x + y

let multiplyFloat (x: float) (y : float) : float =
x *. y


(*
                    Recursion

Ex1: Fibonacci Sequence 
(1 1 2 3 5 8 13 ...)
*)

let rec fibo (x: int) : int =
if x = 0 then 0 else
 if x < 3 then 1 else
  fibo(x-2) + fibo(x - 1)


(* 
Ex2: Factorial 
*)

let rec fact x = 
if x = 0 || x = 1 then 1 else
x * fact(x-1)

