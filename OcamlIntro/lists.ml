(* List Questions and Answers *)

(* Return true if all elements of the list are true *)

let isAllTrue l =
    
    let rec checkAll x =
    match x with
    | [] -> true
    | h::t -> h && checkAll t
    in 

    if l = [] then false else checkAll l

(* 1. Write a function last : 'a list -> 'a option that returns the last element of a list. (easy) *)
let rec last (l: int list) : int =
    match l with
    | [] -> 0
    | h::t -> match t with
        | [] -> h
        | _ -> last t