
function makeCard (question, qnType, options) { 
  return {question, qnType, options}
};

// cards is a ditionary that maps card_id to its content (question, type, and options)
// For easy reference with database, card_id should reflect the question_id as
// it came from database.
let cards =
{1 : makeCard(
    "question 1", 
    "multiple choice", 
    [("option 1", 0), ("option 2", 5), ("option 3", 0), ("option 4", 0)]),
  
2 : makeCard(
    "question 2", 
    "multiple choice", 
    [("option 1", 0), ("option 2", 5), ("option 3", 0), ("option 4", 0)]),

3 : makeCard(
    "question 3", 
    "multiple choice", 
    [("option 1", 0), ("option 2", 5), ("option 3", 0), ("option 4", 0)])
}

// shuffle keys
let shuffledKeys = new Set(Object.keys(cards))
// answered is an array of answered keys 
let answered = []

function nextCard() {
  if (shuffledKeys.size === 0) {
    document.querySelector('.btn-success').style.background = "black"
    return
  } else {
    document.querySelector('.btn-success').style.background = "green";
    const [first] = shuffledKeys;
    document.querySelector('#question').innerHTML = cards[first].question
    answered.push(first)
    shuffledKeys.delete(first)
  }  
}

function prevCard() {
  if (answered.length === 0) {
    document.querySelector('.btn-primary').style.background = "black"
    return
  } else {
    document.querySelector('.btn-primary').style.background = "green"
    // Get previous index from the answered array.
    const previous = answered.pop();
    document.querySelector('#question').innerHTML = cards[previous].question
    // To make sure that this card won't be forgotten(pop()), we are adding it 
    // to uncompled cards again. By the way, if you go back, you probably need
    // to review that question later on.
    shuffledKeys.add(previous)  
  }
  
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#next').onclick = nextCard;
  document.querySelector('#previous').onclick = prevCard;
});