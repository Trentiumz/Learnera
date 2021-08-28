let questions = []
let curInd = 0

function shuffle(array){
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

function place_question(question){
  
}

function update(){
  place_question(curInd);
}

function start(){
  shuffle(questions);
  $("#totalQuestions").html(questions.length + " question(s) in total")
  $("#completedQuestions").html("0 question(s) completed")

}