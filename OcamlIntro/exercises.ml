open Printf

(* Ex1: A function that calculates the Area of a circle *)

let circle_area (r: float): float = 3.14 *. r *. r 

(* Ex2: A function named power that takes in a power 'n' and a float 'x' and returns x^n *)

let rec power (x:float) (n: int): float =
if n = 0 then 1. else
x *. power (x) (n-1)

(* You can re-use functions like this *)
let square x = power x 2


(* Ex3: A function named gcd that computes the greatest common divisor of two positive integers *)

let min a b = 
if a < b then a else 
if b < a then b else
a

let max a b = 
if a > b then a else 
if b > a then b else
a

let rec gcd (a:int) (b:int): int =
if b = 0 then a else 
gcd b (a mod b)

let print_nbr x = 
    for i = 0 to 10 do
        printf "Num: %d \n" x
    done;
