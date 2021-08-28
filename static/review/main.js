let pages = []
let curInd = 0

function shuffle(array){
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

function load_pages(){
  for(let i = 0; i < pages.length; i++){
    let container = document.createElement("div")
    container.classList.add("content")
    container.id = "content-" + i
    if(pages[i].type === "content"){
      let link = pages[i].args.file
      let working = document.createElement("iframe")
      working.src = "https://docs.google.com/gview?url=" + link + "&embedded=true"
      working.classList.add("pdf_content")
      working.frameBorder = "0"
      $(container).hide().append(working)
    }else if(pages[i].type === "questions"){
      let questions = pages[i].args.questions
      for(let question of questions){
        if(question.type === "mc"){
          let working = $("#mc_template")[0].cloneNode(true).content.firstElementChild
          working.querySelector(".question_description").innerHTML = question.question_text

          for(let choice of question.choices){
            let choiceNode = $("#mc_choice")[0].cloneNode(true).content
            choiceNode.querySelector(".mc_choice").innerHTML = choice

            $(choiceNode.firstElementChild).click(function(){
              working.querySelector(".result").innerHTML = (choice === question.correct_choice) ? "Good Job!" : ("Oops, the correct answer was "+ question.correct_choice);
              $(working.querySelector(".preAnswer")).hide()
              $(working.querySelector(".postAnswer")).show()
            })
            $(working.querySelector(".choice_list")).append(choiceNode)
          }

          working.querySelector(".quitButton").click(function(){
              working.querySelector(".result").innerHTML = "Oops, the correct answer was " + correct_choice;
              $(working.querySelector(".preAnswer")).hide()
              $(working.querySelector(".postAnswer")).show()
          })

          $(container).append(working)
        }else if(question.type === "term"){
          let working = $("#term_template")[0].cloneNode(true).content.firstElementChild
          working.querySelector(".question_description").innerHTML = question.question_text

          $(working.querySelector(".submitButton")).click(function(){
            working.querySelector(".result").innerHTML = (working.querySelector(".term_answer").value === question.answer) ? "Good Job!" : ("Oops, the correct answer was " + question.answer);
            $(working.querySelector(".preAnswer")).hide()
            $(working.querySelector(".postAnswer")).show()
          })

          $(working.querySelector(".term_answer")).keypress(function(e){
            if(e.keyCode == 13){
              working.querySelector(".result").innerHTML = (this.value === question.answer) ? "Good Job!" : ("Oops, the correct answer was " + question.answer);
              $(working.querySelector(".preAnswer")).hide()
              $(working.querySelector(".postAnswer")).show()
            }
          })

          $(working.querySelector(".quitButton")).click(function(){
            working.querySelector(".result").innerHTML = "Oops, the correct answer was " + question.answer;
            $(working.querySelector(".preAnswer")).hide()
            $(working.querySelector(".postAnswer")).show()
          })

          $(container).append(working)
        }
      }
    }
    $("#rightPanel").append(container)
  }
}

function update(){
  $("#totalPages").html(pages.length + " page(s) in total")
  $("#currentPage").html("Page " + (curInd + 1))
  for(let i = 0; i < pages.length; i++){
    $("#content-" + i).hide();
  }
  $("#content-" + curInd).show()
}

function start(){
  load_pages()
  update()
  $("#nextButton").click(function(){
    if(curInd < pages.length - 1){
      curInd++;
      update();
    }
  })

  $("#prevButton").click(function(){
    if(curInd > 0){
      curInd--;
      update();
    }
  })
}